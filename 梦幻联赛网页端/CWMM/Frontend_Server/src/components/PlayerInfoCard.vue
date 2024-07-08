<template>
  <el-row>
    <el-card :class="clickable?'clk':'unclk'" id="picd"
             :style="{backgroundImage:'url('+rank_image+')'}"
             @click.native="click">
      <div slot="header">
        <span :style="'color: '+(id==user_id?'#eace2a':'#ffffff')+('; font-size: 12px')">{{
            '[' + rank_name + ']' + username + '(' + rank + ')'
          }}</span>
        <el-image
            v-if="active_data.state == 'in_match' && active_data.match.state == 'wait_for_ready' && id && active_data.match.ready_users.includes(id)"
            style="width: 24px; height: 24px; vertical-align: top"
            :src="require('../assets/ready.png')"></el-image>
      </div>
      <div class="wb">
        <el-image v-if="(this.user?.preference & 0x1) != 0" style="width: 40px; height: 30px;"
                  :src="require('../assets/archer.png')"></el-image>
        <el-image v-if="(this.user?.preference & 0x2) != 0" style="width: 20px; height: 30px;"
                  :src="require('../assets/infantry.png')"></el-image>
        <el-image v-if="(this.user?.preference & 0x4) != 0" style="width: 40px; height: 30px;"
                  :src="require('../assets/cavalry.png')"></el-image>
        <div style="color: #19ccf5">
          <div>胜率：{{ win_rate }}</div>
          <div>KD：{{ kd }}</div>
          <div>每场伤害：{{ avg_damage }}</div>
        </div>
      </div>
    </el-card>
  </el-row>
</template>

<script>
export default {
  name: "PlayerInfoCard",
  props: {
    id: {
      type: Number | undefined,
      required: true,
    },
    clickable: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      user: {},
    }
  },
  computed: {
    user_id: function () {
      return this.$store.getters.getUser.id
    },
    rank_image: function () {
      if (!this.user || !this.$store.getters.getRankDetail(this.user.rank)?.name)
        return ''
      let url = this.$store.getters.getRankDetail(this.user.rank).name + ".png"
      return require("../assets/" + url)
    },
    rank_name: function () {
      if (!this.user || !this.$store.getters.getRankDetail(this.user.rank)?.name)
        return '??'
      return this.$store.getters.getRankDetail(this.user.rank).name
    },
    username: function () {
      return this.user?.username || '??'
    },
    rank: function () {
      if (this.$store.getters.getMode(this.$store.getters.getActiveData?.match?.mode)?.id == 1)
        return this.user?.rank_33 || '??'
      return this.user?.rank || '??'
    },
    kd: function () {
      if (!this.user)
        return '??'
      return this.rounding(this.user.kill / this.user.death)
    },
    win_rate: function () {
      if (!this.user)
        return '??'
      return this.rounding(this.user.win * 100 / (this.user.win + this.user.lose)) + '%'
    },
    avg_damage: function () {
      if (!this.user)
        return '??'
      return this.rounding(this.user.damage / this.user.match)
    },
    active_data: function () {
      return this.$store.getters.getActiveData;
    },
    preference: function () {
      if (!this.user)
        return '??'
      let result = ""
      if ((this.user.preference & 0x1) != 0) {
        result += "射|"
      }
      if ((this.user.preference & 0x2) != 0) {
        result += "步|"
      }
      if ((this.user.preference & 0x4) != 0) {
        result += "骑|"
      }
      if (result.length > 0)
        result = result.substring(0, result.length - 1)
      return result
    },
  },
  mounted() {
    setInterval(() => {
      if (this?.id && !this.$store.getters.getOtherUsers[this.id])
        this.refreshUserData()
      else
        this.user = this.$store.getters.getOtherUsers[this.id]
    }, 1000)
    this.user = this.$store.getters.getOtherUsers[this.id]
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
    refreshUserData() {
      this.$store.dispatch("updateOtherUser", this.id).then(() => {
        this.user = this.$store.getters.getOtherUsers[this.id]
      })
    },
    click() {
      if (this.clickable) {
        this.$emit("click", this.id)
      }
    },
  },
}
</script>

<style scoped>

#picd {
  width: 180px;
  height: 200px;
  display: inline-block;
  margin-bottom: 20px;
  background-size: 180px;
  background-repeat: no-repeat;
  background-position: bottom;

}

#picd ::v-deep .el-card__header {
  padding-left: 0;
  padding-right: 0;
  padding-top: 10px;
  padding-bottom: 10px;
}

.wb {
  padding: 0;
}

.card-body {
  padding: 0;
}

.clk {
  cursor: pointer;
}

.clk:hover {
  background-color: #00df00;
}

</style>