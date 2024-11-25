<script setup>
const showModal = ref(false);
</script>

<template>
  <div>
    <button
      class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
      @click="showModal = true"
    >
      Open Modal
    </button>

    <UIModal
      :is-open="showModal"
      title="Big title here"
      @close="showModal = false"
    >
      Your modal content here
    </UIModal>
  </div>
</template>
