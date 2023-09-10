import re
import pymorphy2
from tqdm.auto import tqdm
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize, download

stemmer = SnowballStemmer("russian")
download('stopwords')
russian_stopwords = stopwords.words("russian")
russian_stopwords.extend(
    ['это', 'как', 'так', 'и', 'в', 'над', 'к', 'до', 'не', 'на', 'но', 'за', 'то', 'с', 'ли', 'а', 'во', 'от', 'со',
     'для', 'о', 'же', 'ну', 'вы', 'бы', 'что', 'кто', 'он', 'она', 'оно', 'из-за'])


def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in russian_stopwords]
    return " ".join(filtered_tokens)


def stemming(texts):
    stemmed_texts_list = []
    for text in tqdm(texts.split()):
        try:
            tokens = word_tokenize(text)
            stemmed_tokens = [stemmer.stem(token) for token in tokens]
            text = " ".join(stemmed_tokens)
            stemmed_texts_list.append(text)

        except Exception as e:
            print(e)

    new_text = " ".join(stemmed_texts_list)
    return new_text


def lemmatizing(texts):
    morph = pymorphy2.MorphAnalyzer()
    lemm_texts_list = []
    for text in tqdm(texts):
        try:
            tokens = word_tokenize(text)
            text_lem = [morph.parse(token)[0].normal_form for token in tokens]
            text = " ".join(text_lem)
            lemm_texts_list.append(text)
        except Exception as e:
            print(e)

    new_text = " ".join(lemm_texts_list)
    return new_text


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
    text = remove_stopwords(text)

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
    text = re.sub(r'\b\d{1,2}\s\w+\s\d{4}\b', '<дата>', text)
    text = re.sub(r'\d+', '<число>', text)
    text = re.sub(r'pr@raexpert\.ru', '', text)
    text = re.sub(r'\+\d{1,2}\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub('rating', '<рейтинг>', text)

    tokens = text.split()
    for i in range(len(tokens)):
        token = tokens[i]

        if token == agency:
            tokens[i] = "<агентство>"
        elif token in ['a', 'aa', 'aaa', 'b', 'bb', 'bbb', 'c', 'cc', 'ccc'] or 'ru' in token:
            tokens[i] = '<рейтинг>'
        elif token == "-":
            tokens[i] = ""

        start_index = token.find("<")
        end_index = token.find(">") + 1
        if start_index not in [-1, 0]:
            tokens[i] = token[start_index:end_index]

    text = (' '.join(tokens))

    return text
