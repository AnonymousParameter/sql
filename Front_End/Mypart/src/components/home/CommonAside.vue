<template>
  <div>
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

  <div class="main">
    <div id="Choose_able" v-show="active==2">
        <Index_home></Index_home>
      </div>
      <div id="Choose_able" v-show="active==3">
        <Choose_able></Choose_able>
      </div>
      <div id="Choose_ed" v-show="active==4">
        <Choose_ed></Choose_ed>
      </div>
      <div id="Self_center" v-show="active==5">
        <Self_center></Self_center>
      </div>
    </div>

  </div>
  </template>


  <script>
  import Choose_able from '../Student/Choose_able.vue';
  import Choose_ed from '../Student/Choose_ed.vue';
  import Self_center from '../Student/Self_center.vue';
  import Index_home from './Index_home.vue';
  export default {
    name: "CommonAside",
    components:{
      Choose_able:Choose_able,
      Choose_ed:Choose_ed,
      Self_center:Self_center,
      Index_home:Index_home
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
    },
  },
  }
  </script>
   
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style lang="less" scoped>
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