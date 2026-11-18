import axios from 'axios'

const api = axios.create({
  baseURL: '/api/'
})

api.interceptors.request.use((config) => {
    // get Acess Token from browser
    const token = localStorage.getItem('access')
    //检查是否有满足条件的url结尾，如果有那就是publich
    const publicEndpoints = [
        '/register/',
        '/token/',
        '/token/refresh/'
    ]
    const isPublicEndpoints = publicEndpoints.some(
        (endpoint) => config.url?.endsWith(endpoint)
    )
    //only token exists then we add header
    if(token){
        config.headers.Authorization =  `Bearer ${token}`
    }
    // continue the request
    return config
})

api.interceptors.response.use(
    (response) => {
        return response
    },
    async (error) => {
        if (error.response?.status === 401) {
            const refreshToken = localStorage.getItem('refresh')

            // No refresh token: clear login information
            if (!refreshToken) {
                localStorage.removeItem('access')
                localStorage.removeItem('refresh')
                return Promise.reject(error)
            }

            try {
                // Request a new access token
                const response = await axios.post(
                    'http://127.0.0.1:8001/api/token/refresh/',
                    {
                        refresh: refreshToken
                    }
                )

                // Save the new access token
                const newAccessToken = response.data.access
                localStorage.setItem('access', newAccessToken)

                // Update the original request's Authorization header
                error.config.headers.Authorization = `Bearer ${newAccessToken}`

                // Retry the original request
                return api(error.config)

            } catch (refreshError) {
                // Refresh token is invalid or expired
                localStorage.removeItem('access')
                localStorage.removeItem('refresh')

                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)
export default api