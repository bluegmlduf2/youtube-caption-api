export interface IYoutube {
  title: string
  thumbnailUrl: string
  duration: string
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
