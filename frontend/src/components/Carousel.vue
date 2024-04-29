<script setup lang="ts">
import type { IYoutube } from '@/type'

defineProps<{
  youtubeInfo: IYoutube
}>()
// https://swiperjs.com/vue
// import Swiper core and required modules
import { Navigation, Pagination, A11y } from 'swiper/modules'

// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue'

// Import Swiper styles
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const onSwiper = (swiper: any) => {
  console.log(swiper)
}
const onSlideChange = (swiper: any) => {
  console.log('slide change')
  console.log(swiper.activeIndex)
}
</script>

<template>
  <swiper
    class="h-56"
    :modules="[Navigation, Pagination, A11y]"
    :slides-per-view="1"
    :space-between="30"
    navigation
    :pagination="{ clickable: true }"
    :scrollbar="{ draggable: true }"
    @swiper="onSwiper"
    @slideChange="onSlideChange"
  >
    <swiper-slide v-for="(caption, i) of youtubeInfo.captionList" :key="i">
      <div class="flex justify-center items-center h-full">
        <div>
          <div>{{ caption.origin.sentence }}</div>
          <div>{{ caption.target.sentence }}</div>
        </div>
      </div>
    </swiper-slide>
  </swiper>
</template>

<style scoped></style>
