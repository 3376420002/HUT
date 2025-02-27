import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    // path: '/',
    // name: 'home',
    // component: () => import('../views/HomeView.vue'),
    // children:[]
    
    path: '/',
    name: 'chart',
    component: () => import('../views/StatisticsView.vue'),
    
    // path: '/',
    // name: 'case',
    // component: () => import('../views/CaseManageView.vue'),
    
    // path: '/',
    // name: 'analyses',
    // component: () => import('../views/ImageAnalysisView.vue'),
    // children:[]

    // path: '/',
    // name: 'ai',
    // component: () => import('../components/IllnessExpectationColumn.vue'),
    // children:[]
  },
]

const router = new VueRouter({
  routes
})

export default router
