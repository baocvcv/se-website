<template>
  <div class="multiple-choice-component">
    <v-form ref="form" v-model="valid">
      <v-row>
        <v-col cols="12" md="9">
          <rich-text-editor
            label="Content*"
            v-model="edited_data.content"
            :readonly="readonly"
            required
            ref="richtext"
          ></rich-text-editor>
          <v-list flat>
            <v-list-item two-line>
              <v-list-item-content align="left">
                <v-list-item-title>Choices</v-list-item-title>
                <v-list-item-subtitle
                  :style="answer == 'none' ? 'color:red' : 'color:green'"
                >
                  {{
                    answer === "none"
                      ? "You haven't selected a right answer"
                      : "You have selected " + answer
                  }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item-group color="primary">
              <v-list-item
                v-for="(item, index) in edited_data.choices"
                :key="item.name"
              >
                <v-list-item-icon>
                  {{ item.name }}
                </v-list-item-icon>
                <v-text-field
                  placeholder="Enter choice"
                  v-model="item.content"
                  :rules="[v => !!v || 'Choice content is required!']"
                  :readonly="readonly"
                ></v-text-field>
                <v-btn
                  icon
                  small
                  @click="readonly ? () => {} : changeRightStatus(item)"
                >
                  <v-icon color="green" v-if="item.right"
                    >mdi-check-circle</v-icon
                  >
                  <v-icon color="red" v-else>mdi-close-circle</v-icon>
                </v-btn>
                <v-btn icon small @click="removeChoice(index)" v-if="!readonly">
                  <v-icon color="red">mdi-minus</v-icon>
                </v-btn>
              </v-list-item>
            </v-list-item-group>
            <v-btn
              text
              height="50px"
              class="mx-2 create-choice-button ml-4 mr-4"
              color="grey"
              @click="addChoice()"
              v-if="!readonly"
            >
              Create New
            </v-btn>
          </v-list>
          <v-textarea
            label="Analysis*"
            v-model="edited_data.analysis"
            :rules="[v => !!v || 'Analysis is required!']"
            outlined
            auto-grow
            :readonly="readonly"
          ></v-textarea>
          <v-textarea
            label="Notes"
            v-model="edited_data.title"
            outlined
            :readonly="readonly"
            hint="Write down some notes if necessary"
          ></v-textarea>
        </v-col>
        <v-col>
          <p class="grey--text caption mb-1">Type:</p>
          <v-chip class="mb-4 mt-2">Brief Answer</v-chip>
          <p class="grey--text caption mb-1">Difficulty:</p>
          <v-rating
            v-model="edited_data.difficulty"
            color="yellow darken-3"
            background-color="grey darken-1"
            :readonly="readonly"
            hover
            small
          ></v-rating>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-btn v-if="!readonly" @click="cancel" text class="cancel-button">
          Cancel
        </v-btn>
        <v-btn
          class="mr-4 reset-button"
          text
          @click="reset()"
          v-if="!readonly && creation"
        >
          Reset
        </v-btn>
        <v-btn
          class="mr-4"
          color="primary"
          outlined
          @click="submit()"
          :disabled="!canSubmit"
          v-if="!readonly"
        >
          Submit
        </v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import RichTextEditor from "@/components/RichTextEditor.vue";
export default {
  name: "multiple-choice",
  components: {
    "rich-text-editor": RichTextEditor
  },
  props: {
    readonly: {
      type: Boolean,
      default: false
    },
    creation: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    answer() {
      let ans = [];
      this.edited_data.rightAnswer.every(item => ans.push(item.name));
      if (ans.length < 1) return "none";
      else return ans.join("");
    },
    canSubmit() {
      return this.valid && this.answer != "none";
    }
  },
  methods: {
    addChoice() {
      let length = this.edited_data.choices.length;
      this.edited_data.choices.push({
        name: String.fromCharCode(65 + length),
        content: "",
        right: false
      });
    },
    removeChoice(index) {
      if (this.edited_data.choices[index].right)
        this.edited_data.rightAnswer.splice(
          this.edited_data.rightAnswer.indexOf(this.edited_data.choices[index])
        );
      this.edited_data.choices.splice(index, 1);
      for (var i = 0; i < this.edited_data.choices.length; i++)
        this.edited_data.choices[i].name = String.fromCharCode(65 + i);
    },
    changeRightStatus(item) {
      item.right = !item.right;
      if (item.right) this.edited_data.rightAnswer.push(item);
      else
        this.edited_data.rightAnswer.splice(
          this.edited_data.rightAnswer.indexOf(item),
          1
        );
      this.edited_data.rightAnswer.sort((a, b) => a.name > b.name);
    },
    submit() {
      this.$emit("submit", this.parse());
    },
    submitted() {
      this.data = JSON.stringify(this.parse());
    },
    cancel() {
      this.updateData(JSON.parse(this.data));
      this.$emit("cancel");
    },
    reset() {
      this.$refs.form.reset();
      this.$refs.richtext.reset();
      this.edited_data.rightAnswer = [];
      this.edited_data.choices = [
        {
          name: "A",
          content: "",
          right: false
        },
        {
          name: "B",
          content: "",
          right: false
        },
        {
          name: "C",
          content: "",
          right: false
        },
        {
          name: "D",
          content: "",
          right: false
        }
      ];
      this.data = JSON.stringify(this.parse());
    },
    updateData(input) {
      //parse data input from backend
      this.data = JSON.stringify(input);

      this.edited_data.id = input.id;
      this.edited_data.parents = input.parents_node;
      this.edited_data.change_time = input.question_change_time;
      this.edited_data.title = input.question_name;
      this.edited_data.content = input.question_content;
      this.edited_data.image = input.question_image;
      this.edited_data.analysis = input.question_solution;
      this.edited_data.difficulty = input.question_level;

      let choices = [];
      input.question_choice.forEach(item => {
        let choiceName = String.fromCharCode(65 + choices.length);
        choices.push({
          name: choiceName,
          content: item,
          right: input.question_ans.indexOf(choiceName) != -1 ? true : false
        });
      });
      this.edited_data.choices = choices;

      let rightAns = [];
      choices.forEach(item => {
        if (item.right) rightAns.push(item);
      });
      this.edited_data.rightAnswer = rightAns;
    },
    parse() {
      let result = {
        id: this.edited_data.id,
        parents_node: this.edited_data.parents,
        question_change_time: this.edited_data.change_time,
        question_name: this.edited_data.title,
        question_type: "multiple",
        question_level: this.edited_data.difficulty,
        question_content: this.edited_data.content,
        question_image: this.edited_data.image,
        question_choice: [],
        question_ans: [],
        question_ans_num: this.edited_data.rightAnswer.length,
        question_solution: this.edited_data.analysis
      };
      this.edited_data.rightAnswer.forEach(item =>
        result.question_ans.push(item.name)
      );
      this.edited_data.choices.forEach(item =>
        result.question_choice.push(item.content)
      );
      return result;
    }
  },
  created() {
    this.data = JSON.stringify(this.parse());
  },
  data: function() {
    return {
      edited_data: {
        id: -1,
        parents: [],
        change_time: "",
        title: "",
        content: "",
        image: [],
        choices: [
          {
            name: "A",
            content: "",
            right: false
          },
          {
            name: "B",
            content: "",
            right: false
          },
          {
            name: "C",
            content: "",
            right: false
          },
          {
            name: "D",
            content: "",
            right: false
          }
        ],
        rightAnswer: [],
        analysis: "",
        difficulty: 0
      },
      data: "",
      valid: false
    };
  }
};
</script>

<style scoped>
.create-choice-button {
  border-style: dashed;
  border-width: 1px;
  width: 100%;
}
</style>
