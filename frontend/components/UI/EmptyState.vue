<script setup>
const props = defineProps({
  icon: { type: String, default: null },
  iconSize: { type: String, default: "64px" },
});
</script>
<template>
  <div
    class="flex h-full w-full flex-col items-center justify-center gap-5 rounded-lg p-5 align-middle text-gray-500 dark:text-white"
  >
    <Icon v-if="props.icon" :name="props.icon" :size="props.iconSize" />
    <span><slot /></span>
  </div>
</template>
