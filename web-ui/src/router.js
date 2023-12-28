import { createRouter, createWebHistory  } from 'vue-router'

import Home from './components/Home.vue'
import  Login  from './components/user/Login.vue'
import Resume from './components/user/Resume.vue'
import JobDetail from './components/detail/JobDetail.vue'
import CompanyDetail from './components/detail/CompanyDetail.vue'
import Stars from './components/sublist/Stars.vue'
import History from './components/sublist/History.vue'

// 创建路由对象
const router = createRouter({
  history: createWebHistory (),
  routes: [
    { path: '/', name:'首页',component: Home },
    { path: '/recommend', name:'推荐',component: Home },
    { path: '/job', name:'职位',component: Home },
    { path: '/company', name:'公司',component: Home },
    { path: '/mine', name:'我的',component: Home },
    { path: '/login', name:'登录',component: Login },
    { path: '/resume', name:'简历',component: Resume },
    { path: '/star', name:'收藏',component: Stars },
    { path: '/history', name:'浏览',component: History },
    { path: '/job/detail/:number', name:'职位详细',component: JobDetail  },
    { path: '/company/detail/:number', name:'企业详细',component:CompanyDetail },
  ],
})

// 全局路由导航守卫
router.beforeEach((to, from, next) => {
const accessToken = localStorage.getItem('accessToken')
  if ((to.path ==='/mine' ) && !accessToken) {
    // 证明用户要访问后台主页
    next('/login')
  } else {
    // 访问的不是后台主页
    next()
  }
})

export default router
