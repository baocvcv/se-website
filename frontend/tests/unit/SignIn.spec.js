import { mount,createLocalVue } from "@vue/test-utils";
import SignInBox from "@/components/SignInBox.vue";
import SignIn from "@/views/SignIn.vue";
import Vuetify from "vuetify";
import Vuex from "vuex";
import Vue from "vue";
import Router from "vue-router";
import router from "@/router";
import "./mock/SignInMock.js";

const localVue = createLocalVue();
Vue.use(Vuetify);
Vue.use(Vuex);
Vue.use(Router);

describe("SignInBox.vue", () => {
    let vuetify;
    beforeEach(() => {
        vuetify = new Vuetify();
    });
    it("Correct Input", () => {
        const wrapper=mount(SignInBox, {
            localVue,
            vuetify,
            sync: false
        });
        wrapper.setData({
            username:"test",
            password:"test"
        });
        wrapper.vm.$nextTick(() => {
            expect(wrapper.contains(".v-btn--disabled")).toBe(false);
        });
    });
    it("Wrong Input", () => {
        const wrapper=mount(SignInBox, {
            localVue,
            vuetify,
            sync: false
        });
        wrapper.setData({
            username:"test",
            password:""
        });
        wrapper.vm.$nextTick(() => {
            expect(wrapper.contains(".v-btn--disabled")).toBe(true);
        });
    });

    it("Try login correctly", async done => {
        const store = new Vuex.Store({
          state: {
            user: null
          },
          mutations: {
            login(state, payload) {
              state.user = payload.user;
              sessionStorage.setItem('user',JSON.stringify(payload.user));
            }
          },
          actions: {}
        });
        const wrapper=mount(SignInBox, {
            localVue,
            vuetify,
            store,
            router,
            sync: false,
            attachToDocument: true
        });
        wrapper.setData({
            username: "testusr",
            password: "testpsw"
        });
        await wrapper.vm.$nextTick();
        wrapper.find("button").trigger("click");
        await wrapper.vm.$nextTick();
        setTimeout(() => {
            expect(wrapper.vm.sign_in_result).toBe("Success");
            sessionStorage.removeItem('user');
            done();
        },1000);
    });

    it("Try login wrongly", async done => {
        const store = new Vuex.Store({
          state: {
            user: null
          },
          mutations: {
            login(state, payload) {
              state.user = payload.user;
              sessionStorage.setItem('user',JSON.stringify(payload.user));
            }
          },
          actions: {}
        });
        const wrapper=mount(SignInBox, {
            localVue,
            vuetify,
            store,
            router,
            sync: false,
            attachToDocument: true
        });
        wrapper.setData({
            username: "testusr",
            password: "wrongpsw"
        });
        await wrapper.vm.$nextTick();
        wrapper.find("button").trigger("click");
        console.log(wrapper.find("button"));
        await wrapper.vm.$nextTick();
        setTimeout(() => {
            console.log(wrapper.vm.sign_in_response);
            expect(wrapper.vm.sign_in_result).toBe("Error");
            done();
        },1000);
        wrapper.destroy();
    });
});

describe("SignIn.vue", () => {
    let vuetify;
    beforeEach(() => {
        vuetify = new Vuetify();
    });
    it("Render Component Correctly", () => {
        const wrapper=mount(SignIn, {
            localVue,
            vuetify,
            sync: false
        });
        expect(wrapper.contains(".sign-in-box")).toBe(true);
        expect(wrapper.contains(".v-text-field")).toBe(true);
        expect(wrapper.contains(".v-btn")).toBe(true);
    });
});