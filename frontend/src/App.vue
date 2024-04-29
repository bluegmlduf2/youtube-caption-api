<script setup lang="ts">
import Carousel from './components/Carousel.vue'
import UserButton from './components/UserButton.vue'
import axios from 'axios'
import { ref } from 'vue'
import type { CaptionList } from '@/type'

const searchWord = ref()
const errMsg = ref()
const isDisabled = ref(false)
const captionList = ref<CaptionList>()

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
      captionList.value = res.data
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
          class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-color1 focus:border-color1"
          placeholder="Input Youtube Url"
          required
        />
        <UserButton :type="'submit'" :disabled="isDisabled">Search</UserButton>
      </div>
    </form>
  </header>
  <main class="max-w-screen-xl mx-auto">
    <section class="mt-5 text-red-500">
      <span class="font-bold">{{ errMsg }}</span>
    </section>
    <section class="flex bg-color1 mt-5 rounded-xl drop-shadow-2xl p-5">
      <div>
        <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
      </div>
      <div class="ml-5">
        <h2 class="text-2xl">유튜브제목</h2>
        <div>상세정보</div>
        <div>
          <UserButton :type="'submit'" :disabled="isDisabled">Download</UserButton>
        </div>
      </div>
    </section>
    <section class="bg-color1 mt-10 rounded-xl drop-shadow-2xl p-5">
      <h2 class="text-2xl">영어문장..</h2>
      <Carousel v-if="captionList" :captionList="captionList" />
      <UserButton :type="'submit'" :disabled="isDisabled">Download</UserButton>
    </section>
  </main>
</template>

<style scoped></style>
