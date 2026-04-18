<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'

import { useAuthStore } from '@/stores/auth'

const autStore = useAuthStore()

const toast = useToast()

definePageMeta({
  layout: 'blank'
})

const fields: AuthFormField[] = [{
  name: 'username',
  type: 'text',
  label: 'Username',
  placeholder: 'Enter your username',
  required: true
}, {
  name: 'password',
  label: 'Password',
  type: 'password',
  placeholder: 'Enter your password',
  required: true
}, {
  name: 'remember',
  label: 'Remember me',
  type: 'checkbox'
}]

const schema = z.object({
  username: z.string('Username is required').min(3, 'Must be at least 3 characters'),
  password: z.string('Password is required').min(5, 'Must be at least 5 characters')
})

type Schema = z.output<typeof schema>

// function onSubmit(payload: FormSubmitEvent<Schema>) {
//   console.log('Submitted', payload)
// }

const onSubmit = (payload: FormSubmitEvent<Schema>) => {
  console.log('Submitted', payload)
  const { username, password } = payload.data

  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  $fetch('/backend/token', {
    method: 'POST',
    body: formData
  })
    .then(async (res) => {
      console.log('RESPONSE', res)
      if (res && res.user) {
        autStore.login(res.access_token, 'true', res.user.username, res.user.email, res.user.full_name)
        await navigateTo('/')
      }
    })
    .catch((err) => {
      console.error('Bad credentials', err)
      autStore.logout()
    })
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md mt-46">
      <UAuthForm
        :schema="schema"
        title="Login"
        description="Enter your credentials to access your account."
        icon="i-lucide-user"
        :fields="fields"
        @submit="onSubmit"
      />
    </UPageCard>
  </div>
</template>
