<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
const autStore = useAuthStore();


const credentials = reactive({
  username: '',
  password: '',
})

async function handleLogin() {
  console.log('CREDENTIALS', credentials)
  const formData = new FormData()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)
  $fetch('/api/token', {
    method: 'POST',
    body: formData
  })
    .then(async (res) => {
      // Refresh the session on client-side and redirect to the home page
      console.log('RESPONSE', res)
      if(res && res.user){
        const email = res.user.email;
        const fullName = res.user.full_name;
        console.log('email', email, fullName);
        autStore.login(res.access_token, true, res.user.username, email, fullName);
        await navigateTo('/');
      }
    })
    .catch((err) => {
      console.error('Bad credentials', err)
      autStore.logout()
    })
}
</script>

<template>
  <section class="bg-gray-50 dark:bg-gray-900">
    <div class="main flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
        <img src="/assets/images/logo.png" alt="logo">
      </a>
      <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
            Sign in to your account
          </h1>
          <form @submit.prevent="handleLogin">
            <div class="mb-4">
              <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                id="username"
                v-model="credentials.username"
                placeholder="Enter your username"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div class="mb-6">
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                id="password"
                v-model="credentials.password"
                placeholder="Enter your password"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button
              type="submit"
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Login
            </button>
          </form>
          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              Don't have an account? <nuxt-link to="/register" class="text-blue-600 hover:underline">Sign up</nuxt-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
section {
  min-height: 100vh;
}
.main {
 margin: 0 300px;
}
</style>
