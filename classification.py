from cleaning import preprocessing_data, lemmatizing, stemming

import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression

data = pd.read_excel('data.xlsx')
ids = data['Id']
texts = data['pr_txt']
categories = data['Категория']
level_ratings = data['Уровень рейтинга']

stem = False
lem = False

new_texts = []
for text in texts:
    tmp = preprocessing_data(text)
    if stem:
        tmp = stemming(tmp)
    if lem:
        tmp = lemmatizing(tmp)
    new_texts.append(tmp)

X_train, X_test, y_train, y_test = train_test_split(new_texts, level_ratings, test_size=0.2, random_state=42)

# -----Naive Bayes Classifier-----
print('Naive Bayes Classifier')
nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
               ])
nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))

# -----Linear Support Vector Machine-----
print('Linear Support Vector Machine')
sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                (
                'clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=1000, tol=None)),
                ])
sgd.fit(X_train, y_train)
y_pred = sgd.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))

# -----Logistic Regression-----
print('Logistic Regression')
logreg = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', LogisticRegression(n_jobs=1, C=1e5, max_iter=1000)),
                   ])
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))
