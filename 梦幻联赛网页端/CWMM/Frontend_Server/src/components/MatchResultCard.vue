<template>
  <div>
    <div style="display: inline-block; width: 1400px;">
      <el-descriptions>
        <el-descriptions-item label="模式">{{ mode_name }}</el-descriptions-item>
        <el-descriptions-item label="地图">{{ map_name }}</el-descriptions-item>
      </el-descriptions>
      <h1><span :style="'color: '+(win(result)>=0?'#00df00':'#ff0000')">{{
          result.team_1_score + " - " + result.team_2_score
        }}
            </span>
        <span
            :style="'color: '+(result.statistics[user_id].rank_change[0]<=result.statistics[user_id].rank_change[1]?'#00df00':'#ff0000')">
                    {{ " (" + rank_delta + ")" }}
                </span>
      </h1>
      <el-row>
        <el-col :span="10">
          <h5 style="color: #ffffff;">{{ team_1_faction }}</h5>
          <el-table :data="team_1_items" :key="isUpdate">
            <el-table-column label="序号" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="名称" align="center">
              <template #default="scope">
                <span :style="'color: '+(scope.row.id==user_id?'#eace2a':'#ffffff')">{{
                    username[scope.row.id]
                  }}</span>
              </template>
            </el-table-column>
            <el-table-column label="击杀" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[0] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="死亡" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[2] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="伤害" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[3] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="队友伤害" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[4] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="Hit" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[5] }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="10" :offset="2">
          <h5 style="color: #ffffff;">{{ team_2_faction }}</h5>
          <el-table :data="team_2_items" :key="isUpdate">
            <el-table-column label="序号" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.$index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="名称" align="center">
              <template #default="scope">
                <span :style="'color: '+(scope.row.id==user_id?'#eace2a':'#ffffff')">{{ username[scope.row.id] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="击杀" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[0] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="死亡" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[2] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="伤害" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[3] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="队友伤害" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[4] }}</span>
              </template>
            </el-table-column>
            <el-table-column label="Hit" align="center" width="60px">
              <template #default="scope">
                <span>{{ scope.row.data.stat[5] }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import PlayerInfoCard from "@/components/PlayerInfoCard.vue";

export default {
  name: "MatchResultCard",
  components: {PlayerInfoCard},
  props: {
    result: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      team_1_items: [],
      team_2_items: [],
      username: {},
      isUpdate: true,
    }
  },
  computed: {
    user_id: function () {
      return this.$store.getters.getUser.id;
    },
    rank_delta: function () {
      let delta = this.result.statistics[this.$store.getters.getUser.id].rank_change[1] - this.result.statistics[this.$store.getters.getUser.id].rank_change[0]
      if (delta > 0)
        return "+" + delta
      else
        return delta
    },
    win: function () {
      return function (result) {
        let my_team_score = 0, enemy_team_score = 0
        for (let i = 0; i < result.team_1.length; i++) {
          if (this.$store.getters.getUser.id == result.team_1[i]) {
            my_team_score = result.team_1_score
            enemy_team_score = result.team_2_score
            break
          }
        }
        for (let i = 0; i < result.team_2.length; i++) {
          if (this.$store.getters.getUser.id == result.team_2[i]) {
            my_team_score = result.team_2_score
            enemy_team_score = result.team_1_score
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
    team_1_faction: function () {
      return this.$store.getters.getFactionName(this.result.team_1_faction)
    },
    team_2_faction: function () {
      return this.$store.getters.getFactionName(this.result.team_2_faction)
    },
    mode_name: function () {
      return this.$store.getters.getMode(this.result.mode)?.name
    },
    map_name: function () {
      return this.$store.getters.getMap(this.result.map)?.name
    },
  },
  mounted() {
    let team_1_items = []
    let team_2_items = []
    for (let id in this.result.statistics) {
      if (this.result.team_1.includes(Number(id))) {
        team_1_items.push({
          id: id,
          data: this.result.statistics[id],
        })
      } else {
        team_2_items.push({
          id: id,
          data: this.result.statistics[id],
        })
      }
    }
    team_1_items.sort((a, b) => {
      return b.data.stat[3] - a.data.stat[3]
    })
    team_2_items.sort((a, b) => {
      return b.data.stat[3] - a.data.stat[3]
    })
    this.team_1_items = team_1_items
    this.team_2_items = team_2_items

    for (let i = 0; i < this.result.team_1.length; i++) {
      let id = this.result.team_1[i]
      if (this.$store.getters.getOtherUsers[id]?.username) {
        this.username[id] = this.$store.getters.getOtherUsers[id].username
      } else
        this.username[id] = ""
    }
    for (let i = 0; i < this.result.team_2.length; i++) {
      let id = this.result.team_2[i]
      if (this.$store.getters.getOtherUsers[id]?.username) {
        this.username[id] = this.$store.getters.getOtherUsers[id].username
      } else
        this.username[id] = ""
    }

    setInterval(() => {
      let ids = []
      for (let i = 0; i < this.team_1_items.length; i++) {
        ids.push(this.team_1_items[i].id)
      }
      for (let i = 0; i < this.team_2_items.length; i++) {
        ids.push(this.team_2_items[i].id)
      }

      for (let i = 0; i < ids.length; i++) {
        let id = ids[i]
        if (!this.username[id]) {
          if (!this.$store.getters.getOtherUsers[id]) {
            this.$store.dispatch("updateOtherUser", id).then(() => {
              this.username[id] = this.$store.getters.getOtherUsers[id].username
              this.isUpdate = !this.isUpdate
            })
          }
        }
      }
    }, 1000)
  },
  methods: {},
}
</script>

<style scoped>

</style>