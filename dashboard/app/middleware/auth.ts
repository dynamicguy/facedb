// import { useAuthStore } from '@/stores/auth'

// export default defineNuxtRouteMiddleware(() => {
//   const autStore = useAuthStore()

//   if (!autStore.isLoggedIn) {
//     return navigateTo('/login')
//   }
// })

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()
  console.log(`From middleware: '${authStore.username}'`)
  
  if (!authStore.isLoggedIn && to.path !== '/login') {
    return navigateTo('/login')
  }

  if (authStore.isLoggedIn && to.path === '/login') {
    return navigateTo('/suspects')
  }
})