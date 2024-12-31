import Vue from 'vue'
import Router from 'vue-router'
import Log from '@/components/log'
//import Students_home from '@/components/Students_home.vue'
import Teachers_home from '@/components/Teachers_home.vue'
import Beatiful_home from '@/components/Beatiful_home.vue'

Vue.use(Router)
//localStorage.removeItem('token');
//console.log('Token stored:', localStorage.getItem('token'));
const router =  new Router({
  routes: [
    {
      path: '/',
      name: 'Log',
      component: Log,
    },
    {
      path: '/student',
      name: 'home',
      component: Beatiful_home,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher',
      name: 'home',
      component:Teachers_home,
      meta: { requiresAuth: true }
    },
    {
      path: '/Students_home',
      name: 'Students_home',
      component:Beatiful_home,
      meta: { requiresAuth: true }
    }
  ]
})
export default router;

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next({
        path: '/',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  } else {
    next();
  }
});


