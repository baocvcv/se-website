<template>
  <div class="sign-in-box">
    <v-card>
      <v-layout row justify-center>
        <v-flex md8>
          <v-card-text>
            <p
              class="text-center display-1 font-weight-bold text--primary text-uppercase pt-4"
            >
              sign in
            </p>
            <v-container>
              <v-form ref="input">
                <v-text-field
                  v-model="username"
                  label="Username"
                  v-bind:rules="[v => !!v || 'Username is required.']"
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  v-bind:type="show_password ? 'text' : 'password'"
                  v-bind:rules="[v => !!v || 'Password is required.']"
                  v-bind:append-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
                  v-on:click:append="show_password = !show_password"
                ></v-text-field>
                <v-row>
                  <v-spacer></v-spacer>
                  <v-btn
                    outlined
                    v-on:click="click"
                    v-bind:disabled="!username || !password"
                    >Sign In</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-row>
              </v-form>
            </v-container>
            <p class="text-center mt-4 mb-0 pb-0">
              <router-link to="/"><small>Forget Password?</small></router-link>
              |
              <router-link to="/signup"
                ><small
                  >Do not have an account yet? click here to sign up.</small
                ></router-link
              >
            </p>
          </v-card-text>
        </v-flex>
      </v-layout>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "sign-in",
  data: function() {
    return {
      username: "",
      password: "",
      show_password: false
    };
  },
  methods: {
    click: function() {
      var cur_user = sessionStorage.getItem("user");
      if (!cur_user) {
        var user = {
          username: this.username,
          password: this.password
          //password: md5(this.password),
        };

        axios
          .post("/api/jwt-auth/", user)
          .then(response => {
            //Sign in successfully

            if (response.data.is_banned) {
              this.$notify({
                type: "error",
                title: "Failed to sign in",
                text: "You are banned! Please contact with the admin."
              });
              return;
            }

            user = response.data.user;
            user.token = response.data.token;

            this.$store.commit("updateUser", {
              user: user
            });

            this.sign_in_result = "Success";

            this.$notify({
              type: "success",
              title: "Successfully sign in!"
            });

            this.$router.push("/").catch(err => console.log(err));
          })
          .catch(error => {
            if (error.response) {
              const status = error.response.status;
              if (status === 400) {
                this.$notify({
                  type: "error",
                  title: "Failed to sign in",
                  text: "Username or password incorrect. Please try again."
                });
              } else if (status === 401) {
                this.$notify({
                  type: "error",
                  title: "Failed to sign in",
                  text:
                    "Your account is banned. Please contact with the admins."
                });
              } else if (status === 403) {
                this.$notify({
                  type: "error",
                  title: "Failed to sign in",
                  text:
                    "User has not been activated. Please check the email you use when signing in and click the link to activate your account."
                });
              }
            } else {
              this.$notify({
                type: "error",
                title: "Failed to sign in"
              });
            }
          })
          .then(() => {});
      }
    }
  }
};
</script>

<style scoped>
a {
  color: grey;
}

a:hover {
  color: dodgerblue;
}
</style>
