import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access'),
    refreshToken: localStorage.getItem('refresh')
  }),
  getters:{
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    async login(username: string, password: string){
        const response = await api.post('/token/',{
            username: username,
            password: password
        })
        localStorage.setItem('access', response.data.access)
        localStorage.setItem('refresh', response.data.refresh)

        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh

    }
  }
})