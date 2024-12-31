<template>
    <div>
        <div class="header">
            个人信息
        </div>
        <div class="body">
            <el-form ref="form" :model="form" label-width="20%" id="selectForm">
                <el-form-item label="账号/工号："  prop="tid">
                    <span>{{ form.tid }}</span>
                    <!-- <el-input v-model="form.user_name"></el-input> -->
                </el-form-item>
                <el-form-item label="姓名：" prop="tname">
                    <span>{{ form.tname }}</span>
                    <!-- <el-input v-model="form.real_name"></el-input> -->
                </el-form-item>
                <el-form-item label="学院：" prop="college">
                    <span>{{ form.college }}</span>
                    <!-- <el-input v-model="form.age"></el-input> -->
                </el-form-item>
                <el-form-item label="邮箱：" prop="email">
                    <span>{{ form.email }}</span>
                    <!-- <el-input v-model="form.sex"></el-input> -->
                </el-form-item>
                <el-form-item label="开设课程：" prop="courses">
                    <el-table :data="form.courses" class="courses" style="width: 150%" :show-header="false">
                        <el-table-column prop="cid" label="课程编号"></el-table-column>
                        <el-table-column prop="cname" label="课程名称"></el-table-column>
                        <el-table-column prop="time" width="200px" label="开课时间"></el-table-column>
                    </el-table>
                    <!-- <el-input v-model="form.sex"></el-input> -->
                </el-form-item>
                <el-form>
                    <el-button class="largebutton" type="primary"  @click="show_edit()" >修改密码</el-button>
                </el-form>
            </el-form>



            <el-dialog title="修改密码" :visible.sync="dia_edit" width="30%">
              <el-form ref="password_form" :model="password_form" label-width="100px" :rules="password_form_rules">
                  <el-form-item label="原密码：" prop="old_password" >
                      <el-input style="width: 300px;" v-model="password_form.old_password"></el-input>
                  </el-form-item>
                  <el-form-item  label="新密码："  prop="new_password">
                      <el-input style="width: 300px;" v-model="password_form.new_password" show-password spellcheck="false"></el-input>
                  </el-form-item>
                  <el-form-item label="确认密码：" prop="check_password">
                      <el-input style="width: 300px;" v-model="password_form.check_password" show-password spellcheck="false"></el-input>
                  </el-form-item>
              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="change_password()">
                      修改
                  </el-button>
              </div>
          </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            dia_edit:false,
            currentPage: 1,
            pageSize: 10,
            form: {
                tname: '',
                tid: '',
                college: '',
                email: '',
                password:'',
                courses:[],
            },
            password_form:{
                old_password:'',
                new_password:'',
                check_password:'',

            },
            password_form_rules:{
                old_password: [{ required: true, message: "必填", trigger: 'blur' }],
                new_password: [{ required: true, message: "必填", trigger: 'blur' }],
                check_password: [{ required: true, message: "必填", trigger: 'blur' }]
            }
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/teachers/information").then((res) => {
                console.log(res.data);
                if (res.data.code == 200) {
                    this.form=res.data.data
                    this.$message({
                        message:res.data.msg,
                        type:"success"
                    })
                }
                else{
                    this.$message({
                        message:res.data.msg,
                        type:"error"
                    })
                }
            })
        },
        change_password() {
            this.$refs.form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    if (this.password_form.check_password == this.password_form.new_password) {
                        this.$axios.post("/api/teachers/information/change_password", this.password_form).then((res) => {
                            if (res.data.code == 200) {
                                this.$message({
                                    message: res.data.msg,
                                    type: "success"
                                })
                                this.dia_edit=false
                                window.localStorage.setItem("token", res.data.token);
                            } else {
                                this.$message({
                                    message: res.data.msg,
                                    type: "error"
                                })
                            }
                        })
                    }
                    else {
                        this.$message({
                            message: "新密码与确认密码不一致",
                            type: "error"
                        })
                    }
            })
        },
        show_edit(){
            this.dia_edit=true
        }
    },
}
</script>

<style scoped>
.largebutton {
    margin-left: 300px;
    margin-top: 50px;
    width: 150px;
    height: 40px;
}
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 50%;
    /* margin: auto; */
    margin-top: 75px;
    margin-left: 300px;
}

#selectForm>>>.el-form-item__label {
    font-size: 18px;
    width: 1000px;
}


span {
    font-size: 18px;
}

/*去掉表格单元格边框*/
.courses th{
     border:none;
   }
.courses td,.courses th.is-leaf {
  border:none;
}
 /*表格最外边框*/
.courses .el-table--border, .el-table--group{
     border: none;
   }
  /*头部边框*/
   .courses thead tr th.is-leaf{
     border: 0px solid #EBEEF5;
     border-right: none;
   }
.courses thead tr th:nth-last-of-type(2){
  border-right: 0px solid #EBEEF5;
}
 /*表格最外层边框-底部边框*/
.courses .el-table--border::after,.courses .el-table--group::after{
     width: 0;
   }
.courses::before{
  width: 0;
}
.courses .el-table__fixed-right::before,.el-table__fixed::before{
  width: 0;
}
.courses .el-table__header tr th{
  background: #fff;
  color: #333333 ;
  padding: 3px ;
  height: 36px ;
  border: 0px;
  font-size: 15px;
}

</style>