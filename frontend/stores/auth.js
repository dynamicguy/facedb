import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: localStorage.getItem('username') || '',
    token: localStorage.getItem('token') || '',
    isLoggedIn: localStorage.getItem('isLoggedIn') || false,
    email: localStorage.getItem('email') || '',
    fullName: localStorage.getItem('fullName') || '',
  }),
  actions: {
    login(token, isLoggedIn, username, email, fullName) {
      this.token = token
      this.username = username
      this.isLoggedIn = isLoggedIn
      this.email = email
      this.fullName = fullName
      localStorage.setItem('username', username)
      localStorage.setItem('token', token)
      localStorage.setItem('isLoggedIn', isLoggedIn)
      localStorage.setItem('email', email)
      localStorage.setItem('fullName', fullName)
    },
    logout() {
      this.username = ''
      this.token = ''
      this.isLoggedIn = false
      this.email = ''
      this.fullName = ''
      localStorage.removeItem('username')
      localStorage.removeItem('token')
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('email')
      localStorage.removeItem('fullName')
    },
  }
})
