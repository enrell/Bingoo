import { createRouter, createWebHistory } from 'vue-router'
import SearchPage from '../views/SearchPage.vue'
import ResultPage from '../views/ResultPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Search',
      component: SearchPage
    },
    {
      path: '/ResultPage',
      name: 'ResultPage',
      component: ResultPage
    }
  ]
})

export default router
