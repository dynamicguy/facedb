import { useAuthStore } from "@/stores/auth";


export default defineNuxtRouteMiddleware(() => {
    const autStore = useAuthStore();

    if (!autStore.isLoggedIn) {
        return navigateTo('/login')
    }
})
