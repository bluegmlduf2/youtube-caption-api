export interface IAudio {
  selectedAudio: string
  audioList: Caption[]
}

export interface IYoutube {
  title: string
  thumbnailUrl: string
  duration: string
  desc: string
  captionList: Caption[]
}

export interface Caption {
  origin: {
    sentence: string
    words: string[]
  }
  target: {
    sentence: string
    words: string[]
  }
}
