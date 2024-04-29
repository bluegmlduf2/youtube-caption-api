<script setup lang="ts">
import type { PropType } from 'vue'

defineProps({
  type: { type: String as PropType<'button' | 'submit'>, default: 'button' },
  disabled: { type: Boolean, default: false }
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="text-white absolute end-2.5 bottom-2.5 bg-color3 hover:bg-color3 focus:ring-4 focus:outline-none focus:ring-color1 font-medium rounded-lg text-sm px-4 py-2 disabled:bg-red-400"
  >
    <slot /><span v-if="disabled">...</span>
  </button>
</template>
