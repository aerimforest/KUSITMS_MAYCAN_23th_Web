import os
import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.models import load_model
# 저장된 모델 가져와서 예측 + 예측값 csv 파일로 저장

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
model = load_model("common/lstm_model.h5")
tokenizer = Tokenizer()
MAX_SEQUENCE_LENGTH = 60


def preprocessing(talk, okt, delete_word):
    word_talk = okt.nouns(talk)
    word_talk = [token for token in word_talk if not token in delete_word]

    return word_talk


def get_nounList(data):
    delete_word = ["이", "그", "데", "음", "제", "의", "좀", "거"]
    okt = Okt()
    noun_list = []

    for d in data["word"]:
        if type(d) == str:
            noun_list.append(preprocessing(d, okt, delete_word))
        else:
            noun_list.append([])

    return noun_list


def predict(filename):
    df_new = pd.read_csv(f"/data/{filename}.csv")

    X_new = df_new.drop(["index"], axis=1)
    new_noun_list = get_nounList(X_new)
    new_txt_sequences = tokenizer.texts_to_sequences(new_noun_list)

    data_new = pad_sequences(new_txt_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding="post")
    score_array = np.array(model.predict(data_new))
    median_array = np.median(score_array, axis=0)
    mean_array = score_array.mean(axis=0)

    value_list = []
    for score in score_array:
        if score[1] > mean_array[1]:
            value_list.append(1)
        elif score[0] > median_array[0]:
            value_list.append(0)
        else:
            value_list.append(2)

    df_value = pd.DataFrame(value_list, columns=["value"])
    df_result = pd.concat([df_new, df_value], axis=1)

    df_result.to_csv(f"/data/{filename}_result.csv")


# predict(FILE_NAME)