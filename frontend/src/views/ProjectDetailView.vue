
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

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
  description: string
  project: number
  is_completed: boolean
  created_at: string
  updated_at: string
}

const route = useRoute()
const router = useRouter()

const project = ref<Project | null>(null)
const tasks = ref<Task[]>([])

const isLoading = ref(false)
const isSaving = ref(false)

const newTaskTitle = ref('')
const newTaskDescription = ref('')

const errorMessage = ref('')
const successMessage = ref('')

// Get project ID from the URL
const projectId = Number(route.params.id)

// Calculate project progress
const completedTasks = computed(() => {
  return tasks.value.filter(task => task.is_completed).length
})

const totalTasks = computed(() => tasks.value.length)

const progress = computed(() => {
  if (totalTasks.value === 0) return 0

  return Math.round((completedTasks.value / totalTasks.value) * 100)
})

// Fetch project and its tasks
async function fetchData() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const [projectResponse, taskResponse] = await Promise.all([
      api.get(`/projects/${projectId}/`),
      api.get('/tasks/')
    ])

    project.value = projectResponse.data

    // Only show tasks belonging to this project
    tasks.value = taskResponse.data.filter(
      (task: Task) => task.project === projectId
    )
  } catch (error) {
    console.error('Failed to load project:', error)
    errorMessage.value = 'Failed to load project data.'
  } finally {
    isLoading.value = false
  }
}

// Create a new task
async function createTask() {
  if (!newTaskTitle.value.trim()) {
    errorMessage.value = 'Task title cannot be empty.'
    return
  }

  isSaving.value = true
  errorMessage.value = ''

  try {
    await api.post('/tasks/', {
      title: newTaskTitle.value.trim(),
      description: newTaskDescription.value.trim(),
      project: projectId,
      is_completed: false
    })

    newTaskTitle.value = ''
    newTaskDescription.value = ''

    await fetchData()

    successMessage.value = 'Task created successfully!'
  } catch (error) {
    console.error('Failed to create task:', error)
    errorMessage.value = 'Failed to create task.'
  } finally {
    isSaving.value = false
  }
}

// Toggle task completion
async function toggleTask(task: Task) {
  const previousStatus = task.is_completed

  // Update the UI immediately
  task.is_completed = !previousStatus

  try {
    await api.patch(`/tasks/${task.id}/`, {
      is_completed: task.is_completed
    })
  } catch (error) {
    console.error('Failed to update task:', error)

    // Restore the previous status if the request fails
    task.is_completed = previousStatus
    errorMessage.value = 'Failed to update task status.'
  }
}

// Delete a task
async function deleteTask(taskId: number) {
  const confirmed = window.confirm(
    'Are you sure you want to delete this task?'
  )

  if (!confirmed) return

  errorMessage.value = ''

  try {
    await api.delete(`/tasks/${taskId}/`)

    tasks.value = tasks.value.filter(task => task.id !== taskId)

    successMessage.value = 'Task deleted successfully!'
  } catch (error) {
    console.error('Failed to delete task:', error)
    errorMessage.value = 'Failed to delete task.'
  }
}

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'

  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="detail-page">

    <!-- Back button -->
    <button class="back-button" @click="router.push('/projects')">
      ← Back to Projects
    </button>

    <!-- Loading -->
    <div v-if="isLoading" class="loading-state">
      Loading project...
    </div>

    <template v-else-if="project">

      <!-- Project Header -->
      <div class="project-header">
        <div>
          <div class="project-label">PROJECT #{{ project.id }}</div>
          <h1>{{ project.name }}</h1>
          <p class="project-description">
            {{ project.description || 'No description provided.' }}
          </p>
        </div>
      </div>

      <!-- Progress Card -->
      <div class="progress-card">
        <div class="progress-heading">
          <div>
            <h2>Project Progress</h2>
            <p>{{ completedTasks }} of {{ totalTasks }} tasks completed</p>
          </div>

          <strong class="progress-number">{{ progress }}%</strong>
        </div>

        <div class="progress-track">
          <div
            class="progress-fill"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <!-- Messages -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Create Task -->
      <div class="content-card">
        <div class="section-heading">
          <div>
            <h2>Add a New Task</h2>
            <p>Create a task for this project.</p>
          </div>
        </div>

        <form class="task-form" @submit.prevent="createTask">
          <div class="form-group">
            <label for="task-title">Task Title</label>
            <input
              id="task-title"
              v-model="newTaskTitle"
              type="text"
              placeholder="What needs to be done?"
            />
          </div>

          <div class="form-group">
            <label for="task-description">Description</label>
            <textarea
              id="task-description"
              v-model="newTaskDescription"
              rows="2"
              placeholder="Optional task description..."
            ></textarea>
          </div>

          <button
            type="submit"
            class="primary-button"
            :disabled="isSaving"
          >
            {{ isSaving ? 'Creating...' : '+ Create Task' }}
          </button>
        </form>
      </div>

      <!-- Task List -->
      <div class="content-card">
        <div class="section-heading">
          <div>
            <h2>Tasks</h2>
            <p>Manage the tasks in this project.</p>
          </div>

          <span class="task-count">{{ totalTasks }} Tasks</span>
        </div>

        <div v-if="tasks.length === 0" class="empty-state">
          <div class="empty-icon">✓</div>
          <h3>No tasks yet</h3>
          <p>Create your first task to get started.</p>
        </div>

        <div v-else class="task-list">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="task-item"
            :class="{ completed: task.is_completed }"
          >
            <label class="task-checkbox">
              <input
                type="checkbox"
                :checked="task.is_completed"
                @change="toggleTask(task)"
              />

              <span class="custom-checkbox"></span>
            </label>

            <div class="task-content">
              <h3>{{ task.title }}</h3>

              <p v-if="task.description">
                {{ task.description }}
              </p>

              <span class="task-date">
                Created {{ formatDate(task.created_at) }}
              </span>
            </div>

            <span
              class="task-status"
              :class="task.is_completed ? 'status-completed' : 'status-active'"
            >
              {{ task.is_completed ? 'Completed' : 'In Progress' }}
            </span>

            <button
              class="delete-button"
              title="Delete task"
              @click="deleteTask(task.id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

    </template>

    <div v-else-if="!isLoading" class="empty-state">
      <h2>Project not found</h2>
      <p>Unable to find this project.</p>
    </div>

  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  padding: 40px;
  background: #f7f8fc;
  color: #25283b;
  font-family: Arial, sans-serif;
}

.back-button {
  margin-bottom: 28px;
  padding: 8px 0;
  border: none;
  background: transparent;
  color: #7568dc;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.project-header {
  margin-bottom: 28px;
}

.project-label {
  margin-bottom: 10px;
  color: #7568dc;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
}

.project-header h1 {
  margin: 0;
  font-size: 28px;
}

.project-description {
  margin-top: 10px;
  color: #85899b;
  font-size: 14px;
}

.progress-card,
.content-card {
  margin-bottom: 24px;
  padding: 25px;
  border: 1px solid #eaebf1;
  border-radius: 14px;
  background: white;
}

.progress-heading,
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.progress-heading h2,
.section-heading h2 {
  margin: 0;
  font-size: 18px;
}

.progress-heading p,
.section-heading p {
  margin: 7px 0 0;
  color: #9295a4;
  font-size: 13px;
}

.progress-number {
  color: #6255cf;
  font-size: 25px;
}

.progress-track {
  height: 10px;
  margin-top: 22px;
  overflow: hidden;
  border-radius: 10px;
  background: #efeff4;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  background: #7568dc;
  transition: width 0.3s ease;
}

.task-form {
  margin-top: 22px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  color: #44475a;
  font-size: 13px;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  box-sizing: border-box;
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #e2e3eb;
  border-radius: 8px;
  outline: none;
  color: #25283b;
  font-family: inherit;
  font-size: 14px;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #7568dc;
  box-shadow: 0 0 0 3px rgba(117, 104, 220, 0.12);
}

.form-group textarea {
  resize: vertical;
}

.primary-button {
  padding: 11px 18px;
  border: none;
  border-radius: 8px;
  background: #685bd2;
  color: white;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.primary-button:hover {
  background: #5548bd;
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.task-count {
  padding: 8px 13px;
  border-radius: 20px;
  background: #eeedff;
  color: #6255cf;
  font-size: 12px;
  font-weight: 600;
}

.task-list {
  margin-top: 20px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 0;
  border-bottom: 1px solid #f0f0f4;
}

.task-item:last-child {
  border-bottom: none;
}

.task-checkbox {
  position: relative;
  display: flex;
  flex-shrink: 0;
  align-items: center;
  cursor: pointer;
}

.task-checkbox input {
  position: absolute;
  width: 20px;
  height: 20px;
  opacity: 0;
  cursor: pointer;
}

.custom-checkbox {
  width: 19px;
  height: 19px;
  border: 2px solid #d4d5e0;
  border-radius: 6px;
  background: white;
}

.task-checkbox input:checked + .custom-checkbox {
  border-color: #7568dc;
  background: #7568dc;
}

.task-checkbox input:checked + .custom-checkbox::after {
  display: block;
  width: 5px;
  height: 9px;
  margin: 2px 0 0 6px;
  border: solid white;
  border-width: 0 2px 2px 0;
  content: '';
  transform: rotate(45deg);
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-content h3 {
  margin: 0;
  font-size: 14px;
}

.task-content p {
  margin: 6px 0;
  color: #85899b;
  font-size: 13px;
}

.task-date {
  display: block;
  margin-top: 7px;
  color: #a0a2ae;
  font-size: 11px;
}

.task-item.completed .task-content h3 {
  color: #a0a2ae;
  text-decoration: line-through;
}

.task-status {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 600;
}

.status-completed {
  color: #29945a;
}

.status-active {
  color: #85899b;
}

.delete-button {
  padding: 7px 10px;
  border: 1px solid #f0dede;
  border-radius: 7px;
  background: white;
  color: #c45c5c;
  cursor: pointer;
  font-size: 12px;
}

.delete-button:hover {
  background: #fff3f3;
}

.empty-state {
  padding: 45px 20px;
  text-align: center;
  color: #9295a4;
}

.empty-state h3 {
  color: #25283b;
}

.empty-icon {
  font-size: 30px;
  color: #7568dc;
}

.loading-state {
  padding: 60px;
  text-align: center;
  color: #85899b;
}

.success-message,
.error-message {
  margin-bottom: 20px;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 13px;
}

.success-message {
  background: #eaf8ef;
  color: #267747;
}

.error-message {
  background: #fff0f0;
  color: #c03939;
}

@media (max-width: 650px) {
  .detail-page {
    padding: 22px 16px;
  }

  .task-item {
    flex-wrap: wrap;
  }

  .task-status {
    margin-left: 35px;
  }
}
</style>
