<template>
  <v-list-group v-show="!!paper_name">
    <template v-slot:activator>
      <v-list-item-title
        >{{ paper_name
        }}<span v-show="!latest" style="color: warning">(Old Version)</span> |
        Total records: {{ paper_records.length }}</v-list-item-title
      >
      <v-list-item-action>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-show="!readonly" icon v-on="on" @click="upload_all">
              <v-icon>mdi-publish</v-icon>
            </v-btn>
          </template>
          <span>Publish Marking Result of This Paper</span>
        </v-tooltip>
      </v-list-item-action>
    </template>
    <v-list-item v-for="(record, key) in paper_records" :key="key">
      <v-list-item-content>
        <v-list-item-title
          ><span>{{ record.username }}</span> |
          <span v-if="record.need_judging" style="color: red; font-size: 80%"
            >Unmarked</span
          ><span v-else style="color: green; font-size: 80%;">Marked</span> |
          <span style="font-size: 80%"
            >Score: {{ record.user_total_points }}/{{
              record.paper_total_points
            }}</span
          ></v-list-item-title
        >
        <v-list-item-subtitle
          v-text="new Date(record.record_time)"
        ></v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <slot name="upload">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                v-show="!readonly"
                icon
                v-on="on"
                @click="upload_marking(key)"
                ><v-icon>mdi-publish</v-icon></v-btn
              >
            </template>
            <span>Confirm Marking Result</span>
          </v-tooltip>
        </slot>
      </v-list-item-action>
      <v-list-item-action>
        <slot name="button" :record_id="record.id">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                icon
                v-on="on"
                @click="$router.push('/admin/testmarks/' + record.id)"
                ><v-icon>mdi-pen-plus</v-icon></v-btn
              >
            </template>
            <span>Mark</span>
          </v-tooltip>
        </slot>
      </v-list-item-action>
    </v-list-item>
  </v-list-group>
</template>

<script>
import axios from "axios";
export default {
  name: "test-paper-marking-list-item",
  props: {
    id: {
      type: Number,
      default: -1
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      paper_name: "",
      paper_records: [],
      latest: true
    };
  },
  created() {
    axios
      .get("/api/papers/" + this.id + "/", {
        headers: {
          Authorization: "Token " + this.$store.state.user.token
        }
      })
      .then(response => {
        this.latest = response.data.is_latest;
      })
      .catch(error => {
        console.log(error);
      });
    axios
      .get("/api/paper_records?paper=" + this.id, {
        headers: {
          Authorization: "Token " + this.$store.state.user.token
        }
      })
      .then(response => {
        let all_records = response.data;
        for (var i = 0; i < all_records.length; i++) {
          if (!all_records[i].is_active) {
            if (this.readonly && all_records[i].need_judging) continue;
            if (all_records[i].need_judging)
              this.paper_records.unshift(all_records[i]);
            else this.paper_records.push(all_records[i]);
          }
        }
        if (
          (this.readonly && this.paper_records.length != 0) ||
          (!this.readonly && all_records.length != 0)
        ) {
          this.paper_name = all_records[0].paper_name;
        }
        this.$emit("show");
      })
      .catch(error => {
        console.log(error);
      });
  },
  methods: {
    async upload_marking(index, single = true) {
      let id = this.paper_records[index].id;
      let success = true;
      await axios
        .put(
          "/api/paper_records/" + id,
          { action: "finish" },
          {
            headers: {
              Authorization: "Token " + this.$store.state.user.token
            }
          }
        )
        .then(() => {
          if (single) {
            this.$notify({
              title: "Marking result published!",
              type: "success"
            });
          }
          this.paper_records[index].need_judging = false;
        })
        .catch(error => {
          if (single) {
            this.$notify({
              title: "Oops.Something went wrong.Try again please",
              type: "error"
            });
          }
          success = false;
        });
      return success;
    },
    upload_all() {
      for (var i = 0; i < this.paper_records.length; i++) {
        if (!this.upload_marking(i, false)) {
          this.$notify({
            title: "Oops.Something went wrong uploading No." + i + "result",
            type: "error"
          });
          return false;
        }
      }
      this.$notify({
        title: "Succeeded!",
        type: "success"
      });
    },
    show() {
      return !!this.paper_name;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style></style>
