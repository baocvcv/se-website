<template>
  <div class="question">
    <v-card>
      <v-card-title v-if="!creation">
        Question
        <v-btn
          absolute
          right
          icon
          @click="change_edit_mode"
          v-if="!creation && _editable"
        >
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </v-card-title>
      <v-container class="ml-0 mr-0" fluid>
        <v-row>
          <v-col cols="12" md="6" sm="8" v-if="creation">
            <v-select
              :items="typeSelection"
              v-model="typeSelected"
              label="Choose Type"
            ></v-select>
          </v-col>
        </v-row>

        <v-row v-show="last_changing_time">
          <v-spacer></v-spacer>
          <p>Last Changed: {{ new Date(last_changing_time) }}</p>
          <v-spacer></v-spacer>
        </v-row>

        <!--tree-view and the words shown in readonly mode-->
        <tree-view
          v-model="node_selection"
          :rootID="root_id"
          v-show="creation || (_editable && edit_mode)"
          ref="tree"
        ></tree-view>

        <p v-show="!creation && !(_editable && edit_mode)">
          {{ knowledge_string }}
        </p>

        <question-multiple-choice
          ref="multiple"
          v-if="typeSelected == 'multiple'"
          :readonly="!creation && !(_editable && edit_mode)"
          v-on:submit="submit"
          v-on:cancel="cancel"
          :creation="creation"
        ></question-multiple-choice>
        <question-single-choice
          ref="single"
          v-if="typeSelected == 'single'"
          :readonly="!creation && !(_editable && edit_mode)"
          v-on:submit="submit"
          v-on:cancel="cancel"
          :creation="creation"
        ></question-single-choice>
        <question-single-choice
          ref="TorF"
          v-if="typeSelected == 'TorF'"
          TF
          :readonly="!creation && !(_editable && edit_mode)"
          v-on:submit="submit"
          v-on:cancel="cancel"
          :creation="creation"
        ></question-single-choice>
        <question-brief-answer
          ref="brief_ans"
          v-if="typeSelected == 'brief_ans'"
          :readonly="!creation && !(_editable && edit_mode)"
          v-on:submit="submit"
          v-on:cancel="cancel"
          :creation="creation"
        ></question-brief-answer>
        <question-fill-in-blank
          ref="fill_blank"
          v-if="typeSelected == 'fill_blank'"
          :readonly="!creation && !(_editable && edit_mode)"
          v-on:submit="submit"
          v-on:cancel="cancel"
          :creation="creation"
        ></question-fill-in-blank>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import QuestionMultipleChoice from "@/components/QuestionMultipleChoice.vue";
import QuestionSingleChoice from "@/components/QuestionSingleChoice.vue";
import QuestionBriefAnswer from "@/components/QuestionBriefAnswer.vue";
import QuestionFillInBlank from "@/components/QuestionFillInBlank.vue";
import TreeView from "@/components/TreeView.vue";
import axios from "axios";

export default {
  name: "question-view",
  components: {
    "question-multiple-choice": QuestionMultipleChoice,
    "question-single-choice": QuestionSingleChoice,
    "question-brief-answer": QuestionBriefAnswer,
    "question-fill-in-blank": QuestionFillInBlank,
    "tree-view": TreeView
  },
  props: {
    root_id: {
      type: Number,
      default: -1
    },
    editable: {
      type: Boolean,
      default: false
    },
    creation: {
      type: Boolean,
      default: false
    },
    questionID: {
      type: Number,
      default: -1
    }
  },
  watch: {
    initData: function(newOne) {
      if (!newOne) this.typeSelected = null;
      else {
        this.typeSelected = this.initData.question_type;
        //then updated will be called
      }
    }
  },
  created() {
    if (!this.creation) {
      let url;
      if (this.questionID == -1) {
        url = "/api/questions/" + this.$route.params.id + "/";
      } else {
        url = "/api/questions/" + this.questionID + "/";
      }
      const headers = {
        Authorization: "Token " + this.$store.state.user.token
      };
      axios
        .get(url, { headers: headers })
        .then(response_outer => {
          this.initData = response_outer.data;
          this.root_id = response_outer.data.root_id;
          this.last_changing_time = response_outer.data.question_change_time;
          axios
            .get("/api/nodes_list/" + this.root_id + "/", { headers: headers })
            .then(response => {
              this.tree_data = [response.data];
              this.$refs.tree.updateData(this.tree_data);
              this.node_selection = [];
              let travelSubnode = item => {
                if (this.initData.parents_node.indexOf(item.id) != -1)
                  this.node_selection.push(item);
                item.subnodes.forEach(travelSubnode);
              };
              this.tree_data[0].subnodes.forEach(travelSubnode);
            })
            .catch(error => {
              if (error.response) {
                let status = error.response.status;
                if (status === "403") {
                  this.$notify({
                    type: "error",
                    title: "You have no access to this question."
                  });
                  this.$router.push("/");
                }
              }
            });
        })
        .catch(error => {
          if (error.response) {
            let status = error.response.status;
            if (status === "403") {
              this.$notify({
                type: "error",
                title: "You have no access to this question."
              });
              this.$router.push("/");
            }
          }
        });
    }
  },
  computed: {
    _editable() {
      if (
        !this.creation &&
        this.$route.fullPath.search("/questions/") != -1 &&
        this.$store.state.user.user_group != "Student"
      )
        return true;
      return this.editable;
    },
    knowledge_string() {
      let result = "";
      this.node_selection.forEach(item => (result += "  " + item.name));
      if (!result) return "Uncategorized";
      return result;
    }
  },
  mounted() {
    if (this.initData) this.typeSelected = this.initData.question_type;
  },
  updated() {
    if (this.initData) {
      this.$refs[this.initData.question_type].updateData(this.initData);
    }
  },
  methods: {
    parse_node() {
      let result = [this.root_id];
      this.node_selection.forEach(item => {
        if (result.indexOf(item.id) == -1) result.push(item.id);
      });
      return result;
    },
    submit(info) {
      const headers = {
        Authorization: "Token " + this.$store.state.user.token
      };
      if (info.parents_node.length == 0) {
        //New question
        info.parents_node = this.parse_node();
        axios
          .post("/api/questions/", [info], { headers: headers })
          .then(response => {
            this.edit_mode = false;
            this.$emit("submit", response.data.id);
            this.$notify({
              type: "success",
              title: "The new question is created."
            });
            this.last_changing_time = response.data.question_change_time;
          })
          .catch(err => {
            this.$notify({
              type: "error",
              title: "Failed to create the new question."
            });
          });
      } else {
        //Edit question
        info.parents_node = this.parse_node();
        axios
          .put("/api/questions/" + info.id.toString() + "/", [info], {
            headers: headers
          })
          .then(response => {
            if (this.$route.fullPath.search("/questions/") == -1) {
              this.$refs[this.typeSelected].submitted();
              this.edit_mode = false;
              this.$emit("submit");
            } else {
              this.$router.push("/questions/" + response.data.id);
              location.reload(false);
            }
            this.$notify({
              type: "success",
              title: "Success",
              text: "Your change is saved."
            });
          })
          .catch(err => {
            this.$notify({
              type: "error",
              title: "Failed to edit the question."
            });
          });
      }
    },
    cancel() {
      this.edit_mode = false;
      this.$emit("cancel");
    },
    change_edit_mode() {
      if (this.edit_mode) this.$refs[this.typeSelected].cancel();
      else this.edit_mode = true;
    }
  },
  data: function() {
    return {
      typeSelection: [
        { text: "Single Choice", value: "single" },
        { text: "Multiple Choice", value: "multiple" },
        { text: "T or F", value: "TorF" },
        { text: "Brief Answer", value: "brief_ans" },
        { text: "Fill in Blank", value: "fill_blank" }
      ],
      typeSelected: null,
      edit_mode: false,
      initData: null,
      node_selection: [],
      tree_data: null,
      last_changing_time: null
    };
  }
};
</script>
