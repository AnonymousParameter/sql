<template>
  <div>
      <div class="header">
          选课管理
      </div>
      <div class="search-container" v-show="active==1">
        <input class="search" type="text" v-model="searchText.input_data" placeholder="请输入课程号或者课程名称查询"> 
        <button type="primary" class="search_button" @click="change_data()">搜索</button>
      </div>
      <div class="body" v-show="active==1">
        <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left" v-if="is_back">返回</el-button>
          <el-table :data="paginatedTableData" style="width: 100%" class="table">
              <el-table-column prop="cid" label="课程编号" width="80" align="center">
              </el-table-column>
              <el-table-column prop="cname" label="课程名称" width="80" align="center">
              </el-table-column>
              <el-table-column prop="tname" label="任课教师" width="80" align="center">
              </el-table-column>
              <el-table-column prop="college" label="开课学院" width="150" align="center">
              </el-table-column>
              <el-table-column prop="time" label="开课时间" width="250" align="center">
              </el-table-column>
              <el-table-column prop="num" label="已选人数" width="80" align="center">
              </el-table-column>
              <el-table-column prop="operate" label="操作" width="250" align="center">
                  <template slot-scope="scope">
                      <el-button size="small" type="success" @click="show_pages(scope.row)">查看&编辑选课学生
                      </el-button>
                      <!--
                      <el-button size="small" type="danger" @click="showdia_dlt(scope.row)">删除课程
                      </el-button>
                    -->
                  </template>
              </el-table-column>
              <!--
              <el-table-column width="120" align="center">
                  <template slot="header">
                      <el-button icon="el-icon-plus" size="small" type="success" @click="showdia_add()">添加课程
                      </el-button>
                  </template>
              </el-table-column>
              -->
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

      </div>

      <div class="Preview" v-show="active==2">
        <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left">返回</el-button>
        <el-table :data="paginatedPageData" style="width: 100%" class="table_preview">
          <el-table-column type="index" label="序号" width="50" align="center"></el-table-column>
              <el-table-column prop="sid" label="学号" width="90" align="center">
              </el-table-column>
              <el-table-column prop="sname" label="姓名" width="70" align="center">
              </el-table-column>
              <el-table-column prop="grade" label="年级" width="80" align="center">
              </el-table-column>
              <el-table-column prop="college" label="学院" width="100" align="center">
              </el-table-column>
              <el-table-column prop="email" label="邮箱" width="150" align="center">
              </el-table-column>
              <el-table-column prop="score" label="分数" width="80" align="center">
                <template slot-scope="scope">
                  <el-input
                    v-if="scope.row.editingScore"
                    v-model="scope.row.score"
                    @keyup.enter.native="handleScoreEnter(scope.row)"/>
                    <!--@blur="handleScoreBlur(scope.row)"-->
                  <span v-else>{{ scope.row.score }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="operate" label="操作" width="230" align="center">
                  <template slot-scope="scope">
                      <el-button size="small" type="danger"  @click="showdia_dlt(scope.row)">帮TA退课
                      </el-button>
                      <el-button size="small" type="success" @click="showdia_edit(scope.row)">登记分数
                      </el-button>
                  </template>
              </el-table-column>

              <el-table-column width="120" align="center">
                  <template slot="header">
                      <el-button icon="el-icon-plus" style="border-radius: 5px;" size="small" type="primary" @click="showdia_add()">帮TA选课
                      </el-button>
                  </template>
              </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange1"
            @current-change="handleCurrentChange1"
            :current-page="currentPage1"
            :page-sizes="[5, 10, 20]"
            :page-size="pageSize1"
            layout="total, sizes, prev, pager, next"
            :total="page_form.pageData.length">
            </el-pagination>


          <el-dialog title="添加选课学生" :visible.sync="dia_add" width="30%">
              <el-form ref="add_form" :model="add_form" label-width="100px" :rules="add_form_rules">
                  <el-form-item label="学号：" prop="sid" >
                      <el-input style="width: 300px;" v-model="add_form.sid"></el-input>
                  </el-form-item>
                  <el-form-item  label="姓名：" prop="sname">
                      <el-input style="width: 300px;" v-model="add_form.sname"></el-input>
                  </el-form-item>
                  <el-form-item label="学院：" prop="college">
                      <el-input style="width: 300px;" v-model="add_form.college"></el-input>
                  </el-form-item>
              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="addstudent()">
                      添加
                  </el-button>
              </div>
          </el-dialog>

          <el-dialog title="退课" :visible.sync="dia_dlt" width="30%">
              <div>
                  确定帮TA退课吗？
              </div>
              <div style="text-align: center;">
                  <el-button type="primary" @click="deletestudent()">
                      确定
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
          tableData: [{cid:"111",cname:"ddvbhfgdfsd",college:"dsvsdb",time:"fdvfsbvfbf",tname:"dsfcdav",num:"fafsggd"}],
          active:1,
          dia_add: false,
          dia_dlt: false,
          origin_score:'',
          select_courses:{},
          currentPage: 1,
          pageSize: 10,
          currentPage1: 1,
          pageSize1: 10,
          //dia_pages:false,
          searchText:{
            input_data:'',
          },
          page_form:{
            pageData:[{sid:"111",sname:"ddvbhfgdfsd",college:"dsvsdb",email:"dsfcdav",grade:"ddqwd",score:"85",editingScore: false}],
            num:'',
          },
          add_form: {
              sname: '',
              sid:'',
              college:'',
          },
          want_delete: '',
          add_form_rules: {
              sid: [{ required: true, message: '必填项', trigger: 'blur' }],
              sname: [{ required: true, message: '必填项', trigger: 'blur' }],
              college: [{ required: true, message: '必填项', trigger: 'blur' }],

          },

      }
  },
  computed: {
    paginatedTableData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.tableData.slice(startIndex, endIndex);
    },
    paginatedPageData() {
      const startIndex1 = (this.currentPage1 - 1) * this.pageSize1;
      const endIndex1 = startIndex1 + this.pageSize1;
      return this.page_form.pageData.slice(startIndex1, endIndex1);
    }
  },
  methods: {
    handleSizeChange(val) {
        this.pageSize = val;
    },
    handleCurrentChange(val) {
        this.currentPage = val;
    },
    handleSizeChange1(val) {
        this.pageSize1 = val;
    },
    handleCurrentChange1(val) {
        this.currentPage1 = val;
    },
      getdata() {
          this.$axios.get("/api/teachers/courseSelection").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.tableData = res.data.courses_data;
              }
          })
      },
      goBack(){
        this.active=1;
        this.getdata();
        this.is_back=false;
      },
      showdia_add() {
          this.dia_add = true;
      },
      showdia_edit(row){
        this.origin_score=row.score;
        row.editingScore=true;
      },
      show_pages(row){
        this.active=2;
        this.select_courses=row
        
        this.$axios.post("/api/teachers/courseSelection/select_students",this.select_courses).then((res) => {
          if(res.data.code==200){
            this.page_form.pageData=res.data.students_data
            this.page_form.num=row.num
            /*
            this.$message({
              message:res.data.msg,
              type:"success"
            })
              */
          }
          else{
            this.$message({
              message:res.data.msg,
              type:"error"
            })
          }
        })
          
        
      },
      edit_score(row){
        this.$axios.post("/api/teachers/courseSelection/modify",{cid:this.select_courses.cid, sid:row.sid, score:row.score}).then((res) => {
          if(res.data.code==200){
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
          this.show_pages(this.select_courses);
        })
      },
      isScoreVaild(score){
        return score>=0 && score <=100 && isNaN(score);
      },
      handleScoreBlur(row) {
        if(this.isScoreVaild(row.score)){
          row.editingScore = false; // 失去焦点时，结束编辑状态
          if(row.score==this.origin_score){
            return;
          }
          this.edit_score(row);
        }
        else{
          this.$message({
            message:"分数必须在0 - 100之间，请重新输入!",
            type:"error"
          })
          //row.editingScore=false;
          this.show_pages(this.select_courses);
        }
        //console.log("分数修改完成，当前行数据:", row);
      },
      handleScoreEnter(row) {
        this.handleScoreBlur(row);
      },
      addstudent() {
          this.$refs.add_form.validate(valid => {
              if (!valid)
                  return;
              else //验证通过再发送请求
                  this.$axios.post("/api/teachers/courseSelection/add", {cid:this.select_courses.cid, sid:this.add_form.sid}).then((res) => {
                      console.log(res.data);
                      if (res.data.code == 200) {
                          this.$message({
                              message: res.data.msg,
                              type: "success"
                          })
                          this.dia_add = false;
                          this.show_pages(this.select_courses);
                      } else {
                          this.$message({
                              message: res.data.msg,
                              type: "error"
                          })
                      }
                  })
          })


      },
      showdia_dlt(row) {
          this.want_delete = row.sid;
          this.dia_dlt = true;
      },
      deletestudent() {
          this.$axios.delete("/api/teachers/courseSelection/delete", { data:{ sid: this.want_delete, cid: this.select_courses.cid }}).then((res) => {
            if (res.data.code == 200) {
                  this.$message({
                      message: res.data.msg,
                      type: "success"
                  })
                  this.show_pages(this.select_courses)
                  this.dia_dlt = false;
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
            this.$axios.post("/api/teachers/courseSelection/select_courses",this.searchText).then((res) => {
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
}
.Preview{
  width: 100%;
  margin: auto;
  margin-top: 30px;
  margin-left: 150px;
}
.back-button{
  background-color: transparent;
border: none;
color: black;
}

.table_preview{
  margin-left: 10px;
}
</style>