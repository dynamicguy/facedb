<script lang="ts" setup>
import { useAuthStore } from '@/stores/auth'
import type { User } from '~/types'

const autStore = useAuthStore()
const route = useRoute()

const UButton = resolveComponent('UButton')
const UIcon = resolveComponent('UIcon')

const { data, status } = useLazyFetch<User>('/backend/users/' + route.params.id, {
  key: 'user-detail',
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  }
})
</script>

<template>
  <UDashboardPanel id="user-details">
    <template #header>
      <UDashboardNavbar title="User Details">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
           <UButton
            label="Back to users"
            to="/users"
            icon="i-lucide-arrow-left"
            color="neutral"
          />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <UPageCard>
        <template #body>
          <div v-if="data" class="space-y-4">
            <h3 class="text-lg font-semibold">
              {{ data.full_name }}
            </h3>
            <p>
              <strong>Username:</strong> {{ data.username }}
            </p>
            <p>
              <strong>Email:</strong> {{ data.email }}
            </p>
            <p>
              <strong>Role:</strong> {{ data.role }}
            </p>
            <p>
              <strong>Status:</strong> {{ data.disabled ? 'Disabled' : 'Active' }}
            </p>
          </div>
          <div v-else-if="status === 'pending'" class="text-center py-4">
            <UIcon name="i-lucide-loader-2" class="animate-spin mx-auto" />
            <p class="mt-2">
              Loading user details...
            </p>
          </div>
          <div v-else class="text-center py-4 text-red-500">
            <UIcon name="i-lucide-alert-circle" class="mx-auto mb-2" />
            Failed to load user details.
          </div>
        </template>
        <template #footer>
          <div class="flex items-center gap-3">
            <UButton label="Edit user" color="neutral" icon="i-lucide-pencil" size="sm" :to="`/users/${route.params.id}/edit`" />
            <UButton label="Delete user" color="error" icon="i-lucide-trash-2" size="sm" />
          </div>
        </template>
      </UPageCard>
    </template>
  </UDashboardPanel>
</template>
