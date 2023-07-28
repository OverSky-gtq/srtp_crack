import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/image',
      name: 'ir',
      component: () => import('../components/ImageRegistration.vue')
    },
    {
      path: '/crack',
      name: 'crack',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../components/CrackIdentity.vue')
    }
  ]
})

export default router
