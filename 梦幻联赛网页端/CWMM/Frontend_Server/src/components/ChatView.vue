<template>
    <div>
        <el-container style="height: 85vh;">
            <el-main style="background: #cccccc;">
                <div v-for="item in history" :key="item.id">
                    <div style="height: 50px;" class="rcd">
                        <el-row>
                            <div style="float: left;">
                                {{ item.time + " - " + item.user }}
                            </div>
                        </el-row>
                        <el-row>
                            <div style="float: left;">{{ item.message }}</div>
                        </el-row>
                    </div>
                </div>
            </el-main>
            <el-footer style=" background-color: #00dfbe">
                <el-input v-model="message" style="margin-top: 10px;" placeholder="发送"
                          @keyup.enter.native="sendMessage"></el-input>
            </el-footer>
        </el-container>
    </div>
</template>

<script>
export default {
    name: "ChatView",
    data() {
        return {
            message: "",
        }
    },
    computed: {
        history: function () {
            let h = []
            for (let i = 0; i < this.$store.getters.getMessages.length; i++)
                h.push(this.$store.getters.getMessages[this.$store.getters.getMessages.length - i - 1])
            return h
        },
    },
    methods: {
        sendMessage() {
            if (this.message) {
                this.$emit("sendMessage", this.message)
                this.message = ""
            }
        },
    },
}
</script>

<style scoped>
.rcd:hover {
    background: #aaaaaa;
}
</style>