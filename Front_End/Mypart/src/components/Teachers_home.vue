<template>
  <div>
      <div class="header">
        中山大学学生选课系统
      </div>
      <div class="body">
          <!-- 左侧导航栏 -->
          <div class="liner">
              <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                  active-text-color="#ffd04b" @select="handleselect">
                  <el-menu-item index="1">
                      <i class="el-icon-menu"></i>
                      <span slot="title">课程管理</span>
                  </el-menu-item>

                  <el-menu-item index="2">
                      <i class="el-icon-menu"></i>
                      <span slot="title">学生管理</span>
                  </el-menu-item>

                  <el-menu-item index="3">
                      <i class="el-icon-menu"></i>
                      <span slot="title">选课管理</span>
                  </el-menu-item>   
                  <el-menu-item index="4">
                      <i class="el-icon-menu"></i>
                      <span slot="title">个人中心</span>
                  </el-menu-item> 
                  <el-menu-item index="5">
                      <i class="el-icon-menu"></i>
                      <span slot="title">退出登录</span>
                  </el-menu-item> 
                  <!--               
                  <el-submenu index="2">
                      <template slot="title">
                          <i class="el-icon-setting"></i>
                          <span>全部课程</span>
                      </template>
                      <el-menu-item-group>

                          <el-menu-item index="3">已选课程</el-menu-item>
                          <el-menu-item index="4"></el-menu-item>
                          <el-menu-item index="5">未发货订单</el-menu-item>
                      </el-menu-item-group>

                  </el-submenu>

                  <el-submenu>
                      <template slot="title">
                          <i class="el-icon-s-home"></i>
                          <span>个人中心</span>
                      </template>
                      <el-menu-item-group>

                          <el-menu-item index="6">个人信息</el-menu-item>
                          <el-menu-item index="7">修改密码</el-menu-item>
                      </el-menu-item-group>

                  </el-submenu>
                -->

              </el-menu>
          </div>
          <div class="main">
            <div id="courses" v-show="active == 1">
                  <CoursesManagement></CoursesManagement>
              </div>            
            <div id="Students" v-show="active == 2">
                  <StudentsManagement></StudentsManagement>
              </div>
              <div id="choose" v-show="active == 3">
                  <ChooseManagement></ChooseManagement>
              </div>
              <div id="choose" v-show="active == 4">
                  <SelfManagement></SelfManagement>
              </div>
          </div>

          <el-dialog title="退出登录" :visible.sync="dia_dlt" width="30%">
              <div>
                  确定要退出登录吗？
              </div>
              <div style="text-align: center;">
                  <el-button type="primary" @click="return_login()">
                      确定
                  </el-button>
              </div>
          </el-dialog>

      </div>
  </div>
</template>

<script>
import ChooseManagement from './Teacher/ChooseManagement.vue'
import CoursesManagement from './Teacher/CoursesManagement.vue'
import StudentsManagement from './Teacher/StudentsManagement.vue'
import SelfManagement from './Teacher/SelfManagement.vue';
export default {
  components: {
      ChooseManagement:ChooseManagement,
      CoursesManagement:CoursesManagement,
      StudentsManagement:StudentsManagement,
      SelfManagement:SelfManagement
  },
  data() {
      return {
          active: 1,
          dia_dlt:false,
      };
  },
  methods: {
      handleselect(index) {
          if(index==5){
            this.dia_dlt=true;
          }
          else{
            this.active = index;
          }
      },
      return_login(){
        this.$router.push('/');
      }
  },
}  
</script>

<style scoped>
.header {
  width: 100%;
  height: 10vh;
  /*text-align: center; */
  line-height: 10vh;
  font-size: 30px;
  font-weight: 800;
  background-color: #e3e3e3;
  /* padding-left: 100px; */
}
.el-menu-item {
  height: 100px;
  font-size: 18px;
  width: 100%;
}

.body {

  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: space-around;

  grid-template-rows: auto; /* 行高自动适应内容 */
}

.liner {
  width: 14%;
  height: 100vh;
  background-color: #545c64;
  margin-left: 0%;


  /*
  display: flex; /* 将.liner变为弹性容器 */
  /*flex-direction: column; /* 设置主轴方向为垂直方向 */
  /*justify-content: center; /* 在主轴（垂直方向）上居中对齐内部元素 */
}

.main {
  width: 85%;
}
</style>

<!--
<template>
  <div id=".top_menu">
    <el-menu
        :default-active="toIndex" 
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64" 
        text-color="#fff"
        active-text-color="#ffd04b"
        @select="handleSelect"
    >
      <el-menu-item v-for="(item, index) in itemList" :index="item.path" :key="index">
        <span slot="title">{{ item.title }}</span>
      </el-menu-item>
    </el-menu>
    <el-main>
      <router-view></router-view>
    </el-main>
  </div>
</template>

<script>
export default {
  name: "top_menu",
  data() {
    return {
      itemList: [    // 水平一级菜单栏的菜单
        { path: '/Students_home', title: '选课' },
        { path: '/movie', title: '个人中心' },
        { path: '/novel', title: '小说' },

      ],
    };
  },
  computed: {
    toIndex(){  // 根据路径绑定到对应的一级菜单，防止页面刷新重新跳回第一个
      return'/Students_home'
      //return '/' + this.$route.path.split('/')[0];
    },
  },
  methods: {
    handleSelect(path){  // 切换菜单栏
      this.$router.push({
        path: path
      });
    },
  },

};
</script>

<style scoped>
</style>


<style scoped>
.header {
  width: 100%;
  height: 10vh;
  /* text-align: center; */
  line-height: 10vh;
  font-size: 25px;
  font-weight: 800;
  background-color: #e3e3e3;
  /* padding-left: 100px; */
}

.body {
  width: 100%;
  height: 648px;
  display: flex;
  justify-content: space-around;
}

.top_menu {
  width: 15%;
  height: 100%;
  background-color: #545c64;
}

.main {
  width: 85%;
}
</style>
-->