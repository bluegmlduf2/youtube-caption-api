<script setup lang="ts">
import Carousel from './components/Carousel.vue'
import UserButton from './components/UserButton.vue'
import axios from 'axios'
import { ref } from 'vue'
import type { IYoutube } from '@/type'

const searchWord = ref('')
const errMsg = ref()
const isDisabled = ref(false)
const youtubeInfo = ref<IYoutube>()
const selectedAudioSrc = ref()
const selectedAudioType = ref()
const serverUrl=import.meta.env.VITE_API_URL

async function submitForm() {
  errMsg.value=null
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

    const pathautdio = `${serverUrl}/audio?url=${youtubeUrl}`

    await axios
    .get(pathautdio,{
      timeout: 30000,
      responseType: 'arraybuffer',  // 바이너리 데이터를 위해 responseType을 'arraybuffer'로 설정
      // JavaScript에서 Blob을 생성할 때, axios가 응답을 자동으로 JSON으로 변환하려 할 때 바이너리 데이터(예: 오디오 파일)를 적절히 처리하지 못해 문제가 발생할 수 있습니다. 
    })
    .then((res) => {
      selectedAudioType.value = res.headers['content-type']
      const audioFile =  new Blob([res.data], { type : selectedAudioType.value })
      selectedAudioSrc.value = URL.createObjectURL(audioFile)
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

async function downloadCaption() {
  const youtubeUrl = new URLSearchParams(searchWord.value.split('?')[1]).get('v')
  const pathdownload = `${serverUrl}/download?url=${youtubeUrl}`

  await axios
    .get(pathdownload,{
      timeout: 30000,
    })
    .then((res) => {
      const fileName = `${res.data.title+'_'+Math.floor(Date.now() / 1000)}.txt`
      const element = document.createElement('a');
      const captionList=res.data.captionList
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(captionList.join("\n")));
      element.setAttribute('download', fileName);
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
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
    
    <template v-if="youtubeInfo?.thumbnailUrl">
      <h2 class="text-2xl mt-7 mb-3 text-color4 ml-3">Video Information</h2>
      <section class="flex bg-color1 rounded-xl drop-shadow-2xl p-5">
        <div>
          <img class="w-44 min-w-40 rounded-md" alt="youtubethumbnail" :src="youtubeInfo.thumbnailUrl" />
        </div>
        <div class="ml-5 flex flex-col justify-between overflow-hidden">
          <div class="text-lg md:text-xl font-bold line-clamp-2">{{ youtubeInfo?.title }}</div>
          <div class="line-clamp-2">{{ youtubeInfo?.desc }}</div>
          <div class="mt-3">
            {{ youtubeInfo?.duration }}
            <UserButton :disabled="isDisabled" @click="downloadCaption">Caption Download</UserButton>
          </div>
        </div>
      </section>
    </template>
    
    <template v-if="youtubeInfo">
      <h2 class="text-2xl mt-7 mb-3 text-color4 ml-3">English Sentence</h2>
      <section class="bg-color1 rounded-xl drop-shadow-2xl p-5">
        <Carousel :youtubeInfo="youtubeInfo" />
      </section>
    </template>
    
    <template v-if="selectedAudioSrc">
      <h2 class="text-2xl mt-7 mb-3 text-color4 ml-3">Audio Playback</h2>
      <section class="bg-color1 rounded-xl drop-shadow-2xl p-5">
        <audio controls :src="selectedAudioSrc" :type="selectedAudioType" class="w-full"></audio>
      </section>
    </template>
  </main>
</template>


<style scoped></style>
