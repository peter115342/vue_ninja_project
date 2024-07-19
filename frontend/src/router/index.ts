/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import HomePage from '@/components/HomePage.vue'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  extendRoutes: (routes: any) => {
    const extendedRoutes = setupLayouts(routes)
    extendedRoutes.push({
      path: '/home',
      name: 'Home',
      component: HomePage
    })
    return extendedRoutes
  },
})

export default router
