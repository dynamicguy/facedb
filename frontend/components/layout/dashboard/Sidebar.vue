<script setup>
import { useSidebarStore } from "@/stores/sidebar";
const sidebarStore = useSidebarStore();

defineProps({
  menu: {
    type: Object,
    default: () => ({}),
  },
});
const expandProfile = ref(false);
const profileButton = ref(null);
const profileMenu = ref(null);

const handleClickOutside = (event) => {
  const isClickOnButton = profileButton.value?.contains(event.target);
  const isClickOnMenu = profileMenu.value?.contains(event.target);

  if (!isClickOnButton && !isClickOnMenu && expandProfile.value) {
    expandProfile.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
<template>
  <div
    class="fixed inset-y-0 left-0 z-50 w-72 transform overflow-y-scroll bg-white px-4 text-gray-500 transition-transform duration-300 ease-in-out"
    :class="[
      {
        shadow: sidebarStore.isOpen,
      },
    ]"
  >
    <div class="mb-5 mt-4 flex flex-row justify-between">
      <HeaderLogo
        title="Dynamic FaceDB"
        subtitle="Face recognition system"
        class="sticky top-0 z-50"
      />
    </div>
    <ul class="min-h-full">
      <LayoutDashboardSidebarMenu :menu />
    </ul>

    <div
      class="sticky bottom-0 left-0 right-0 bg-white pb-3 transition-all duration-200"
    >
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform translate-y-6 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-200 ease-out"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform translate-y-6 opacity-0"
      >
        <div
          v-show="expandProfile"
          ref="profileMenu"
          class="profile-menu mb-2 rounded-lg bg-slate-100 p-2"
        >
          <ul class="flex flex-col gap-1">
            <li>
              <router-link
                to="/settings"
                class="flex select-none items-center gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-200 hover:text-gray-600"
              >
                <Icon name="ph:user" />
                <span>Profile</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/settings"
                class="flex select-none items-center gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-200 hover:text-gray-600"
              >
                <Icon name="ph:gear" />
                <span>Settings</span>
              </router-link>
            </li>
            <li>
              <router-link
                to="/settings"
                class="flex select-none items-center gap-2 rounded-md px-3 py-2 font-medium hover:bg-slate-200 hover:text-gray-600"
              >
                <Icon name="ph:sign-out" />
                <span>Sign out</span>
              </router-link>
            </li>
          </ul>
        </div>
      </transition>
      <button
        ref="profileButton"
        class="z-50 flex w-full flex-row items-center rounded-lg bg-slate-100 p-2 px-2.5 text-left align-middle hover:bg-slate-100"
        :class="[
          {
            'bg-slate-100': expandProfile,
          },
        ]"
        @click="expandProfile = !expandProfile"
      >
        <NuxtImg
          class="max-h-10 min-h-10 min-w-10 max-w-10 rounded-full bg-slate-300"
          src="https://i.pravatar.cc/150"
        />
        <div class="ml-3 flex w-full items-center justify-between align-middle">
          <div class="grid grid-flow-row">
            <span class="font-medium">Nurul Ferdous</span>
            <span class="text-sm">Administrator</span>
          </div>
          <Icon
            name="ph:caret-up"
            class="transform transition-transform"
            :class="{ 'rotate-180': expandProfile }"
          />
        </div>
      </button>
    </div>
  </div>
</template>
