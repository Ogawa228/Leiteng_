import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import {BootstrapVue, IconsPlugin} from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import axios from "axios";
import {BACKEND_HOST, BACKEND_PORT} from "./config";
import {Button, Cell, CellGroup, Divider} from 'vant';
import 'vant/lib/index.css';
import ElementUI from 'element-ui';
//import 'element-ui/lib/theme-chalk/index.css';
import "../style/theme/index.css"

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

Vue.use(ElementUI);

Vue.use(Button)
Vue.use(Cell)
Vue.use(CellGroup)
Vue.use(Divider)

axios.defaults.baseURL = "http://" + BACKEND_HOST + ":" + BACKEND_PORT + "/"
axios.defaults.timeout = 5000
Vue.prototype.$axios = axios

Vue.config.productionTip = false

let app = new Vue({
    router,
    store,
    render: h => h(App)
})

app.$mount('#app')
