
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'

import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()

// Hide the workspace layout on Login and Register pages
const showLayout = computed(() => {
  return route.path !== '/login' && route.path !== '/register'
})
</script>

<template>
  <template v-if="showLayout">
    <Sidebar />
    <Navbar />

    <main class="main-content">
      <RouterView />
    </main>
  </template>

  <RouterView v-else />
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  color: #25283b;
}

.main-content {
  min-height: 100vh;
  margin-left: 250px;
  padding-top: 72px;
  background: #f7f8fc;
}

@media (max-width: 700px) {
  .main-content {
    margin-left: 0;
    padding-top: 64px;
  }
}
</style>
