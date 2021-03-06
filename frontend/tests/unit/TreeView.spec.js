import { mount, createLocalVue } from "@vue/test-utils";
import TreeView from "@/components/TreeView.vue";
import Vue from "vue";
import Vuex from "vuex";
import Vuetify from "vuetify";
import Router from "vue-router";
import Notification from "vue-notification";
import { wrap } from "module";

const localVue = createLocalVue();
Vue.use(Vuex);
Vue.use(Vuetify);
Vue.use(Router);
Vue.use(Notification);

describe("TreeView.vue", () => {
  let vuetify, router, store;

  beforeEach(() => {
    vuetify = new Vuetify();
    store = new Vuex.Store({
      state: {
        user: {
          id: 123
        }
      },
      mutations: {
        updateUser(state, payload) {},
        updateUserWithKey(state, payload) {}
      }
    });
  });

  it("travel through all funcs", () => {
    const wrapper = mount(TreeView, {
      localVue,
      vuetify,
      router,
      store,
      sync: false
    });
    wrapper.vm.select([wrapper.vm.treeData[0]]);
    wrapper.vm.beginEdit();
    wrapper.vm.select([wrapper.vm.treeData[0]]);
    wrapper.vm.clearSelection();
    wrapper.vm.submit();
    wrapper.vm.cancel();
    wrapper.vm.updateData([]);
  });

  it("travel through all funcs", () => {
    const wrapper = mount(TreeView, {
      localVue,
      vuetify,
      router,
      store,
      sync: false
    });
    wrapper.vm.removeNode();
    wrapper.vm.rename();
    wrapper.vm.beginEdit();
    wrapper.vm.select([wrapper.vm.treeData[0]]);
    wrapper.vm.rename();
    wrapper.vm.renameConfirmation();
    wrapper.vm.removeNode();
  });
});
