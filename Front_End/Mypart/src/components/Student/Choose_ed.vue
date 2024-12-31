<template>
    <div>
        <div class="header">
            已选课程
        </div>
        <div class="search-container">
          <input class="search" type="text" v-model="searchText.input_data" placeholder="请输入课程号或者课程名称查询"> 
          <button type="primary" class="search_button" @click="change_data()">搜索</button>
        </div>
        <div class="body">
            <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left" v-if="is_back">返回</el-button>
            <el-table :data="paginatedTableData" style="width: 110%" class="table">
                <el-table-column prop="cid" label="课程编号" width="100" align="center">
                </el-table-column>
                <el-table-column prop="cname" label="课程名称" width="120" align="center">
                </el-table-column>
                <el-table-column prop="tname" label="任课教师" width="100" align="center">
                </el-table-column>
                <el-table-column prop="college" label="开课学院" width="130" align="center">
                </el-table-column>
                <el-table-column prop="time" label="开课时间" width="250" align="center">
                </el-table-column>
                <el-table-column prop="score" label="分数" width="100" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" width="220" align="center">
                    <template slot-scope="scope">
                        <el-button size="small"  :type="danger"  @click="showdia_delete(scope.row)">退课
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


            <el-dialog title="退选课程" :visible.sync="dia_delete" width="30%">
              <div>
                  确定要退选此课程吗？
              </div>
              <div style="text-align: center;">
                  <el-button type="primary" @click="delete_choosed()">
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
        if (newVal === 3) { // 判断是否是当前组件对应的active值
            this.getdata();
        }
        }
    },
    created() {
        this.getdata()
        /*
        this.tableData=[
          {"cid":12,"cname":"lxd","time":"1-17周每周星期二第3节-第4节","college":"新闻与传播学院","tname":"潘蓉"},
          {"cid":12,"cname":"lxd","time":"1-17周每周星期二第3节-第4节","college":"生命科学学院","tname":"周杰因"},
        ]
          */
    },
    data() {
        return {
            tableData: [],
            dia_delete:false,
            is_back:false,
            currentPage: 1,
            pageSize: 10,
            want_delete:{
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
            this.$axios.get("/api/students/choosedCourses").then((res) => {
                console.log(res.data);
                if (res.data.code==200) {
                    this.tableData = res.data.courses_data;
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
        showdia_delete(row) {
            this.dia_delete = true;
            this.want_delete.cid=row.cid;
        },
        delete_choosed(){
            this.$axios.delete("/api/students/choosedCourses",{data:{ cid :this.want_delete.cid }}).then((res) => {
                console.log(res.data);
                if (res.data.code==200) {
                    this.dia_delete=false;
                    this.getdata();
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
        change_data(){
        if (this.searchText.input_data!=""){
            this.$axios.post("/api/students/choosedCourses/select",this.searchText).then((res) => {
                // console.log(res.data);
                if (res.data.code == 200) {
                    this.tableData = res.data.courses_data;
                    // console.log(this.tableData);
                    this.is_back=true;
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
  
    width: 80%;
    margin: auto;
    margin-top: 30px;
    margin-left: 200px;
  }
  .back-button{
  background-color: transparent;
border: none;
color: black;
}

  
  </style>