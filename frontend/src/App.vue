<script setup lang="ts">
import Carousel from './components/Carousel.vue'
import UserButton from './components/UserButton.vue'
import axios from 'axios'
import { ref } from 'vue'
import type { IYoutube } from '@/type'

// TODO 임시로 넣음
const searchWord = ref('https://www.youtube.com/watch?v=0lMC_eZZtWA&t=3s&ab_channel=BestEverFoodReviewShow')
const errMsg = ref()
const isDisabled = ref(false)
const youtubeInfo = ref<IYoutube>()

async function submitForm() {
  errMsg.value=null
  const serverUrl=import.meta.env.VITE_API_URL
  const youtubeUrl = new URLSearchParams(searchWord.value.split('?')[1]).get('v')
  const path = `${serverUrl}/caption?language=ko&url=${youtubeUrl}`
  isDisabled.value = true

  await axios
    .get(path,{
      timeout: 30000,
    })
    .then((res) => {
      youtubeInfo.value = res.data
    })
    .catch((error) => {
      if(error.response?.data){
        errMsg.value = error.response.data.message
        return
      }
      errMsg.value = error.message
    })
    .finally(() => {
      isDisabled.value = false
    })
}
</script>

<template>
  <header class="w-screen bg-color2 py-5 flex justify-center">
    <form class="w-full max-w-screen-lg mx-10" @submit.prevent="submitForm">
      <div class="relative">
        <div
          class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none text-color4"
        >
          <span class="material-symbols-rounded">search</span>
        </div>
        <input
          v-model="searchWord"
          type="search"
          class="block w-full p-4 pr-24 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-color1 focus:border-color1"
          placeholder="Input Youtube Url"
          required
        />
        <UserButton :type="'submit'" :disabled="isDisabled">Search</UserButton>
      </div>
    </form>
  </header>
  <main class="max-w-screen-xl mx-auto">
    <section v-if="errMsg" class="mt-5 text-red-500 px-3">
      <span class="font-bold">{{ errMsg }}</span>
    </section>
    <h2 class="text-2xl mt-7 mb-3">동영상정보</h2>
    <section class="flex bg-color1 rounded-xl drop-shadow-2xl p-5">
      <div>
        <img alt="Vue logo" class="logo" :src="youtubeInfo?.thumbnailUrl" width="125" height="125" />
      </div>
      <div class="ml-5">
        <div>{{ youtubeInfo?.title }}</div>
        <div>{{ youtubeInfo?.duration }}</div>  
        <UserButton :type="'submit'" :disabled="isDisabled">Download</UserButton>
      </div>
    </section>
    <h2 class="text-2xl mt-7 mb-3">영어문장</h2>
    <section class="bg-color1 rounded-xl drop-shadow-2xl p-5">
      <Carousel v-if="youtubeInfo" :youtubeInfo="youtubeInfo" />
      <UserButton :type="'submit'" :disabled="isDisabled">Download</UserButton>
    </section>
  </main>
</template>

<style scoped></style>
