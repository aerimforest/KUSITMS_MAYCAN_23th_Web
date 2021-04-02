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
import json
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from common.models import Profile
import getpass # 현재 로그인된 사용자 이름 추출
from os.path import basename # 파일명 추출
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# "kakao" 자리에 txt 파일 확장자명 제외한 이름을 str 형태로 입력
# FILE_NAME = dirname(Profile.objects.filter(name = getpass.getuser()).values('kakaoTalk')) # user가 넣은 파일명
USER_NAME = Profile.objects.filter(name = getpass.getuser()).values('kakaoName')
global FILE_NAME

# >>> csv 파일 만들기

def check_line(line):
    str1, str2, str3 = "", "", ""
    pass_words = ["---------------", "저장한 날짜 : ", "님을 초대하였습니다.", "님과 카카오톡 대화", "님이 나갔습니다."]

    for pass_word in pass_words:
        if pass_word in line:
            str1 += "pass"

    for idx, l in enumerate(line):
        start = idx
        end = idx + 9

        if l == "[" and line[idx + 1] == "오" and line[idx + 3] == " ":
            try:
                check_num = int(line[idx + 5])
            except ValueError:
                end -= 1

            str1 += line[1:start - 2]
            str2 += line[start + 1: end]
            str3 += line[end + 1:-1]

    return str1, str2, str3


def create_list(lines):
    name_list, date_list, word_list = [], [], []

    for idx, line in enumerate(lines):
        name, date, word = check_line(line)
        if not name:
            word += line[:-1]

        name_list.append(name.strip())
        date_list.append(date.strip())
        word_list.append(word.strip())

    return name_list, date_list, word_list


def create_df(list1, list2, list3):
    df = pd.DataFrame({"name": list1, "date": list2, "word": list3})
    df.drop(df.loc[df["word"] == ""].index, inplace=True)
    df.replace("", None, inplace=True)
    df["index"] = [i for i in range(len(df))]
    result = df.set_index("index", drop=True)

    return result


def create_csv(filename):
    global FILE_NAME
    FILE_NAME = filename
    # open_txt = open(f"/data/{filename}.txt", "r")
    open_txt = open(f"media/{filename}.txt", "r")
    lines = open_txt.readlines()

    names, dates, words = create_list(lines)
    df = create_df(names, dates, words)

    # {filename} 앞까지 로컬에 맞게 저장할 경로 입력
    df.to_csv(f"media/{filename}.csv")


# >>> 머신러닝 결과값 비율로 나타내기

def init(filename):
    global df
    global name_list
    data = pd.read_csv(f'media/{filename}_result.csv')
    df = data.reindex(columns=['name', 'value', 'date', 'word'])
    df = df.sort_values(by=['name', 'value'])
    name_list = df["name"].drop_duplicates().tolist()


def get_nameRatio():
    df_nameRatio = df.groupby('name').size() / df['name'].count() * 100
    return df_nameRatio


def get_valueRatio(idx):
    df_value = df[df["value"].isin([idx])]
    df_valueRatio = df_value.groupby("name").size() / df_value["name"].count() * 100
    return df_valueRatio


def get_ratioJson(df_ratio):
    dict_ratio = df_ratio.to_dict()
    key_list = list(dict_ratio.keys())

    for name in name_list:
        if name not in key_list:
            dict_ratio[name] = 0

    json_ratio = json.dumps(dict_ratio, ensure_ascii=False)
    return json_ratio


def get_result(idx):
    """
    :param idx: 참여성=0, 창의성=1, 성실성="name", 기타=2
    :return: type 별 최종 비율을 json 형태로
    """
    if idx == "name":
        df_ratio = get_nameRatio()
    else:
        df_ratio = get_valueRatio(idx)
    return get_ratioJson(df_ratio)


def get_contribution(name, weight_list):
    """
    :param name: 로그인한 유저의 카카오톡 이름
    :param weight_list: 가중치 리스트 [참여성, 창의성, 성실성]
    :return: 최종 기여도 점수, 기준(모든 사람이 정확히 1/n 만큼 기여했을 때의 값)
    """
    value_list = [json.loads(get_result(idx))[name] for idx in range(2)]
    dict_name = get_nameRatio()
    value_list.append(dict_name[name])

    contribution_array = np.dot(np.array(value_list), np.array(weight_list))
    standard = 100 / len(dict_name)

    return float(contribution_array), standard


# >>> wordcloud 만들기

def create_noun_tags(data):
    text = ""
    for word in data["word"]:
        text += word

    noun_list = Okt().nouns(text)
    delete_word = ["이", "그", "데", "음", "저", "제", "의", "좀", "거", "것"]
    clean_noun_list = [noun for noun in noun_list if noun not in delete_word]

    counts = Counter(clean_noun_list)
    tags = counts.most_common(60)

    return tags


def create_wordcloud(filename, user_name, idx):
    data = pd.read_csv(f"media/{filename}_result.csv")

    data.name = data["name"].str.strip()
    user = user_name
    df_nameWord = data.loc[data.name == user]
    df_nameWord = df_nameWord[df_nameWord["value"].isin([idx])]

    font_path = "KOTRA_BOLD.otf"
    tags = create_noun_tags(df_nameWord)

    cloud = WordCloud(height=800, width=800,
                      font_path=font_path,
                      background_color="white")
    cloud = cloud.generate_from_frequencies(dict(tags))
    cloud.to_file(f"media/{filename}_value{idx}.jpg")


# >>> 함수 돌리기

# create_csv(FILE_NAME)  # txt 파일 csv 변환
# predict(FILE_NAME)  # 머신러닝으로 예측 (결과 파일: FILE_NAME_result.csv)

# value0 = get_result(0)  # 사람별 참여성 비율
# value1 = get_result(1)  # 사람별 창의성 비율
# value_name = get_result("name")  # 사람별 성실성 비율

# contribution, standard = get_contribution(USER_NAME, [0.3, 0.3, 0.4])  # 최종 기여도 점수, 기준

# # 워드클라우드 참여성, 창의성, 기타
# for i in range(3):
#     create_wordcloud(FILE_NAME, USER_NAME, i)
