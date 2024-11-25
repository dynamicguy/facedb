<script setup>
defineProps({
  menu: {
    type: Object,
    default: () => ({}),
  },
});
</script>
<template>
  <div>
    <template v-for="(category, index) in menu" :key="index">
      <li class="mb-6">
        <span class="text-sm font-semibold uppercase">{{
          category.label
        }}</span>
        <ul class="mt-2 space-y-0.5">
          <LayoutDashboardSidebarMenuItems :items="category.items" />
        </ul>
      </li>
    </template>
  </div>
</template>
