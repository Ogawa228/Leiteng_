<template>
    <div>
        <audio ref="choose.ogg" src="../assets/choose.ogg" preload="auto"/>
        <audio ref="ready.mp3" src="../assets/ready.mp3" preload="auto"/>
        <audio ref="messageSound" src="../assets/message.ogg" preload="auto"/>
        <el-header style="height: 10vh;">
            <div style="margin-top: 20px;">
                <h1 style="color: #eace2a; float: left; display: inline-block;">{{ user.username }}</h1>
                <el-link style="margin-top: 20px; float: left; margin-left: 20px; text-align: center" type="primary"
                         href="https://kook.top/IPn9WZ"
                         target="_blank">前往语音频道
                </el-link>
                <el-button style="float: right; display: inline-block;" type="danger" size="medium"
                           icon="el-icon-switch-button" @click="confirmQuitLogin()" round>
                    退出登录
                </el-button>
            </div>
        </el-header>
        <div>
            <b-alert v-model="showDisconnectAlert" variant="danger">
                您已离线，正在尝试重连……
            </b-alert>
        </div>
        <div class="home">
            <el-row>
                <el-col :span="20">
                    <b-tabs content-class="mt-3" @input="changeTab">
                        <b-tab title="首页" active>
                            <MainPage/>
                        </b-tab>
                        <b-tab title="个人数据">
                            <PersonalStatistics @setPreference="setPreference" @setPassword="setPassword"
                                                @setGuid="setGuid"
                                                @setUsername="setUsername"></PersonalStatistics>
                        </b-tab>
                        <b-tab title="开始排位">
                            <MatchPanel @startPool="startPool"
                                        @cancelPool="cancelPool"
                                        @chooseTeammate="chooseTeammate"
                                        @acceptMatch="acceptMatch"></MatchPanel>
                        </b-tab>
                        <b-tab title="对局记录">
                            <MatchHistory :doUpdate="doUpdateMatchHistory"/>
                        </b-tab>
                        <b-tab title="排行榜">
                            <LeaderboardView :doUpdate="doUpdateLeaderboard"/>
                        </b-tab>
                        <b-tab title="管理面板" v-if="user.admin_level > 0">
                            <AdminPanel @cancelMatch="cancelMatch"/>
                        </b-tab>
                        <b-tab title="关于">
                            <AboutPage/>
                        </b-tab>
                    </b-tabs>
                </el-col>
                <el-col :span="4">
                    <ChatView @sendMessage="sendMessage"/>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src

// @ is an alias to /src
import PersonalStatistics from "@/components/PersonalStatistics.vue";
import MatchPanel from "@/components/MatchPanel.vue";
import {BACKEND_HOST, BACKEND_PORT} from "@/config";
import ChatView from "@/components/ChatView.vue";
import LeaderboardView from "@/components/LeaderboardView.vue";
import MatchHistory from "@/components/MatchHistory.vue";
import MainPage from "@/components/MainPage.vue";
import AboutPage from "@/components/AboutPage.vue";
import AdminPanel from "@/components/AdminPanel.vue";

export default {
    name: 'HomeView',
    components: {
        AdminPanel,
        AboutPage, MainPage, MatchHistory, LeaderboardView, ChatView, MatchPanel, PersonalStatistics
    },
    data() {
        return {
            onlineUntilTime: Date.now() + 3,
            socket: null,
            showDisconnectAlert: false,
            heartBeatInterval: 2000,
            heartBeatDuration: 5000,
            currentTab: 0,
            doUpdateLeaderboard: false,
            doUpdateMatchHistory: false,
        }
    },
    computed: {
        user: function () {
            return this.$store.getters.getUser
        },
    },
    mounted() {
        if (this.user?.id) {
            this.refreshUserData()
            this.getTotalData()
            this.initWebSocket()

            window.addEventListener("beforeunload", () => {
                this.setManualClose()
            })

            setInterval(() => {
                if (Date.now() > this.onlineUntilTime + this.heartBeatDuration)
                    this.showDisconnectAlert = true
                else
                    this.showDisconnectAlert = false

                if (this.socket.readyState == WebSocket.OPEN)
                    this.socket.send(JSON.stringify({op: "heart_beat"}))
                else
                    this.initWebSocket()
            }, this.heartBeatInterval)
        } else {
            this.$router.replace("/login")
        }
    },
    methods: {
        initWebSocket() {
            this.socket = new WebSocket("ws://" + BACKEND_HOST + ":" + BACKEND_PORT + "/connect")
            this.socket.onmessage = this.onSocketMessage;
            this.socket.onopen = this.onSocketOpen;
            this.socket.onerror = this.onSocketError;
            this.socket.onclose = this.onSocketClose;
        },
        onSocketOpen() {
            let msg = {
                op: "connect",
                args: {
                    id: this.user.id,
                    username: this.user.username,
                    password: this.user.password
                }
            }
            if (this.socket.readyState == WebSocket.OPEN)
                this.socket.send(JSON.stringify(msg))
        },
        onSocketMessage(msg) {
            let data = JSON.parse(msg.data)
            //console.log(data)
            if (data.op == "relogin") {
                this.quitLogin()
            } else if (data.op == "heart_beat_received") {
                this.$store.commit("setActiveData", data.args.active_data)
            } else if (data.op == "send_message") {
                this.$store.commit("addMessage", data.args.message)
                if (data.args.message.user != "系统") {
                    this.$refs.messageSound.volume = 0.1
                    //this.$refs.messageSound.currentTime = 0
                    this.$refs.messageSound.play()
                }
            } else if (data.op == "alert") {
                this.$bvToast.toast(data.args.message, {
                    title: "错误",
                    variant: "danger",
                    autoHideDelay: 2000,
                    toaster: "b-toaster-top-center",
                })
            } else if (data.op == "update_user") {
                this.$store.commit("setOtherUsers", data.args.users)
            } else if (data.op == "play_sound") {
                this.$refs[data.args.name].play()
            }
            this.onlineUntilTime = Date.now() + this.heartBeatDuration
        },
        onSocketError() {

        },
        onSocketClose() {

        },
        cancelPool() {
            this.socket.send(JSON.stringify({
                op: "cancel_pool",
            }))
        },
        sendMessage(message) {
            this.socket.send(JSON.stringify({
                op: "send_message",
                args: {
                    message: message,
                },
            }))
        },
        setManualClose() {
            if (this.socket.readyState == WebSocket.OPEN)
                this.socket.send(JSON.stringify({op: "manual_close"}))
        },
        startPool(mode_id) {
            this.socket.send(JSON.stringify({
                op: "start_pool",
                args: {
                    mode_id: mode_id,
                },
            }))
        },
        quitLogin() {
            this.setManualClose()
            this.$store.commit("setUser", {})
            this.socket.close()
            location.reload()
        },
        chooseTeammate(id) {
            this.socket.send(JSON.stringify({
                op: "choose_player",
                args: {
                    user: id,
                },
            }))
        },
        setPreference(p) {
            this.$axios.post("/set-preference", {
                id: this.user.id,
                username: this.user.username,
                password: this.user.password,
                preference: p,
            }).then(res => {
                if (res.data?.success) {
                    this.$store.commit("setUser", res.data.data.user)
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
        },
        setGuid(guid) {
            this.$axios.post("/set-guid", {
                id: this.user.id,
                username: this.user.username,
                password: this.user.password,
                guid: guid,
            }).then(res => {
                if (res.data?.success) {
                    this.$store.commit("setUser", res.data.data.user)
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
        },
        setUsername(name) {
            this.$axios.post("/change-username", {
                id: this.user.id,
                username: this.user.username,
                password: this.user.password,
                new_username: name,
            }).then(res => {
                if (res.data?.success) {
                    this.$store.commit("setUser", res.data.data.user)
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
        },
        changeTab(t) {
            if (t == 4 && this.currentTab != t) {
                this.doUpdateLeaderboard = true
            } else
                this.doUpdateLeaderboard = false

            if (t == 3 && this.currentTab != t) {
                this.doUpdateMatchHistory = true
            } else
                this.doUpdateMatchHistory = false
            this.currentTab = t
        },
        setPassword(pass) {
            this.$axios.post("/change-password", {
                id: this.user.id,
                username: this.user.username,
                password: this.user.password,
                new_password: pass,
            }).then(res => {
                if (res.data?.success) {
                    this.$store.commit("setUser", res.data.data.user)
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
        },
        getTotalData() {
            this.$axios.get("/get-total-data").then(res => {
                if (res.data?.success) {
                    this.$store.commit("setMaps", res.data.data.maps)
                    this.$store.commit("setModes", res.data.data.modes)
                    this.$store.commit("setRanks", res.data.data.ranks)
                    this.$store.commit("setConfig", res.data.data.config)
                }
            }).catch(err => {
                this.$bvToast.toast(err.message, {
                    title: "错误",
                    variant: "danger",
                    autoHideDelay: 2000,
                    toaster: "b-toaster-top-center",
                })
            })
        },
        cancelMatch(name) {
            this.socket.send(JSON.stringify({
                op: "cancel_match",
                args: {
                    server: name,
                },
            }))
        },
        refreshUserData() {
            this.$axios.get("/refresh-user-data", {
                params: {
                    id: this.user.id,
                    username: this.user.username,
                    password: this.user.password,
                }
            }).then(res => {
                if (res.data?.success) {
                    this.$store.commit("setUser", res.data.data.user)
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
        },
        confirmQuitLogin() {
            this.$confirm('确认退出登录?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.quitLogin()
            }).catch(() => {
            })
        },
        acceptMatch() {
            this.socket.send(JSON.stringify({
                op: "accept_match",
            }))
        },
    },
}
</script>
