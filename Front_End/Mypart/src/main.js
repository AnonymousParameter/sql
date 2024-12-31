import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from '@/router'

//引入axios配置
import axios from '@/api/index'
Vue.use(ElementUI);
Vue.config.productionTip = false
//修改vue的原型链
Vue.prototype.$axios = axios

new Vue({
  axios,
  router,
  render: h => h(App),
}).$mount('#app')
/*
router.beforeEach((to, from, next) => {
  let isLogin = window.localStorage.getItem('token')
    if (isLogin) {
      next()
    } else {
      if (to.path === '/login') {
        next()
      } else {
        Message.error('没有访问权限或登录已过期，请重新登录！')
        next('/login')
        }
    }
 })
*/
