<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

import type { Suspect } from '~/types'
import { useAuthStore } from '@/stores/auth'

// definePageMeta({
//   middleware: 'auth'
// })

const autStore = useAuthStore()
const route = useRoute()

const { data, status } = await useFetch<Suspect>('/backend/items/' + route.params.id, {
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  }
})

const genders = ['Man', 'Woman']
const districts = ['Dhaka', 'Chittagong', 'Khulna', 'Rajshahi', 'Barisal', 'Sylhet', 'Rangpur', 'Mymensingh', 'Bogra', 'Comilla', 'Narayanganj', 'Gazipur', 'Tangail', 'Faridpur', 'Kishoreganj', 'Munshiganj', 'Shariatpur']

const schema = z.object({
  name: z.string('Name is required').min(2, 'Must be at least 2 characters'),
  description: z.string('Description is required').min(8, 'Must be at least 8 characters'),
  gender: z.enum(genders),
  birth_place: z.string('Birth place is required').min(2, 'Must be at least 2 characters').optional()
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  name: data.value?.name,
  description: data.value?.description,
  gender: data.value?.gender,
  birth_place: data.value?.birth_place
})

const toast = useToast()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  console.log(event.data)
  await $fetch('/backend/items/' + route.params.id, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${autStore.token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(event.data)
  })
  toast.add({ title: 'Success', description: 'Suspect updated successfully.', color: 'success' })
  navigateTo(`/suspects`)
}
</script>

<template>
  <UDashboardPanel id="suspects-edit">
    <template #header>
      <UDashboardNavbar title="Edit suspect details">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton icon="i-lucide-eye" :to="`/suspects/${route.params.id}`">
            View Suspect
          </UButton>
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div v-if="data">
        <UCard
          :ui="{
            header: 'p-0 sm:px-0'
          }"
        >
          <template #header>
            <img
              :src="data.image_url"
              class="w-full h-100 object-contain"
            >
          </template>
          <UCardBody>
            <UForm
              :schema="schema"
              :state="state"
              class="space-y-4"
              @submit="onSubmit"
            >
              <UFormField label="Name" name="name" class="w-full">
                <UInput v-model="state.name" class="w-full" />
              </UFormField>

              <UFormField label="Description" name="description" class="w-full">
                <UTextarea v-model="state.description" class="w-full" />
              </UFormField>

              <UFormField label="Gender" name="gender">
                <USelect v-model="state.gender" :items="genders" class="w-48" />
              </UFormField>

              <UFormField label="Birth place" name="birth_place">
                <USelect v-model="state.birth_place" :items="districts" class="w-48" />
              </UFormField>

              <UButton type="submit">
                Submit
              </UButton>
            </UForm>
          </UCardBody>
        </UCard>
      </div>
    </template>
  </UDashboardPanel>
</template>
