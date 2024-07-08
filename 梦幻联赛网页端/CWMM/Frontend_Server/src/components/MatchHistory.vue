<template>
  <div>
    <el-table :data="matches" @row-click="rowClick">
      <el-table-column label="模式" align="center">
        <template #default="scope">
          <span>{{ mode_name(scope.row.result.mode) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="地图" align="center">
        <template #default="scope">
          <span>{{ map_name(scope.row.result.map) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="比分" align="center">
        <template #default="scope">
                        <span :style="'color: '+(win(scope.row)>=0?'#00df00':'#ff0000')">{{
                            scope.row.result.team_1_score + " - " + scope.row.result.team_2_score
                          }}</span>
        </template>
      </el-table-column>
      <el-table-column label="时间" align="center">
        <template #default="scope">
          <span>{{ scope.row.start_time }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-if="showDialog" :visible.sync="showDialog" width="90%">
      <MatchResultCard
          :result="showResult"/>
    </el-dialog>
  </div>
</template>

<script>

import MatchResultCard from "@/components/MatchResultCard.vue";

export default {
  name: "MatchHistory",
  components: {MatchResultCard},
  props: {
    doUpdate: {
      type: Boolean,
    }
  },
  data() {
    return {
      showDialog: false,
      showResult: {},
    }
  },
  watch: {
    doUpdate: {
      handler(val, oldVal) {
        if (val) {
          this.updateMatchHistory()
        }
      },
    },
  },
  computed: {
    matches: function () {
      let mat = []
      for (let i = 0; i < this.$store.getters.getMatchHistory.length; i++) {
        if (this.$store.getters.getMap(this.$store.getters.getMatchHistory[i].result.map)?.name) {
          mat.push(this.$store.getters.getMatchHistory[i])
        }
      }
      return mat
    },
    map_name: function () {
      return function (id) {
        return this.$store.getters.getMap(id).name
      }
    },
    win: function () {
      return function (match) {
        let my_team_score = 0, enemy_team_score = 0
        for (let i = 0; i < match.result.team_1.length; i++) {
          if (this.$store.getters.getUser.id == match.result.team_1[i]) {
            my_team_score = match.result.team_1_score
            enemy_team_score = match.result.team_2_score
            break
          }
        }
        for (let i = 0; i < match.result.team_2.length; i++) {
          if (this.$store.getters.getUser.id == match.result.team_2[i]) {
            my_team_score = match.result.team_2_score
            enemy_team_score = match.result.team_1_score
            break
          }
        }
        if (my_team_score > enemy_team_score)
          return 1
        if (my_team_score < enemy_team_score)
          return -1
        return 0
      }
    },
    mode_name: function () {
      return function (id) {
        return this.$store.getters.getMode(id).name
      }
    },
  },
  methods: {
    rowClick(row, column, event) {
      this.showResult = row.result
      this.showDialog = true
    },
    rounding(value) {
      let realVal = "";
      if (!isNaN(value) && value !== "" && isFinite(value)) {
        realVal = parseFloat(value).toFixed(2);
      } else {
        realVal = "--";
      }
      return realVal;
    },
    updateMatchHistory() {
      this.$store.dispatch("updateMatchHistory").then(() => {
            this.$forceUpdate()
          }
      ).catch()
    },
  },
}
</script>

<style scoped>

</style>