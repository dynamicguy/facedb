<script setup>
defineProps({
  title: { type: String, required: false, default: "" },
  subtitle: { type: String, required: false, default: "" },
  size: { type: String, required: false, default: "10" },
  alignCenter: { type: Boolean, required: false, default: true },
});
</script>
<template>
  <div
    class="flex"
    :class="[
      {
        'items-center': !alignCenter,
      },
    ]"
  >
    <Icon
      class=""
      :class="`min-h-${size} min-w-${size}`"
      name="solar:three-squares-bold-duotone"
    />
    <h2 v-if="title || subtitle" class="ml-3 hidden flex-col md:flex">
      <span v-if="title" class="text-xl font-semibold">{{ title }}</span>
      <span v-if="subtitle">{{ subtitle }}</span>
    </h2>
  </div>
</template>
