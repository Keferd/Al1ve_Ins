import re
from pymystem3 import Mystem
from tqdm.auto import tqdm
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize

stemmer = SnowballStemmer("russian")
mystem = Mystem()

russian_stopwords = stopwords.words("russian")
russian_stopwords.extend(['…', '«', '»', '...', 'т.д.', 'т', 'д'])


def stemming(texts):
    stemmed_texts_list = []
    for text in tqdm(texts):
        try:
            tokens = word_tokenize(text)
            stemmed_tokens = [stemmer.stem(token) for token in tokens if token not in russian_stopwords]
            text = " ".join(stemmed_tokens)
            stemmed_texts_list.append(text)
        except Exception as e:
            print(e)

    return stemmed_texts_list


def lemmatizing(texts):
    lemm_texts_list = []
    for text in tqdm(texts):
        try:
            text_lem = mystem.lemmatize(text)
            tokens = [token for token in text_lem if token != ' ' and token not in russian_stopwords]
            text = " ".join(tokens)
            lemm_texts_list.append(text)
        except Exception as e:
            print(e)

    return lemm_texts_list


def get_subinfo(text, start_keyword, end_keyword):
    start_index = text.find(start_keyword)
    end_index = text.find(end_keyword)
    if start_index != -1 and end_index != -1:
        return text[start_index + len(start_keyword):end_index]
    else:
        return text


def get_agency(text):
    agency = None
    if 'pr@ratings.ru' in text:
        agency = 'нкр'
    elif 'акра' in text:
        agency = 'акра'
    elif '@ra-national.ru' in text:
        agency = 'нра'
    elif 'эксперт ра' in text:
        agency = 'ра'
    return agency


def clearing_nkr(text):
    cv = get_subinfo(text, 'резюме', 'информация о рейтингуемом лице')
    info = get_subinfo(text, 'факторы, определившие уровень боск:', 'регуляторное раскрытие')
    info = ' '.join(info.split()[1:])
    if cv is not None and info is not None:
        content = cv + ' ' + info
        content = re.sub(r'\b\w+\.ru\b', '<rating>', content)
        return content
    return text


def clearing_nra(text):
    info = get_subinfo(text, '(далее – нра, агентство)', 'дополнительная информация')
    if info is not None:
        return info
    return text


def clearing_akra(text):
    end_index = -1
    if 'регуляторное раскрытие' in text:
        end_index = text.find('регуляторное раскрытие')
    if 'рейтинги выпусков' in text:
        end_index = text.find('рейтинги выпусков')
    return text[:end_index]


def clearing_ra(text):
    info = get_subinfo(text, ' ', 'контакты для сми')
    if info is not None:
        return info
    return text


def preprocessing_data(text):
    text = text.lower()

    agency = get_agency(text)
    if agency == 'ра':
        text = clearing_ra(text)
    elif agency == 'нра':
        text = clearing_nra(text)
    elif agency == 'акра':
        text = clearing_akra(text)
    elif agency == 'нкр':
        text = clearing_nkr(text)

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[^\w\d])-|-(?=[^\w\d])|[^\w\d\s-]', '', text)
    text = re.sub(r'\d+', '<number>', text)
    text = re.sub(r'\b\d{1,2}\s\w+\s\d{4}\b', '<date>', text)
    text = re.sub(r'pr@raexpert\.ru', '', text)
    text = re.sub(r'\+\d{1,2}\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub('rating', '<rating>', text)

    tokens = text.split()
    for i in range(len(tokens)):
        token = tokens[i]
        start_index = token.find("<")
        end_index = token.find(">") + 1
        if token == agency:
            tokens[i] = "<agency>"
        elif token in ['a', 'aa', 'aaa', 'b', 'bb', 'bbb', 'c', 'cc', 'ccc'] or 'ru' in token:
            tokens[i] = '<rating>'
        elif token == "-":
            tokens[i] = ""
        elif start_index != -1:
            if start_index != 0:
                tokens[i] = token[start_index:end_index]

    text = (' '.join(tokens))

    return text
