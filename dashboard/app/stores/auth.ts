export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '',
    username: '',
    isLoggedIn: '',
    email: '',
    fullName: ''
  }),
  actions: {
    login(token: string, isLoggedIn: string, username: string, email: string, fullName: string) {
      this.token = token
      this.username = username
      this.isLoggedIn = isLoggedIn
      this.email = email
      this.fullName = fullName
    },
    logout() {
      this.token = ''
      this.username = ''
      this.isLoggedIn = ''
      this.email = ''
      this.fullName = ''
    }
  },
  persist: {
    storage: piniaPluginPersistedstate.localStorage(),
  },
})
