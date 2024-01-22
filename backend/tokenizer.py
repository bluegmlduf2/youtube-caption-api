import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# NLTK 리소스 다운로드
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")


def tokenize_text(text):
    """문장을 토큰화합니다."""
    return word_tokenize(text)


def remove_stopwords(tokens):
    """토큰에서 불용어를 제거합니다."""
    english_stopwords = stopwords.words("english")
    return [token for token in tokens if token not in english_stopwords]


def filter_pos(tokens):
    """지정된 품사에 해당하는 토큰만 필터링합니다."""
    # 중요한 품사 태그 정의
    IMPORTANT_POS_TAGS = [
        "NN",
        "NNS",
        "NNP",
        "NNPS",  # ~명사
        "VB",
        "VBD",
        "VBG",
        "VBN",
        "VBP",
        "VBZ",  # ~동사
        "JJ",
        "JJR",
        "JJS",  # ~형용사
        "RB",
        "RBR",
        "RBS",  # ~부사
    ]
    tagged_tokens = pos_tag(tokens)
    return [word for word, tag in tagged_tokens if tag in IMPORTANT_POS_TAGS]


def get_tokenized_words(text_list):
    """주어진 텍스트 리스트에서 핵심 단어를 추출합니다."""
    try:
        key_words = []

        for text in text_list:
            tokens = tokenize_text(text)
            tokens_without_stopwords = remove_stopwords(tokens)
            filtered_words = filter_pos(tokens_without_stopwords)

            key_words.append(
                {"1": text, "2": filtered_words}
            )  # 필터링된 단어과 문장을 key_words 리스트에 추가합니다.

        return key_words
    except Exception as e:
        print(f"에러 : {e}")
