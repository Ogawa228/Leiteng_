<template>
  <div>
    <b-container class="bv-example-row">
      <b-row>
        <b-col>
          <van-cell title="游戏名" :value="user.username"/>
        </b-col>
        <b-col>
          <b-input size="sm" v-model="username"
                   style="width: 200px; display: inline-block; margin-right: 20px;"></b-input>
          <b-button size="sm" style="display: inline-block" @click="onChangeUsername">修改名称</b-button>
        </b-col>
        <b-col>
          <van-cell v-if="user.ban_until_time && new Date(user.ban_until_time.replace(/-/g, '/')) > Date.now()"
                    title="被封禁至：" style="color: red">
            {{ user.ban_until_time }}
          </van-cell>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <van-cell title="GUID" :value="user.unique_id?user.unique_id:'-'"/>

        </b-col>
        <b-col>
          <b-input size="sm" v-model="guid" type="number"
                   style="width: 200px; display: inline-block; margin-right: 20px;"></b-input>
          <b-button size="sm" style="display: inline-block" @click="onSetGuid">设置GUID</b-button>
        </b-col>
        <b-col>

        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <van-cell title="排位分" :value="user.rank"/>

        </b-col>
        <b-col>

        </b-col>
        <b-col>
          <van-cell title="排位分(3v3)" :value="user.rank_33"/>
        </b-col>
      </b-row>
      <van-divider/>
      <PlayerInfoCard :id="user.id"/>
      <van-divider/>
      <b-row>
        <b-col>
          <van-cell title="兵种偏好">
            <b-form-checkbox-group
                id="checkbox-group-2"
                v-model="preferences"
                :options="options"
                name="flavour-2"
                @change="changePreferences"
            >
            </b-form-checkbox-group>
          </van-cell>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <van-cell title="总场数" :value="user.match"/>
        </b-col>
        <b-col>
          <van-cell title="胜场" :value="user.win+'（'+rounding(user.win*100/user.match)+'%）'"/>
        </b-col>
        <b-col>
          <van-cell title="败场" :value="user.lose+'（'+rounding(user.lose*100/user.match)+'%）'"/>
        </b-col>
        <b-col>
          <van-cell title="平局" :value="user.even+'（'+rounding(user.even*100/user.match)+'%）'"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <van-cell title="总击杀" :value="user.kill"/>
        </b-col>
        <b-col>
          <van-cell title="总死亡" :value="user.death"/>
        </b-col>
        <b-col>
          <van-cell title="KD比" :value="rounding(user.kill/user.death)"/>
        </b-col>
        <b-col>
          <van-cell title="场均伤害" :value="rounding(user.damage/user.match)"/>
        </b-col>
      </b-row>
      <van-divider/>
      <b-row>
        <b-col>
          <b-card class="cont" header="修改密码">
            <b-form>
              <b-form-group label="密码" label-for="input-2" class="ig"
                            description="密码长度不小于6位">
                <b-form-input

                    v-model="password"
                    type="password"
                    placeholder="请输入密码"
                    required
                ></b-form-input>
              </b-form-group>

              <b-form-group label="确认密码" label-for="input-2" class="ig">
                <b-form-input

                    type="password"
                    v-model="confirm_password"
                    placeholder="请再次输入密码"
                    required
                ></b-form-input>
              </b-form-group>
              <b-button class="btn" variant="primary" @click="onChangePassword">修改密码</b-button>
            </b-form>
          </b-card>
        </b-col>
        <b-col>

        </b-col>
        <b-col>

        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import PlayerInfoCard from "@/components/PlayerInfoCard.vue";

export default {
  name: "PersonalStatistics",
  components: {PlayerInfoCard},
  data() {
    return {
      preferences: [],
      options: [
        {text: '射手', value: 0x1, disabled: false},
        {text: '步兵', value: 0x2, disabled: false},
        {text: '骑兵', value: 0x4, disabled: false},
      ],
      username: "",
      password: "",
      confirm_password: "",
      guid: "",
    }
  },
  computed: {
    user: function () {
      return this.$store.getters.getUser
    },
  },
  watch: {
    user: {
      handler(val, oldVal) {
        this.preferences = []
        let p = val.preference
        let count = 0
        while (p != 0) {
          if ((p & 0x1) != 0)
            this.preferences.push(1 << count)
          count++
          p >>>= 1
          if (count > 64)
            break
        }
      },
      immediate: true,
    }
  },
  methods: {
    rounding(value) {
      let realVal = "";
      if (!isNaN(value) && value !== "" && isFinite(value)) {
        realVal = parseFloat(value).toFixed(2);
      } else {
        realVal = "--";
      }
      return realVal;
    },
    onSetGuid() {
      if (this.guid) {
        this.$confirm('GUID设置后不能被更改，确认修改GUID?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$emit("setGuid", this.guid)
        }).catch(() => {
        })
      }
    },
    changePreferences(val) {
      let p = 0
      for (let i = 0; i < val.length; i++)
        p |= val[i]
      this.$emit("setPreference", p)
    },
    onChangeUsername() {
      if (this.username) {
        this.$confirm('确认修改名称?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$emit("setUsername", this.username)
        }).catch(() => {
        })
      }
    },
    onChangePassword() {
      let errorMsg = ""
      if (this.password == "" || this.confirm_password == "") {
        return
      }
      if (!errorMsg && this.password.length < 6) {
        errorMsg = "密码长度不能少于6位"
      }
      if (!errorMsg && this.password.length > 32) {
        errorMsg = "密码长度不能超过32位"
      }
      if (!errorMsg && this.confirm_password != this.password) {
        errorMsg = "两次输入的密码不一致"
      }
      if (errorMsg) {
        this.$bvToast.toast(errorMsg, {
          title: "错误",
          variant: "danger",
          autoHideDelay: 2000,
          toaster: "b-toaster-top-center",
        })
        return
      }
      this.$confirm('确认修改密码?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit("setPassword", this.password)
      }).catch(() => {
      })
    },
  },
}
</script>

<style scoped>

</style>