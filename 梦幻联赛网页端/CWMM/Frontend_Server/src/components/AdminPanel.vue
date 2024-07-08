<template>
  <div>
    <div style="display: inline-block;">
      <el-descriptions title="玩家管理" style="margin-left: 20px; margin-right: 20px;">
        <el-descriptions-item label="用户名">{{ user_query_data.username }}
          <el-tag type="success" v-if="user_query_data.admin_level>0" style="margin-left: 20px;">管理员</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="GUID">{{ user_query_data.unique_id }}
          <el-button v-if="user_query_data?.unique_id" type="danger" size="small" style="margin-left: 20px;"
                     @click="clearGuid">重置GUID
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="封禁状态">
          <div>
            <div
                v-if="user_query_data?.ban_until_time&&new Date(user_query_data.ban_until_time.replace(/-/g, '/')) > Date.now()">
              <el-tag type="danger">被封禁至：{{ user_query_data.ban_until_time }}</el-tag>
              <el-button type="warning" size="small" style="margin-left: 20px;" @click="unBanUser">取消封禁</el-button>
            </div>
            <div v-else-if="user_query_data?.id">
              <el-tag type="success">未被封禁</el-tag>
              <el-button type="danger" size="small" @click="showBanDialog"
                         style="margin-left: 20px;">封禁
              </el-button>
            </div>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="曾用名">{{ history_names }}</el-descriptions-item>
        <el-descriptions-item label="最后登录ip">{{ user_query_data.last_login_ip }}</el-descriptions-item>
        <el-descriptions-item label="操作">
          <div v-if="user_query_data?.id">
            <div v-if="user.admin_level>=10">
              <el-input v-model="new_username" placeholder="请输入新名称" style="width: 200px;"></el-input>
              <el-button type="danger" size="small" @click="setUsername"
                         style="margin-left: 20px;">设置名称
              </el-button>
            </div>
            <el-input v-model="new_password" type="password" placeholder="请输入密码" style="width: 200px;"></el-input>
            <el-button type="danger" size="small" @click="setPassword"
                       style="margin-left: 20px;">设置密码
            </el-button>
            <div v-if="user.admin_level>=10">
              <el-button type="danger" size="small" @click="resetStatistics"
                         style="margin-left: 20px;">重置数据
              </el-button>
            </div>
            <el-button type="success" size="small" @click="setAdmin"
                       v-if="user_query_data.admin_level==0&&user.admin_level>=10"
                       style="margin-left: 20px;">设为管理
            </el-button>
            <el-button type="danger" size="small" @click="unsetAdmin"
                       v-else-if="user_query_data.admin_level<10&&user.admin_level>=10"
                       style="margin-left: 20px;">取消管理
            </el-button>
          </div>
        </el-descriptions-item>
      </el-descriptions>
      <el-form :model="user_query_param" ref="user_query_param" label-width="100px"
               style="float:left; width: 30%; display: inline-block">
        <el-form-item label="查询条件" prop="type">
          <el-radio-group v-model="user_query_param.type" placeholder="请选择"
                          style="float:left; width: 100%;">
            <el-radio-button label="用户名"/>
            <el-radio-button label="GUID"/>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="查询内容" prop="value">
          <el-input v-model="user_query_param.value" placeholder="请输入要搜索的用户名或GUID"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="onQueryUser" :loading="is_querying_user">查询用户</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-divider/>
    <div>
      <el-descriptions title="服务器列表" style="margin-left: 20px;">
      </el-descriptions>
      <el-table :data="active_data.servers">
        <el-table-column label="名称" align="center">
          <template #default="scope">
            <span>{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center">
          <template #default="scope">
            <span>{{ scope.row.state }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <el-button v-if="scope.row.state=='in_match'" type="danger" round size="medium"
                       @click="cancelMatch(scope.row.name)">取消比赛
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog title="封禁玩家" :visible.sync="ban_dialog_visible">
      <el-form :model="ban_user_param">
        封禁玩家{{ user_query_data.username }}一定时长
        <el-divider/>
        <el-form-item label="封禁时长" label-width="120px" style="width: 50%">
          <el-select v-model="ban_user_param.minutes" placeholder="请选择封禁时长" style="margin-left: 20px">
            <el-option label="30分钟" :value="30"/>
            <el-option label="一天" :value="60*24"/>
            <el-option label="一周" :value="60*24*7"/>
            <el-option label="一个月" :value="60*24*30"/>
            <el-option label="永久封禁" :value="60*24*360*100"/>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="ban_dialog_visible = false">取 消</el-button>
        <el-button type="primary" @click="onBanUser" :loading="is_banning_user">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "AdminPanel",
  data() {
    return {
      is_querying_user: false,
      user_query_data: {},
      user_query_param: {type: "用户名", value: ""},

      is_banning_user: false,
      ban_user_param: {minutes: ""},
      ban_dialog_visible: false,

      new_password: "",
      new_username: "",
    }
  },
  computed: {
    active_data: function () {
      return this.$store.getters.getActiveData
    },
    user: function () {
      return this.$store.getters.getUser
    },
    history_names: function () {
      let text = ""
      if (this.user_query_data?.history_names) {
        for (let i = 0; i < this.user_query_data.history_names.length; i++) {
          text += this.user_query_data.history_names[i] + (i == this.user_query_data.history_names.length - 1 ? "" : "，")
        }
      }
      return text
    },
  },
  methods: {
    setAdmin() {
      this.$confirm('确认提升' + this.user_query_data.username + '为管理员?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/set-admin", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    unsetAdmin() {
      this.$confirm('确认取消' + this.user_query_data.username + '的管理员身份?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/unset-admin", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    setPassword() {
      if (!this.new_password)
        return
      if (this.new_password.length < 6) {
        this.$bvToast.toast("密码不能小于6位", {
          title: "错误",
          variant: "danger",
          autoHideDelay: 2000,
          toaster: "b-toaster-top-center",
        })
        return
      }
      this.$confirm('确认重置' + this.user_query_data.username + '的密码?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/set-password", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
          new_password: this.new_password,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    resetStatistics() {
      this.$confirm('确认重置' + this.user_query_data.username + '的数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/reset-statistics", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    setUsername() {
      if (!this.new_username)
        return
      this.$confirm('确认设置' + this.user_query_data.username + '的名称?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/admin-set-username", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
          new_username: this.new_username,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    unBanUser() {
      this.$confirm('确认取消封禁' + this.user_query_data.username + '?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/unban-user", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    clearGuid() {
      this.$confirm('确认重置' + this.user_query_data.username + '的GUID?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post("/clear-guid", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          target_user: this.user_query_data.id,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("操作成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        })
      }).catch(() => {
      })
    },
    onBanUser() {
      if (!this.ban_user_param?.minutes)
        return
      this.is_banning_user = true
      this.$axios.post("/ban-user", {
        id: this.user.id,
        username: this.user.username,
        password: this.user.password,
        target_user: this.user_query_data.id,
        minutes: this.ban_user_param.minutes,
      }).then(res => {
        if (res.data?.success) {
          this.user_query_data = res.data.data.user
          this.ban_dialog_visible = false
          this.$bvToast.toast("操作成功", {
            title: "成功",
            variant: "success",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        } else {
          this.$bvToast.toast(res.data.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        }
      }).catch(err => {
        this.$bvToast.toast(err.message, {
          title: "错误",
          variant: "danger",
          autoHideDelay: 2000,
          toaster: "b-toaster-top-center",
        })
      }).finally(() => {
        this.is_banning_user = false
      })
    },
    onQueryUser() {
      if (this.user_query_param.value) {
        this.is_querying_user = true
        this.$axios.post("/query-user-admin", {
          id: this.user.id,
          username: this.user.username,
          password: this.user.password,
          query_type: this.user_query_param.type == "用户名" ? 1 : 0,
          query_value: this.user_query_param.value,
        }).then(res => {
          if (res.data?.success) {
            this.user_query_data = res.data.data.user
            this.$bvToast.toast("查询成功", {
              title: "成功",
              variant: "success",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          } else {
            this.$bvToast.toast(res.data.message, {
              title: "错误",
              variant: "danger",
              autoHideDelay: 2000,
              toaster: "b-toaster-top-center",
            })
          }
        }).catch(err => {
          this.$bvToast.toast(err.message, {
            title: "错误",
            variant: "danger",
            autoHideDelay: 2000,
            toaster: "b-toaster-top-center",
          })
        }).finally(() => {
          this.is_querying_user = false
        })
      }
    },
    showBanDialog() {
      this.ban_dialog_visible = true
    },
    cancelMatch(name) {
      this.$confirm('确认取消进行中的比赛?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit("cancelMatch", name)
      }).catch(() => {
      })
    },
  },
}
</script>

<style scoped>

</style>