<script setup>
defineProps({
  items: {
    type: Object,
    default: () => ({}),
  },
  level: {
    type: Number,
    default: 0,
  },
});

const getIndentClass = (level) => {
  console.log(level);
  return `margin-left: ${level * 6}px !important`; // Increased multiplier for more distinct levels
};

const route = useRoute();
const toggleSubmenu = (item) => {
  item.expanded = !item.expanded;
};

const isActive = (to) => {
  if (!to) return;
  const currentPath = route.path.replace(/\/$/, "");
  const targetPath = to.replace(/\/$/, "");
  return currentPath === targetPath;
};

const classIsActive = (to) => {
  if (!to) return;
  if (isActive(to)) {
    return "bg-slate-100 text-gray-600";
  }
};
</script>

<template>
  <template v-for="(item, itemIndex) in items" :key="itemIndex">
    <li>
      <!-- Regular Link -->
      <router-link
        v-if="item.to"
        :to="item.to"
        class="flex select-none items-center gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-100 hover:text-gray-600"
        :class="[classIsActive(item.to)]"
        :style="getIndentClass(level)"
      >
        <Icon v-if="isActive(item.to)" :name="`${item.icon}-fill`" />
        <Icon v-else :name="`${item.icon}`" />
        <div class="flex w-full justify-between">
          <span>{{ item.label }}</span>
          <span
            v-if="item?.badge"
            class="flex items-center rounded-full bg-slate-400 px-2 text-center align-middle text-xs tabular-nums text-white"
            >{{ item.badge }}</span
          >
        </div>
      </router-link>

      <!-- External Link -->
      <a
        v-else-if="item.url"
        :href="item.url"
        :target="item.target"
        class="flex select-none items-center justify-between gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-100 hover:text-gray-600"
        :style="getIndentClass(level)"
      >
        <div>
          <Icon :name="`${item.icon}`" />
          <span class="pl-2">{{ item.label }}</span>
          <span
            v-if="item?.badge"
            class="flex items-center rounded-full bg-slate-400 p-1 px-2 text-center align-middle text-xs text-white"
            >{{ item.badge }}</span
          >
        </div>
        <div>
          <Icon name="ph:arrow-square-out" />
        </div>
      </a>

      <!-- Nested Menu -->
      <template v-else-if="item.items">
        <div
          class="flex cursor-pointer select-none items-center justify-between gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-100 hover:text-gray-600"
          :style="getIndentClass(level)"
          @click="() => toggleSubmenu(item)"
        >
          <div class="flex items-center gap-2">
            <Icon :name="`${item.icon}`" />
            <span>{{ item.label }}</span>
            <span
              v-if="item?.hasBadge"
              class="flex h-2 w-2 items-center rounded-full bg-slate-400 text-center align-middle text-xs text-white"
            />
          </div>
          <Icon
            name="ph:caret-down"
            class="transform transition-transform"
            :class="{ 'rotate-180': item.expanded }"
          />
        </div>

        <LayoutDashboardSidebarMenuItems
          v-if="item.expanded"
          :items="item.items"
          :level="level + 2"
          class="mt-1 space-y-1"
        />
      </template>

      <!-- Disabled Item -->
      <div
        v-else
        class="disabled flex cursor-not-allowed select-none items-center gap-2 rounded-md px-3 py-2 text-gray-400"
        :style="getIndentClass(level)"
      >
        <Icon :name="`${item.icon}`" />
        <div class="flex w-full justify-between">
          <span>{{ item.label }}</span>
          <span
            v-if="item?.badge"
            class="flex items-center rounded-full bg-slate-400 px-2 text-center align-middle text-xs tabular-nums text-white"
            >{{ item.badge }}</span
          >
        </div>
      </div>
    </li>
  </template>
</template>
