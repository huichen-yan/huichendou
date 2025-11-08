
import os
import numpy as np
import pandas as pd
import random
import copy

from huichen_dou.dou_2 import card_prepare, code_
from huichen_dou.bidding import get_cards
from Alphadou.baseline.SLModel import BidModel
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# 全局变量，只在第一次导入时加载
_model_cache = {}
_data_loaded = None
_scaler = None
_X_train = None


def s12(t):
    try:
        t = t[0]
    except:
        pass
    return t


def _initialize_model(model):
    """Initialize the model and data, execute only once"""
    global _data_loaded, _scaler, _X_train, _model_cache

    if not _data_loaded:
        _scaler = StandardScaler()

        data = pd.read_excel(r"C:\Users\86131\Desktop\python online\networks\code_card_data.xlsx")
        data = data.drop_duplicates(subset=data.columns[:54].tolist())
        data = data.to_numpy()

        data1 = data[:, :]
        X = data1[:4000, :54]
        _X_train = _scaler.fit_transform(X)
        _data_loaded = True

    if model not in _model_cache:
        if model == "0.3_64":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.3_64\model\data_03_64_26.keras')
        elif model == "0.3_128":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.3_128\model\data_03_128_25.keras')
        elif model == "0.4_64":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.4_64\model\data_04_64_38.keras')
        elif model == "0.4_128":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.4_128\model\data_04_128_28.keras')
        elif model == "0.4_64":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.2_64\model\data_02_64_13.keras')
        elif model == "0.4_128":
            _model_cache[model] = load_model(
                r'C:\Users\86131\Desktop\python online\networks\0.2_128\model\data_02_128_28.keras')
        else:
            e = Exception(f"There is no {model} model")
            raise e
    return _model_cache[model], _scaler

    # if model == "0.3_64":
    #     _loaded_model = load_model(r'C:\Users\86131\Desktop\python online\networks\0.3_64\model\data_03_64_26.keras')
    # elif model == "0.3_128":
    #     _loaded_model = load_model(r'C:\Users\86131\Desktop\python online\networks\0.3_128\model\data_03_128_25.keras')
    # else:
    #     e = Exception(f"There is no {model} model")
    #     raise e


def bidding3_alphadou(card):
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

    card_ = transform_card(card)
    _score_ = alphadou_bidding(BidModel.predict_score(card_))

    return _score_


def bidding3_traingdata(card, agent):
    def my_bidding1(c0):
        # Ensure that the model has been initialized
        _model, _scaler = _initialize_model(agent)
        code = code_(c0).code_one_vector()
        code_numpy = np.array([code])
        test = _scaler.transform(code_numpy)
        k = _model.predict(test, verbose=0)  # verbose=0 close the prediction progress bar
        y_pred = np.argmax(k, axis=1)
        return y_pred

    _score = my_bidding1(card)
    return int(_score)


def bidding3_sommodel(card):
    import joblib
    som_model = joblib.load(r'C:\Users\86131\Desktop\python online\networks\som_model.pkl')
    scaler_model = joblib.load(r'C:\Users\86131\Desktop\python online\networks\scaler.pkl')
    neuron_labels = joblib.load(r'C:\Users\86131\Desktop\python online\networks\neuron_labels.pkl')

    code = code_(card).code_one_vector()
    code_numpy = np.array([code])
    new_data_scaled = scaler_model.transform(code_numpy)
    winner = som_model.winner(new_data_scaled[0])
    if winner in neuron_labels:
        return int(neuron_labels[winner])
    else:
        return random.choice([0, 1, 2, 3])


class bidding3_choose_agent:
    def __init__(self, a, b, c, dp):
        self.a = a
        self.b = b
        self.c = c
        self.dp = dp

    def choose_agent(self, agent_a="local", agent_b="local", agent_c="local"):
        def bidding_agent(card, agent):
            if agent == "local":
                point = s12(get_cards.expoint(get_cards.total_point(card).exact_point()))
            elif agent == "random":
                point = random.choice([0, 1, 2, 3])
            elif agent == "alphadou":
                point = bidding3_alphadou(card)
            elif agent == "som":
                point = bidding3_sommodel(card)
            elif agent == "0.3_64" or agent == "0.3_128" or agent == "0.4_64" or agent == "0.4_128" or agent == "0.2_64" or agent == "0.2_128":
                point = bidding3_traingdata(card, agent)
            else:
                e = Exception(f"There is no {agent} agent")
                raise e
            return point

        def add_dp(card, dp):
            card_ = copy.copy(card)
            for i in dp:
                card_.append(i)
            return card_

        # dicc = {
        #     "a": bidding_agent(self.a, agent_a),
        #     "b": bidding_agent(self.b, agent_b),
        #     "c": bidding_agent(self.c, agent_c)
        # }
        dicc = {}
        point_a = bidding_agent(self.a, agent_a)
        dicc["a"] = point_a
        if point_a == 3:
            a_ = add_dp(self.a, self.dp)
            b_ = copy.copy(self.b)
            c_ = copy.copy(self.c)
        else:
            point_b = bidding_agent(self.b, agent_b)
            if point_b == 3:
                dicc["b"] = point_b
                b_ = add_dp(self.b, self.dp)
                a_ = copy.copy(self.a)
                c_ = copy.copy(self.c)
            else:
                if point_b <= point_a:
                    point_b = 0
                dicc["b"] = point_b
                point_c = bidding_agent(self.c, agent_c)
                if point_c == 3:
                    dicc["c"] = point_c
                    c_ = add_dp(self.c, self.dp)
                    b_ = copy.copy(self.b)
                    a_ = copy.copy(self.a)
                else:
                    if point_c > point_b and point_c > point_a:
                        dicc["c"] = point_c
                        c_ = add_dp(self.c, self.dp)
                        b_ = copy.copy(self.b)
                        a_ = copy.copy(self.a)
                    else:
                        dicc["c"] = 0
                        if dicc["a"] > dicc["b"]:
                            a_ = add_dp(self.a, self.dp)
                            b_ = copy.copy(self.b)
                            c_ = copy.copy(self.c)
                        elif dicc["a"] < dicc["b"]:
                            b_ = add_dp(self.b, self.dp)
                            a_ = copy.copy(self.a)
                            c_ = copy.copy(self.c)
                        else:
                            a_ = copy.copy(self.a)
                            b_ = copy.copy(self.b)
                            c_ = copy.copy(self.c)
        # if dicc["b"] <= dicc["a"]:
        #     dicc["b"] = 0
        # if dicc['c'] <= dicc["a"] or dicc['c'] <= dicc["b"]:
        #     dicc["c"] = 0
        #
        # if dicc["a"] > dicc["b"] and dicc["a"] > dicc["c"]:
        #     for card in self.dp:
        #         self.a.append(card)
        # else:
        #     if dicc["b"] > dicc["c"]:
        #         for card in self.dp:
        #             self.b.append(card)
        #     else:
        #         for card in self.dp:
        #             self.c.append(card)

        card_value = card_prepare().card_value
        a = sorted(a_, key=lambda x: card_value[x])
        b = sorted(b_, key=lambda x: card_value[x])
        c = sorted(c_, key=lambda x: card_value[x])

        return a, b, c, dicc
