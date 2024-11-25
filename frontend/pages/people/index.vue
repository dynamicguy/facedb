<script setup>
import { useSidebarStore } from "@/stores/sidebar";
const sidebarStore = useSidebarStore();
const route = useRoute();

const dynamicguySidebar = ref([
  {
    label: "Overview",
    items: [
      { label: "Home", icon: "ph:house", to: "/" },
      { label: "Dashboard", icon: "ph:house", to: "/dashboard" },
    ],
  },
  {
    label: "Navigation",
    items: [
      {
        label: "People",
        icon: "ph:devices",
        items: [
          {
            label: "All",
            icon: "ph:circle",
            badge: "221500",
            to: "/people",
          },
          {
            label: "Search",
            icon: "ph:circle",
            to: "/search"
          },
          {
            label: "Add",
            icon: "ph:circle",
            to: "/add"
          },
        ],
      },
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
  'items',
  () => $fetch('/api/items')
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

      <!-- Dashboard Overview Cards -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Card 1 -->
        <div class="rounded-lg bg-white p-6 shadow-lg">
          <h3 class="mb-2 text-xl font-semibold">Total Sales</h3>
          <p class="text-2xl font-bold text-blue-600">$23,450</p>
          <p class="text-sm text-gray-500">+5% compared to last month</p>
        </div>

        <!-- Card 2 -->
        <div class="rounded-lg bg-white p-6 shadow-lg">
          <h3 class="mb-2 text-xl font-semibold">New Users</h3>
          <p class="text-2xl font-bold text-green-600">1,230</p>
          <p class="text-sm text-gray-500">+12% compared to last month</p>
        </div>

        <!-- Card 3 -->
        <div class="rounded-lg bg-white p-6 shadow-lg">
          <h3 class="mb-2 text-xl font-semibold">Active Subscriptions</h3>
          <p class="text-2xl font-bold text-yellow-600">345</p>
          <p class="text-sm text-gray-500">+3% compared to last month</p>
        </div>
      </div>

      <!-- Performance Chart Section -->
      <div class="mt-8">
        <div class="rounded-lg bg-white p-6 shadow-lg">
          <h3 class="mb-4 text-xl font-semibold">Search for people by uploading your image</h3>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-6">

            <div v-for="item in data" class="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
              <a :href="'/people/'+item.id">
                <img class="rounded-t-lg" :src="item.image_url" alt="" />
              </a>
              <div class="p-5">
                <a href="#">
                  <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{item.name}}</h5>
                </a>
                <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{item.description}}</p>
                <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{item.birth_place}}</p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>
