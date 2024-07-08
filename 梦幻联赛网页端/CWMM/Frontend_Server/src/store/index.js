import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import dayjs from "dayjs";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        user: {},
        maps: [],
        modes: [],
        active_data: {},
        config: {},
        other_users: {},
        messages: [],
        leaderboard: {},
        match_history: [],
        ranks: [],
    },
    getters: {
        getLeaderboard(state) {
            return state.leaderboard
        },
        getUser(state) {
            if (state.user?.id) {
                return state.user
            }
            let user = JSON.parse(sessionStorage.getItem("user"))
            if (user?.id) {
                state.user = user
                return state.user
            }
            return {}
        },
        getOtherUsers(state) {
            return state.other_users
        },
        getRankDetail(state) {
            return function (rank) {
                for (let i = 0; i < state.ranks.length; i++) {
                    if (rank >= state.ranks[i].rank)
                        return state.ranks[i]
                }
                return state.ranks[state.ranks.length - 1]
            }
        },
        getFactionName(state) {
            return function (id) {
                return ["斯瓦迪亚王国", "维基亚王国", "库吉特汗国", "诺德王国", "罗多克王国", "萨兰德苏丹国"][id - 1]
            }
        },
        getMessages(state) {
            return state.messages
        },
        getMap(state) {
            return function (id) {
                for (let i = 0; i < state.maps.length; i++) {
                    if (id == state.maps[i].id) {
                        return state.maps[i]
                    }
                }
            }
        },
        getMode(state) {
            return function (id) {
                for (let i = 0; i < state.modes.length; i++) {
                    if (id == state.modes[i].id) {
                        return state.modes[i]
                    }
                }
            }
        },
        getMaps(state) {
            return state.maps
        },
        getModes(state) {
            return state.modes
        },
        getActiveData(state) {
            return state.active_data
        },
        getConfig(state) {
            return state.config
        },
        getMatchHistory(state) {
            return state.match_history
        },
    },
    mutations: {
        setUser(state, user) {
            state.user = user
            sessionStorage.setItem("user", JSON.stringify(user))
        },
        setMaps(state, maps) {
            state.maps = maps
        },
        setLeaderboard(state, data) {
            state.leaderboard = data
        },
        addMessage(state, message) {
            message.time = dayjs(Date.now()).format("HH:mm:ss")
            state.messages.push(message)
        },
        setModes(state, modes) {
            state.modes = modes
        },
        setRanks(state, data) {
            state.ranks = data
        },
        setActiveData(state, data) {
            state.active_data = data
        },
        setConfig(state, data) {
            state.config = data
        },
        setOtherUser(state, data) {
            state.other_users[data.id] = data
        },
        setMatchHistory(state, date) {
            state.match_history = date
        },
        setOtherUsers(state, data) {
            for (let index in data) {
                let user = data[index]
                state.other_users[user.id] = user
                if (user.id == state.user.id) {
                    for (let key in user) {
                        state.user[key] = user[key]
                    }
                }
            }
        },
    },
    actions: {
        updateOtherUser(context, id) {
            return new Promise((resolve, reject) => {
                axios.get("/query-user-info", {params: {id: id}}).then(
                    res => {
                        if (res.data?.success) {
                            context.commit("setOtherUser", res.data.data.user)
                            resolve()
                        }
                    }
                ).catch(err => {
                    resolve()
                })
            })
        },
        updateLeaderboard(context) {
            return new Promise((resolve, reject) => {
                axios.get("/get-leaderboard").then(
                    res => {
                        if (res.data?.success) {
                            context.commit("setLeaderboard", res.data.data)
                            resolve()
                        }
                    }
                ).catch(err => {
                    resolve()
                })
            })
        },
        updateMatchHistory(context) {
            return new Promise((resolve, reject) => {
                axios.get("/get-match-history", {
                    params: {
                        id: context.state.user.id,
                        username: context.state.user.username,
                        password: context.state.user.password,
                    },
                }).then(
                    res => {
                        if (res.data?.success) {
                            context.commit("setMatchHistory", res.data.data.matches.reverse())
                            resolve()
                        }
                    }
                ).catch(err => {
                    resolve()
                })
            })
        },
    },
    modules: {}
})
