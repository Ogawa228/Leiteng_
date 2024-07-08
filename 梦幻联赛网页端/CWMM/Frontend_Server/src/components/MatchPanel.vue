<template>
    <div>
        <b-row>
            <b-col>
                <van-cell title="在线人数" :value="active_data.online_user_count"/>
            </b-col>
            <b-col>
                <van-cell title="可用服务器" :value="active_data.idle_server_count"/>
            </b-col>
            <b-col>

            </b-col>
            <b-col>

            </b-col>
        </b-row>
        <el-divider/>
        <div>
            <div v-if="active_data.state=='in_lobby'">
                <el-select v-model="mode" placeholder="请选择模式">
                    <el-option
                            v-for="item in modes"
                            :key="item.id"
                            :label="item.name+'（'+active_data.pool_size[item.id]+'人匹配中）'"
                            :value="item.id">
                    </el-option>
                </el-select>
                <el-button type="success" style="margin-left: 20px;" @click="startPool" size="medium" round>开始匹配
                </el-button>
                <b-row>
                    <b-col>
                        <b-card v-if="chosenModeName!=''" style="display: inline-block; margin-top: 20px; width: 600px;"
                                :header="chosenModeName">
                            <p>{{ chosenModeDescription }}</p>
                            <p>{{ chosenModeMaps }}</p>
                        </b-card>
                    </b-col>
                </b-row>
            </div>
            <div v-else-if="active_data.state=='in_pool'">
                <el-select v-model="active_data.pool_match_id" disabled>
                    <el-option
                            v-for="item in modes"
                            :key="item.id"
                            :label="item.name+'（'+active_data.pool_size[item.id]+'人匹配中）'"
                            :value="item.id">
                    </el-option>
                </el-select>
                <el-button type="success" style="margin-left: 20px;" :loading="true" @click="startPool"
                           size="medium"
                           round>匹配中
                </el-button>
                <b-row>
                    <b-col>
                        <b-card style="display: inline-block; margin-top: 20px; width: 600px;"
                                header="队列中">
                            <p>已等待局数：{{ active_data.waited_matches }}</p>
                            <el-button type="danger" style="margin-left: 20px;" @click="cancelPool" size="medium"
                                       round>取消匹配
                            </el-button>
                        </b-card>
                    </b-col>
                </b-row>
                <el-divider/>
                <el-row>
                    <el-col v-for="item in active_data.pool.users" :key="item" :span="4">
                        <PlayerInfoCard :id="item"/>
                    </el-col>
                </el-row>
            </div>
            <div v-else-if="active_data.state=='in_match'">
                <div style="display: inline-block; width: 1200px;"
                     v-if="match.state!='show_result'&&match.state!='wait_for_ready'">
                    <el-descriptions :title="match.server" style="color: #ba25cb">
                        <el-descriptions-item label="模式">{{ mode_name }}</el-descriptions-item>
                        <el-descriptions-item label="地图">{{ map_name }}</el-descriptions-item>
                        <el-descriptions-item label="兵种限制">{{ troop_limit }}</el-descriptions-item>
                    </el-descriptions>
                </div>
                <el-divider v-if="match.state!='show_result'&&match.state!='wait_for_ready'"/>
                <div v-if="isWaitingForReady&&active_data.match.state=='wait_for_ready'">
                    <el-row>
                        <el-progress style="width: 1000px; display: inline-block" :percentage="readyCounter"
                                     status="warning"></el-progress>
                    </el-row>
                    <el-row style="margin-bottom: 20px;">
                        <el-button v-show="!is_ready" type="success" size="medium" @click="acceptMatch"
                                   round>
                            接受
                        </el-button>
                        <el-button v-show="is_ready" type="success" size="medium" round disabled>已接受
                        </el-button>
                    </el-row>
                    <el-row>
                        <el-col v-for="item in active_data.match.users" :key="item" :span="4">
                            <PlayerInfoCard :id="item"/>
                        </el-col>
                    </el-row>
                </div>
                <div v-else-if="active_data.match.state=='choose_team'">
                    <el-row>
                        <el-col :span="8">
                            <h5>{{ team_1_faction }}</h5>
                            <el-progress style="width: 200px; display: inline-block" :percentage="chooseCounter(1)"
                                         status="warning"></el-progress>
                            <div v-for="(item,index) in active_data.match.team_1" :key="item">
                                <div v-if="index%2 == 0">
                                    <el-row>
                                        <el-col :span="12">
                                            <PlayerInfoCard :id="active_data.match.team_1[index]"/>
                                        </el-col>
                                        <el-col :span="12">
                                            <PlayerInfoCard v-if="index+1<active_data.match.team_1.length"
                                                            :id="active_data.match.team_1[index+1]"/>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <h5 style="margin-bottom: 32px;">可选人员</h5>
                            <div v-for="(item,index) in unchosenUsers" :key="item">
                                <div v-if="index%2 == 0">
                                    <el-row>
                                        <el-col :span="12">
                                            <PlayerInfoCard :id="unchosenUsers[index]" @click="chooseTeam"
                                                            :clickable="i_am_current_leader"/>
                                        </el-col>
                                        <el-col :span="12">
                                            <PlayerInfoCard
                                                    v-if="index+1<unchosenUsers.length"
                                                    :id="unchosenUsers[index+1]" @click="chooseTeam"
                                                    :clickable="i_am_current_leader"/>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <h5>{{ team_2_faction }}</h5>
                            <el-progress style="width: 200px; display: inline-block" :percentage="chooseCounter(2)"
                                         status="warning"></el-progress>
                            <div v-for="(item,index) in active_data.match.team_2" :key="item">
                                <div v-if="index%2 == 0">
                                    <el-row>
                                        <el-col :span="12">
                                            <PlayerInfoCard :id="active_data.match.team_2[index]"/>
                                        </el-col>
                                        <el-col :span="12">
                                            <PlayerInfoCard v-if="index+1<active_data.match.team_2.length"
                                                            :id="active_data.match.team_2[index+1]"/>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </div>
                <div v-else-if="active_data.match.state=='in_game'">
                    <el-row>
                        <el-col :span="12">
                            <h5>{{ team_1_faction }}</h5>
                            <div v-for="(item,index) in active_data.match.team_1" :key="item">
                                <div v-if="index%2 == 0">
                                    <el-row>
                                        <el-col :span="12">
                                            <PlayerInfoCard :id="active_data.match.team_1[index]"/>
                                        </el-col>
                                        <el-col :span="12">
                                            <PlayerInfoCard v-if="index+1<active_data.match.team_1.length"
                                                            :id="active_data.match.team_1[index+1]"/>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="12">
                            <h5>{{ team_2_faction }}</h5>
                            <div v-for="(item,index) in active_data.match.team_2" :key="item">
                                <div v-if="index%2 == 0">
                                    <el-row>
                                        <el-col :span="12">
                                            <PlayerInfoCard :id="active_data.match.team_2[index]"/>
                                        </el-col>
                                        <el-col :span="12">
                                            <PlayerInfoCard v-if="index+1<active_data.match.team_2.length"
                                                            :id="active_data.match.team_2[index+1]"/>
                                        </el-col>
                                    </el-row>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </div>
                <div v-else-if="active_data.match.state=='show_result'">
                    <MatchResultCard :result="active_data.match.result"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PlayerInfoCard from "@/components/PlayerInfoCard.vue";
import MatchResultCard from "@/components/MatchResultCard.vue";

export default {
    name: "MatchPanel",
    components: {MatchResultCard, PlayerInfoCard},
    data() {
        return {
            mode: 2,
            ready_timer: Date.now(),
        }
    },
    watch: {
        /*"active_data.match.state": {
            handler(n, o) {
                if (n == "wait_for_ready") {
                    this.$refs.readySound.play()
                }
            },
        },*/
    },
    mounted() {
        setInterval(() => {
            this.ready_timer = Date.now()
            this.$forceUpdate()
        }, 200)
    },
    computed: {
        team_1_faction: function () {
            return this.$store.getters.getFactionName(this.match.team_1_faction)
        },
        team_2_faction: function () {
            return this.$store.getters.getFactionName(this.match.team_2_faction)
        },
        troop_limit: function () {
            let limit = [0, 0, 0]
            const map = this.$store.getters.getMap(this.match.map)
            if (map) {
                limit = this.$store.getters.getMode(this.match.mode).limit[map.type]
            }
            return limit[0] + "射——" + limit[1] + "步——" + limit[2] + "骑"
        },
        mode_name: function () {
            return this.$store.getters.getMode(this.match.mode)?.name
        },
        map_name: function () {
            return this.$store.getters.getMap(this.match.map)?.name
        },
        i_am_current_leader: function () {
            return (this.active_data.match.team_1[0] == this.$store.getters.getUser.id &&
                this.active_data.match.choosing_team == 1) || (this.active_data.match.team_2[0] == this.$store.getters.getUser.id &&
                this.active_data.match.choosing_team == 2)
        },
        is_ready: function () {
            let myId = this.$store.getters.getUser.id
            for (let i = 0; i < this.$store.getters.getActiveData.match.ready_users.length; i++) {
                if (myId == this.$store.getters.getActiveData.match.ready_users[i])
                    return true
            }
            return false
        },
        isWaitingForReady: function () {
            return this.$store.getters.getActiveData.state == "in_match" // && new Date(this.$store.getters.getActiveData.match.wait_for_ready_until.replace(/-/g, "/")) > this.ready_timer
        },
        chosenModeName: function () {
            if (this.mode) {
                for (let i = 0; i < this.modes.length; i++) {
                    if (this.modes[i].id == this.mode)
                        return this.modes[i].name
                }
            }
            return ""
        },
        unchosenUsers: function () {
            let users = []

            for (let i = 0; i < this.active_data?.match?.users.length; i++) {
                if (!(this.active_data.match.team_1.includes(this.active_data.match.users[i]) || this.active_data.match.team_2.includes(this.active_data.match.users[i]))) {
                    users.push(this.active_data.match.users[i])
                }
            }

            return users
        },
        chosenModeDescription: function () {
            if (this.mode) {
                for (let i = 0; i < this.modes.length; i++) {
                    if (this.modes[i].id == this.mode)
                        return this.modes[i].description
                }
            }
            return ""
        },
        chosenModeMaps: function () {
            if (this.mode) {
                let maps = "地图池："
                for (let i = 0; i < this.maps.length; i++) {
                    for (let j = 0; j < this.maps[i].modes.length; j++) {
                        if (this.maps[i].modes[j] == this.mode) {
                            maps += this.maps[i].name + "、"
                        }
                    }
                }
                return maps.substring(0, maps.length - 1)
            }
            return ""
        },
        readyCounter: function () {
            if (this.$store.getters.getActiveData?.state == "in_match") {
                let progress = (new Date(this.$store.getters.getActiveData.match.wait_for_ready_until.replace(/-/g, "/")) - this.ready_timer) / (10 * this.$store.getters.getConfig.match_wait_ready_seconds)
                return Math.max(Math.min(progress, 100), 0)
            }
            return 50
        },
        maps: function () {
            return this.$store.getters.getMaps
        },
        modes: function () {
            return this.$store.getters.getModes
        },
        active_data: function () {
            return this.$store.getters.getActiveData
        },
        match: function () {
            if (this.$store.getters.getActiveData?.state == "in_match") {
                return this.$store.getters.getActiveData.match
            }
            return undefined
        }
    },
    methods: {
        chooseCounter(team) {
            if (this.match?.choose_until && this.match?.choosing_team == team) {
                let progress = (new Date(this.match.choose_until.replace(/-/g, "/")) - this.ready_timer) / (10 * this.$store.getters.getConfig.match_pick_teammate_seconds)
                return Math.max(Math.min(progress, 100), 0)
            }
            return 0
        },
        chooseTeam(id) {
            this.$emit("chooseTeammate", id)
        },
        userIsNotChosen(id) {
            for (let i = 0; i < this.active_data.match.team_1.length; i++) {
                if (this.active_data.match.team_1[i] == id)
                    return false
            }
            for (let i = 0; i < this.active_data.match.team_2.length; i++) {
                if (this.active_data.match.team_2[i] == id)
                    return false
            }
            return true
        },
        startPool() {
            if (this.mode) {
                if (this.$store.getters.getUser?.preference == 0) {
                    this.$bvToast.toast("请设置您的兵种偏好（至少选择一项）", {
                        title: "错误",
                        variant: "danger",
                        autoHideDelay: 2000,
                        toaster: "b-toaster-top-center",
                    })
                } else if (this.$store.getters.getUser?.unique_id > 0) {
                    this.$emit("startPool", this.mode)
                } else {
                    this.$bvToast.toast("请先设置您的GUID", {
                        title: "错误",
                        variant: "danger",
                        autoHideDelay: 2000,
                        toaster: "b-toaster-top-center",
                    })
                }
            }
        },
        cancelPool() {
            this.$confirm('确认取消匹配?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$emit("cancelPool")
            }).catch(() => {
            })
        },
        acceptMatch() {
            this.$emit("acceptMatch")
        },
    },
}
</script>

<style scoped>

h5 {
    color: #ffffff;
}

p {
    color: #000000;
}

</style>
