
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

// ---------- Types ----------

interface Project {
  id: number
  name: string
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

// ---------- State ----------

const projects = ref<Project[]>([])
const tasks = ref<Task[]>([])

const searchQuery = ref('')
const activeFilter = ref<'all' | 'active' | 'completed'>('all')

const isLoading = ref(true)
const isSaving = ref(false)

const errorMessage = ref('')
const successMessage = ref('')

// Create Task
const newTitle = ref('')
const newDescription = ref('')
const newProjectId = ref<number | null>(null)

// Edit Task
const editingTask = ref<Task | null>(null)
const editTitle = ref('')
const editDescription = ref('')
const editProjectId = ref<number | null>(null)

// ---------- Computed Statistics ----------

const totalTasks = computed(() => tasks.value.length)

const completedTasks = computed(() =>
  tasks.value.filter(task => task.is_completed).length
)

const activeTasks = computed(() =>
  totalTasks.value - completedTasks.value
)

const completionRate = computed(() => {
  if (totalTasks.value === 0) return 0

  return Math.round(
    (completedTasks.value / totalTasks.value) * 100
  )
})

// ---------- Project Name ----------

function getProjectName(projectId: number) {
  const project = projects.value.find(
    project => project.id === projectId
  )

  return project?.name || 'Unknown Project'
}

// ---------- Filter Tasks ----------

const filteredTasks = computed(() => {
  let result = tasks.value

  if (activeFilter.value === 'active') {
    result = result.filter(task => !task.is_completed)
  } else if (activeFilter.value === 'completed') {
    result = result.filter(task => task.is_completed)
  }

  const keyword = searchQuery.value.trim().toLowerCase()

  if (keyword) {
    result = result.filter(task =>
      task.title.toLowerCase().includes(keyword) ||
      (task.description || '').toLowerCase().includes(keyword) ||
      getProjectName(task.project).toLowerCase().includes(keyword)
    )
  }

  return result
})

// ---------- Fetch Data ----------

async function fetchData() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const [projectResponse, taskResponse] = await Promise.all([
      api.get('/projects/'),
      api.get('/tasks/')
    ])

    projects.value = projectResponse.data
    tasks.value = taskResponse.data

  } catch (error) {
    console.error('Failed to fetch tasks:', error)
    errorMessage.value = 'Failed to load tasks. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// ---------- Create Task ----------

async function createTask() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!newTitle.value.trim()) {
    errorMessage.value = 'Task title is required.'
    return
  }

  if (newProjectId.value === null) {
    errorMessage.value = 'Please select a project.'
    return
  }

  isSaving.value = true

  try {
    await api.post('/tasks/', {
      title: newTitle.value.trim(),
      description: newDescription.value.trim(),
      project: newProjectId.value,
      is_completed: false
    })

    newTitle.value = ''
    newDescription.value = ''
    newProjectId.value = null

    await fetchData()

    successMessage.value = 'Task created successfully!'

  } catch (error) {
    console.error('Failed to create task:', error)
    errorMessage.value = 'Failed to create task.'
  } finally {
    isSaving.value = false
  }
}

// ---------- Toggle Task Completion ----------

async function toggleTask(task: Task) {
  errorMessage.value = ''
  successMessage.value = ''

  const previousStatus = task.is_completed

  // Update the UI immediately
  task.is_completed = !previousStatus

  try {
    await api.patch(`/tasks/${task.id}/`, {
      is_completed: task.is_completed
    })
  } catch (error) {
    console.error('Failed to update task:', error)

    // Restore previous status if request fails
    task.is_completed = previousStatus
    errorMessage.value = 'Failed to update task status.'
  }
}

// ---------- Open Edit Modal ----------

function handleEdit(task: Task) {
  editingTask.value = task

  editTitle.value = task.title
  editDescription.value = task.description || ''
  editProjectId.value = task.project

  errorMessage.value = ''
  successMessage.value = ''
}

// ---------- Close Edit Modal ----------

function closeModal() {
  if (isSaving.value) return

  editingTask.value = null
  editTitle.value = ''
  editDescription.value = ''
  editProjectId.value = null
  errorMessage.value = ''
}

// ---------- Save Task Changes ----------

async function saveTask() {
  if (!editingTask.value) return

  errorMessage.value = ''

  if (!editTitle.value.trim()) {
    errorMessage.value = 'Task title cannot be empty.'
    return
  }

  if (editProjectId.value === null) {
    errorMessage.value = 'Please select a project.'
    return
  }

  isSaving.value = true

  try {
    await api.patch(`/tasks/${editingTask.value.id}/`, {
      title: editTitle.value.trim(),
      description: editDescription.value.trim(),
      project: editProjectId.value
    })

    await fetchData()

    editingTask.value = null
    successMessage.value = 'Task updated successfully!'

  } catch (error) {
    console.error('Failed to update task:', error)
    errorMessage.value = 'Failed to update task.'
  } finally {
    isSaving.value = false
  }
}

// ---------- Delete Task ----------

async function deleteTask(task: Task) {
  const confirmed = window.confirm(
    `Are you sure you want to delete "${task.title}"?`
  )

  if (!confirmed) return

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await api.delete(`/tasks/${task.id}/`)

    await fetchData()

    successMessage.value = 'Task deleted successfully!'

  } catch (error) {
    console.error('Failed to delete task:', error)
    errorMessage.value = 'Failed to delete task.'
  }
}

// ---------- Date Formatting ----------

function formatDate(dateString: string) {
  if (!dateString) return 'N/A'

  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

// ---------- Lifecycle ----------

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="tasks-page">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>My Tasks</h1>
        <p>Organize your work and keep track of your progress.</p>
      </div>

      <div class="task-count">
        {{ totalTasks }} Tasks
      </div>
    </div>

    <!-- Messages -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="isLoading" class="loading">
      Loading tasks...
    </div>

    <template v-else>

      <!-- Statistics -->
      <section class="stats-grid">

        <div class="stat-card">
          <div class="stat-icon purple">☷</div>
          <p>Total Tasks</p>
          <h2>{{ totalTasks }}</h2>
          <span>All your tasks</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon orange">◷</div>
          <p>Active Tasks</p>
          <h2>{{ activeTasks }}</h2>
          <span>Tasks to be completed</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon green">✓</div>
          <p>Completed Tasks</p>
          <h2>{{ completedTasks }}</h2>
          <span>Successfully completed</span>
        </div>

        <div class="stat-card">
          <div class="stat-icon blue">%</div>
          <p>Completion Rate</p>
          <h2>{{ completionRate }}%</h2>
          <span>Overall task progress</span>
        </div>

      </section>

      <!-- Create Task -->
      <section class="panel create-panel">

        <div class="section-heading">
          <div>
            <h2>Create a Task</h2>
            <p>Add a new task to one of your projects.</p>
          </div>
        </div>

        <form @submit.prevent="createTask">

          <div class="form-grid">

            <div class="form-group">
              <label for="task-title">Task Title</label>
              <input
                id="task-title"
                v-model="newTitle"
                type="text"
                placeholder="e.g. Implement login page"
              />
            </div>

            <div class="form-group">
              <label for="task-project">Project</label>
              <select
                id="task-project"
                v-model="newProjectId"
              >
                <option :value="null" disabled>
                  Select a project
                </option>

                <option
                  v-for="project in projects"
                  :key="project.id"
                  :value="project.id"
                >
                  {{ project.name }}
                </option>
              </select>
            </div>

          </div>

          <div class="form-group">
            <label for="task-description">Description</label>
            <textarea
              id="task-description"
              v-model="newDescription"
              rows="3"
              placeholder="Describe what needs to be done..."
            ></textarea>
          </div>

          <button
            type="submit"
            class="primary-button"
            :disabled="isSaving || projects.length === 0"
          >
            {{ isSaving ? 'Creating...' : '+ Create Task' }}
          </button>

          <p v-if="projects.length === 0" class="helper-text">
            You need to create a project before adding tasks.
          </p>

        </form>

      </section>

      <!-- Task List -->
      <section class="task-section">

        <div class="task-heading">
          <div>
            <h2>All Tasks</h2>
            <p>Manage and monitor your tasks.</p>
          </div>

          <div class="search-box">
            <span>⌕</span>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search tasks..."
            />
          </div>
        </div>

        <!-- Filters -->
        <div class="filter-tabs">

          <button
            :class="{ active: activeFilter === 'all' }"
            @click="activeFilter = 'all'"
          >
            All
            <span>{{ totalTasks }}</span>
          </button>

          <button
            :class="{ active: activeFilter === 'active' }"
            @click="activeFilter = 'active'"
          >
            Active
            <span>{{ activeTasks }}</span>
          </button>

          <button
            :class="{ active: activeFilter === 'completed' }"
            @click="activeFilter = 'completed'"
          >
            Completed
            <span>{{ completedTasks }}</span>
          </button>

        </div>

        <!-- Task List -->
        <div v-if="filteredTasks.length > 0" class="task-list">

          <article
            v-for="task in filteredTasks"
            :key="task.id"
            class="task-card"
            :class="{ 'task-completed': task.is_completed }"
          >

            <div class="task-main">

              <input
                type="checkbox"
                class="task-checkbox"
                :checked="task.is_completed"
                @change="toggleTask(task)"
                :aria-label="`Mark ${task.title} as completed`"
              />

              <div class="task-content">
                <h3>{{ task.title }}</h3>

                <p>
                  {{ task.description || 'No description provided.' }}
                </p>

                <div class="task-meta">
                  <span class="project-label">
                    {{ getProjectName(task.project) }}
                  </span>

                  <span>
                    Created {{ formatDate(task.created_at) }}
                  </span>
                </div>
              </div>

            </div>

            <div class="task-actions">

              <span
                class="status-label"
                :class="{ completed: task.is_completed }"
              >
                {{ task.is_completed ? 'Completed' : 'Active' }}
              </span>

              <button
                class="action-button"
                @click="handleEdit(task)"
                aria-label="Edit task"
              >
                Edit
              </button>

              <button
                class="delete-button"
                @click="deleteTask(task)"
                aria-label="Delete task"
              >
                Delete
              </button>

            </div>

          </article>

        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">☷</div>

          <h3>
            {{ searchQuery ? 'No tasks found' : 'No tasks here yet' }}
          </h3>

          <p>
            {{
              searchQuery
                ? 'Try another search keyword.'
                : 'Create your first task to get started.'
            }}
          </p>
        </div>

      </section>

    </template>

    <!-- Edit Task Modal -->
    <div
      v-if="editingTask"
      class="modal-overlay"
      @click.self="closeModal"
    >
      <div
        class="modal-content"
        role="dialog"
        aria-modal="true"
        aria-labelledby="edit-title"
      >

        <div class="modal-header">
          <div>
            <h2 id="edit-title">Edit Task</h2>
            <p>Update your task information.</p>
          </div>

          <button
            class="close-button"
            @click="closeModal"
            :disabled="isSaving"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div class="form-group">
          <label>Task ID</label>
          <div class="readonly-field">
            #{{ editingTask.id }}
          </div>
        </div>

        <div class="form-group">
          <label for="edit-task-title">Task Title</label>
          <input
            id="edit-task-title"
            v-model="editTitle"
            type="text"
            placeholder="Enter task title"
          />
        </div>

        <div class="form-group">
          <label for="edit-task-description">Description</label>
          <textarea
            id="edit-task-description"
            v-model="editDescription"
            rows="4"
            placeholder="Describe your task..."
          ></textarea>
        </div>

        <div class="form-group">
          <label for="edit-task-project">Project</label>
          <select
            id="edit-task-project"
            v-model="editProjectId"
          >
            <option
              v-for="project in projects"
              :key="project.id"
              :value="project.id"
            >
              {{ project.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Status</label>
          <div class="readonly-field">
            {{ editingTask.is_completed ? 'Completed' : 'Active' }}
          </div>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="modal-footer">
          <button
            class="cancel-button"
            @click="closeModal"
            :disabled="isSaving"
          >
            Cancel
          </button>

          <button
            class="primary-button"
            @click="saveTask"
            :disabled="isSaving"
          >
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<style scoped>
/* Page */
.tasks-page {
  min-height: 100vh;
  padding: 40px;
  background: #f7f8fc;
  color: #25283b;
  font-family: Arial, sans-serif;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.page-header p {
  margin-top: 8px;
  color: #85899b;
  font-size: 14px;
}

.task-count {
  padding: 9px 16px;
  border-radius: 20px;
  background: #eeedff;
  color: #6255cf;
  font-size: 13px;
  font-weight: 600;
}

/* Messages */
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
  font-size: 19px;
  font-weight: 700;
}

.purple {
  background: #efedff;
  color: #7568dc;
}

.orange {
  background: #fff3e6;
  color: #df9943;
}

.green {
  background: #e9f7ef;
  color: #35a879;
}

.blue {
  background: #e9f2ff;
  color: #4985d5;
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
.panel {
  padding: 24px;
  border: 1px solid #ededf3;
  border-radius: 13px;
  background: white;
}

.create-panel {
  margin-bottom: 35px;
}

.section-heading h2,
.task-heading h2 {
  margin: 0;
  font-size: 17px;
}

.section-heading p,
.task-heading p {
  margin: 7px 0 0;
  color: #9699a8;
  font-size: 12px;
}

/* Form */
.create-panel form {
  margin-top: 23px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

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

.form-group input,
.form-group textarea,
.form-group select {
  box-sizing: border-box;
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #e2e3eb;
  border-radius: 8px;
  outline: none;
  background: white;
  color: #25283b;
  font-family: inherit;
  font-size: 13px;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #7568dc;
  box-shadow: 0 0 0 3px rgba(117, 104, 220, 0.1);
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

.helper-text {
  margin-top: 10px;
  color: #9699a8;
  font-size: 11px;
}

/* Task Section */
.task-section {
  margin-bottom: 30px;
}

.task-heading {
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

/* Filters */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}

.filter-tabs button {
  padding: 8px 13px;
  border: 1px solid #e8e8ef;
  border-radius: 8px;
  background: white;
  color: #85899b;
  cursor: pointer;
  font-size: 12px;
}

.filter-tabs button.active {
  border-color: #7568dc;
  background: #eeedff;
  color: #6255cf;
  font-weight: 600;
}

.filter-tabs button span {
  margin-left: 5px;
}

/* Task Cards */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border: 1px solid #ededf3;
  border-radius: 12px;
  background: white;
  transition: box-shadow 0.2s;
}

.task-card:hover {
  box-shadow: 0 5px 18px rgba(30, 35, 90, 0.05);
}

.task-main {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  min-width: 0;
  flex: 1;
}

.task-checkbox {
  width: 18px;
  height: 18px;
  margin-top: 3px;
  accent-color: #7568dc;
  cursor: pointer;
}

.task-content {
  min-width: 0;
}

.task-content h3 {
  overflow-wrap: anywhere;
  margin: 0 0 7px;
  font-size: 14px;
}

.task-content p {
  overflow-wrap: anywhere;
  margin: 0 0 12px;
  color: #9699a8;
  font-size: 12px;
  line-height: 1.5;
}

.task-completed .task-content h3 {
  color: #9699a8;
  text-decoration: line-through;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #a0a2af;
  font-size: 10px;
}

.project-label {
  color: #6255cf;
  font-weight: 600;
}

.task-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
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

.action-button,
.delete-button {
  padding: 7px 11px;
  border: 1px solid #e4e3f3;
  border-radius: 7px;
  background: white;
  color: #6255cf;
  cursor: pointer;
  font-size: 11px;
}

.action-button:hover {
  background: #f4f3ff;
}

.delete-button {
  border-color: #f2dddd;
  color: #c03939;
}

.delete-button:hover {
  background: #fff0f0;
}

/* Empty State */
.empty-state {
  padding: 65px 20px;
  border: 1px dashed #dedee9;
  border-radius: 12px;
  background: white;
  text-align: center;
}

.empty-icon {
  color: #7568dc;
  font-size: 35px;
}

.empty-state h3 {
  margin: 14px 0 7px;
  font-size: 15px;
}

.empty-state p {
  color: #9699a8;
  font-size: 12px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(25, 28, 50, 0.55);
  backdrop-filter: blur(4px);
}

.modal-content {
  box-sizing: border-box;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.2s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 25px;
}

.modal-header h2 {
  margin: 0;
  font-size: 22px;
}

.modal-header p {
  margin-top: 7px;
  color: #9295a4;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  color: #85899b;
  cursor: pointer;
  font-size: 28px;
  line-height: 1;
}

.readonly-field {
  padding: 12px 14px;
  border: 1px solid #eaebf1;
  border-radius: 8px;
  background: #f7f8fc;
  color: #85899b;
  font-size: 13px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eeeef3;
}

.cancel-button {
  padding: 11px 18px;
  border: 1px solid #e2e3eb;
  border-radius: 8px;
  background: white;
  color: #66697a;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.cancel-button:hover {
  background: #f7f8fc;
}

.cancel-button:disabled,
.close-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 1000px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .tasks-page {
    padding: 24px 16px;
  }

  .page-header {
    align-items: flex-start;
    gap: 15px;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .task-heading {
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

  .task-card {
    align-items: flex-start;
    flex-direction: column;
  }

  .task-actions {
    padding-left: 33px;
  }

  .modal-content {
    padding: 22px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .stat-card {
    padding: 15px;
  }

  .filter-tabs {
    flex-wrap: wrap;
  }
}
</style>
