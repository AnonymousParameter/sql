<template>
    <div>
        <el-row>
            <el-col :span="1">
                <div>
                    <el-button icon="el-icon-menu" size="mini" @click="menuHandler"></el-button>
                </div>
            </el-col>
            <el-col :span="1"><div class="table">首页</div></el-col>
            <el-col :span="20"><div class="table">&nbsp;</div></el-col>
            <el-col :span="2">
                <!--   头像下拉菜单 -->
                <el-dropdown trigger="click">
                    <div class="circle">
                        <el-avatar :size="50" :src="imgUrl"></el-avatar>
                    </div>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item icon="el-icon-close" @click.native="goToLogout">退出</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-col>
        </el-row>
    </div>
</template>
 
<script>
export default {
  name: "CommonHeader",

  data() {
    return {
      //菜单控制
      isCollapse: false,
      //头像地址
      imgUrl:require('@/assets/exo6.jpg')
    }
  },
  methods: {
    menuHandler(){
        //this.$store.commit('MENUHANDLER')
        this.isCollapse=!this.isCollapse;
        window.localStorage.setItem("isCollapse",this.isCollapse)
    },
    goToLogout() {
            this.$router.push('/'); 
        }
  }
}
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.table {
  color: #C0C4CC;
  line-height: 60px;
}
.circle{
    height: 60px;
}
.el-avatar{
    margin: 5px 0 0 0;
}
</style>