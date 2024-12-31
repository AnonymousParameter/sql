<template>
    <div>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <!-- 首页user信息 -->
            <el-card shadow= 'hover'>
              <div class="userCard">
                <el-avatar :size="150" :src=imgUrl></el-avatar>
                <div class="userInfo">
                  <p class="important-font">{{ selfData.sname }}</p>
                  <p class="secondary-font">SYSUer</p>
                </div>
              </div>
              <div class="login-info">
                <p>上次登录时间: 2022/07/06 18:16</p>
              </div>
            </el-card>
            <!-- 首页表格 -->
            <el-card shadow= 'hover' class="tableInfo">
              <div slot="header">
                <span class="important-font">课程信息</span>
              </div>
              <div>
                <el-table
                  :data="tableData"
                  stripe
                  border
                  height="420px"
                  style="width: 100%">
                  <el-table-column
                    prop="time"
                    label="时间"
                    width="210">
                  </el-table-column>
                  <el-table-column
                    prop="tname"
                    label="任课教师"
                    width="80">
                  </el-table-column>
                  <el-table-column
                    prop="cname"
                    label="课程">
                  </el-table-column>
                </el-table>
              </div> 
            </el-card>
          </div>
        </el-col>
        <el-col :span="16">
          <!-- 六个订单信息 -->
          <div class="num top-margin">
            <el-card shadow= 'hover' v-for="item in countData" :key="item.name" :body-style="{ display: 'flex',padding: 0,margin: 'auto'}" class="OrderCard">
              <i class="icon" :class="'el-icon-'+item.icon" :style="{ background: item.color}"></i>
              <div>
                <p class="important-font">{{item.value}}</p>
                <p class="secondary-font">{{item.name}}</p>
              </div>
            </el-card>
          </div>
          <!-- 柱状图 -->
          <el-card style="height: 280px">
            <div style="height:280px;" ref="barEcharts">{{initBarEcharts()}}</div>
          </el-card>
          <div class= "num graph">
            <el-card style="width: 34%;height: 265px;marginRight: 1%">
              <div style="width: 100%;height: 265px;" ref="pieEcharts">{{initPieEcharts()}}</div>
            </el-card>
            <el-card style="width:65%;height: 350px"><div style="height: 400px"><el-calendar class="calendar" v-model="value"></el-calendar></div></el-card>
          </div>
        </el-col>
      </el-row>
    </div>
    </template>
     
    <script>
    import * as echarts from 'echarts';
     
    export default {
      name: "Index_home",
      created(){
        this.getdata()
      },
      data() {
        return {
          imgUrl:require('@/assets/exo6.jpg'),
          value: new Date(),
          tableData: [],
          scoredData:[],
          selfData:[],
          score:[],
          countData:[

          {
          name: '已修课程',
          value: '',
          icon: 'success',
          color: '#2ec7c9'
        },
        {
          name: '已选课程',
          value: '',
          icon: 'star-on',
          color: '#ffb980'
        },
          ],
        }
      },
      mounted() {
        this.getdata();
    },
      methods:{
        getdata(){
          //this.countData[1].value=6;
          this.$axios.get("/api/students/information").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.selfData = res.data.data;
              }
          })
          this.$axios.get("/api/home/courses_ed").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.tableData = res.data.courses;
                  this.countData[1].value=this.tableData.length;
              }
          })
          this.$axios.get("/api/home/courses_scored").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.scoredData = res.data.courses;
                  this.countData[0].value=this.scoredData.length;
                  this.initBarEcharts();
              }
          })
          this.$axios.get("/api/students/score").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.score = res.data.score_data;
              }
          })
        },
        //柱状图
        initBarEcharts () {
        // 新建一个promise对象
          let p = new Promise((resolve) => {
            resolve()
          })
          //然后异步执行echarts的初始化函数
          p.then(() => {
            //	此dom为echarts图标展示dom
            let myChart = echarts.init(this.$refs.barEcharts)
            let option = {
              title: {
                text: '分数表'
              },
              tooltip: {},
              legend: {
                data: ['<60','60-70','70-80','80-90','90-100']
              },
              xAxis: {
                data: ['<60','60-70','70-80','80-90','90-100']
              },
              yAxis: {},
              series: [
                {
                  name: '课程门数',
                  type: 'bar',
                  data: this.score
                },
              ]
            }
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
          })
        },
        //饼图
        initPieEcharts () {
          let p = new Promise((resolve) => {
            resolve()
          })
        //然后异步执行echarts的初始化函数
          p.then(() => {
            let myChart = echarts.init(this.$refs.pieEcharts);
            const filteredData = this.score.map((val, index) => ({
            value: val,
            name: ['<60', '60-70', '70-80', '80-90', '90-100'][index]
            })).filter(item => item.value!== 0);
            let option= {
              tooltip: {
                trigger: 'item'
              },
              legend: {
                top: '0%',
                left: 'left'
              },
              series: [
                {
                  name: '分数构成',
                  type: 'pie',
                  radius: ['20%', '65%'],
                  avoidLabelOverlap: false,
                  label: {
                    show: false,
                    position: 'left'
                  },
                  labelLine: {
                    show: false,
                  },
                  /*
                  data: [
                    { value: this.score[0], name: '<60' },
                    { value: this.score[1], name: '60-70' },
                    { value: this.score[2], name: '70-80' },
                    { value: this.score[3], name: '80-90' },
                    { value: this.score[4], name: '90-100' }
                  ]*/
                 data:filteredData,
                }
              ]
            }
            myChart.setOption(option);
          })
        }
      }
    }
    </script>
     
    <!-- Add "scoped" attribute to limit CSS to this component only -->
    <style lang="less" scoped>
    .el-card__body {
        padding: 10px;
    }
  .top-margin {
      margin-top: 20px; /* 这里同样可以按需调整数值大小 */
  }
    .userCard{
      height: 180px;
      display: flex;
      border-bottom: 2px solid #DCDFE6;
      border-radius: 2px;
    }
    .userInfo{
      width: auto;
      padding: 6% 0 0 6%;
    }
    .el-calendar /deep/  .el-calendar-table .el-calendar-day{
    width: 60px;
    height: 35px;
  }

    .important-font{
        font-weight: 900;
        font-size: 25px;
    }
    .secondary-font{
      color: #909399;
    }
    .login-info{
      height: 40px;
      text-align: left;
      color: #909399;
    }
    .tableInfo{
      margin: 20px 0 0 0;
    }
    .OrderCard{
       margin: 0 0 30px 30px;
       border: #DCDFE6 1px solid;
       text-align: center;
       border-radius: 10px;
       i{
         width: 30%;
         line-height: 120px;
         font-size: 30px;
         color:#fff
       }
       div{
         width: 300px;
       }
    }
    .el-card{
      border: none;
    }
    .num{
      display: flex;
      flex-wrap: wrap;
    }
    .graph{
      margin: 15px 0 0 0;
    }
    .el-calendar{
      height: 265px ;
    }
    </style>