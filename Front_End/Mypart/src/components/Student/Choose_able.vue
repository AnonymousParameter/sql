<template>
    <div>
        <div class="header">
            可选课程
        </div>
        <div class="search-container">
          <input class="search" type="text" v-model="searchText.input_data" placeholder="请输入课程号或者课程名称查询"> 
          <button type="primary" class="search_button" @click="change_data()">搜索</button>
        </div>
        <div class="button">
            <el-button
                type="primary"
                class="back-button"
                :class="{ 'active-button': selectedButton === 'button3' }"
                @click="selectButton('button3')"
            >全部课程</el-button>
        <el-button
                type="primary"
                class="back-button"
                :class="{ 'active-button': selectedButton === 'button1' }"
                @click="selectButton('button1')"
            >本专业</el-button>
            <el-button
                type="primary"
                class="back-button"
                :class="{ 'active-button': selectedButton === 'button2' }"
                @click="selectButton('button2')"
            >跨专业</el-button>
        </div>
        <div class="body">
            <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left" v-if="is_back">返回</el-button>
            <el-table :data="paginatedTableData" style="width: 89%" class="table">
                <el-table-column prop="cid" label="课程编号" width="80" align="center">
                </el-table-column>
                <el-table-column prop="cname" label="课程名称" width="120" align="center">
                </el-table-column>
                <el-table-column prop="tname" label="任课教师" width="80" align="center">
                </el-table-column>
                <el-table-column prop="college" label="开课学院" width="130" align="center">
                </el-table-column>
                <el-table-column prop="time" label="开课时间" width="250" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="220" align="center">
                    <template slot-scope="scope">
                        <el-button size="small"  :disabled="scope.row.is_choosed" type="primary" @click="showdia_choose(scope.row)">{{ scope.row.is_choosed === 1? '已选' : '选课' }}
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[5, 10, 20]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next"
            :total="tableData.length">
            </el-pagination>

            <el-dialog title="选修课程" :visible.sync="dia_choose" width="30%">
              <div>
                  确定要选修此课程吗？
              </div>
              <div style="text-align: center;">
                  <el-button type="primary" @click="Choose_courses()">
                      确定
                  </el-button>
              </div>
          </el-dialog>

        </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['active'],
    watch: {
     active(newVal) {
        if (newVal === 2) { // 判断是否是当前组件对应的active值
            this.getdata();
        }
        }
    },
    created() {
        this.getdata()
          
    },
    data() {
        return {
            tableData: [],
            dia_choose:false,
            selectedButton: '',
            currentPage: 1,
            pageSize: 10,
            is_back:false,
            want_choose:{
                cid:'',
            },
            searchText:{
              input_data:'',
            },
        }
    },
    computed: {
    paginatedTableData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.tableData.slice(startIndex, endIndex);
    },
  },
    methods: {

        handleSizeChange(val) {
            this.pageSize = val;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        },
        getdata() {
            this.$axios.get("/api/students/allCourses").then((res) => {
                console.log(res.data);
                if (res.data.code==200) {
                    this.tableData = res.data.courses_data;
                }
            })
        },
        selectButton(buttonId) {
            this.selectedButton = buttonId;
            if(this.selectedButton=="button1"){
                this.$axios.get("/api/students/allCourses/major").then((res) => {
                    console.log(res.data);
                    if (res.data.code==200) {
                        this.tableData = res.data.courses_data;
                    }
                })
            }
            else if(this.selectedButton=="button2"){
                this.$axios.get("/api/students/allCourses/others").then((res) => {
                    console.log(res.data);
                    if (res.data.code==200) {
                        this.tableData = res.data.courses_data;
                    }
                })  
            }
            else{
                this.getdata();
            }
        },
        showdia_choose(row) {
            this.dia_choose = true;
            this.want_choose.cid=row.cid;
        },
        Choose_courses(){
            this.$axios.post("/api/students/allCourses",this.want_choose).then((res) => {
                console.log(res.data);
                if (res.data.code==200) {
                    this.getdata();
                    this.dia_choose=false;
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
        goBack(){
            this.is_back=false;
            this.getdata();
        },
        change_data(){
        if (this.searchText.input_data!=""){
            this.$axios.post("/api/students/allCourses/select",this.searchText).then((res) => {
                // console.log(res.data);
                if (res.data.code == 200) {
                    this.tableData = res.data.courses_data;
                    this.is_back=true;
                    this.selectedButton='';
                    // console.log(this.tableData);
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
        }
        else{
            this.getdata()
            this.$message({
                message:"未输入内容",
                type:"warning"
            })
        }
      },
    }
  }
  </script>
  
  <style scoped>
  .header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
  }
  
  .search-container{
      display:flex;
    align-items: center;
    justify-content: space-between;
    width: 400px; 
    height: 40px;
    margin: 20px auto; 
    border: 1px solid #e3e3e3;
    border-radius: 5px;
    overflow: hidden; 
    /*border-color: #4d9bef;*/
    
  }
  
  .search{
      flex: 1; 
      border-radius: 10px;
    padding: 10px;
    border: none;
    outline: none; 
   
  }
  
  .search_button{
      background-color: #4d9bef;
    color: white;
    padding: 10px 20px;
    height: 40px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease; /* 过渡效果，鼠标悬停时背景色平滑变化 */
  }
  .search_button:hover {
    background-color: #0056b3; /* 鼠标悬停时的背景色变化 */
  }
  .body {
  
    width: 70%;
    margin: auto;
    margin-top: 30px;
    margin-left: 250px;
  }

  .active-button {
    color: rgb(20, 16, 20); /* 可以根据需求调整高亮颜色 */
    font-weight: bold; /* 使文字加粗，突出显示，也可按需调整样式 */
    }

    .button{
        display: flex;
        margin-left: 550px;
        align-items: center; /*子元素在交叉轴（垂直方向）居中 */
    }
    .back-button{
        background-color: transparent;
        border: none;
        color: black;
}

  </style>