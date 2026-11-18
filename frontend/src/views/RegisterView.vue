
<script setup lang="ts">
import { ref } from 'vue'
import api from '@/services/api'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

async function handleClick() {
  errorMessage.value = ''
  successMessage.value = ''

  // Validate inputs
  if (!username.value.trim()) {
    errorMessage.value = 'Username is required.'
    return
  }

  if (!email.value.trim()) {
    errorMessage.value = 'Email is required.'
    return
  }

  if (!password.value) {
    errorMessage.value = 'Password is required.'
    return
  }

  if (!confirmPassword.value) {
    errorMessage.value = 'Please confirm your password.'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

  if (!emailRegex.test(email.value)) {
    errorMessage.value = 'Invalid email format.'
    return
  }

  isLoading.value = true

  try {
    await api.post('/register/', {
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value
    })

    successMessage.value = 'Account created successfully!'

    // Clear form
    username.value = ''
    email.value = ''
    password.value = ''
    confirmPassword.value = ''

  } catch (error) {
    console.error('Failed to register:', error)
    errorMessage.value = 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="register-page">

    <div class="register-card">

      <!-- Brand -->
      <div class="brand">
        <div class="brand-icon">P</div>
        <span>PlanFlow</span>
      </div>

      <!-- Header -->
      <div class="register-header">
        <h1>Create an account</h1>
        <p>Start organizing your projects and tasks.</p>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="handleClick">

        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Choose a username"
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Create a password"
            autocomplete="new-password"
          />
        </div>

        <div class="form-group">
          <label for="confirm-password">Confirm Password</label>
          <input
            id="confirm-password"
            v-model="confirmPassword"
            type="password"
            placeholder="Enter your password again"
            autocomplete="new-password"
          />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <!-- Register Button -->
        <button
          type="submit"
          class="register-button"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Creating Account...' : 'Create Account' }}
        </button>

      </form>

      <!-- Login Link -->
      <div class="login-link">
        Already have an account?
        <RouterLink to="/login">Log in</RouterLink>
      </div>

    </div>

    <p class="footer-text">
      © 2026 PlanFlow. All rights reserved.
    </p>

  </div>
</template>

<style scoped>
/* Page */
.register-page {
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

/* Register Card */
.register-card {
  width: 100%;
  max-width: 440px;
  padding: 38px 40px;
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
  margin-bottom: 30px;
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
.register-header {
  margin-bottom: 26px;
  text-align: center;
}

.register-header h1 {
  margin: 0;
  font-size: 25px;
  font-weight: 700;
}

.register-header p {
  margin-top: 9px;
  color: #9295a4;
  font-size: 13px;
  line-height: 1.6;
}

/* Form */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 17px;
}

.form-group label {
  color: #44475a;
  font-size: 13px;
  font-weight: 600;
}

.form-group input {
  box-sizing: border-box;
  width: 100%;
  padding: 12px 14px;
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

/* Messages */
.error-message,
.success-message {
  margin-bottom: 17px;
  padding: 12px 14px;
  border-radius: 8px;
  font-size: 12px;
}

.error-message {
  background: #fff0f0;
  color: #c03939;
}

.success-message {
  background: #eaf8ef;
  color: #267747;
}

/* Register Button */
.register-button {
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

.register-button:hover {
  background: #5548bd;
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Login Link */
.login-link {
  margin-top: 24px;
  color: #9295a4;
  font-size: 12px;
  text-align: center;
}

.login-link a {
  margin-left: 4px;
  color: #685bd2;
  font-weight: 600;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Footer */
.footer-text {
  margin-top: 25px;
  color: #a0a2af;
  font-size: 11px;
}

@media (max-width: 480px) {
  .register-card {
    padding: 28px 22px;
  }
}
</style>
