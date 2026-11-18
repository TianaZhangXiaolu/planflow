
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const pageTitle = computed(() => {
  if (route.path === '/dashboard') return 'Dashboard'
  if (route.path === '/projects') return 'My Projects'
  if (route.path.startsWith('/projects/')) return 'Project Details'
  return 'Workspace'
})

function logout() {
  authStore.accessToken = null
  authStore.refreshToken = null

  localStorage.removeItem('access')
  localStorage.removeItem('refresh')

  router.push('/login')
}
</script>

<template>
  <header class="navbar">
    <div class="navbar-left">
      <div class="mobile-brand">
        <div class="brand-logo">P</div>
        <span>PlanFlow</span>
      </div>

      <div class="page-title">
        {{ pageTitle }}
      </div>
    </div>

    <div class="navbar-right">
      <div class="user-info">
        <div class="user-avatar">U</div>
        <span>My Account</span>
      </div>

      <button class="logout-button" @click="logout">
        <span class="logout-icon">↪</span>
        Logout
      </button>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  right: 0;
  left: 250px;
  z-index: 100;
  display: flex;
  height: 72px;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid #eaebf1;
  background: #ffffff;
  font-family: Arial, sans-serif;
}

.navbar-left,
.navbar-right,
.mobile-brand,
.user-info {
  display: flex;
  align-items: center;
}

.navbar-left {
  gap: 24px;
}

.mobile-brand {
  display: none;
  gap: 9px;
  color: #25283b;
  font-size: 16px;
  font-weight: 700;
}

.brand-logo {
  display: flex;
  width: 32px;
  height: 32px;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  background: #7568dc;
  color: white;
  font-size: 17px;
  font-weight: 700;
}

.page-title {
  color: #25283b;
  font-size: 17px;
  font-weight: 700;
}

.navbar-right {
  gap: 24px;
}

.user-info {
  gap: 10px;
  color: #66697a;
  font-size: 13px;
}

.user-avatar {
  display: flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #eeedff;
  color: #6255cf;
  font-size: 13px;
  font-weight: 700;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 13px;
  border: 1px solid #e8e7f2;
  border-radius: 8px;
  background: white;
  color: #66697a;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s, color 0.2s;
}

.logout-button:hover {
  background: #f4f3ff;
  color: #6255cf;
}

.logout-icon {
  font-size: 17px;
}

@media (max-width: 700px) {
  .navbar {
    left: 0;
    height: 64px;
    padding: 0 16px;
  }

  .navbar-left {
    gap: 12px;
  }

  .mobile-brand {
    display: flex;
  }

  .page-title {
    display: none;
  }

  .navbar-right {
    gap: 12px;
  }

  .user-info span {
    display: none;
  }

  .logout-button {
    padding: 8px 10px;
  }
}
</style>
