<script setup lang="ts">
defineProps({ error: { type: Object, default: null } });
</script>
<template>
  <pre>{{ error }}</pre>
</template>
