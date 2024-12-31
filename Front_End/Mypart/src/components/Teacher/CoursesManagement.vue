<template>
  <div>
      <div class="header">
          课程管理
      </div>
      <div class="search-container">
        <input class="search" type="text" v-model="searchText.input_data" placeholder="请输入课程号或者课程名称查询"> 
        <button type="primary" class="search_button" @click="change_data()">搜索</button>
      </div>
      <div class="body">
        <el-button type="primary" @click="goBack()" class="back-button" icon="el-icon-arrow-left" v-if="is_back">返回</el-button>
          <el-table :data="paginatedTableData" style="width: 200%" class="table">
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
              <el-table-column prop="operate" label="操作" width="280" align="center">
                  <template slot-scope="scope">
                      <el-button size="small" type="success" @click="showdia_edit(scope.row)">修改课程信息
                      </el-button>
                      <el-button size="small" type="danger" @click="showdia_dlt(scope.row)">删除课程
                      </el-button>
                  </template>
              </el-table-column>
              <el-table-column width="120" align="center">
                  <template slot="header">
                      <el-button icon="el-icon-plus" size="small" type="success" @click="showdia_add()">添加课程
                      </el-button>
                  </template>
              </el-table-column>
          </el-table>


          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[5,10,20]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next"
            :total="tableData.length">
            </el-pagination>


          <el-dialog title="修改课程信息" :visible.sync="dia_edit" width="30%">
              <el-form ref="edit_form" :model="edit_form" label-width="140px" :rules="edit_form_rules">
                  <el-form-item label="课程号：" prop="cid">
                    <span>{{ edit_form.cid }}</span>
                  </el-form-item>
                  <el-form-item label="课程名称：" prop="cname">
                    <span>{{ edit_form.cname }}</span>
                  </el-form-item>
                  <el-form-item label="开课学院：" prop="college">
                    <span>{{ edit_form.college }}</span>
                  </el-form-item>
                  <el-form-item label="任课教师工号：" prop="tid">
                      <el-input v-model="edit_form.tid"></el-input>
                  </el-form-item>

                  <el-form-item label="开课周数：">
                            <el-select v-model="edit_form.week" placeholder="请选择周数范围">
                                <el-option label="1-17周" value="1-17"></el-option>
                                <el-option label="1-9周" value="1-9"></el-option>
                                <el-option label="10-17周" value="10-17"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>

                  <el-form-item label="开课时间：">
                            <el-select v-model="edit_form.day" placeholder="请选择具体工作日">
                                <el-option label="星期一" value="星期一"></el-option>
                                <el-option label="星期二" value="星期二"></el-option>
                                <el-option label="星期三" value="星期三"></el-option>
                                <el-option label="星期四" value="星期四"></el-option>
                                <el-option label="星期五" value="星期五"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>


                  <el-form-item label="开课节数：">
                            <el-select v-model="edit_form.time" placeholder="请选择具体节数">
                                <el-option label="1-2节" value="1-2"></el-option>
                                <el-option label="3-4节" value="3-4"></el-option>
                                <el-option label="5-6节" value="5-6"></el-option>
                                <el-option label="7-8节" value="7-8"></el-option>
                                <el-option label="9-11节" value="9-11"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>

              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="editcourses()">
                      修改
                  </el-button>
              </div>
          </el-dialog>


          <el-dialog title="添加课程" :visible.sync="dia_add" width="30%">
              <el-form ref="add_form" :model="add_form" label-width="140px" :rules="add_form_rules">
                  <el-form-item label="课程号：" prop="cid" >
                      <el-input style="width: 300px;" v-model="add_form.cid"></el-input>
                  </el-form-item>
                  <el-form-item  label="课程名称：" prop="cname">
                      <el-input style="width: 300px;" v-model="add_form.cname"></el-input>
                  </el-form-item>
                  <el-form-item label="任课教师工号：" prop="tid">
                      <el-input style="width: 300px;" v-model="add_form.tid"></el-input>
                  </el-form-item>
                  <el-form-item label="开课周数：">
                            <el-select v-model="add_form.week" placeholder="请选择周数范围">
                                <el-option label="1-17周" value="1-17"></el-option>
                                <el-option label="1-9周" value="1-9"></el-option>
                                <el-option label="10-17周" value="10-17"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>

                  <el-form-item label="开课时间：">
                            <el-select v-model="add_form.day" placeholder="请选择具体工作日">
                                <el-option label="星期一" value="星期一"></el-option>
                                <el-option label="星期二" value="星期二"></el-option>
                                <el-option label="星期三" value="星期三"></el-option>
                                <el-option label="星期四" value="星期四"></el-option>
                                <el-option label="星期五" value="星期五"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>


                  <el-form-item label="开课节数：">
                            <el-select v-model="add_form.time" placeholder="请选择具体节数">
                                <el-option label="1-2节" value="1-2"></el-option>
                                <el-option label="3-4节" value="3-4"></el-option>
                                <el-option label="5-6节" value="5-6"></el-option>
                                <el-option label="7-8节" value="7-8"></el-option>
                                <el-option label="9-11节" value="9-11"></el-option>
                                <el-option label="待定" value=""></el-option>
                            </el-select>
                  </el-form-item>
              </el-form>
              <div style="text-align: center;">
                  <el-button type="primary" @click="addcourses()">
                      添加
                  </el-button>
              </div>
          </el-dialog>


          <el-dialog title="删除课程" :visible.sync="dia_dlt" width="30%">
              <div>
                  确定要删除此课程吗？
              </div>
              <div style="text-align: center;">
                  <el-button type="primary" @click="deletecourses()">
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
      this.getdata();
  },
  data() {
      return {
          tableData: [],
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
              cid: '',
              cname: '',
              week: '',
              day:'',
              time:'',
              tid:'',
          },
          edit_form:{
              cid: '',
              cname: '',
              week: '',
              day:'',
              time:'',
              college:'',
              tid:'',
          },
          want_delete: '',
          add_form_rules: {
              cid: [{ required: true, message: 'cid必须是5位数字', trigger: 'blur' ,pattern: /^\d{5}$/}],
              cname: [{ required: true, message: '必填项', trigger: 'blur' }],
              week:[{ required: true, message: '必填项', trigger: 'blur' }],
              day:[{ required: true, message: '必填项', trigger: 'blur' }],
              time:[{ required: true, message: '必填项', trigger: 'blur' }],
              tid:[{ required: true, message: '必填项', trigger: 'blur' }]

          },
          edit_form_rules:{
              cid: [{ required: true, message: '必填项', trigger: 'blur' }],
              cname: [{ required: true, message: '必填项', trigger: 'blur' }],
              week:[{ required: true, message: '必填项', trigger: 'blur' }],
              day:[{ required: true, message: '必填项', trigger: 'blur' }],
              time:[{ required: true, message: '必填项', trigger: 'blur' }],
              tid:[{ required: true, message: '必填项', trigger: 'blur' }]
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
          this.$axios.get("/api/teachers/courses").then((res) => {
              console.log(res.data);
              if (res.data.code==200) {
                  this.tableData = res.data.courses_data;
              }
          })
      },
      showdia_add() {
          this.dia_add = true;
      },
      showdia_edit(row){
        this.edit_form.cid=row.cid;
        this.edit_form.cname=row.cname;
        this.edit_form.college=row.college;
        this.edit_form.tid=row.tid;
        if(this.edit_form.week.week){
          this.edit_form.week=row.week.slice(0, -1);
        }
        if(this.edit_form.day){
          this.edit_form.day=row.day;
        }
        if(this.edit_form.time){
          this.edit_form.time=row.period.slice(0, -1);
        }
        this.dia_edit=true;
      },
      change_data(){
        if (this.searchText.input_data!=""){
            this.$axios.post("/api/teachers/courses/select",this.searchText).then((res) => {
                // console.log(res.data);
                if (res.data.code == 200) {
                    this.tableData = res.data.courses_data;
                    this.is_back=true;
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
      goBack(){
            this.is_back=false;
            this.getdata();
        },
      editcourses(){
        this.$refs.edit_form.validate(valid =>{
          if (!valid)return;
          else
            //console.log(this.edit_form)
            this.$axios.post("/api/teachers/courses/modify",this.edit_form).then((res) =>{
              console.log(this.edit_form);
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
      addcourses() {
          this.$refs.add_form.validate(valid => {
              if (!valid)
                  return;
              else //验证通过再发送请求
                  this.$axios.post("/api/teachers/courses/add", this.add_form).then((res) => {
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
          this.want_delete = row.cid;
          this.dia_dlt = true;
      },
      deletecourses() {
          this.$axios.delete("/api/teachers/courses/delete", { data:{cid: this.want_delete  }}).then((res) => {
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
  margin: auto;
  margin-top: 30px;
  margin-left: 100px;
}

.back-button{
  background-color: transparent;
border: none;
color: black;
}

</style>