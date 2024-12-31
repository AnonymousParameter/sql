<template>
  <div class="background-container">
    <div class="login_box">
      <div class="head">
        中山大学选课系统
      </div>
      <!-- 登录 -->
      <div v-show="true">
        <el-form label-width="0" class="login_form" :model="login_form" :rules="login_rules" ref="login_form">
          <!-- 用户名 -->
          <el-form-item prop="userid">
            <el-input v-model="login_form.userid" spellcheck="false" placeholder="学号">
            </el-input>
          </el-form-item>
          <!-- 密码 -->
          <el-form-item prop="password">
            <el-input v-model="login_form.password" show-password spellcheck="false" placeholder="密码">
            </el-input>
          </el-form-item>

          <!--身份选项-->
          <el-form-item prop="role">
            <el-radio-group v-model="login_form.role" label="身份信息">
              <el-radio label="student" >学生</el-radio>
              <el-radio label="teacher">教师</el-radio>
            </el-radio-group>

          </el-form-item>

          <!-- 按钮 -->
          <el-form-item class="btns">
            <el-button class="a"  type="primary" @click="llogin()">登录</el-button>
          </el-form-item>

        </el-form>
        <!--
        <div>
          <div class="operate">
            <span id="op1" @click="change(2)">注册</span>
            <span id="op2" @click="change(3)">忘记密码</span>
          </div>
        </div>
        -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyLogin',
  data () {
    //const student = "student";
    //const teacher = "teacher";
    return {
      getcode_show: true,
      time_count: '',
      timer: null,
      target: 1,
      login_form: {
        userid: '',
        password: '',
        role: '',
      },
      login_rules: {
        userid: [
          { required: true, message: '请输入学号', trigger: 'blur' }],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }],
        role: [
          { required: true, message: '请选择身份', trigger:'blur' }
        ]
      },
    }
  },
  methods: {
    llogin() {
      this.$refs.login_form.validate(valid => {
        if (!valid)
          return;
        else //验证通过再发送请求
          this.login();
      })


    },







    async login() {

      this.$axios.post("/api/user/login", this.login_form).then((res) => {
        console.log(res.code);
        //200登录成功
        if (res.data.code != 200) {
          return this.$message({
            message: res.data.msg,
            type: 'error'
          })
        } else {
          this.$message({
            message: '登录成功',
            type: 'success'
          })

          window.localStorage.setItem("token", res.data.token);

          if (this.login_form.role == "student")
            this.$router.push('/student')
          else
            this.$router.push('/teacher')
        }
      })

    },

  }
}

</script>



<style lang="less" scoped>
.background-container {
    //background-color:rgb(2, 69, 2);
    height: 100%;
    width: 100%;

    background-image: url('@/assets/sysu3.jpg') !important;
    background-size: cover;
    background-position: center;
}

.head {
    text-align: center;
    height: 50px;
    line-height: 50px;
    font-size: larger;
    //color: rgb(236, 36, 126);
}

.login_box {
    height: 300px;
    width: 450px;
    background-color: white;//rgb(235, 174, 202);
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.reg_box {
    height: 400px;
    width: 450px;
    background-color: white;//rgb(240, 196, 74);
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.forget_box {
    height: 350px;
    width: 450px;
    background-color: white;//rgb(240, 196, 74);
    border-radius: 3px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.input {
    width: 350px;
    height: 50px;
    margin-left: 50px;
}

.el-form-item {
    width: 350px;
    margin-left: 50px;
    background-color:white; //rgb(235, 174, 202);
}

.btns {
    text-align: center;
    //color: antiquewhite;
}

.operate {
    text-align: center;
    color: #000;
    opacity: 0.5;
    font-weight: 400;
    font-size: 16px;
    margin-left: 28px;
}

.a{
  background-color: rgb(2, 69, 2);//#e694eeb9;
  border-color:black;//#f498d9b9;
}


#op1 {
    padding-left: 15px;
    padding-right: 30px;
    border-right: 1px solid #bdb9b9;
    cursor: pointer;
}

#op2 {
    padding-left: 30px;
    padding-right: 15px;
    /* border-right: 1px solid #e5e5e5; */
    cursor: pointer;
}
</style>