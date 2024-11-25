<script setup>
import { useSidebarStore } from "@/stores/sidebar";
const sidebarStore = useSidebarStore();
const route = useRoute();
// const mockupSidebar = ref([
//   {
//     label: "Home",
//     items: [{ label: "Dashboard", icon: "ph:house", to: "/dashboard" }],
//   },
//   {
//     label: "Hierarchy",
//     items: [
//       {
//         label: "Submenu 1",
//         icon: "ph:bookmark",
//         items: [
//           {
//             label: "Submenu 1.1",
//             icon: "ph:bookmark",
//             items: [
//               {
//                 label: "Submenu 1.1.1",
//                 icon: "ph:bookmark",
//               },
//               {
//                 label: "Submenu 1.1.2",
//                 icon: "ph:bookmark",
//                 to: "/dashboard/2",
//               },
//               {
//                 label: "Submenu 1.1.3",
//                 icon: "ph:bookmark",
//                 items: [
//                   {
//                     label: "Submenu 1.1.3.1",
//                     icon: "ph:bookmark",
//                   },
//                   {
//                     label: "Submenu 1.1.3.2",
//                     icon: "ph:bookmark",
//                     to: "/dashboard/2",
//                   },
//                   {
//                     label: "Submenu 1.1.3.3",
//                     icon: "ph:bookmark",
//                     to: "/dashboard/3",
//                   },
//                 ],
//               },
//             ],
//           },
//           {
//             label: "Submenu 1.2",
//             icon: "ph:bookmark",
//             items: [
//               {
//                 label: "Submenu 1.2.1",
//                 icon: "ph:bookmark",
//                 to: "/dashboard/34",
//               },
//             ],
//           },
//         ],
//       },
//       {
//         label: "Submenu 2",
//         icon: "ph:bookmark",
//         items: [
//           {
//             label: "Submenu 2.1",
//             icon: "ph:bookmark",
//             items: [
//               { label: "Submenu 2.1.1", icon: "ph:bookmark" },
//               { label: "Submenu 2.1.2", icon: "ph:bookmark" },
//             ],
//           },
//           {
//             label: "Submenu 2.2",
//             icon: "ph:bookmark",
//             items: [{ label: "Submenu 2.2.1", icon: "ph:bookmark" }],
//           },
//         ],
//       },
//     ],
//   },
//   {
//     label: "UI Components",
//     items: [
//       {
//         label: "Form Layout",
//         icon: "ph:identification-card",
//         to: "/uikit/formlayout",
//       },
//       { label: "Input", icon: "ph:check-square", to: "/uikit/input" },
//       {
//         label: "Button",
//         icon: "ph:radio-button",
//         to: "/uikit/button",
//         class: "rotated-icon",
//       },
//       { label: "Table", icon: "ph:table", to: "/uikit/table" },
//       { label: "List", icon: "ph:list", to: "/uikit/list" },
//       { label: "Tree", icon: "ph:tree-view", to: "/uikit/tree" },
//       { label: "Panel", icon: "ph:device-tablet", to: "/uikit/panel" },
//       { label: "Overlay", icon: "ph:images", to: "/uikit/overlay" },
//       { label: "Media", icon: "ph:image", to: "/uikit/media" },
//       { label: "Menu", icon: "ph:list", to: "/uikit/menu" },
//       { label: "Message", icon: "ph:chat-circle", to: "/uikit/message" },
//       { label: "File", icon: "ph:file", to: "/uikit/file" },
//       { label: "Chart", icon: "ph:chart-bar", to: "/uikit/charts" },
//       {
//         label: "Timeline",
//         icon: "ph:calendar",
//         to: "/uikit/timeline",
//       },
//       { label: "Misc", icon: "ph:circle", to: "/uikit/misc" },
//     ],
//   },
//   {
//     label: "Pages",
//     icon: "ph:briefcase",
//     to: "/pages",
//     items: [
//       {
//         label: "Landing",
//         icon: "ph:globe",
//         to: "/landing",
//       },
//       {
//         label: "Auth",
//         icon: "ph:user",
//         items: [
//           {
//             label: "Login",
//             icon: "ph:sign-in",
//             to: "/auth/login",
//           },
//           {
//             label: "Error",
//             icon: "ph:x",
//             to: "/auth/error",
//           },
//           {
//             label: "Access Denied",
//             icon: "ph:lock",
//             to: "/auth/access",
//           },
//         ],
//       },
//       {
//         label: "Crud",
//         icon: "ph:pencil",
//         to: "/pages/crud",
//       },
//       {
//         label: "Not Found",
//         icon: "ph:x",
//         to: "/pages/notfound",
//       },
//       {
//         label: "Empty",
//         icon: "ph:circle",
//         to: "/pages/empty",
//       },
//     ],
//   },

//   {
//     label: "Get Started",
//     items: [
//       {
//         label: "Documentation",
//         icon: "ph:book",
//         to: "/documentation",
//       },
//       {
//         label: "View Source",
//         icon: "ph:github-logo",
//         url: "https://github.com/primefaces/sakai-vue",
//         target: "_blank",
//       },
//     ],
//   },
// ]);
const mockupSidebar = ref([
  {
    label: "Overview",
    items: [
      { label: "Home", icon: "ph:house", to: "/" },
      { label: "People", icon: "ph:house", to: "/people" },
      { label: "Dashboard", icon: "ph:house", to: "/dashboard" }
    ],
  },
  {
    label: "Monitoring",
    items: [
      {
        label: "Devices",
        icon: "ph:devices",
        items: [
          {
            label: "Unregistered",
            icon: "ph:circle",
            analysisbadge: "221500",
            to: "/devices/unregistered",
          },
          {
            label: "Registered",
            icon: "ph:circle",
          },
          {
            label: "Monitoring",
            icon: "ph:circle",
          },
        ],
      },
    ],
  },
  {
    label: "Pages",
    icon: "ph:briefcase",
    to: "/pages",
    items: [
      {
        label: "Landing",
        icon: "ph:globe",
        to: "/landing",
      },
      {
        label: "Auth",
        icon: "ph:user",
        items: [
          {
            label: "Login",
            icon: "ph:sign-in",
            to: "/auth/login",
          },
          {
            label: "Error",
            icon: "ph:x",
            to: "/auth/error",
          },
          {
            label: "Access Denied",
            icon: "ph:lock",
            to: "/auth/access",
          },
        ],
      },
      {
        label: "Crud",
        icon: "ph:pencil",
        to: "/pages/crud",
      },
      {
        label: "Not Found",
        icon: "ph:x",
        to: "/pages/notfound",
      },
      {
        label: "Empty",
        icon: "ph:circle",
        to: "/pages/empty",
      },
    ],
  },
]);
// Modify your mockupSidebar ref to include the expanded property
// mockupSidebar.value = mockupSidebar.value.map((category) => ({
//   ...category,
//   items: category.items.map((item) => ({
//     ...item,
//     expanded: false,
//     items: item.items?.map((subItem) => ({
//       ...subItem,
//       expanded: false,
//     })),
//   })),
// }));
// mockupSidebar.value = mockupSidebar.value.map((category) => ({
//   ...category,
//   items: category.items.map((item) => ({
//     ...item,
//     expanded: true,
//     items: item.items?.map((subItem) => ({
//       ...subItem,
//       expanded: true,
//     })),
//   })),
// }));
mockupSidebar.value = mockupSidebar.value.map((category) => {
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

// Add this computed property

const isSidebarOpen = ref(true);
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

// Add this to automatically expand parent menus containing the active route
onMounted(() => {
  mockupSidebar.value.forEach((category) => {
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
      :menu="mockupSidebar"
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
        <h1 class="ml-4 text-3xl font-semibold">Welcome back, John</h1>
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
          <h3 class="mb-4 text-xl font-semibold">Performance Overview</h3>
          <div class="h-64 rounded-lg bg-gray-200">
            <!-- Placeholder for Chart -->
            <p class="pt-24 text-center text-gray-500">[Insert Chart Here]</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
