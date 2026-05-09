<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const genders = ['Man', 'Woman']

const open = ref(false)
const analysis = ref(null)
const loading = ref(false)
const inputFile = ref<File[]>([])

const schema = z.object({
  name: z.string().min(2, 'Too short'),
  bio: z.string().min(2, 'Too short'),
  gender: z.enum(genders),
  dob: z.string(),
  birth_place: z.string('Birth place is required').min(2, 'Must be at least 2 characters').optional(),
  image: z.file().optional()
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  name: '',
  bio: '',
  gender: 'Man',
  dob: undefined,
  birth_place: undefined,
  image: undefined
})

const toast = useToast()

// const { data, status } = await useFetch<Suspect>('/backend/suspects/' + route.params.id, {
//   headers: {
//     'Authorization': `Bearer ${autStore.token}`,
//     'Content-Type': 'application/json'
//   }
// })

const doAnalyze = async (event: any) => {
  loading.value = true
  if (!inputFile.value || inputFile.value.length === 0) {
    loading.value = false
    analysis.value = null
    return
  }

  const formData = new FormData()
  formData.append('file', inputFile.value)

  const res = await $fetch('/backend/analyze', {
    method: 'POST',
    body: formData,
    headers: {
      Authorization: `Bearer ${authStore.token}`
    }
  })
  analysis.value = res
  loading.value = false
}

async function onSubmit(event: FormSubmitEvent<Schema>) {
  toast.add({ title: 'Success', description: `New suspect ${event.data.name} added`, color: 'success' })
  if (!analysis.value) {
    return
  }
  // open.value = false
  loading.value = true
  const formData = new FormData()
  formData.append('name', event.data.name)
  formData.append('bio', event.data.bio)
  formData.append('gender', event.data.gender)
  formData.append('dob', event.data.dob)
  formData.append('birth_place', event.data.birth_place)
  formData.append('img_path', analysis.value.img_path)
  formData.append('identified_age', analysis.value.identified_age)
  formData.append('identified_gender', analysis.value.identified_gender)
  formData.append('identified_race', analysis.value.identified_race)
  formData.append('identified_emotion', analysis.value.identified_emotion)

  const object: Record<string, any> = {}
  formData.forEach(function (value, key) {
    object[key] = value
  })
  const json = JSON.stringify(object)
  console.log('form data', object, json)

  const res = await $fetch('/backend/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    },
    body: json
  })
  loading.value = false
  open.value = false
  return navigateTo('/suspects', { redirectCode: 301 })
}
</script>

<template>
  <UModal v-model:open="open" title="New suspect" description="Add a new suspect to the database">
    <UButton label="New suspect" icon="i-lucide-plus" />

    <template #body>
      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField label="Name" placeholder="John Doe" name="name">
          <UInput v-model="state.name" class="w-full" />
        </UFormField>
        <UFormField label="Bio" placeholder="Bio of the suspect" name="bio">
          <UTextarea v-model="state.bio" class="w-full" />
        </UFormField>
        <UFormField label="Gender" name="gender">
          <USelect v-model="state.gender" :items="genders" class="w-48" />
        </UFormField>
        <UFormField label="Birth place" name="birth_place" class="w-full">
          <UInput v-model="state.birth_place" class="w-full" />
        </UFormField>
        <UFormField label="Date of birth" name="dob" class="w-full">
          <UInput v-model="state.dob" type="date" class="w-full" />
        </UFormField>
        <UFormField label="Image" name="image">
          <UFileUpload
            v-model="inputFile"
            class="w-full min-h-32"
            accept="image/*"
            @change="doAnalyze"
          />
        </UFormField>
        <pre>{{ analysis }}</pre>

        <div class="flex justify-end gap-2">
          <UButton
            label="Cancel"
            color="neutral"
            variant="subtle"
            @click="open = false"
          />
          <UButton
            label="Create"
            color="primary"
            variant="solid"
            type="submit"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
