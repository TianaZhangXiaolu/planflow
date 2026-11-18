
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

// Data structures
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

// Router
const router = useRouter()

function openProject(projectId: number) {
  router.push(`/projects/${projectId}`)
}

// State
const projects = ref<Project[]>([])
const tasks = ref<Task[]>([])

const editingProject = ref<Project | null>(null)
const editName = ref('')
const editDescription = ref('')

const isSaving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Fetch Projects and Tasks
async function fetchProjects() {
  try {
    const [projectResponse, taskResponse] = await Promise.all([
      api.get('/projects/'),
      api.get('/tasks/')
    ])

    projects.value = projectResponse.data
    tasks.value = taskResponse.data

    errorMessage.value = ''
  } catch (error) {
    console.error('Failed to fetch projects and tasks:', error)
    errorMessage.value = 'Failed to load project data.'
  }
}

// Calculate progress for each project
const projectProgress = computed(() => {
  return projects.value.map(project => {
    const projectTasks = tasks.value.filter(
      task => task.project === project.id
    )

    const completedTasks = projectTasks.filter(
      task => task.is_completed
    ).length

    const totalTasks = projectTasks.length

    const progress = totalTasks === 0
      ? 0
      : Math.round((completedTasks / totalTasks) * 100)

    return {
      ...project,
      totalTasks,
      completedTasks,
      progress
    }
  })
})

// Open edit modal
function handleEdit(project: Project) {
  editingProject.value = project
  editName.value = project.name
  editDescription.value = project.description || ''

  errorMessage.value = ''
  successMessage.value = ''
}

// Close modal
function closeModal() {
  if (isSaving.value) return

  editingProject.value = null
  editName.value = ''
  editDescription.value = ''
  errorMessage.value = ''
}

// Save project changes
async function saveProject() {
  if (!editingProject.value) return

  if (!editName.value.trim()) {
    errorMessage.value = 'Project name cannot be empty.'
    return
  }

  isSaving.value = true
  errorMessage.value = ''

  try {
    await api.patch(`/projects/${editingProject.value.id}/`, {
      name: editName.value.trim(),
      description: editDescription.value.trim()
    })

    await fetchProjects()

    editingProject.value = null
    successMessage.value = 'Project updated successfully!'
  } catch (error) {
    console.error('Failed to update project:', error)
    errorMessage.value = 'Failed to update project. Please try again.'
  } finally {
    isSaving.value = false
  }
}

// Format date
function formatDate(dateString: string) {
  if (!dateString) return 'N/A'

  return new Date(dateString).toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Load projects when the page is mounted
onMounted(() => {
  fetchProjects()
})
</script>

<template>
  <div class="projects-page">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>My Projects</h1>
        <p>Manage and organize your projects.</p>
      </div>

      <div class="project-count">
        {{ projects.length }} Projects
      </div>
    </div>

    <!-- Success and Error Messages -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Project List -->
    <div v-if="projectProgress.length > 0" class="project-grid">

      <div
        v-for="project in projectProgress"
        :key="project.id"
        class="project-card"
        @click="openProject(project.id)"
      >
        <div class="card-top">
          <div class="project-icon">
            {{ project.name.charAt(0).toUpperCase() }}
          </div>

          <button
            class="edit-button"
            @click.stop="handleEdit(project)"
          >
            ✎ Edit
          </button>
        </div>

        <h2>{{ project.name }}</h2>

        <p class="project-description">
          {{ project.description || 'No description provided.' }}
        </p>

        <!-- Task Progress -->
        <div class="progress-info">
          <span>Task Progress</span>
          <strong>{{ project.progress }}%</strong>
        </div>

        <div class="progress-track">
          <div
            class="progress-fill"
            :style="{ width: `${project.progress}%` }"
          ></div>
        </div>

        <div class="task-info">
          {{ project.completedTasks }} / {{ project.totalTasks }}
          Tasks completed
        </div>

        <div class="card-footer">
          <span>Created</span>
          <span>{{ formatDate(project.created_at) }}</span>
        </div>

      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">📁</div>
      <h2>No projects yet</h2>
      <p>Create your first project to get started.</p>
    </div>

    <!-- Edit Project Modal -->
    <div
      v-if="editingProject"
      class="modal-overlay"
      @click.self="closeModal"
    >
      <div class="modal-content" role="dialog" aria-modal="true">

        <!-- Modal Header -->
        <div class="modal-header">
          <div>
            <h2>Edit Project</h2>
            <p>Update your project information.</p>
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

        <!-- Project ID -->
        <div class="form-group">
          <label>Project ID</label>
          <div class="readonly-field">
            #{{ editingProject.id }}
          </div>
        </div>

        <!-- Project Name -->
        <div class="form-group">
          <label for="project-name">Project Name</label>
          <input
            id="project-name"
            v-model="editName"
            type="text"
            placeholder="Enter project name"
          />
        </div>

        <!-- Project Description -->
        <div class="form-group">
          <label for="project-description">Description</label>
          <textarea
            id="project-description"
            v-model="editDescription"
            placeholder="Describe your project..."
            rows="4"
          ></textarea>
        </div>

        <!-- Created At -->
        <div class="form-group">
          <label>Created At</label>
          <div class="readonly-field">
            {{ formatDate(editingProject.created_at) }}
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button
            class="cancel-button"
            @click="closeModal"
            :disabled="isSaving"
          >
            Cancel
          </button>

          <button
            class="save-button"
            @click="saveProject"
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
.projects-page {
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
}

.page-header p {
  margin-top: 8px;
  color: #85899b;
  font-size: 14px;
}

.project-count {
  padding: 9px 16px;
  border-radius: 20px;
  background: #eeedff;
  color: #6255cf;
  font-size: 13px;
  font-weight: 600;
}

/* Project Cards */
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 22px;
}

.project-card {
  padding: 24px;
  border: 1px solid #eaebf1;
  border-radius: 14px;
  background: white;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(30, 35, 90, 0.07);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #eeedff;
  color: #6255cf;
  font-size: 18px;
  font-weight: 700;
}

.edit-button {
  padding: 7px 12px;
  border: 1px solid #e4e3f3;
  border-radius: 7px;
  background: white;
  color: #6255cf;
  cursor: pointer;
  font-size: 13px;
}

.edit-button:hover {
  background: #f4f3ff;
}

.project-card h2 {
  margin: 0 0 10px;
  font-size: 18px;
}

.project-description {
  min-height: 40px;
  color: #85899b;
  font-size: 14px;
  line-height: 1.6;
}

/* Progress */
.progress-info {
  display: flex;
  justify-content: space-between;
  margin: 22px 0 9px;
  color: #85899b;
  font-size: 12px;
}

.progress-info strong {
  color: #6255cf;
}

.progress-track {
  height: 8px;
  overflow: hidden;
  border-radius: 10px;
  background: #efeff4;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  background: #7568dc;
  transition: width 0.4s ease;
}

.task-info {
  margin-top: 9px;
  color: #9699a8;
  font-size: 11px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 22px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f4;
  color: #9699a8;
  font-size: 11px;
}

/* Empty State */
.empty-state {
  padding: 80px 20px;
  text-align: center;
  color: #85899b;
}

.empty-icon {
  margin-bottom: 15px;
  font-size: 40px;
}

.empty-state h2 {
  color: #25283b;
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
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
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

.form-group input,
.form-group textarea {
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
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #7568dc;
  box-shadow: 0 0 0 3px rgba(117, 104, 220, 0.12);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.readonly-field {
  padding: 12px 14px;
  border: 1px solid #eaebf1;
  border-radius: 8px;
  background: #f7f8fc;
  color: #85899b;
  font-size: 14px;
}

/* Modal Footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #eeeef3;
}

.cancel-button,
.save-button {
  padding: 11px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.cancel-button {
  border: 1px solid #e2e3eb;
  background: white;
  color: #66697a;
}

.cancel-button:hover {
  background: #f7f8fc;
}

.save-button {
  border: none;
  background: #685bd2;
  color: white;
}

.save-button:hover {
  background: #5548bd;
}

.cancel-button:disabled,
.save-button:disabled,
.close-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* Responsive */
@media (max-width: 600px) {
  .projects-page {
    padding: 22px 16px;
  }

  .page-header {
    align-items: flex-start;
    gap: 15px;
  }

  .modal-content {
    padding: 22px;
  }
}
</style>
