<script setup>
import { useSidebarStore } from "@/stores/sidebar";
const sidebarStore = useSidebarStore();
const route = useRoute();

const analysis = ref(null);
const result = ref(null);
const file = ref(null);
const previewSrc = ref(null);
const loading = ref(false);

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
            analysisbadge: "221500",
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

const doAnalyze = async (event) => {
  loading.value = true;
  file.value = event.target.files[0];
  previewSrc.value = URL.createObjectURL(file.value);
  const formData = new FormData();
  formData.append('file', file.value);

  const res = await $fetch('/api/analyze', {
    method: 'POST',
    body: formData,
  })
  analysis.value = res;
  loading.value = false;
};

const doSubmit = async (event) => {
  event.preventDefault();
  loading.value = true;
  const formData = new FormData();
  formData.append('name', event.target.name.value);
  formData.append('description', event.target.description.value);
  formData.append('gender', event.target.gender.value);
  formData.append('dob', event.target.dob.value);
  formData.append('birth_place', event.target.birth_place.value);
  formData.append('img_path', analysis.value.img_path);
  formData.append('identified_age', analysis.value.identified_age);
  formData.append('identified_gender', analysis.value.identified_gender);
  formData.append('identified_race', analysis.value.identified_race);
  formData.append('identified_emotion', analysis.value.identified_emotion);

  let object = {};
  formData.forEach(function(value, key){
    object[key] = value;
  });
  const json = JSON.stringify(object);

  const res = await $fetch('/api/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: json,
  })
  result.value = res;
  await navigateTo({ path: '/search' })
  loading.value = false;
};

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
      <div class="rounded-lg bg-white p-6 shadow-lg">
        <h3 class="mb-4 text-xl font-semibold">Add a new person</h3>
        <div class="flex items-center justify-center w-full mb-4">
          <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
              </svg>
              <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
            </div>
            <input id="dropzone-file" name="file" type="file" class="hidden" @change="doAnalyze" >
          </label>
        </div>

        <div v-if="previewSrc" class="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
          <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-s-lg" :src="previewSrc" alt="search image">
          <div v-if="loading" role="status">
            <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
          <div class="flex flex-col justify-between p-4 leading-normal" v-if="analysis">
            <h5 class="mb-1 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Input image analysis</h5>
            <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Age: {{ analysis.identified_age }}</p>
            <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Gender: {{ analysis.identified_gender }}</p>
            <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Race: {{ analysis.identified_race }}</p>
            <p class="mb-1 font-normal text-gray-700 dark:text-gray-400">Emotion: {{ analysis.identified_emotion }}</p>
          </div>
        </div>



        <form class="max-w-sm mx-auto mt-4" @submit="doSubmit">
          <div class="mb-5">
            <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Name</label>
            <input type="text" id="name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
          </div>
          <div class="mb-5">
            <label for="description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Description</label>
            <input type="text" id="description" class="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          </div>
          <div class="mb-5">
            <label for="gender" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Gender</label>
            <select id="gender" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
              <option selected>Choose a gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
          <div class="mb-5">
            <label for="dob" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Date of birth</label>
            <input type="date" id="dob" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required autocomplete="off" />
          </div>

          <div class="mb-5">
            <label for="birth_place" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Birth place</label>
            <input type="text" id="birth_place" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
          </div>

          <button type="submit" class="text-black p-3 bg-blue-500 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
        </form>

      </div>
    </div>
  </div>
</template>
