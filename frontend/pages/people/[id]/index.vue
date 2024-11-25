<script setup>
import { useSidebarStore } from "@/stores/sidebar";
const sidebarStore = useSidebarStore();
const route = useRoute();

const dynamicguySidebar = ref([
  {
    label: "Overview",
    items: [
      { label: "Home", icon: "ph:house", to: "/" },
      { label: "People", icon: "ph:user", to: "/people" },
      { label: "Search", icon: "ph:user", to: "/search" },
      { label: "Dashboard", icon: "ph:house", to: "/dashboard" },
    ],
  },
]);

dynamicguySidebar.value = dynamicguySidebar.value.map((category) => {
  const calculateBadges = (items) => {
    const updatedItems = items.map((item) => {
      if (item.items) {
        const { items: updatedChildren, hasBadges } = calculateBadges(
          item.items,
        );
        item.items = updatedChildren;
        item.hasBadge = hasBadges;
      }
      return { ...item, expanded: true };
    });
    return {
      items: updatedItems,
      hasBadges: updatedItems.some((item) => item.badge || item.hasBadge),
    };
  };

  if (category.items) {
    const { items: updatedItems } = calculateBadges(category.items);
    category.items = updatedItems;
  }

  return category;
});

const { data, status, error, refresh, clear } = await useAsyncData(
  'data',
  () => $fetch('/api/items/'+route.params.id)
);

// Add this computed property
const isSidebarOpen = ref(true);
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Add this to automatically expand parent menus containing the active route
onMounted(() => {
  dynamicguySidebar.value.forEach((category) => {
    category.items?.forEach((item) => {
      const expandParentIfChildActive = (items) => {
        return items?.some((subItem) => {
          if (subItem.to === route.path) {
            item.expanded = true;
            return true;
          }
          if (subItem.items) {
            const hasActiveChild = expandParentIfChildActive(subItem.items);
            if (hasActiveChild) {
              item.expanded = true;
              subItem.expanded = true;
            }
            return hasActiveChild;
          }
          return false;
        });
      };

      if (item.items) {
        expandParentIfChildActive(item.items);
      }
    });
  });
});
</script>

<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <LayoutDashboardSidebar
      :menu="dynamicguySidebar"
      :class="{
        'translate-x-0': sidebarStore.isOpen,
        '-translate-x-full': !sidebarStore.isOpen,
      }"
    />

    <!-- Main Content Area -->
    <div
      :class="{
        'ml-72': sidebarStore.isOpen,
        'ml-0 px-8': !sidebarStore.isOpen,
      }"
      class="flex-1 p-6 transition-all duration-300 ease-in-out"
    >
      <!-- Header -->
      <div class="mb-8 flex items-center justify-start">
        <button
          class="rounded-lg bg-white p-2 px-4 text-xl text-gray-500 shadow-sm transition duration-200 hover:shadow"
          @click="sidebarStore.toggle"
        >
          <Icon name="ph:list" />
        </button>
        <h1 class="ml-4 text-3xl font-semibold">Welcome back, Nurul Ferdous</h1>
      </div>

      <!-- Performance Chart Section -->
      <div class="mt-8">
        <div class="rounded-lg bg-white p-6 shadow-lg">

          <div class="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
            <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-s-lg" :src="data.image_url" alt="image">
            <div class="flex flex-col justify-between p-4 leading-normal">
              <h5 class="mb-1 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{data.name}}</h5>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">{{data.description}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Gender: {{data.gender}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Date of birth: {{data.dob}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Birth place: {{data.birth_place}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Identified gender: {{data.identified_gender}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Identified age: {{data.identified_age}}</p>
              <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Identified race: {{data.identified_race}}</p>
              <p class="font-normal text-gray-700 dark:text-gray-400">Identified emotion: {{data.identified_emotion}}</p>
            </div>
          </div>


        </div>
      </div>
    </div>
  </div>
</template>
