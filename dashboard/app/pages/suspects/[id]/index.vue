<script setup lang="ts">
import type { Suspect } from '~/types'
import { useAuthStore } from '@/stores/auth'

// definePageMeta({
//   middleware: 'auth'
// })

const autStore = useAuthStore()
const route = useRoute()

const { data, status } = await useFetch<Suspect>('/backend/items/' + route.params.id, {
  lazy: true,
  headers: {
    'Authorization': `Bearer ${autStore.token}`,
    'Content-Type': 'application/json'
  }
})
</script>

<template>
  <UDashboardPanel id="suspects-details">
    <template #header>
      <UDashboardNavbar title="Suspect details">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton icon="i-lucide-user-pen" :to="`/suspects/${route.params.id}/edit`">
            Edit Suspect
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
              class="w-full h-200 object-contain"
            >
          </template>
          <UCardBody>
            <UCardTitle>{{ data.name }}</UCardTitle>
            <p>{{ data.description }}</p>
            <p>Location: {{ data.birth_place }}</p>
            <p>Gender: {{ data.gender }}</p>
            <p>Date of Birth: {{ data.dob }}</p>
            <p>Age: {{ data.identified_age }}</p>
            <p>Race: {{ data.identified_race }}</p>
            <p>Emotion: {{ data.identified_emotion }}</p>
            <p>
              Created at: <NuxtTime
                :datetime="data.created_at"
                year="numeric"
                month="long"
                day="numeric"
                hour="2-digit"
                minute="2-digit"
              />
            </p>
          </UCardBody>
        </UCard>
      </div>
    </template>
  </UDashboardPanel>
</template>
