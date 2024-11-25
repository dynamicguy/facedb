<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  showClose: {
    type: Boolean,
    required: false,
    default: true,
  },
  title: {
    type: String,
    required: false,
    default: "",
  },
  fullscreen: {
    type: Boolean,
    required: false,
    default: false,
  },
  showBackdrop: {
    type: Boolean,
    required: false,
    default: true,
  },
  disableCloseOnClickOutside: {
    type: Boolean,
    required: false,
    default: false,
  },
});

defineEmits(["close"]);
</script>
<template>
  <template v-if="isOpen">
    <div class="fixed inset-0 z-50">
      <div
        class="absolute inset-0"
        :class="[
          {
            'bg-black/20 backdrop-blur-sm': showBackdrop,
            'bg-transparent': !showBackdrop,
          },
        ]"
        @click="disableCloseOnClickOutside ? '' : $emit('close')"
      />

      <div
        class="absolute"
        :class="[
          {
            'left-1/2 top-1/4 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white shadow-xl':
              !fullscreen,
          },
        ]"
      >
        <header
          v-if="title && !fullscreen"
          class="flex items-center justify-between border-b p-4"
        >
          <div class="text-xl font-bold text-gray-700">
            {{ title }}
          </div>
          <button
            v-if="showClose"
            class="text-bold rounded bg-red-100 p-2 px-4 text-red-600 transition-all duration-100 hover:bg-red-200"
            @click="$emit('close')"
          >
            X
          </button>
        </header>
        <div :class="[{ 'p-4 py-6': !fullscreen }]">
          <slot />
        </div>
      </div>
    </div>
  </template>
</template>
