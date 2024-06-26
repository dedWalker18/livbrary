import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import BootstrapVue from "bootstrap-vue/dist/bootstrap-vue.esm";
import "bootstrap-vue/dist/bootstrap-vue.css";
import bootstrap from "bootstrap/dist/css/bootstrap.css";

Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.use(bootstrap);
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
