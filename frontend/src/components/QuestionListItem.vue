<template>
  <div id="question-list-item">
    <v-card outlined>
      <v-card-title>
        <v-chip color="primary">
          {{ question.question_type }}
        </v-chip>
        <!--TODO: Change here into computed-->
        <v-chip v-for="node in nodes" :key="node">
          {{ node }}
        </v-chip>
        <div class="flex-grow-1"></div>
        <v-btn text @click="click">
          View<v-icon>mdi-arrow-right</v-icon>
        </v-btn>
        <v-rating
          v-model="question.question_level"
          readonly
          small
          dense
        ></v-rating>
      </v-card-title>
      <v-spacer></v-spacer>
      <v-card-text
        class="question-content"
        ref="content"
        v-bind:style="{ 'max-height': max_height + 'px' }"
      >
        <rich-text-editor
          readonly
          label="Question"
          v-model="content"
        ></rich-text-editor>
        <v-textarea
          outlined
          readonly
          label="Answer"
          v-model="question.question_ans"
          auto-grow
          rows="1"
        >
        </v-textarea>
        <div class="read-more" v-if="content_too_long && hide_content">
          <v-btn icon v-on:click="read_more">
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <div class="collapse" v-if="content_too_long && !hide_content">
          <v-btn text v-on:click="collapse">
            Collapse
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>

    <!--This dialog is for viewing questions-->
    <v-dialog
      v-model="viewing_question"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" icon @click="viewing_question = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </template>
            <span>Close</span>
          </v-tooltip>
          <v-toolbar-title>Viewing Question</v-toolbar-title>
        </v-toolbar>
        <question-view :questionID="question.id" editable="true" />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
import Question from "@/views/Question.vue";
import RichTextEditor from "@/components/RichTextEditor.vue";

export default {
  name: "question-list-item",
  props: {
    question: Object,
    dialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    hide_content: false,
    content_too_long: false,
    width: 0,
    max_height: 400,
    max_height_cache: 0,
    content: "",
    viewing_question: false,
    nodes: []
  }),
  components: {
    "question-view": Question,
    "rich-text-editor": RichTextEditor
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
    this.max_height_cache = this.max_height;
    this.content += this.question.question_content;
    if (this.question.question_choice) {
      this.content += "\n";
      let index;
      for (index = 0; index < this.question.question_choice.length; index++) {
        this.content +=
          "\n" +
          String.fromCharCode(index + 65) +
          ". " +
          this.question.question_choice[index];
      }
    }
    let index;
    const headers = {
      Authorization: "Token " + this.$store.state.user.token
    };
    for (index in this.question.parents_node) {
      let node = this.question.parents_node[index];
      axios
        .get("/api/knowledge_nodes/" + node + "/", { headers: headers })
        .then(response => {
          if (node != this.question.root_id)
            this.nodes.push(response.data.name);
          if (
            this.nodes.length == 0 &&
            index == this.question.parents_node.length - 1
          )
            this.nodes.push("Uncategorized");
        })
        .catch(error => {
          this.$notify({
            type: "error",
            title:
              "Failed to get the knowledge node for question No." +
              this.question.id
          });
        })
        .then(() => {
          if (
            this.nodes.length === 0 &&
            node === this.question.parents_node.length - 1
          )
            this.nodes.push("Uncategorized");
        });
    }
  },
  watch: {
    width: function() {
      let content = this.$refs.content;
      /*
            if (!content)
                return;
            */
      if (content.offsetHeight >= this.max_height) {
        this.content_too_long = true;
        this.hide_content = true;
      } else {
        this.content_too_long = false;
        this.hide_content = false;
      }
    }
    /*
        question: function() {
            this.content += this.question.question_content;
            if (this.question.question_choice)
                this.content += "\n" + this.question.question_choice;
        }
        */
  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
    },
    read_more() {
      this.max_height = 1000000000;
      this.hide_content = false;
    },
    collapse() {
      this.max_height = this.max_height_cache;
      this.hide_content = true;
    },
    click() {
      if (this.dialog) this.viewing_question = true;
      else this.$router.push("/questions/" + this.question.id + "/");
    }
  }
};
</script>

<style scoped>
.question-content {
  overflow: hidden;
  position: relative;
}

.question-content .read-more {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  margin: 0;
  padding: 20px 0;

  background-image: linear-gradient(to bottom, transparent, white);
}

.question-content .collapse {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
}
</style>
