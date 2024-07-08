<template>
    <div class="root">
        <b-card class="cont" header="China Warband Matchmaking">
            <b-form>
                <b-form-group
                        id="input-group-1"
                        class="ig"
                        label="账号"
                        label-for="input-1"
                        :description="isLogin?'':'用户名必须与游戏内名称一致'">
                    <b-form-input
                            id="input-1"
                            v-model="loginData.username"
                            placeholder="请输入用户名"
                            required></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="密码" label-for="input-2" class="ig"
                              :description="isLogin?'':'密码长度不小于6位'">
                    <b-form-input
                            id="input-2"
                            v-model="loginData.password"
                            type="password"
                            placeholder="请输入密码"
                            required
                    ></b-form-input>
                </b-form-group>

                <b-form-group v-if="!isLogin" id="input-group-2" label="确认密码" label-for="input-2" class="ig"
                >
                    <b-form-input
                            id="input-2"
                            type="password"
                            v-model="loginData.confirm_password"
                            placeholder="请再次输入密码"
                            required
                    ></b-form-input>
                </b-form-group>

                <b-button class="btn" :variant="isLogin?'primary':'success'" @click="onLogin">{{
                    isLogin ? "登录" : "注册"
                    }}
                </b-button>
                <b-button class="btn" variant="outline-primary" @click="isLogin=!isLogin">我要{{
                    isLogin ? "注册" : "登录"
                    }}
                </b-button>
            </b-form>

        </b-card>
    </div>
</template>

<script>
export default {
    name: "LoginView",
    data() {
        return {
            "isLogin": true,
            "loginData": {
                username: "",
                password: "",
                confirm_password: "",
            },
        }
    },
    methods: {
        onLogin() {
            let errorMsg = ""
            if (this.loginData.username == "" || this.loginData.password == "" ||
                (!this.isLogin && this.loginData.confirm_password == "")) {
                errorMsg = '请完成输入'
            }
            if (!errorMsg && !this.loginData.username.match("^[a-zA-Z0-9_-]+$")) {
                errorMsg = '用户名只能包含数字、字母、短横杠和下划线'
            }
            if (!errorMsg && this.loginData.username.length > 32) {
                errorMsg = "用户名长度不能超过32位"
            }
            if (!errorMsg && this.loginData.username == "New_Player") {
                errorMsg = "禁止使用昵称New_Player"
            }
            if (!errorMsg && this.loginData.password.length < 6) {
                errorMsg = "密码长度不能少于6位"
            }
            if (!errorMsg && this.loginData.password.length > 32) {
                errorMsg = "密码长度不能超过32位"
            }
            if (!errorMsg && !this.isLogin && this.loginData.confirm_password != this.loginData.password) {
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

            if (this.isLogin) {
                this.$axios.post("/login", {
                    "username": this.loginData.username,
                    "password": this.loginData.password,
                }).then(res => {
                    if (res.data?.success) {
                        this.$store.commit("setUser", res.data.data.user)
                        this.$router.replace("/")
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
            } else {
                this.$axios.post("/register", {
                    "username": this.loginData.username,
                    "password": this.loginData.password,
                    "confirm_password": this.loginData.confirm_password,
                }).then(res => {
                    if (res.data?.success) {
                        this.$store.commit("setUser", res.data.data.user)
                        this.$router.replace("/")
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
            }
        },
    }
}
</script>

<style scoped>
.cont {
    margin-top: 100px;
    width: 500px;
    align-content: center;
    display: inline-block;
}

.ig {
    margin-bottom: 15px;
}

.btn {
    margin: 5px;
}
</style>