<template>
  <div id="app">
    <el-container>
      <!-- 侧边栏组件 -->
      <el-aside width="15%">

        <div class="liner">
        <el-menu
          default-active="1"
          class="el-menu-vertical-demo"               
          :collapse="false"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleSelect">
          <h3>{{isCollapse?'标题':'学生选课系统管理'}}</h3>
          <el-menu-item v-for="(item, index) in itemList" :index="item.index" :key="index">
              <span slot="title">{{ item.title }}</span>
            </el-menu-item>
        </el-menu>
      </div>

      </el-aside>
      <el-container>
        <!-- 顶部组件 -->
        <el-header>
          <common-header></common-header>
        </el-header>
        <!-- 首页组件 
        <el-main>
          <Index_home></Index_home>
        </el-main>
      -->
      <div class="main">
    <div id="Choose_able" v-show="active==1">
        <Index_home ref="Index_home"></Index_home>
      </div>
      <div id="Choose_able" v-show="active==2">
        <Choose_able ref="Choose_able"></Choose_able>
      </div>
      <div id="Choose_ed" v-show="active==3">
        <Choose_ed ref="Choose_ed"></Choose_ed>
      </div>
      <div id="Self_center" v-show="active==4">
        <Self_center ref="Self_center"></Self_center>
      </div>
    </div>

      </el-container>
    </el-container>
  </div>
</template>
 
<script>
//import CommonAside from './home/CommonAside.vue';
import CommonHeader from './home/CommonHeader.vue';
import Index_home from './home/Index_home.vue';
import Choose_able from './Student/Choose_able.vue';
import Choose_ed from './Student/Choose_ed.vue';
import Self_center from './Student/Self_center.vue';
 
export default {
  name: "App",
  components: {
    //CommonAside,
    CommonHeader,
    Index_home,
    Choose_able,
    Choose_ed,
    Self_center,
  },
  mounted(){
    console.log(this)
  },
  data() {
      return {
        active:'1',
        itemList: [    // 水平一级菜单栏的菜单
          { index: '1', title: '首页' },
          { index: '2', title: '全部选课' },
          { index: '3', title: '已选课程' },
          { index: '4', title: '个人中心' },

      ],     
      }
    },
    methods: {
    handleSelect(index){  // 切换菜单栏
      this.active=index;
      if(index==1){
        this.$refs.Index_home.getdata();
      }
      else if(index==2){
        this.$refs.Choose_able.getdata();
      }
      else if(index==3){
        this.$refs.Choose_ed.getdata();
      }
      else{
        this.$refs.Self_center.getdata();
      }
    },
  },
}
</script>
 
<style>
html,body{
  margin: 0px;
  padding: 0px;
}
.el-header {
  background-color: #303133;
  color: #333;
  text-align: center;
  line-height: 60px;
}
 
.el-aside {
  background-color: #545c64;
  color: #333;
  text-align: center;
  line-height: 200px;
  height: 100vh;
}
 
.el-main {
  background-color: #F2F6FC;
  color: #333;
  text-align: center;
  padding: 10px;
}
 
body > .el-container {
  margin-bottom: 40px;
}
 
.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}
 
.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 100vh;
    border: none;
  }
  .el-menu {
     border: none;
  }
  .el-menu-item-group__title {
      padding: 0; 
  }

.liner {
  width: 15%;
  height: 100%;
  background-color: #545c64;
}   

  h3{
      color: aliceblue;
      line-height: 30px; 
  }
   
  span,.el-menu-item{
    font-size: 16px;
  }
</style>