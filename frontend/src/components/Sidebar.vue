
<script setup lang="ts">
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()

function isProjectsActive() {
  return route.path === '/projects' || route.path.startsWith('/projects/')
}
</script>

<template>
  <aside class="sidebar">
    <!-- Brand -->
    <RouterLink to="/dashboard" class="brand">
      <div class="brand-logo">P</div>

      <div class="brand-text">
        <span class="brand-name">PlanFlow</span>
        <span class="brand-subtitle">PROJECT MANAGEMENT</span>
      </div>
    </RouterLink>

    <!-- Navigation -->
    <div class="nav-section">
      <p class="nav-label">WORKSPACE</p>

      <nav class="nav-menu">
        <RouterLink
          to="/dashboard"
          class="nav-item"
          :class="{ active: route.path === '/dashboard' }"
        >
          <span class="nav-icon">▦</span>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/projects"
          class="nav-item"
          :class="{ active: isProjectsActive() }"
        >
          <span class="nav-icon">▣</span>
          <span>Projects</span>
        </RouterLink>
      </nav>
    </div>

    <!-- Bottom -->
    <div class="sidebar-footer">
      <div class="footer-decoration"></div>
      <p>Stay organized.</p>
      <span>Make progress every day.</span>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 110;
  display: flex;
  width: 250px;
  flex-direction: column;
  padding: 28px 18px 22px;
  border-right: 1px solid #eaebf1;
  background: #ffffff;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 10px;
  margin-bottom: 52px;
  color: inherit;
  text-decoration: none;
}

.brand-logo {
  display: flex;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #7568dc;
  color: white;
  font-size: 22px;
  font-weight: 700;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.brand-name {
  color: #25283b;
  font-size: 18px;
  font-weight: 700;
}

.brand-subtitle {
  color: #a0a2ae;
  font-size: 9px;
  letter-spacing: 1px;
}

/* Navigation */
.nav-label {
  padding: 0 12px;
  margin-bottom: 12px;
  color: #a0a2ae;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.2px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 12px 14px;
  border-radius: 9px;
  color: #777b8d;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.nav-item:hover {
  background: #f7f6ff;
  color: #6255cf;
}

.nav-item.active {
  background: #eeedff;
  color: #6255cf;
  font-weight: 600;
}

.nav-icon {
  display: flex;
  width: 20px;
  justify-content: center;
  font-size: 19px;
}

/* Footer */
.sidebar-footer {
  margin-top: auto;
  padding: 18px 14px;
  border-radius: 12px;
  background: #f7f6ff;
}

.footer-decoration {
  width: 28px;
  height: 4px;
  margin-bottom: 13px;
  border-radius: 4px;
  background: #7568dc;
}

.sidebar-footer p {
  margin: 0 0 6px;
  color: #45485d;
  font-size: 13px;
  font-weight: 700;
}

.sidebar-footer span {
  color: #9295a4;
  font-size: 11px;
}

@media (max-width: 700px) {
  .sidebar {
    display: none;
  }
}
</style>
