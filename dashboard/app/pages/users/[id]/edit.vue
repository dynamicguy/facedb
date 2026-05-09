<script lang="ts" setup>
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

import { useAuthStore } from '@/stores/auth'
import type { User } from '~/types'

const autStore = useAuthStore()
const route = useRoute()
const toast = useToast()

const UButton = resolveComponent('UButton')

const { data, status } = await useFetch<User>('/backend/users/' + route.params.id, {
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  }
})

const roles = ['admin', 'user']

const schema = z.object({
  full_name: z.string('Full name is required').min(2, 'Must be at least 2 characters'),
  username: z.string('Username is required').min(8, 'Must be at least 8 characters'),
  email: z.string('Email is required').email('Must be a valid email address'),
  role: z.enum(roles),
  disabled: z.boolean('Disabled')
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  full_name: data.value?.full_name,
  username: data.value?.username,
  email: data.value?.email,
  role: data.value?.role,
  disabled: data.value?.disabled
})

async function onSubmit(event: FormSubmitEvent<Schema>) {
  console.log(event.data)
  await $fetch('/backend/users/' + route.params.id, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${autStore.token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(event.data)
  })
  toast.add({ title: 'Success', description: 'User updated successfully.', color: 'success' })
  navigateTo(`/users`)
}
</script>

<template>
  <UDashboardPanel id="edit-user-details">
    <template #header>
      <UDashboardNavbar title="Edit User">
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
      <UCard>
        <UForm
          :schema="schema"
          :state="state"
          class="space-y-4"
          @submit="onSubmit"
        >
          <UFormField label="Full Name" name="full_name" class="w-full">
            <UInput v-model="state.full_name" class="w-full" />
          </UFormField>
          
          <UFormField label="Username" name="username" class="w-full">
            <UInput v-model="state.username" class="w-full" />
          </UFormField>

          <UFormField label="Email" name="email" class="w-full">
            <UInput v-model="state.email" class="w-full" />
          </UFormField>

          <UFormField label="Role" name="role">
            <USelect v-model="state.role" :items="roles" class="w-48" />
          </UFormField>

          <UFormField label="Disabled" name="disabled">
            <UCheckbox v-model="state.disabled" />
          </UFormField>

          <UButton type="submit" icon="i-lucide-save">
            Submit
          </UButton>
        </UForm>
      </UCard>
    </template>
  </UDashboardPanel>
</template>
