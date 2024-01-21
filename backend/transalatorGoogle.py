from googletrans import Translator


def get_translated_text(textList, targetLanguage):
    try:
        if textList:
            translator = Translator()
            translations = translator.translate(textList, dest=targetLanguage)
            print(1)
            return 
            # load_dotenv()
            # client_id = os.environ.get("NAVER_CLIENT_KEY")
            # client_secret = os.environ.get("NAVER_CLIENT_SECRET")
            # encText = urllib.parse.quote(text)
            # data = "source=en&target=" + targetLanguage + "&text=" + encText
            # url = "https://openapi.naver.com/v1/papago/n2mt"
            # request = urllib.request.Request(url)
            # request.add_header("X-Naver-Client-Id", client_id)
            # request.add_header("X-Naver-Client-Secret", client_secret)
            # response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            # rescode = response.getcode()
            # if rescode == 200:
            #     response_body = json.loads(response.read())
            #     translatedText = response_body["message"]["result"]["translatedText"]
            #     return translatedText
            # else:
            #     print("Error Code:" + rescode)
            #     raise Exception("translate error")
    except Exception as err:
        print(err)
