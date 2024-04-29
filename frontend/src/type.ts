export interface CaptionList {
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
