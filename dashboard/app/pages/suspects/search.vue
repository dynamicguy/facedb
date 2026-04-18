<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import type { SearchResult } from '~/types'

// definePageMeta({
//   middleware: 'auth'
// })

const autStore = useAuthStore()

const inputFile = ref<File[]>([])
const loading = ref(false)
const result = ref(null)

const doSearch = async () => {
  loading.value = true
  if (!inputFile.value || inputFile.value.length === 0) {
    loading.value = false
    result.value = null
    return
  }
  const formData = new FormData()
  formData.append('file', inputFile.value)

  const { data, status } = await useFetch<SearchResult>('/backend/search', {
    lazy: true,
    method: 'POST',
    body: formData,
    headers: {
      Authorization: `Bearer ${autStore.token}`
    },
    query: computed(() => ({
      quid: new Date().getTime()
    }))
  })
  console.log('search results', data.value, status.value)
  result.value = data.value
  loading.value = false
}
</script>

<template>
  <UDashboardPanel id="suspects-search">
    <template #header>
      <UDashboardNavbar title="Search suspects">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <SuspectsAddModal />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="flex">
        <div>
          <UFileUpload
            v-model="inputFile"
            accept="image/*"
            class="w-96 min-h-65"
            label="Drop your image here"
            description="PNG, JPG or GIF (max. 20MB)"
            @change="doSearch"
          />
        </div>

        <div class="w-full pl-4">
          <p>Search for suspects by uploading an image. The system will analyze the image and return potential matches from the database.</p>
          <div v-if="result">
            <UPageFeature :description="result.identified.identified_age" title="Identified age" />
            <UPageFeature :description="result.identified.identified_gender" title="Identified gender" />
            <UPageFeature :description="result.identified.identified_race" title="Identified race" />
            <UPageFeature :description="result.identified.identified_emotion" title="Identified emotion" />
            <p class="mb-4">
              <UBadge>{{ result.items.length }}</UBadge> search results shown from a total of <UBadge>{{ result.total }}</UBadge> possible matches in <UBadge>{{ result.took }}</UBadge> milliseconds
            </p>
          </div>
        </div>
      </div>
      <div>
        <UProgress v-if="loading" />
        <div v-if="result" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="(suspect, index) in result.items" :key="index">
            <NuxtLink :to="`/suspects/${suspect.id}`">
              <UCard
                :ui="{
                  header: 'p-0 sm:px-0'
                }"
              >
                <template #header>
                  <img
                    :src="suspect.image_url"
                    class="w-full h-100 object-cover"
                  >
                </template>
                <UCardBody>
                  <UCardTitle class="flex items-center justify-between">
                    <span>{{ suspect.name }}</span>

                    <UBadge :color="suspect.score > 1.8 ? 'error' : 'neutral'" :label="(suspect.score-1).toFixed(4)"/>
                  </UCardTitle>
                  <p>{{ suspect.description }}</p>

                </UCardBody>
              </UCard>
            </NuxtLink>
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
