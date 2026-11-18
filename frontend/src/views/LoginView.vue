
<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')

const authStore = useAuthStore()
const router = useRouter()

const errorMessage = ref('')
const isLoading = ref(false)

async function handleClick() {
  errorMessage.value = ''

  if (!username.value.trim() || !password.value) {
    errorMessage.value = 'Please enter your username and password.'
    return
  }

  isLoading.value = true

  try {
    await authStore.login(username.value, password.value)
    router.push('/dashboard')
  } catch (error) {
    errorMessage.value = 'Invalid username or password.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">

    <div class="login-card">

      <!-- Logo / Brand -->
      <div class="brand">
        <div class="brand-icon">P</div>
        <span>PlanFlow</span>
      </div>

      <!-- Header -->
      <div class="login-header">
        <h1>Welcome back!</h1>
        <p>Log in to manage your projects and tasks.</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleClick">

        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter your username"
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            autocomplete="current-password"
          />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          class="login-button"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Logging in...' : 'Log In' }}
        </button>

      </form>

      <!-- Register Link -->
      <div class="register-link">
        Don't have an account?
        <RouterLink to="/register">Create an account</RouterLink>
      </div>

    </div>

    <p class="footer-text">
      © 2026 PlanFlow. All rights reserved.
    </p>

  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 24px;
  box-sizing: border-box;
  background: #f7f8fc;
  color: #25283b;
  font-family: Arial, sans-serif;
}

/* Login Card */
.login-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border: 1px solid #eaebf1;
  border-radius: 16px;
  background: white;
  box-shadow: 0 8px 30px rgba(30, 35, 90, 0.05);
  box-sizing: border-box;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 35px;
  color: #25283b;
  font-size: 20px;
  font-weight: 700;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 11px;
  background: #eeedff;
  color: #6255cf;
  font-size: 20px;
}

/* Header */
.login-header {
  margin-bottom: 30px;
  text-align: center;
}

.login-header h1 {
  margin: 0;
  font-size: 25px;
  font-weight: 700;
}

.login-header p {
  margin-top: 10px;
  color: #9295a4;
  font-size: 13px;
  line-height: 1.6;
}

/* Form */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 9px;
  margin-bottom: 20px;
}

.form-group label {
  color: #44475a;
  font-size: 13px;
  font-weight: 600;
}

.form-group input {
  box-sizing: border-box;
  width: 100%;
  padding: 13px 14px;
  border: 1px solid #e2e3eb;
  border-radius: 8px;
  outline: none;
  background: white;
  color: #25283b;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input::placeholder {
  color: #b0b2bf;
}

.form-group input:focus {
  border-color: #7568dc;
  box-shadow: 0 0 0 3px rgba(117, 104, 220, 0.12);
}

/* Error Message */
.error-message {
  margin-bottom: 18px;
  padding: 12px 14px;
  border-radius: 8px;
  background: #fff0f0;
  color: #c03939;
  font-size: 12px;
}

/* Login Button */
.login-button {
  width: 100%;
  margin-top: 5px;
  padding: 13px;
  border: none;
  border-radius: 8px;
  background: #685bd2;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.2s;
}

.login-button:hover {
  background: #5548bd;
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Register Link */
.register-link {
  margin-top: 25px;
  color: #9295a4;
  font-size: 12px;
  text-align: center;
}

.register-link a {
  margin-left: 4px;
  color: #685bd2;
  font-weight: 600;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Footer */
.footer-text {
  margin-top: 25px;
  color: #a0a2af;
  font-size: 11px;
}

@media (max-width: 480px) {
  .login-card {
    padding: 28px 22px;
  }
}
</style>
