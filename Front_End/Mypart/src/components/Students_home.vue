<template>
  <div>
    <div class="header">
      中山大学学生选课系统
    </div>
    <div id="top_menu">
      <el-menu
          default-active="1" 
          class="el-menu-demo"
          mode="horizontal"
          background-color="#545c64" 
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleSelect"
      >
        <el-menu-item v-for="(item, index) in itemList" :index="item.index" :key="index">
          <span slot="title">{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="main">
      <div id="Choose_able" v-show="active==1">
        <Choose_able></Choose_able>
      </div>
      <div id="Choose_ed" v-show="active==2">
        <Choose_ed></Choose_ed>
      </div>
      <div id="Self_center" v-show="active==3">
        <Self_center></Self_center>
      </div>
    </div>
  </div>
</template>

<script>
import Choose_able from './Student/Choose_able.vue';
import Choose_ed from './Student/Choose_ed.vue';
import Self_center from './Student/Self_center.vue';
export default {
  name: "top_menu",
  components:{
    Choose_able:Choose_able,
    Choose_ed:Choose_ed,
    Self_center:Self_center
  },
  data() {
    return {
      active:'1',
      itemList: [    // 水平一级菜单栏的菜单
        { index: '1', title: '全部选课' },
        { index: '2', title: '已选课程' },
        { index: '3', title: '个人中心' },

      ],
    };
  },
  methods: {
    handleSelect(index){  // 切换菜单栏
      this.active=index;
    },
  },

};
</script>

<style scoped>
</style>


<style scoped>
.header {
  width: 100%;
  height: 5vh;
  text-align: center; 
  line-height: 7vh;
  font-size: 25px;
  font-weight: 800;
  padding-top: 0vh;
  background-color: #545c64;
  color:white;
  /* padding-left: 100px; */
}
.menu-title {
    display: flex;
    font-size: 18px;
    color: black;
    margin: 0 auto;
    /* 可以根据实际情况调整左右的外边距，让其看起来在中心位置 */
    margin-left: 40%;
    margin-right: 40%;
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
