# import caching as caching
from flask import Flask, jsonify, request
from sqlalchemy import text

from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import auth
# from aliyunsms.sms_send import send_sms
import logging
import pinyin


# 跨域
from flask_cors import CORS
from flask_cors import cross_origin


app = Flask(__name__)
app.config.from_object(BaseConfig)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:123@localhost/school'
db = SQLAlchemy(app)


logging.basicConfig(level=logging.INFO)  # 设置日志级别为 INFO
logger = logging.getLogger(__name__)  # 获取模块级别的 logger
# 检查数据库连接是否成功
with app.app_context():
    pass
    # sql = text("select * from get_courses(:cid)")
    # data = db.session.execute(sql, {"cid": None})
    """sql = text("update courses\
                    set cname = :cname\
                    where cid = :cid")
    db.session.execute(sql, {"cname": '数据库', "cid": '10001'})
    db.session.commit()"""

    # tid = '123456789'
    # sql = text("insert into teachers values (:tid, '潘嵘', '计算机学院', 'zcf_m@def.com');")
    # data = db.session.execute(sql, {"tid": tid})
    # db.session.commit()


@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():# 
    logger.info(request.json)
    user_id = request.json.get("userid").strip()
    password = request.json.get("password").strip()
    role = request.json.get("role").strip()
    database = "students_password" if role == "student" else "teachers_password"
    id_name = "sid" if role == "student" else "tid"
    sql = text(("select * from {0} where {1} = :user_id and password = :password").format(database, id_name))
    # sql = text(("select * from {0} where {1} = '{2}' and password = '{3}'").format(database, id_name, user_id, password))
    data = db.session.execute(sql, {"user_id": user_id, "password": password}).first()
    # data = db.session.execute(sql).first()
    if data != None:
        if role == "teacher":
            sql = text("select coid from teacher_college where tid = :tid")
            data_ = db.session.execute(sql, {"tid": user_id}).first()
            if data_[0] == '00001':
                role = 'teacher_admin'
        
        user = {id_name: data[0], 'password': data[1], 'role': role} # , 'username': data[1]
        # 生成token
        token = auth.encode_func(user)
        logger.info(token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token}) # , "role": data[4]
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


def get_password(token):
    data = auth.decode_func(token)
    return data['password']

def get_role(token):
    data = auth.decode_func(token)
    if 'tid' in data:
        return (data['role'], data['tid'])
    else:
        return (data['role'], data['sid'])
    

#########################课程页面###########################
@app.route("/api/teachers/courses", methods=["GET"])
@cross_origin()
def get_courses():
    sql = text("select * from get_courses(:data)")
    # logger.info(sql)
    data = db.session.execute(sql, {"data": None}).fetchall()
    Data = []
    for information in data:
        dic = dict(cname=information[0], cid=information[1], tid = information[2],tname=information[3], 
                college=information[4], week = information[5], day = information[6], 
                period = information[7], time=information[8])
        Data.append(dic)
    logger.info("Get data!")
    # return jsonify({"code":"200", "tabledata": Data})
    return jsonify(code=200, msg = '查询成功', courses_data=Data)

# 增
@app.route("/api/teachers/courses/add", methods=["POST"])
@cross_origin()
def add_courses():
    logger.info(request.json) # cname, cid, week, day, time, tid, college
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher' and role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份添加课程")
    try:
        cname = request.json.get("cname").strip()
        cid = request.json.get("cid").strip()
        week = request.json.get("week").strip()
        week_1, week_2 = [int(i) for i in week.split('-')] if week != '' else (None, None)
        day = request.json.get("day").strip()
        day = day if day != '' else None
        period = request.json.get("time").strip()
        period_1, period_2 = [int(i) for i in period.split('-')] if period != '' else (None, None)
        tid = request.json.get("tid").strip()
        # college = request.json.get("college").strip()

        if role == 'teacher' and tid_ != tid:
            return jsonify(code=1000, msg = '非法身份添加课程，请联系教务处')
        if (week!='' or day!=None or period!='')and not (week!='' and day!=None and period!=''):
            return jsonify(code=1000, msg = '请输入完整时间信息或全部留空')
        
        sql = text("insert into courses\
                   values (:cid, :cname, :start_week, :end_week, :week_day, :start_period, :end_period);\
                   insert into course_teacher values (:cid, :tid);")
        
        db.session.execute(sql, {"cid": cid, "cname": cname, "tid": tid, "start_week": week_1, 
                                "end_week": week_2, "week_day": day, "start_period": period_1, "end_period": period_2})

        db.session.commit()
        return jsonify(code=200, msg = '成功加入课程')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '请检查教师时间冲突及课程号和教师工号是否有误')


# 删
@app.route("/api/teachers/courses/delete", methods=["DELETE"])
@cross_origin()
def delete_courses():
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher' and role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份删除课程")
    try:
        cid = request.json.get("cid")
        sql = text('select tid from course_teacher where cid = :cid')
        data = db.session.execute(sql, {"cid": cid}).first()
        if role == 'teacher' and data[0] != tid_:
            return jsonify(code=1000, msg="非法身份删除课程，请联系教务处")
        sql = text('delete from courses where cid = :cid')
        db.session.execute(sql, {"cid": cid})
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg="删除失败")
        
# 改
@app.route("/api/teachers/courses/modify", methods=["POST"])
@cross_origin()
def modify_courses():
    # TODO：1， 修改信息违法：比如时间段小于0 2， 时间有重合，比如同一个老师课程的时间冲突，这个需要在后端判断。
    logger.info(request.json) # cname, cid, week, day, time, tid, college
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份修改课程")
    try:
        cname = request.json.get("cname").strip()
        cid = request.json.get("cid").strip()
        week = request.json.get("week").strip()
        week_1, week_2 = [int(i) for i in week.split('-')] if week != '' else (None, None)
        day = request.json.get("day").strip()
        day = day if day != '' else None
        period = request.json.get("time").strip()
        period_1, period_2 = [int(i) for i in period.split('-')] if period != '' else (None, None)
        tid = request.json.get("tid").strip()
        if (week!='' or day!=None or period!='')and not (week!='' and day!=None and period!=''):
            return jsonify(code=1000, msg = '请输入完整时间信息或全部留空')
        sql = text("update courses \
                    set start_week = :start_week, end_week = :end_week, \
                    week_day = :week_day, start_period = :start_period, end_period = :end_period \
                    where cid = :cid;\
                    update course_teacher \
                    set tid = :tid where cid = :cid;")
        db.session.execute(sql, {"cname": cname, "tid": tid, "start_week": week_1, 
                                "end_week": week_2, "week_day": day, "start_period": period_1,
                                "end_period": period_2, "cid": cid})
        db.session.commit()
        return jsonify(code=200, msg = '修改成功')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '请检查教师时间冲突及课程号和教师工号是否有误')

# 查
@app.route("/api/teachers/courses/select", methods=["POST"])
@cross_origin()
def select_courses():
    logger.info(request.json)
    input_data = request.json.get("input_data").strip()
    sql = text("select * from get_courses(:data)")
    # logger.info(sql)
    data = db.session.execute(sql, {"data": input_data}).fetchall()
    Data = []
    for information in data:
        dic = dict(cname=information[0], cid=information[1], tid = information[2],tname=information[3], 
                college=information[4], week = information[5], day = information[6], 
                period = information[7], time=information[8])
        Data.append(dic)
    logger.info(Data)
    
    # logger.info(Data)
    # return jsonify({"code":"200", "tabledata": Data})
    return jsonify(code=200, msg = '查询成功', courses_data=Data)


#################################学生管理页面##########################
@app.route("/api/teachers/students", methods=["GET"])
@cross_origin()
def get_students():
    sql = text("select * from students_view;")
    # logger.info(sql)
    data = db.session.execute(sql).fetchall()
    Data = []
    # sid, sname, email, college, grade
    for information in data:
        dic = dict(sid=information[0], sname=information[1], grade = information[2],
                   college = information[3], email = information[4])
        Data.append(dic)
    logger.info("Get students data!")
    # return jsonify({"code":"200", "tabledata": Data})
    return jsonify(code=200, msg = '查询成功', tabledata=Data)

# 获取课程
@app.route("/api/teachers/students/get_college", methods=["GET"])
@cross_origin()
def get_colleges():
    try:
        sql = text("select * from colleges;")
        data = db.session.execute(sql)
        Data = []
        for information in data:
            Data.append({"coid": information[0], "coname": information[1]})
        return jsonify(code=200, colleges_data = Data)
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '网络故障')
# 增
@app.route("/api/teachers/students/add", methods=["POST"])
@cross_origin()
def add_students():
    logger.info(request.json) # sid, sname, email, college, grade
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份添加学生，请联系教务老师")
    try:
        sname = request.json.get("sname").strip()
        sid = request.json.get("sid").strip()
        email = request.json.get("email").strip()
        email = email if email != '' else None
        coid = request.json.get("college").strip()
        grade = request.json.get("grade").strip()
        grade = grade if grade != '' else None
    
        sql = text("insert into students\
                   values (:sid, :sname, :email, :grade);\
                   insert into student_college\
                   values (:sid, :coid)")

        db.session.execute(sql, {"sid": sid, "sname": sname, "email": email, "coid": coid, "grade": grade})
        db.session.commit()
        return jsonify(code=200, msg = '成功添加学生')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '请检查输入是否合法及学号是否有重复')

# 删
@app.route("/api/teachers/students/delete", methods=["DELETE"])
@cross_origin()
def delete_students():
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份删除学生，请联系教务老师")
    try:
        sid = request.json.get("sid")
        logger.info(sid)
        sql = text('delete from students where sid = :sid')
        db.session.execute(sql, {"sid": sid})
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg="删除失败，请稍后再试")

# 改
@app.route("/api/teachers/students/modify", methods=["POST"])
@cross_origin()
def modify_students():
    logger.info(request.json) # sid, sname, grade, college, email
    logger.info("Enter modify_students")
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份修改学生信息，请联系教务老师")
    try:
        sid = request.json.get("sid").strip()
        email = request.json.get("email")
        if email != None:
            email = email.strip()
        coid = request.json.get("college").strip()
        grade = request.json.get("grade")
        grade = grade if grade != '' else None
        # 检查学生
        sql = text("update students set email = :email, grade = :grade where sid = :sid;\
                   update student_college set coid = :coid where sid = :sid;")
        db.session.execute(sql, {"email": email, "grade": grade, "coid": coid, "sid": sid})
        db.session.commit()
        return jsonify(code=200, msg = '修改成功')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '输入存在不合法信息，请重新检查输入')

# 查
@app.route("/api/teachers/students/select", methods=["POST"])
@cross_origin()
def select_students():
    logger.info(request.json)
    input_data = request.json.get("input_data").strip()
    input_data = '%' + input_data + '%'
    sql = text("select * from students_view where sid like :sid or sname like :sname;")
    # logger.info(sql)
    data = db.session.execute(sql, {"sid": input_data, "sname": input_data}).fetchall()
    logger.info(data)
    Data = []
    for information in data:
        dic = dict(sid=information[0], sname=information[1], grade = information[2],
                   college = information[3], email = information[4])
        Data.append(dic)
    
    logger.info(Data)
    # return jsonify({"code":"200", "tabledata": Data})
    return jsonify(code=200, msg = '查询成功', students_information=Data)

#################################选课页面#############################
@app.route("/api/teachers/courseSelection", methods=["GET"])
@cross_origin()
def get_choice():
    sql = text("select * from get_course_selection(:data)")
    # logger.info(sql)
    data = db.session.execute(sql, {"data": None}).fetchall()
    Data = []
    for information in data:
        dic = dict(cname = information[0], cid = information[1], time = information[2], 
                   tname = information[3], college = information[4], num = information[5])
        Data.append(dic)
    return jsonify(code=200, msg = '查询成功', courses_data=Data)

@app.route("/api/teachers/courseSelection/add", methods=["POST"])
@cross_origin()
def add_choice():
    # TODO：需要判断1，cid、sid相同 2,对sid筛选进行判断，确定没有冲突课程
    logger.info(request.json) # cid, sid
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份添加选课信息，请联系教务处")
    try:
        logger.info('123')
        cid = request.json.get("cid").strip()
        
        sid = request.json.get("sid").strip()
        # college = request.json.get("college").strip()

        sql = text("insert into choices values (null, :sid, :cid)")
        
        db.session.execute(sql, {"cid": cid, "sid": sid})
        db.session.commit()
        return jsonify(code=200, msg = '成功加入选课')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '请检查学生是否已经存在或是否存在时间冲突')


@app.route("/api/teachers/courseSelection/delete", methods=["DELETE"])
@cross_origin()
def delete_choice():
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份删除选课信息，请联系教务处")
    try:
        cid = request.json.get("cid").strip()
        sid = request.json.get("sid").strip()
        sql = text("delete from choices where cid = :cid and sid = :sid")
        db.session.execute(sql, {"cid": cid, "sid": sid})
        db.session.commit()
        return jsonify(code=200, msg = '成功删除课程')
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '已修课程无法退课')

@app.route("/api/teachers/courseSelection/select_courses", methods=["POST"])
@cross_origin()
def select_choice_courses():
    sql = text("select * from get_course_selection(:data)")
    # logger.info(sql)
    input_data = request.json.get("input_data").strip()
    data = db.session.execute(sql, {"data": input_data}).fetchall()
    Data = []
    for information in data:
        dic = dict(cname = information[0], cid = information[1], time = information[2], 
                   tname = information[3], college = information[4], num = information[5])
        Data.append(dic)
    return jsonify(code=200, msg = '查询成功', courses_data=Data)

@app.route("/api/teachers/courseSelection/select_students", methods=["POST"])
@cross_origin()
def select_choice_students():
    cid = request.json.get("cid").strip()
    sql = text("select * from students_information where cid = :cid and sid in (select sid from choices where cid = :cid) order by college, sid;")
    data = db.session.execute(sql, {"cid": cid}).fetchall()
    Data = []
    for information in data:
        dic = dict(sid = information[0], sname = information[2], email = information[3], college = information[4],
                   grade = information[5], score = information[6], editingScore = False)
        Data.append(dic)
    return jsonify(code=200, msg = '查询成功', students_data=Data)


@app.route("/api/teachers/courseSelection/modify", methods=["POST"])
@cross_origin()
def modity_choices():
    role, tid_ = get_role(request.headers.get('token'))
    if role != 'teacher' and role != 'teacher_admin':
        return jsonify(code=1000, msg="非法身份修改成绩")
    cid = request.json.get("cid").strip()

    sql = text('select tid from course_teacher where cid = :cid')
    data = db.session.execute(sql, {"cid": cid}).first()
    if role == 'teacher' and data[0] != tid_:
        return jsonify(code=1000, msg="非法身份修改成绩")
    sid = request.json.get("sid").strip()
    
    score = request.json.get("score").strip()
    score = score if score != '' else None
    sql = text("update choices set score = :score where cid = :cid and sid = :sid;")
    db.session.execute(sql, {"cid": cid, "sid": sid, "score": score})
    db.session.commit()
    return jsonify(code=200, msg = '修改成功')

#################################个人中心############################
@app.route("/api/teachers/information", methods=["GET"])
@cross_origin()
def get_personal_information():
    role, tid = get_role(request.headers.get('token'))
    if role != 'teacher' and role != 'teacher_admin':
        return jsonify(code=1000, msg = '身份信息非老师')
    
    sql = text("select teachers.tid, teachers.tname, colleges.coname, teachers.email\
                from teachers\
                join teacher_college on teacher_college.tid = teachers.tid\
                join colleges on colleges.coid = teacher_college.coid\
                where teachers.tid = :tid;")
    data_ = db.session.execute(sql, {"tid": tid}).first()
    

    sql = text("select * from courses where cid in (select cid from course_teacher where tid = :tid)")
    data_2 = db.session.execute(sql, {"tid": tid}).fetchall()
    courses_data = []
    for information in data_2: # cid, cname, time
        time_ = ''
        if  information[2] != None and information[3] != None and information[4] != None and information[5] != None and information[6] != None:
            time_ = '{}-{}每周{}第{}节-第{}节'.format(information[2], information[3], information[4], information[5], information[6])
        dic = dict(cid = information[0], cname = information[1], time = time_)
        courses_data.append(dic)

    data = dict(tid = data_[0], tname = data_[1], college = data_[2], email = data_[3], courses = courses_data)
    logger.info(data)
    return jsonify(code=200, msg = '查询成功', data = data)

@app.route("/api/teachers/information/change_password", methods=["POST"])
@cross_origin()
def change_password():
    # TODO：检查格式和非法字符
    old_password = request.json.get("old_password").strip()
    new_password = request.json.get("new_password").strip()
    role, id = get_role(request.headers.get('token'))
    sql = None

    if get_password(request.headers.get('token')) != old_password:
        return jsonify(code=1000, msg = '原密码错误，请重新输入')
    
    if role == 'teacher':
        sql = text("update teachers_password set password = :password where tid = :id;")
    else:
        sql = text("update students_password set password = :password where sid = :id;")
    

    db.session.execute(sql, {"password": new_password, "id": id})
    db.session.commit()

    if role == 'teacher' or role == 'teacher_admin':
        token = auth.encode_func({'tid': id, 'password': new_password, 'role': role})
    else:
        token = auth.encode_func({'sid': id, 'password': new_password, 'role': role})
    
    return jsonify(code = 200, msg = '修改成功', token = token)
    


######################################学生端#######################################
################################主页#################################
@app.route("/api/students/score", methods=["GET"])
@cross_origin()
def get_score():
    role, sid = get_role(request.headers.get('token'))
    sql = text('select score from choices where sid = :sid')
    data = db.session.execute(sql, {"sid": sid}).fetchall()
    Data = [0, 0, 0, 0, 0]
    for information in data:
        if information[0] == None:
            continue
        if information[0] < 60:
            Data[0] += 1
        elif information[0] < 70:
            Data[1] += 1
        elif information[0] < 80:
            Data[2] += 1
        elif information[0] < 90:
            Data[3] += 1
        else:
            Data[4] += 1
    logger.info(Data)
    return jsonify(code = 200, msg = '成功返回', score_data = Data)

# 返回没有分数的课程
@app.route("/api/home/courses_ed", methods=["GET"])
@cross_origin()
def get_my_choosing_courses():
    role, sid = get_role(request.headers.get('token'))
    sql = text('select * from get_course_score(null, :sid) where score is null')
    data = db.session.execute(sql, {"sid": sid})
    Data = []
    for information in data:
        Dic = dict(time = information[2], tname = information[3], cname = information[0])
        Data.append(Dic)

    return jsonify(code = 200, msg = '成功返回', courses = Data)

# 返回有分数的课程
@app.route("/api/home/courses_scored", methods=["GET"])
@cross_origin()
def get_my_choosed_courses():
    role, sid = get_role(request.headers.get('token'))
    sql = text('select * from get_course_score(null, :sid) where score is not null')
    data = db.session.execute(sql, {"sid": sid})
    Data = []
    for information in data:
        Dic = dict(time = information[2], tname = information[3], cname = information[0])
        Data.append(Dic)
    return jsonify(code = 200, msg = '成功返回', courses = Data)

##################可选课程########################
def get_student_data(data, Data: list, is_choosed):
    for information in data:
        dic = dict(cname=information[0], cid=information[1],
            tname=information[3], college=information[4], time=information[8],
            is_choosed = 1 if is_choosed else 0)
        Data.append(dic)


@app.route("/api/students/allCourses", methods=["GET", "POST"])
@cross_origin()
def get_student_courses():
    role, sid = get_role(request.headers.get('token'))
    if request.method == "GET":
        Data = []
        sql = text("select * from get_courses(null) where cid not in(select cid from choices where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        get_student_data(data, Data, False)
        sql = text("select * from get_courses(null) where cid in(select cid from choices where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        logger.info(data)
        get_student_data(data, Data, True)
        return jsonify(code = 200, msg = '查询成功', courses_data = Data)
    if request.method == "POST":
        try:
            cid = request.json.get("cid").strip()
            sql = text("insert into choices values (null, :sid, :cid)")
            db.session.execute(sql, {"cid": cid, "sid": sid})
            db.session.commit()
            return jsonify(code = 200, msg = '添加成功')
        except Exception as e:
            logger.info(e)
            return jsonify(code = 1000, msg = '课程时间冲突')

@app.route("/api/students/allCourses/major", methods=["GET"])
@cross_origin()
def select_major_courses():
    role, sid = get_role(request.headers.get('token'))
    if request.method == "GET":
        Data = []
        sql = text("select * from get_courses(null) where cid not in(select cid from choices where sid = :sid)\
                   and college = (select coname from students_view where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        get_student_data(data, Data, False)
        sql = text("select * from get_courses(null) where cid in(select cid from choices where sid = :sid)\
                   and college = (select coname from students_view where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        get_student_data(data, Data, True)
        return jsonify(code = 200, msg = '查询成功', courses_data = Data)


@app.route("/api/students/allCourses/others", methods=["GET"])
@cross_origin()
def select_other_courses():
    role, sid = get_role(request.headers.get('token'))
    if request.method == "GET":
        Data = []
        sql = text("select * from get_courses(null) where cid not in(select cid from choices where sid = :sid)\
                   and college != (select coname from students_view where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        get_student_data(data, Data, False)
        sql = text("select * from get_courses(null) where cid in(select cid from choices where sid = :sid)\
                   and college != (select coname from students_view where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        logger.info(data)
        get_student_data(data, Data, True)
        return jsonify(code = 200, msg = '查询成功', courses_data = Data)

@app.route("/api/students/allCourses/select", methods=["POST"])
@cross_origin()
def select_student_courses():
    role, sid = get_role(request.headers.get('token'))
    try:
        Data = []
        input_data = request.json.get("input_data").strip()
        sql = text("select * from get_courses(:input_data) where cid not in (select cid from choices where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid, "input_data": input_data})
        get_student_data(data, Data, False)
        sql = text("select * from get_courses(:input_data) where cid in (select cid from choices where sid = :sid)")
        data = db.session.execute(sql, {"sid": sid, "input_data": input_data})
        get_student_data(data, Data, True)
        return jsonify(code = 200, msg = '查询成功', courses_data = Data)
    except Exception as e:
        logger.info(e)
        return jsonify(code = 1000, msg = '发生故障')


@app.route("/api/students/choosedCourses", methods=["DELETE", "GET"])
@cross_origin()
def get_choosed_courses():
    role, sid = get_role(request.headers.get('token'))
    if request.method == "GET":
        Data = []
        sql = text("select * from get_course_score(null, :sid)")
        data = db.session.execute(sql, {"sid": sid}).fetchall()
        logger.info(data)
        for information in data:
            dic = dict(cname=information[0], cid=information[1], time=information[2],
            tname=information[3], college=information[4], score=information[5])
            Data.append(dic)
        return jsonify(code = 200, msg = '查询成功', courses_data = Data)
    if request.method == "DELETE":
        logger.info(request.json)
        try:
            logger.info(request.json)
            cid = request.json.get("cid").strip()
            sql = text("select score from choices where cid = :cid and sid = :sid")
            score = db.session.execute(sql, {"cid": cid, "sid": sid}).first()
            if score[0] != None:
                return jsonify(code = 1000, msg = '无法退除已修课程')
            sql = text("delete from choices where cid = :cid and sid = :sid")
            db.session.execute(sql, {"cid": cid, "sid": sid})
            db.session.commit()
            return jsonify(code = 200, msg = '退课成功')
        except Exception as e:
            logger.info(e)
            return jsonify(code = 1000, msg = '网络故障')

@app.route("/api/students/choosedCourses/select", methods=["POST"])
@cross_origin()
def select_choosed_courses():
    role, sid = get_role(request.headers.get('token'))
    input_data = request.json.get("input_data").strip()
    Data = []
    sql = text("select * from get_course_score(:input_data, :sid)")
    data = db.session.execute(sql, {"sid": sid, "input_data": input_data}).fetchall()
    logger.info(data)
    for information in data:
        dic = dict(cname=information[0], cid=information[1], time=information[2],
        tname=information[3], college=information[4], score=information[5])
        Data.append(dic)
    logger.info(Data)
    return jsonify(code = 200, msg = '查询成功', courses_data = Data)

########################个人中心############################
@app.route("/api/students/information", methods=["GET"])
@cross_origin()
def get_student_information():
    try:
        role, sid = get_role(request.headers.get('token'))
        sql = text("select * from students_view where sid = :sid")
        data = db.session.execute(sql, {"sid": sid}).first()
    
        sql = text("select avg(score) from choices where sid = :sid")
        avg_score = (db.session.execute(sql, {"sid": sid}).first())[0]
        gpa = None
        if avg_score != None:
            gpa = f"{(avg_score-50)/10:.2f}"
        data = dict(sid = data[0], sname = data[1], grade = data[2], college = data[3], email = data[4], 
                avg_score = gpa)

        return jsonify(code=200, msg = '查询成功', data = data)
    except Exception as e:
        logger.info(e)
        return jsonify(code=1000, msg = '非法访问')

if __name__ == '__main__':
    # logger.info('123')
    pass
    app.run(debug=True, host='127.0.0.1', port='5000')
    # 开启了debug模式
    """sql = text('select * from courses')
    data = db.session.execute(sql).first()
    for row in data:
        print(row)"""