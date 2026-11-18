
<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '@/services/api'

// ---------- Types ----------

interface Project {
  id: number
  name: string
  description: string
  created_at: string
  updated_at: string
}

interface Task {
  id: number
  title: string
  project: number
  is_completed: boolean
}

// ---------- State ----------

const projects = ref<Project[]>([])
const tasks = ref<Task[]>([])

const newProjectName = ref('')
const newProjectDescription = ref('')

const searchQuery = ref('')

const successMessage = ref('')
const errorMessage = ref('')

const isCreating = ref(false)
const isLoading = ref(true)

// ECharts
const chartElement = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

// ---------- Computed Statistics ----------

const totalProjects = computed(() => projects.value.length)

const totalTasks = computed(() => tasks.value.length)

const completedTasks = computed(() =>
  tasks.value.filter(task => task.is_completed).length
)

const remainingTasks = computed(() =>
  totalTasks.value - completedTasks.value
)

const overallProgress = computed(() => {
  if (totalTasks.value === 0) return 0

  return Math.round(
    (completedTasks.value / totalTasks.value) * 100
  )
})

// Calculate progress for each project
const projectProgress = computed(() => {
  return projects.value.map(project => {
    const projectTasks = tasks.value.filter(
      task => task.project === project.id
    )

    const completed = projectTasks.filter(
      task => task.is_completed
    ).length

    const total = projectTasks.length

    const progress = total === 0
      ? 0
      : Math.round((completed / total) * 100)

    return {
      ...project,
      totalTasks: total,
      completedTasks: completed,
      progress
    }
  })
})

// Search projects
const filteredProjects = computed(() => {
  const keyword = searchQuery.value.trim().toLowerCase()

  if (!keyword) return projectProgress.value

  return projectProgress.value.filter(project =>
    project.name.toLowerCase().includes(keyword) ||
    project.description.toLowerCase().includes(keyword)
  )
})

// ---------- Fetch Data ----------

async function fetchDashboardData() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const [projectResponse, taskResponse] = await Promise.all([
      api.get('/projects/'),
      api.get('/tasks/')
    ])

    projects.value = projectResponse.data
    tasks.value = taskResponse.data

    await nextTick()
    updateChart()

  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    errorMessage.value = 'Failed to load dashboard data.'
  } finally {
    isLoading.value = false
  }
}

// ---------- Create Project ----------

async function handleCreateProject() {
  successMessage.value = ''
  errorMessage.value = ''

  if (!newProjectName.value.trim()) {
    errorMessage.value = 'Please enter a project name.'
    return
  }

  isCreating.value = true

  try {
    await api.post('/projects/', {
      name: newProjectName.value.trim(),
      description: newProjectDescription.value.trim()
    })

    newProjectName.value = ''
    newProjectDescription.value = ''

    await fetchDashboardData()

    successMessage.value = 'Project created successfully!'

  } catch (error) {
    console.error('Failed to create project:', error)
    errorMessage.value = 'Failed to create project.'
  } finally {
    isCreating.value = false
  }
}

// ---------- ECharts ----------

function updateChart() {
  if (!chartElement.value) return

  if (!chartInstance) {
    chartInstance = echarts.init(chartElement.value)
  }

  const hasTasks = totalTasks.value > 0

  chartInstance.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },

    legend: {
      bottom: 0,
      left: 'center',
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        color: '#85899b'
      }
    },

    series: [
      {
        name: 'Task Progress',
        type: 'pie',
        radius: ['62%', '82%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: true,

        itemStyle: {
          borderRadius: 6,
          borderColor: '#ffffff',
          borderWidth: 3
        },

        label: {
          show: false
        },

        emphasis: {
          scale: true,
          scaleSize: 8
        },

        data: hasTasks
          ? [
              {
                value: completedTasks.value,
                name: 'Completed',
                itemStyle: { color: '#7568dc' }
              },
              {
                value: remainingTasks.value,
                name: 'Remaining',
                itemStyle: { color: '#e8e7f0' }
              }
            ]
          : [
              {
                value: 1,
                name: 'No tasks',
                itemStyle: { color: '#e8e7f0' }
              }
            ]
      }
    ],

    graphic: [
      {
        type: 'text',
        left: 'center',
        top: '36%',
        style: {
          text: `${overallProgress.value}%`,
          textAlign: 'center',
          fill: '#25283b',
          fontSize: 28,
          fontWeight: 700
        }
      },
      {
        type: 'text',
        left: 'center',
        top: '49%',
        style: {
          text: 'Completed',
          textAlign: 'center',
          fill: '#85899b',
          fontSize: 12
        }
      }
    ]
  })
}

function handleResize() {
  chartInstance?.resize()
}

// ---------- Helpers ----------

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'

  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

function getProgressColor(progress: number) {
  if (progress === 100) return '#35a879'
  if (progress >= 60) return '#7568dc'
  if (progress >= 30) return '#e5a34b'

  return '#8c91a5'
}

// ---------- Lifecycle ----------

onMounted(async () => {
  await fetchDashboardData()

  if (chartElement.value) {
    updateChart()
  }

  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)

  chartInstance?.dispose()
  chartInstance = null
})
</script>

<template>
  <div class="dashboard">

    <!-- Header -->
    <header class="dashboard-header">
      <div>
        <p class="eyebrow">WORKSPACE OVERVIEW</p>
        <h1>Dashboard</h1>
        <p class="subtitle">
          Track your projects and stay on top of your tasks.
        </p>
      </div>

      <div class="header-date">
        {{ new Date().toLocaleDateString('en-GB', {
          day: '2-digit',
          month: 'long',
          year: 'numeric'
        }) }}
      </div>
    </header>

    <!-- Messages -->
    <div v-if="successMessage" class="message success-message">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="message error-message">
      {{ errorMessage }}
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading">
      Loading your dashboard...
    </div>

    <template v-else>

      <!-- Statistics -->
      <section class="stats-grid">

        <div class="stat-card">
          <div class="stat-icon purple">▦</div>
          <p>Total Projects</p>
          <h2>{{ totalProjects }}</h2>
          <span>Projects in your workspace</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon blue">☷</div>
          <p>Total Tasks</p>
          <h2>{{ totalTasks }}</h2>
          <span>Across all projects</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon green">✓</div>
          <p>Completed Tasks</p>
          <h2>{{ completedTasks }}</h2>
          <span>{{ remainingTasks }} tasks remaining</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon orange">◷</div>
          <p>Overall Progress</p>
          <h2>{{ overallProgress }}%</h2>
          <span>Task completion rate</span>
        </div>

      </section>

      <!-- Analytics -->
      <section class="analytics-grid">

        <div class="panel chart-panel">
          <div class="section-heading">
            <div>
              <h2>Task Completion</h2>
              <p>Overall task progress</p>
            </div>
          </div>

          <div ref="chartElement" class="chart-container"></div>
        </div>

        <!-- Quick Create -->
        <div class="panel create-panel">
          <div class="section-heading">
            <div>
              <h2>Create a Project</h2>
              <p>Start organizing something new.</p>
            </div>
          </div>

          <form @submit.prevent="handleCreateProject">
            <div class="form-group">
              <label for="project-name">Project Name</label>
              <input
                id="project-name"
                v-model="newProjectName"
                type="text"
                placeholder="e.g. Website Development"
              />
            </div>

            <div class="form-group">
              <label for="project-description">Description</label>
              <textarea
                id="project-description"
                v-model="newProjectDescription"
                rows="4"
                placeholder="What is this project about?"
              ></textarea>
            </div>

            <button
              type="submit"
              class="create-button"
              :disabled="isCreating"
            >
              {{ isCreating ? 'Creating...' : '+ Create Project' }}
            </button>
          </form>
        </div>

      </section>

      <!-- Projects -->
      <section class="projects-section">

        <div class="projects-heading">
          <div>
            <h2>Your Projects</h2>
            <p>Monitor the progress of each project.</p>
          </div>

          <div class="search-box">
            <span>⌕</span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search projects..."
            />
          </div>
        </div>

        <div v-if="filteredProjects.length > 0" class="projects-grid">

          <article
            v-for="project in filteredProjects"
            :key="project.id"
            class="project-card"
          >

            <div class="project-card-header">
              <div class="project-avatar">
                {{ project.name.charAt(0).toUpperCase() }}
              </div>

              <span
                class="status-label"
                :class="{ completed: project.progress === 100 }"
              >
                {{ project.progress === 100 ? 'Completed' : 'In Progress' }}
              </span>
            </div>

            <h3>{{ project.name }}</h3>

            <p class="project-description">
              {{ project.description || 'No description provided.' }}
            </p>

            <div class="progress-info">
              <span>Progress</span>
              <strong>{{ project.progress }}%</strong>
            </div>

            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{
                  width: `${project.progress}%`,
                  background: getProgressColor(project.progress)
                }"
              ></div>
            </div>

            <div class="project-meta">
              <span>
                {{ project.completedTasks }} / {{ project.totalTasks }} tasks
              </span>
              <span>{{ formatDate(project.created_at) }}</span>
            </div>

          </article>

        </div>

        <div v-else class="empty-state">
          <div class="empty-icon">▦</div>
          <h3>No projects found</h3>
          <p>
            {{
              searchQuery
                ? 'Try another search keyword.'
                : 'Create your first project to get started.'
            }}
          </p>
        </div>

      </section>

    </template>

  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 36px 42px;
  background: #f7f8fc;
  color: #292b40;
  font-family: Arial, sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.eyebrow {
  margin: 0 0 9px;
  color: #7568dc;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 30px;
  font-weight: 700;
}

.subtitle {
  margin: 9px 0 0;
  color: #9295a6;
  font-size: 14px;
}

.header-date {
  padding: 10px 15px;
  border: 1px solid #ececf2;
  border-radius: 9px;
  background: white;
  color: #777b8e;
  font-size: 12px;
}

/* Messages */

.message {
  margin-bottom: 18px;
  padding: 12px 16px;
  border-radius: 9px;
  font-size: 13px;
}

.success-message {
  background: #eaf8f0;
  color: #267747;
}

.error-message {
  background: #fff0f0;
  color: #c03939;
}

.loading {
  padding: 50px;
  color: #85899b;
  text-align: center;
}

/* Statistics */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 22px;
}

.stat-card {
  padding: 22px;
  border: 1px solid #ededf3;
  border-radius: 13px;
  background: white;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  margin-bottom: 17px;
  border-radius: 10px;
  font-size: 20px;
  font-weight: 700;
}

.purple {
  background: #efedff;
  color: #7568dc;
}

.blue {
  background: #e9f2ff;
  color: #4985d5;
}

.green {
  background: #e9f7ef;
  color: #35a879;
}

.orange {
  background: #fff3e6;
  color: #df9943;
}

.stat-card p {
  margin: 0;
  color: #85899b;
  font-size: 12px;
}

.stat-card h2 {
  margin: 9px 0;
  font-size: 27px;
}

.stat-card span {
  color: #a0a2af;
  font-size: 11px;
}

/* Panels */

.analytics-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 20px;
  margin-bottom: 35px;
}

.panel {
  padding: 24px;
  border: 1px solid #ededf3;
  border-radius: 13px;
  background: white;
}

.section-heading h2,
.projects-heading h2 {
  margin: 0;
  font-size: 17px;
}

.section-heading p,
.projects-heading p {
  margin: 7px 0 0;
  color: #9699a8;
  font-size: 12px;
}

.chart-container {
  width: 100%;
  height: 260px;
}

/* Create Form */

.create-panel form {
  margin-top: 23px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  color: #55586b;
  font-size: 12px;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  box-sizing: border-box;
  width: 100%;
  padding: 11px 13px;
  border: 1px solid #e5e5ed;
  border-radius: 8px;
  outline: none;
  color: #292b40;
  background: white;
  font-family: inherit;
  font-size: 13px;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #7568dc;
  box-shadow: 0 0 0 3px rgba(117, 104, 220, 0.1);
}

.form-group textarea {
  resize: vertical;
}

.create-button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: #7568dc;
  color: white;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.create-button:hover {
  background: #6255c9;
}

.create-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Project List */

.projects-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 13px;
  border: 1px solid #e8e8ef;
  border-radius: 8px;
  background: white;
  color: #85899b;
}

.search-box input {
  width: 180px;
  border: none;
  outline: none;
  color: #292b40;
  font-size: 12px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.project-card {
  padding: 21px;
  border: 1px solid #ededf3;
  border-radius: 12px;
  background: white;
  transition: transform 0.2s, box-shadow 0.2s;
}

.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(30, 35, 90, 0.06);
}

.project-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.project-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 39px;
  height: 39px;
  border-radius: 10px;
  background: #efedff;
  color: #7568dc;
  font-size: 17px;
  font-weight: 700;
}

.status-label {
  padding: 5px 9px;
  border-radius: 20px;
  background: #fff3e6;
  color: #c48635;
  font-size: 10px;
  font-weight: 600;
}

.status-label.completed {
  background: #e9f7ef;
  color: #35a879;
}

.project-card h3 {
  overflow-wrap: anywhere;
  margin: 0 0 9px;
  font-size: 15px;
}

.project-description {
  min-height: 35px;
  overflow-wrap: anywhere;
  margin: 0 0 22px;
  color: #9699a8;
  font-size: 12px;
  line-height: 1.6;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 9px;
  color: #85899b;
  font-size: 11px;
}

.progress-info strong {
  color: #45485b;
}

.progress-track {
  height: 7px;
  overflow: hidden;
  border-radius: 10px;
  background: #efeff4;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.4s ease;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-top: 15px;
  color: #a0a2af;
  font-size: 10px;
}

/* Empty State */

.empty-state {
  padding: 55px 20px;
  border: 1px dashed #dedee9;
  border-radius: 12px;
  background: white;
  text-align: center;
}

.empty-icon {
  color: #7568dc;
  font-size: 32px;
}

.empty-state h3 {
  margin: 14px 0 7px;
  font-size: 15px;
}

.empty-state p {
  color: #9699a8;
  font-size: 12px;
}

/* Responsive */

@media (max-width: 1050px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .projects-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .dashboard {
    padding: 24px 16px;
  }

  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 15px;
  }

  .analytics-grid {
    grid-template-columns: 1fr;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .projects-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .search-box {
    width: 100%;
    box-sizing: border-box;
  }

  .search-box input {
    width: 100%;
  }
}
</style>
