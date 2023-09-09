from preprocessing import preprocessing_data, lemmatizing, stemming

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
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import VotingClassifier

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

X_train, X_test, y_train, y_test = train_test_split(new_texts, level_ratings, test_size=0.2, random_state=42,
                                                    stratify=level_ratings)

# -----SGD Classifier-----
print('SGD Classifier')
sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                (
                    'clf',
                    SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=1000, tol=None)),
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

# -----Support Vector Classifier-----
print('Support Vector Classifier')
svc = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SVC(kernel='linear', C=1.0, random_state=42, max_iter=1000)),
                ])
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))

# -----Passive Aggressive Classifier-----
print('Passive Aggressive Classifier')
pac = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', PassiveAggressiveClassifier(max_iter=1000, random_state=42, tol=None)),
                ])
pac.fit(X_train, y_train)
y_pred = pac.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))

# -----Voting Classifier-----
print('Voting Classifier')
estimators = [('sgd',
               SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=1000, tol=None)),
              ('lr', LogisticRegression(n_jobs=1, C=1e5, max_iter=1000)),
              ('pa', PassiveAggressiveClassifier(max_iter=1000, random_state=42, tol=None))]

voting = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', VotingClassifier(estimators=estimators, voting='hard')),
                   ])
voting.fit(X_train, y_train)
y_pred = voting.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred, target_names=level_ratings.unique(), zero_division=0))
