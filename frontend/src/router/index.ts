
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import DashboardView from "../views/DashboardView.vue"
import ProjectsView from "../views/ProjectsView.vue"
import TasksView from "../views/TasksView.vue"
import ProjectDetailView from "../views/ProjectDetailView.vue"
import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: '/login',
    component: LoginView
    },
    {
        path: '/register',
        component: RegisterView
    },
    {
        path: '/dashboard',
        component: DashboardView
    },
    {
        path: '/projects',
        component: ProjectsView
    },
    {
        path: '/tasks',
        component: TasksView
    },
    {
        path: '/projects/:id',
        component: ProjectDetailView
    },
    {
        path: '/navbar',
        component: Navbar
    },
    {
        path: '/sidebar',
        component: Sidebar
    },
  ]
})

export default router
