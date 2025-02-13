import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  //  {
  //       path: '/',
  //       redirect: '/DashBoard',//测试用
  //   },
   {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login.vue')
  },
  {
    path: '/DashBoard',
    component: () => import('@/views/DashBoard.vue'),
    redirect: '/DashBoard/ActivityOverview',
    children: [
      { 
        path: 'SelfPage', 
        name: 'SelfPage',
        component: () => import('@/components/SelfPage.vue') 
      },
      { 
        path: 'ActivityOverview', 
        name: 'ActivityOverview',
        component: () => import('@/components/ActivityOverview.vue') 
      },
      { 
        path: 'ActivityList', 
        name: 'ActivityList',
        component: () => import('@/components/ActivityList.vue') 
      },
    ]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('username')
  
  if (to.path === '/login') {
    next()
  } else if (!isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
