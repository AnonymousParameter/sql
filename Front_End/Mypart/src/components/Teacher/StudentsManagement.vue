<template>
  <div>
      <div class="header">
          学生管理
      </div>
      <div class="search-container">
        <input class="search"  type="text" v-model="searchText.input_data" placeholder="请输入学号或者姓名查询"> 
        <button type="primary" class="search_button" @click="change_data()">搜索</button>
      </div>
      <div class="body">
        <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left" v-if="is_back">返回</el-button>
          <el-table :data="paginatedTableData" style="width: 89%" class="table">
              <el-table-column prop="sid" label="学号" width="100" align="center">
              </el-table-column>
              <el-table-column prop="sname" label="姓名" width="100" align="center">
              </el-table-column>
              <el-table-column prop="grade" label="年级" width="100" align="center">
              </el-table-column>
              <el-table-column prop="college" label="学院" width="150" align="center">
              </el-table-column>
              <el-table-column prop="email" label="邮箱" width="150" align="center">
              </el-table-column>
              <el-table-column prop="operate" label="操作" width="280" align="center">
                  <template slot-scope="scope">
                      <el-button size="small" type="success" @click="showdia_edit(scope.row)">修改学生信息
                      </el-button>
                      <el-button size="small" type="danger" @click="showdia_dlt(scope.row)">开除
                      </el-button>
                  </template>
              </el-table-column>
              <el-table-column width="120" align="center">
                  <template slot="header">
                      <el-button icon="el-icon-plus" size="small" type="success" @click="showdia_add()">添加学生
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


          <el-dialog title="修改学生信息" :visible.sync="dia_edit" width="30%">
              <el-form ref="edit_form" :model="edit_form" label-width="120px" :rules="edit_form_rules">
                  <el-form-item label="学号：" prop="sid">
                    <span>{{ edit_form.sid }}</span>
                  </el-form-item>
                  <el-form-item label="姓名：" prop="sname">
                    <span>{{ edit_form.sname }}</span>
                  </el-form-item>
                  <el-form-item label="年级：" prop="grade">
                      <el-input v-model="edit_form.grade"></el-input>
                  </el-form-item>
                  <el-form-item label="学院：" prop="college">
                    <el-select v-model="edit_form.college" placeholder="请选择学院">
                      <el-option v-for="(collegeItem, index) in collegeData" :key="index" :label="collegeItem.coname" :value="collegeItem.coid"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item type="email" label="邮箱：" prop="email">
                      <el-input v-model="edit_form.email"></el-input>
                  </el-form-item>
              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="editstudent()">
                      修改
                  </el-button>
              </div>
          </el-dialog>


          <el-dialog title="添加学生" :visible.sync="dia_add" width="30%">
              <el-form ref="add_form" :model="add_form" label-width="100px" :rules="add_form_rules">
                  <el-form-item label="学号：" prop="sid" >
                      <el-input style="width: 300px;" v-model="add_form.sid"></el-input>
                  </el-form-item>
                  <el-form-item  label="姓名：" prop="sname">
                      <el-input style="width: 300px;" v-model="add_form.sname"></el-input>
                  </el-form-item>
                  <el-form-item label="年级：" prop="grade">
                      <el-input style="width: 300px;" v-model="add_form.grade"></el-input>
                  </el-form-item>
                  <el-form-item label="学院：" prop="college">
                    <el-select v-model="add_form.college" placeholder="请选择学院">
                      <el-option v-for="(collegeItem, index) in collegeData" :key="index" :label="collegeItem.coname" :value="collegeItem.coid"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item type="email" label="邮箱：" prop="email">
                      <el-input style="width: 300px;" v-model="add_form.email"></el-input>
                  </el-form-item>
              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="addstudent()">
                      添加
                  </el-button>
              </div>
          </el-dialog>


          <el-dialog title="开除学生" :visible.sync="dia_dlt" width="30%">
              <div>
                  确定要开除此学生吗？
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
      this.$axios.get("/api/teachers/students/get_college").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.collegeData = res.data.colleges_data;
              }
          })
  },
  data() {
      return {
          tableData: [],
          collegeData:[],
          dia_add: false,
          dia_dlt: false,
          dia_edit:false,
          is_back:false,
          currentPage: 1,
          pageSize: 10,
          searchText:{
            input_data:'',
          },
          add_form: {
              sid: '',
              sname: '',
              grade: '',
              college:'',
              email:'',
          },
          edit_form:{
              sid: '',
              sname: '',
              grade: '',
              college:'',
              email:'',
          },
          want_delete:'',
          add_form_rules: {
              sid: [{ required: true, message: '必填项', trigger: 'blur', pattern: /^\d{8}$/ }],
              sname: [{ required: true, message: '必填项', trigger: 'blur' }],
              college: [{ required: true, message: '必填项', trigger: 'blur' }]

          },
          edit_form_rules:{
              sid: [{ required: true, message: '必填项', trigger: 'blur' }],
              sname: [{ required: true, message: '必填项', trigger: 'blur' }],
              college: [{ required: true, message: '必填项', trigger: 'blur' }]
          },

      }
  },
  computed: {
    paginatedTableData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.tableData.slice(startIndex, endIndex);
    }
  },
  methods: {
    handleSizeChange(val) {
        this.pageSize = val;
    },
    handleCurrentChange(val) {
        this.currentPage = val;
    },
      getdata() {
          this.$axios.get("/api/teachers/students").then((res) => {
              console.log(res.data);
              if (res.data.code == 200) {
                  this.tableData = res.data.tabledata;
              }
              else{
                this.$message({
                    message:res.data.msg,
                    type:"error"
                })
              }
          })
      },
      showdia_add() {
          this.dia_add = true;
      },
      goBack(){
        this.is_back=false;
        this.getdata();
      },
      showdia_edit(row){
        this.edit_form.sid=row.sid;
        this.edit_form.sname=row.sname;
        this.edit_form.college=row.college;
        this.edit_form.email=row.email;
        this.edit_form.grade=row.grade;
        this.dia_edit=true;
      },
      change_data(){
        if (this.searchText.input_data!==""){
            this.$axios.post("/api/teachers/students/select",this.searchText).then((res) => {
                console.log(res.data);
                if (res.data.code == 200) {
                    this.tableData = res.data.students_information;
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
      editstudent(){
        this.$refs.edit_form.validate(valid =>{
          if (!valid)return;
          else
            this.$axios.post("/api/teachers/students/modify",this.edit_form).then((res) =>{
              console.log(res.data);
              if(res.data.code ==200){
                this.$message({
                  message:res.data.msg,
                  type:"success"
                })
                this.dia_edit=false;
                this.getdata();
              }
              else{
                this.$message({
                    message:res.data.msg,
                    type:"error"
                })
              }
          })
        })
      },
      addstudent() {
          this.$refs.add_form.validate(valid => {
              if (!valid)
                  return;
              else //验证通过再发送请求
                  this.$axios.post("/api/teachers/students/add", this.add_form).then((res) => {
                      console.log(res.data);
                      if (res.data.code == 200) {
                          this.$message({
                              message: res.data.msg,
                              type: "success"
                          })
                          this.dia_add = false;
                          this.getdata();
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
            //
          this.$axios.delete("/api/teachers/students/delete", { data:{sid: this.want_delete }}).then((res) => {
              if (res.data.code == 200) {
                  this.$message({
                      message: res.data.msg,
                      type: "success"
                  })
                  this.getdata()
                  this.dia_dlt = false;
              }
              else{
                this.$message({
                    message:res.data.msg,
                    type:"error"
                })
              }
          })
      }
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
  height: auto;
  margin: auto;
  margin-top: 30px;
}

.back-button{
  background-color: transparent;
border: none;
color: black;
}


</style>