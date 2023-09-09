from joblib import load
import numpy as np
from preprocessing import preprocessing_data


def load_model(model_filename):
    model = load(model_filename)
    return model


def predict_class_and_get_word_weights(text, model):
    predicted_class = model.predict([text])[0]
    class_index = np.where(model.classes_ == predicted_class)[0][0]
    coef = model.named_steps['clf'].coef_[class_index]
    feature_names = model.named_steps['vect'].get_feature_names_out()
    input_words = text.split()
    word_coef_dict = {word: coef[np.where(feature_names == word)[0][0]] for word in input_words if
                      word in feature_names}

    return predicted_class, word_coef_dict


def normalize_word_weights(word_weights):
    min_weight = min(word_weights.values())
    max_weight = max(word_weights.values())
    target_min = -1
    target_max = 1

    normalized_word_weights = {}
    for word, weight in word_weights.items():
        normalized_weight = ((weight - min_weight) / (max_weight - min_weight)) * (target_max - target_min) + target_min
        normalized_word_weights[word] = normalized_weight

    return normalized_word_weights


def solution(text):
    model_filename = 'models/logistic_regression_classifier.joblib'
    loaded_model = load_model(model_filename)
    text = preprocessing_data(text)
    predicted_class, word_weights = predict_class_and_get_word_weights(text, loaded_model)

    normalized_word_weights = normalize_word_weights(word_weights)
    result_dict = {}
    for word, weight in normalized_word_weights.items():
        result_dict[word] = weight
    return predicted_class, result_dict


def get_class(text):
    target_class, _ = solution(text)
    return target_class
