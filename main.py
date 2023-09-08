import pandas as pd
import re

data = pd.read_excel('data.xlsx')
ids = data['Id']
texts = data['pr_txt']
categories = data['Категория']
level_ratings = data['Уровень рейтинга']


def get_subinfo(text, start_keyword, end_keyword):
    start_index = text.find(start_keyword) + 1
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


def clear_nkr(text):
    cv = get_subinfo(text, 'резюме', 'информация о рейтингуемом лице')
    info = get_subinfo(text, 'факторы, определившие уровень боск:', 'регуляторное раскрытие')
    info = ' '.join(info.split()[1:])
    if cv is not None and info is not None:
        new_text = cv + ' ' + info
        new_text = re.sub(r'\b\w+\.ru\b', '<rating>', new_text)
        return new_text
    return text


def clear_nra(text):
    info = get_subinfo(text, '(далее – нра, агентство)', 'дополнительная информация')
    if info is not None:
        return info
    return text


def clear_akra(text):
    end_index = -1
    if 'регуляторное раскрытие' in text:
        end_index = text.find('регуляторное раскрытие')
    if 'рейтинги выпусков' in text:
        end_index = text.find('рейтинги выпусков')
    return text[:end_index]


def clear_ra(text):
    info = get_subinfo(text, ' ', 'контакты для сми')
    if info is not None:
        return info
    return text


def clear_data(text):
    text = text.lower()

    agency = get_agency(text)
    print(agency)
    if agency == 'ра':
        text = clear_ra(text)
    elif agency == 'нра':
        text = clear_nra(text)
    elif agency == 'акра':
        text = clear_akra(text)
    elif agency == 'нкр':
        text = clear_nkr(text)

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[^\w\d])-|-(?=[^\w\d])|[^\w\d\s-]', '', text)
    text = re.sub(r'\d+', '<number>', text)
    text = re.sub(r'\b\d{1,2}\s\w+\s\d{4}\b', '<date>', text)
    text = re.sub(agency, '<agency>', text)
    text = re.sub(r'pr@raexpert\.ru', '', text)
    text = re.sub(r'\+\d{1,2}\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub('rating', '<rating>', text)
    tokens = text.split()
    text = (' '.join(tokens))
    return text


print(clear_data(texts[728]))
