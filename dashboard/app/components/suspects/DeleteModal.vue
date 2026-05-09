<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const toast = useToast()

const emit = defineEmits(['refreshSuspects'])

withDefaults(defineProps<{
  count?: number
  suspectIds?: string[]
}>(), {
  count: 0,
  suspectIds: () => []
})

const open = ref(false)

async function onSubmit(ids: string[] | undefined) {
  if (!ids || ids.length === 0) {
    toast.add({ title: 'Error', description: 'No suspect selected.', color: 'error' })
    return
  }
  for (const sid of ids) {
    await $fetch('/backend/suspects/' + sid, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })
  }
  open.value = false
  emit('refreshSuspects')
  toast.add({ title: 'Success', description: 'Suspect deleted successfully.', color: 'success' })
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="`Delete ${count} suspect${count > 1 ? 's' : ''}`"
    :description="`Are you sure, this action cannot be undone.`"
  >
    <slot />

    <template #body>
      <div class="flex justify-end gap-2">
        <UButton
          label="Cancel"
          color="neutral"
          variant="subtle"
          @click="open = false"
        />
        <UButton
          label="Delete"
          color="error"
          variant="solid"
          loading-auto
          @click="onSubmit(suspectIds)"
        />
      </div>
    </template>
  </UModal>
</template>
