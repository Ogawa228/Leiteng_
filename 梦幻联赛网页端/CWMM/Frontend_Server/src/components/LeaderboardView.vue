<template>
  <div>
    <el-descriptions title="排行榜" style="margin-left: 20px;">
      <el-descriptions-item label="更新时间">{{ leaderboard.update_time }}</el-descriptions-item>
    </el-descriptions>
    <el-table :data="leaderboard.leaderboard">
      <el-table-column label="排名" align="center">
        <template #default="scope">
          <span>{{ scope.$index + 1 }}</span>
        </template>
      </el-table-column>
      <el-table-column label="名称" align="center">
        <template #default="scope">
          <span :style="'color: '+(scope.row.id==user_id?'#eace2a':'#ffffff')">{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="分数" align="center">
        <template #default="scope">
          <span>{{ scope.row.rank }}</span>
        </template>
      </el-table-column>
      <el-table-column label="总场数" align="center">
        <template #default="scope">
          <span>{{ scope.row.match }}</span>
        </template>
      </el-table-column>
      <el-table-column label="胜率" align="center">
        <template #default="scope">
          <span>{{ rounding(scope.row.win * 100 / (scope.row.win + scope.row.lose)) + "%" }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "LeaderboardView",
  props: {
    doUpdate: {
      type: Boolean,
    }
  },
  data() {
    return {}
  },
  watch: {
    doUpdate: {
      handler(val, oldVal) {
        if (val) {
          this.updateLeaderboard()
        }
      },
    },
  },
  computed: {
    leaderboard: function () {
      return this.$store.getters.getLeaderboard
    },
    user_id: function () {
      return this.$store.getters.getUser.id
    },
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
    updateLeaderboard() {
      this.$store.dispatch("updateLeaderboard").then(() => {
            this.$forceUpdate()
          }
      ).catch()
    },
  },
}
</script>

<style scoped>

</style>