from googletrans import Translator


def get_translated_text(textList, targetLanguage):
    if textList:
        translator = Translator()
        translations = translator.translate(textList, dest=targetLanguage)
        return translations

