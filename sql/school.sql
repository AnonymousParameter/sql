drop view students_view;
drop view students_information;
drop view choices_information;
drop view courses_information;
drop table choices;
drop table courses cascade;
drop table teachers_password;
drop table teachers;
drop table students_password;
drop table students;
drop table colleges;
---------------------------college--------------------

create table colleges(
  coid varchar(5) not null primary key,
  coname text not null
);

insert into colleges values ('00001', '教务处');
insert into colleges values ('00002', '计算机学院');
insert into colleges values ('00003', '新闻传播学院');
insert into colleges values ('00004', '生命科学学院');

---------------------------students-------------------------------
create table students(
	sid char(8) not null primary key,
	sname varchar(30) not null,
	email varchar(30) null,
	grade int null
);
insert into students values ('22336157', '刘晓丹', 'liuxiaodan@cse.edu', 2022);
insert into students values ('22336146', '刘婵姝', 'liuchanshu@cse.edu', 2022);
insert into students values ('22234567', '李敏妍', 'liminyan@cse.edu', 2022);
insert into students values ('21345678', '刘晨曦', 'liuchenxi@cse.edu', 2021);
insert into students values ('24234568', '陈雅婷', 'chenyating@cse.edu', 2024);
insert into students values ('23234568', '赵启蒙', 'zhaoqimeng@cse.edu', 2023);

insert into students values ('22234569', '李彤', 'litong@lifesci.edu', 2022);
insert into students values ('22345679', '王欣怡', 'wangxinyi@lifesci.edu', 2022);
insert into students values ('23234571', '陈佳', 'chenjia@lifesci.edu', 2023);
insert into students values ('24234573', '赵丽娜', 'zhaolina@lifesci.edu', 2024);
insert into students values ('22234571', '孙博', 'sunbo@lifesci.edu', 2022);
insert into students values ('23234572', '周薇', 'zhouwei@lifesci.edu', 2023);

insert into students values ('22234575', '陈琪', 'chenqi@journalism.edu', 2022);
insert into students values ('22345680', '李明', 'liming@journalism.edu', 2022);
insert into students values ('23234574', '王思远', 'wangsiyuan@journalism.edu', 2023);
insert into students values ('24234576', '赵颖', 'zhaoying@journalism.edu', 2024);
insert into students values ('22234572', '孙洁', 'sunjie@journalism.edu', 2022);
insert into students values ('23234575', '周逸', 'zhouyi@journalism.edu', 2023);

--------------------------students_password----------------

create table students_password(
	sid char(8) not null primary key,
	password varchar(12) not null,
	constraint fk_password_students foreign key(sid) references students(sid) on delete cascade
);

insert into students_password values ('22336157', 'Shujuku1234');
insert into students_password values ('22336146', 'Shujuku1234');
insert into students_password values ('22234567', 'Shujuku1234');
insert into students_password values ('21345678', 'Shujuku1234');
insert into students_password values ('24234568', 'Shujuku1234');
insert into students_password values ('23234568', 'Shujuku1234');
-- insert into students_password values ('22134568', 'Sjq4568');
-- insert into students_password values ('24234569', 'Yyx4569');
-- insert into students_password values ('23134569', 'Zyc4569');
-- insert into students_password values ('22234568', 'Msy4568');

insert into students_password values ('22234569', 'Shujuku1234');
insert into students_password values ('22345679', 'Shujuku1234');
insert into students_password values ('23234571', 'Shujuku1234');
insert into students_password values ('24234573', 'Shujuku1234');
insert into students_password values ('22234571', 'Shujuku1234');
insert into students_password values ('23234572', 'Shujuku1234');
-- insert into students_password values ('24234574', 'Yl4574');
-- insert into students_password values ('23134572', 'Wc4572');
-- insert into students_password values ('21234571', 'Ll4571');
-- insert into students_password values ('22134573', 'Dsj4573');

insert into students_password values ('22234575', 'Shujuku1234');
insert into students_password values ('22345680', 'Shujuku1234');
insert into students_password values ('23234574', 'Shujuku1234');
insert into students_password values ('24234576', 'Shujuku1234');
insert into students_password values ('22234572', 'Shujuku1234');
insert into students_password values ('23234575', 'Shujuku1234');
-- insert into students_password values ('24234577', 'Yxl4577');
-- insert into students_password values ('23134573', 'Wl4573');
-- insert into students_password values ('21234572', 'Lcx4572');
-- insert into students_password values ('22134574', 'Dwj4574');
-------------------------student_college-----------------
create table student_college(
	sid char(8) not null,
	coid varchar(5) not null,
constraint fk_student foreign key(sid) references students(sid) on delete cascade,
constraint fk_college foreign key(coid) references colleges(coid) on delete cascade,
constraint uq_student_college unique (sid, coid)
);

insert into student_college values ('22336157', '00002');
insert into student_college values ('22336146', '00002');
insert into student_college values ('22234567', '00002');
insert into student_college values ('21345678', '00002');
insert into student_college values ('24234568', '00002');
insert into student_college values ('23234568', '00002');

insert into student_college values ('22234569', '00004');
insert into student_college values ('22345679', '00004');
insert into student_college values ('23234571', '00004');
insert into student_college values ('24234573', '00004');
insert into student_college values ('22234571', '00004');
insert into student_college values ('23234572', '00004');

insert into student_college values ('22234575', '00003');
insert into student_college values ('22345680', '00003');
insert into student_college values ('23234574', '00003');
insert into student_college values ('24234576', '00003');
insert into student_college values ('22234572', '00003');
insert into student_college values ('23234575', '00003');

--------------------------teachsers----------------------------
create table teachers(
	tid char(9) not null primary key,
	tname varchar(30) not null,
	email varchar(30) null
);

insert into teachers values ('120000001', '吴先有', 'aacl4y0@jdxom.edu');
insert into teachers values ('150000001', '孙涵树', '63em@gxoa.com');

insert into teachers values ('200012345', '潘嵘', 'zcf_m@def.com');
insert into teachers values ('201912346', '赵云雷', 'lt_2020@abc.com');
insert into teachers values ('201512347', '张颖菲', 'zy_2020@xyz.com');
insert into teachers values ('201002348', '王强博', 'wq_2020@edu.com');


insert into teachers values ('200800001', '李涛', 'lt@lifesci.edu');
insert into teachers values ('200612389', '赵娜', 'zhona@lifesci.edu');
insert into teachers values ('201718643', '陈明阳', 'chming@lifesci.edu');

insert into teachers values ('200739465', '张磊', 'zhanglei@journalism.edu');
insert into teachers values ('201412696', '李霞', 'lixia@journalism.edu');
insert into teachers values ('201529467', '周亚楠', 'zhouyanan@journalism.edu');

--------------------------teachers_password--------------------

create table teachers_password(
	tid char(9) not null primary key,
	password varchar(12) not null,
	constraint fk_password_teachers foreign key(tid) references teachers(tid) on delete cascade
);

insert into teachers_password values ('120000001', 'Wxy00001');
insert into teachers_password values ('150000001', 'Shs00001');

insert into teachers_password values ('200012345', 'Pr12345');
insert into teachers_password values ('201912346', 'Lt12346');
insert into teachers_password values ('201512347', 'Zyf12347');
insert into teachers_password values ('201002348', 'Wqb12348');
-- insert into teachers_password values ('202312349', 'Ljl12349');

-- 生命科学学院
insert into teachers_password values ('200800001', 'Lt00001');
insert into teachers_password values ('200612389', 'Zn12389');
insert into teachers_password values ('201718643', 'Cmy18643');
-- insert into teachers_password values ('202467434', 'Wl67434');
-- insert into teachers_password values ('201335468', 'Ljj35468');
-- 新闻传播学院
insert into teachers_password values ('200739465', 'Zl39465');
insert into teachers_password values ('201412696', 'Lx12696');
insert into teachers_password values ('201529467', 'Zyn29467');
-- insert into teachers_password values ('201095348', 'Ww95348');
-- insert into teachers_password values ('202312619', 'Lx12619');
--------------------------teacher_college-------------------
create table teacher_college(
	tid char(9) not null,
	coid varchar(5) not null,
constraint fk_teacher foreign key(tid) references teachers(tid) on delete cascade,
constraint fk_college foreign key(coid) references colleges(coid) on delete cascade,
constraint uq_teacher_college unique (tid, coid)
);

insert into teacher_college values ('120000001', '00001');
insert into teacher_college values ('150000001', '00001');

insert into teacher_college values ('200012345', '00002');
insert into teacher_college values ('201912346', '00002');
insert into teacher_college values ('201512347', '00002');
insert into teacher_college values ('201002348', '00002');

insert into teacher_college values ('200800001', '00004');
insert into teacher_college values ('200612389', '00004');
insert into teacher_college values ('201718643', '00004');

insert into teacher_college values ('200739465', '00003');
insert into teacher_college values ('201412696', '00003');
insert into teacher_college values ('201529467', '00003');

---------------------------courses-----------------------------
create table courses(
	cid char(5) not null primary key,
	cname varchar(30) not null,
	start_week int null check(start_week >= 1),
	end_week int null check (end_week >= start_week and end_week <= 21),
	week_day varchar(20) null check (week_day in ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期七')),
	start_period int null check (start_period >= 1),
	end_period int null check (end_period >= start_period and end_period<= 11)
);


insert into courses values ('10001','数据库', 1, 17, '星期一', 3, 4);
insert into courses values ('10002', '数据结构与算法', 1, 17, '星期二', 1, 2);
insert into courses values ('10003', '操作系统', 1, 9, '星期四', 9, 11);
insert into courses values ('10004', '计算机网络', 10, 17, '星期五', 1, 2);

insert into courses values ('20001', '生物化学', 1, 17, '星期二', 3, 4);
insert into courses values ('20002', '细胞生物学', 1, 17, '星期三', 5, 6);
insert into courses values ('20003', '遗传学', 1, 9, '星期五', 2, 3);

insert into courses values ('30001', '新闻学原理', 1, 17, '星期二', 3, 4);
insert into courses values ('30002', '传播学概论', 1, 17, '星期三', 5, 6);
insert into courses values ('30003', '新闻采编与写作', 1, 17, '星期五', 1, 2);

----------------------------------course_teacher-----------------------
create table course_teacher(
	cid char(5) not null,
	tid char(9) not null,
constraint fk_course foreign key(cid) references courses(cid) on delete cascade,
constraint fk_teacher foreign key(tid) references teachers(tid) on delete cascade,
constraint uq_course_teacher unique (cid, tid)
);


insert into course_teacher values ('10001', '200012345');
insert into course_teacher values ('10002', '201912346');
insert into course_teacher values ('10003', '201512347');
insert into course_teacher values ('10004', '201002348');

insert into course_teacher values ('20001', '200800001');
insert into course_teacher values ('20002', '200612389');
insert into course_teacher values ('20003', '201718643');

insert into course_teacher values ('30001', '200739465');
insert into course_teacher values ('30002', '201412696');
insert into course_teacher values ('30003', '201529467');

---------------------------------choices-------------------------------------
create table choices(
	no int not null primary key,
	sid char(8) not null,
	cid char(5) not null,
	score int null check (score >= 0 and score <= 100),
constraint fk_choices_courses foreign key(cid) references courses(cid) on delete cascade,
constraint fk_choices_students foreign key(sid) references students(sid) on delete cascade,
constraint uq_course_students unique (cid, sid)
);


insert into choices values (1, '22336157', '10001', NULL);
insert into choices values (2, '22336157', '10002', NULL);
insert into choices values (3, '22336146', '10001', NULL);
insert into choices values (4, '22336146', '10003', NULL);
insert into choices values (5, '22234567', '10002', NULL);
insert into choices values (6, '22234567', '10004', NULL);
insert into choices values (7, '21345678', '10001', NULL);
insert into choices values (8, '21345678', '10004', NULL);
insert into choices values (9, '24234568', '10002', NULL);
---------------------------------courses_information-------------------------------------
create view courses_information as
select courses.cname, courses.cid, teachers.tid, teachers.tname, colleges.coname, 
courses.start_week||'-'||courses.end_week||'周' as week, courses.week_day,
courses.start_period||'-'||courses.end_period||'节' as period,
courses.start_week||'-'||courses.end_week||'每周'||courses.week_day||'第'||
courses.start_period||'节-第'||courses.end_period||'节' as time
from courses
join course_teacher on courses.cid = course_teacher.cid
join teachers on course_teacher.tid = teachers.tid
join teacher_college on teachers.tid = teacher_college.tid
join colleges on teacher_college.coid = colleges.coid;

----------------------------choices_information-----------------------------
create view choices_information as
select courses.cid, courses.start_week, courses.end_week, courses.week_day,
courses.start_period, courses.end_period, choices.sid
from courses
join choices on courses.cid = choices.cid;

-------------------------------students_information--------------------
create view students_information as
select students.sid, choices.cid, students.sname, students.email, 
colleges.coname as college, students.grade, choices.score 
from students
join choices on students.sid = choices.sid
join student_college on students.sid = student_college.sid
join colleges on student_college.coid = colleges.coid;

---------------------------------students_view-------------------------------
create view students_view as
select students.sid, students.sname, students.grade,
colleges.coname, students.email
from students
join student_college on students.sid = student_college.sid
join colleges on colleges.coid = student_college.coid
order by colleges.coname, sid;

------------------------------存储过程获取课程------------------------------
create or replace function get_courses(input_data text)
returns table(cname varchar(30), 
			  cid char(5), 
			  tid char(9), 
			  tname varchar(30), 
			  college text, 
			  week text, 
			  week_day varchar(20), 
			  period text,
			  time_ text)
as $$
declare
	query_ text;
	course record;
	query_data text;
begin
	-- execute format('set role %I', role_name);
	query_ := format('select * from courses_information order by coname, cid');
	query_data := '%'||input_data||'%';
	if input_data is not null then
		query_ := format('select * from courses_information where cid like %L or cname like %L order by coname, cid', 
		query_data, query_data);
	end if;
	
	return query execute query_;
	-- reset role;
end;
$$ language plpgsql;


---------------------------------get_course_selection---------------------------
create or replace function get_course_selection(input_data text)
returns table(cname text,
			  cid char(5),
			  total_time text, 
			  tname text, 
			  college text, 
			  students_num int)
as $$
declare
	query_ text;
	course record;
	query_data text;
begin
	query_ := format('select * from courses_information order by coname, cid');
	query_data := '%'||input_data||'%';
	if input_data is not null then
		query_ := format('select * from courses_information where cid like %L or cname like %L order by coname, cid', 
		query_data, query_data);
	end if;

	for course in execute query_
	loop
		cname := course.cname;
        cid := course.cid;
        total_time := course.time;
        tname := course.tname;
        college := course.coname;
		query_ := format('select count(*) from choices where cid = %L', course.cid);
		execute query_ into students_num;
		return next;
	end loop;
	-- reset role;
end;
$$ language plpgsql;

------------------------------------获取学生已选课程以及对应分数------------------------------
create or replace function get_course_score(input_data text, sid varchar(8))
returns table(cname text,
			  cid char(5),
			  total_time text, 
			  tname text, 
			  college text, 
			  score int)
as $$
declare
	query_ text;
	course record;
	query_data text;
begin
	query_ := format('
	select cname, cid, time, tname, coname
	from courses_information
	where cid in (select cid from choices where sid = %L)
	order by coname, cid;
	', sid);
	query_data := '%'||input_data||'%';
	if input_data is not null then
		query_ := format('
		select cname, cid, time, tname, coname
		from courses_information 
		where cid like %L or cname like %L 
		and cid in (select cid from choices where sid = %L)
		order by coname, cid', query_data, query_data, sid);
	end if;

	for course in execute query_
	loop
		cname := course.cname;
        cid := course.cid;
        total_time := course.time;
        tname := course.tname;
        college := course.coname;
		query_ := format('select score from choices where cid = %L and sid = %L', course.cid, sid);
		execute query_ into score;
		return next;
	end loop;
	-- reset role;
end;
$$ language plpgsql;

-------------------------------------触发器验证添加课程是否合法--------------------------------
create or replace function validate_course_teacher()
returns trigger as $$
declare
	query text;
	current_course record;
	course record;
begin
	query := format('select * from courses where cid = %L', new.cid);
	execute query into current_course;
	query := format('select * from courses where cid in 
	(select cid from course_teacher where tid = %L) 
	except select * from courses where cid = %L', new.tid, new.cid);
	for course in execute query
	loop
		if current_course.end_week>=course.start_week and current_course.start_week<=course.end_week 
		and current_course.week_day=course.week_day and current_course.end_period>=course.start_period 
		and current_course.start_period<=course.end_period then
			raise exception '教师课程时间段重复';
		end if;
	end loop;
	return new;
end;
$$ language plpgsql; 

create or replace trigger validate_course_trigger
before insert or update on course_teacher
for each row
execute function validate_course_teacher();

--------------------------判断选课是否合法-----------------------------------------------------
create or replace function validate_choice()
returns trigger as $$
declare
	query text;
	current_course record;
	course record;
begin
	if new.no is null then
		query := format('select max(no) from choices');
		execute query into new.no;
		new.no := new.no+1;
		if new.no is null then
			new.no := 1;
		end if;
	end if;
	query := format('select * from courses where cid = %L', new.cid);
	execute query into current_course;
	query := format('select * from courses
					 where cid in (
					 	select cid 
						from choices_information
						where sid = %L
					 )', new.sid);
					 
	for course in execute query
	loop
		if current_course.end_week>=course.start_week and current_course.start_week<=course.end_week 
		and current_course.week_day=course.week_day and current_course.end_period>=course.start_period 
		and current_course.start_period<=course.end_period then
			raise exception '学生课程时间冲突';
		end if;
	end loop;
	return new;
end;
$$ language plpgsql; 


create or replace trigger validate_choice_trigger
before insert on choices
for each row
execute function validate_choice();

----------------------------检查删除选课是否合法（如果已经登分，即为已修课程，则不能删除）---------
-- create or replace function validate_delete_choice()
-- returns trigger as $$
-- declare
-- 	query text;
-- 	score int;
-- begin
-- 	query := format('select score from choices where sid = %L and cid = %L', old.sid, old.cid);
-- 	execute query into score;
-- 	if score is not null then
-- 		raise exception '已修课程无法退课';
-- 	end if;
-- 	return old;
-- end;
-- $$ language plpgsql; 


-- create or replace trigger validate_delete_choice_trigger
-- before delete on choices
-- for each row
-- execute function validate_delete_choice();
--------------------------学生------------------------------------
create or replace function validate_students()
returns trigger as $$
declare
	query text;
begin
	query := format('insert into students_password values(%L, %L)', new.sid, 'Shujuku1234');
	execute query;
	return new;
end;
$$ language plpgsql; 


create or replace trigger validate_students_trigger
after insert on students
for each row
execute function validate_students();