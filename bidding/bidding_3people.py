from huichen_dou import tf_config
import os
import numpy as np
import pandas as pd
import copy

from huichen_dou.dou_2 import card_prepare, code_
from huichen_dou.bidding import get_cards
from Alphadou.baseline.SLModel import BidModel
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# 全局变量，只在第一次导入时加载
_loaded_model = None
_scaler = None
_X_train = None


def s12(t):
    try:
        t = t[0]
    except:
        pass
    return t


def bidding3(a, b, c, dp):
    dicc = {}

    point_a = s12(get_cards.expoint(get_cards.total_point(a).exact_point()))
    dicc["a"] = point_a
    if point_a == 3:
        print(dicc)
        for card in dp:
            a.append(card)
    else:
        point_b = s12(get_cards.expoint(get_cards.total_point(b).exact_point()))
        if point_b == 3:
            dicc["b"] = point_b
            print(dicc)
            for card in dp:
                b.append(card)
        else:
            if point_b <= point_a:
                point_b = 0
            dicc["b"] = point_b
            point_c = s12(get_cards.expoint(get_cards.total_point(c).exact_point()))
            if point_c == 3:
                dicc["c"] = point_c
                print(dicc)
                for card in dp:
                    c.append(card)
            else:
                if point_c > point_b and point_c > point_a:
                    dicc["c"] = point_c
                    print(dicc)
                    for card in dp:
                        c.append(card)
                else:
                    dicc["c"] = 0
                    print(dicc)
                    if dicc["a"] > dicc["b"]:
                        for card in dp:
                            a.append(card)
                    else:
                        for card in dp:
                            b.append(card)

    card_value = card_prepare().card_value
    a = sorted(a, key=lambda x: card_value[x])
    b = sorted(b, key=lambda x: card_value[x])
    c = sorted(c, key=lambda x: card_value[x])

    return a, b, c, dicc


def _initialize_model():
    """Initialize the model and data, execute only once"""
    global _loaded_model, _scaler, _X_train

    if _loaded_model is None:
        _loaded_model = load_model(r'C:\Users\86131\Desktop\python online\networks\0.3_64\model\data_03_64_26.keras')
        _scaler = StandardScaler()

        data = pd.read_excel(r"C:\Users\86131\Desktop\python online\networks\code_card_data.xlsx")
        data = data.drop_duplicates(subset=data.columns[:54].tolist())
        data = data.to_numpy()

        data1 = data[:, :]
        X = data1[:4000, :54]
        _X_train = _scaler.fit_transform(X)


def bidding3_alphadou(a, b, c, dp):
    def transform_card(card0):
        card = copy.copy(card0)
        for i in range(len(card)):
            if card[i] == "B" or card[i] == "R":
                if card[i] == "B":
                    card[i] = "D"
                else:
                    card[i] = "X"
        c0 = ''.join(item for item in card)
        return c0
    def alphadou_bidding(_score):
        if _score <= -0.1:
            s = 0
        elif _score <= 0:
            s = 1
        elif _score <= 0.1:
            s = 2
        else:
            s = 3
        return s

    a_ = transform_card(a)
    b_ = transform_card(b)
    c_ = transform_card(c)

    dicc = {"a": alphadou_bidding(BidModel.predict_score(a_)),
            "b": alphadou_bidding(BidModel.predict_score(b_)),
            "c": alphadou_bidding(BidModel.predict_score(c_))}
    if dicc["b"] <= dicc["a"]:
        dicc["b"] = 0
    if dicc['c'] <= dicc["a"] or dicc['c'] <= dicc["b"]:
        dicc["c"] = 0

    if dicc["a"] > dicc["b"] and dicc["a"] > dicc["c"]:
        for card in dp:
            a.append(card)
    else:
        if dicc["b"] > dicc["c"]:
            for card in dp:
                b.append(card)
        else:
            for card in dp:
                c.append(card)

    card_value = card_prepare().card_value
    a = sorted(a, key=lambda x: card_value[x])
    b = sorted(b, key=lambda x: card_value[x])
    c = sorted(c, key=lambda x: card_value[x])

    return a, b, c, dicc


def bidding3_traingdata(a, b, c, dp):
    # Ensure that the model has been initialized
    def my_bidding1(c0):
        _initialize_model()
        code = code_(c0).code_one_vector()
        code_numpy = np.array([code])
        test = _scaler.transform(code_numpy)
        k = _loaded_model.predict(test, verbose=0)  # verbose=0 close the prediction progress bar
        y_pred = np.argmax(k, axis=1)
        return y_pred


    # a_code = code_(a).code_one_vector()
    # b_code = code_(b).code_one_vector()
    # c_code = code_(c).code_one_vector()
    #
    # code_numpy_a = np.array([a_code])
    # code_numpy_b = np.array([b_code])
    # code_numpy_c = np.array([c_code])
    #
    # # Use a global scaler for transformation
    # test_a = _scaler.transform(code_numpy_a)
    #
    # # Using a global model for prediction
    # k = _loaded_model.predict(test, verbose=0)  # verbose=0 close the prediction progress bar
    # y_pred = np.argmax(k, axis=1)

    dicc = {"a": int(my_bidding1(a)), "b": int(my_bidding1(b)), "c": int(my_bidding1(c))}

    if dicc["b"] <= dicc["a"]:
        dicc["b"] = 0
    if dicc['c'] <= dicc["a"] or dicc['c'] <= dicc["b"]:
        dicc["c"] = 0

    if dicc["a"] > dicc["b"] and dicc["a"] > dicc["c"]:
        for card in dp:
            a.append(card)
    else:
        if dicc["b"] > dicc["c"]:
            for card in dp:
                b.append(card)
        else:
            for card in dp:
                c.append(card)

    card_value = card_prepare().card_value
    a = sorted(a, key=lambda x: card_value[x])
    b = sorted(b, key=lambda x: card_value[x])
    c = sorted(c, key=lambda x: card_value[x])

    return a, b, c, dicc

# def bidding3_traingdata(a, b, c, dp):
#     import numpy as np
#     import pandas as pd
#     from sklearn.preprocessing import StandardScaler
#     from tensorflow.keras.models import load_model
#     loaded_model = load_model(r'C:\Users\86131\Desktop\python online\networks\my_model.keras')
#     scaler = StandardScaler()
#
#     data = pd.read_excel(r"C:\Users\86131\Desktop\python online\networks\code_card_data.xlsx")
#     data = data.drop_duplicates(subset=data.columns[:54].tolist())
#     data = data.to_numpy()
#
#     data1 = data[:, :]
#     X = data1[:4000, :54]
#
#     a_code = code_(a).code_one_vector()
#     b_code = code_(b).code_one_vector()
#     c_code = code_(c).code_one_vector()
#     code_numpy = np.array([a_code, b_code, c_code])
#     # print(len(a_code))
#     # print(a_code)
#     train = scaler.fit_transform(X)
#     test = scaler.transform(code_numpy)
#     k = loaded_model.predict(test)
#     y_pred = np.argmax(k, axis=1)
#     dicc = {"a": int(y_pred[0]), "b": int(y_pred[1]), "c": int(y_pred[2])}
#
#     if dicc["b"]<=dicc["a"]:
#         dicc["b"]=0
#     if dicc['c']<=dicc["a"] or dicc['c']<=dicc["b"]:
#         dicc["c"]=0
#
#     if dicc["a"]>dicc["b"] and dicc["a"]>dicc["c"]:
#         for card in dp:
#             a.append(card)
#     else:
#         if dicc["b"]>dicc["c"]:
#             for card in dp:
#                 b.append(card)
#         else:
#             for card in dp:
#                 c.append(card)
#
#     card_value = card_prepare().card_value
#     a = sorted(a, key=lambda x: card_value[x])
#     b = sorted(b, key=lambda x: card_value[x])
#     c = sorted(c, key=lambda x: card_value[x])
#
#     return a, b, c, dicc
