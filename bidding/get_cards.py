import random
import json
from huichen_dou.dou_2 import card_prepare
from collections import Counter, OrderedDict
from huichen_dou import dou_2
import copy

card_type = dou_2.enter_card_type().card_type
with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_2.json") as f:
    card_type1 = json.load(f)


# class get_cards:
#     def __init__(self):
#         self.cards = ['7', '8', '8', '8', '8', '9', '9', '9', '9', 'T', 'T', 'T', 'T', 'J', 'J', 'J',
#                       'J', 'Q', 'Q', 'Q', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', 'Q',
#                       'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A', '2', '2', '2', '2', 'B', 'R', '3', '3', '3', '3', '4',
#                       '4', '4', '4']
#         random.shuffle(self.cards)
#         self.wj1 = []
#         self.wj2 = []
#         self.dipai = None
#
#     def fapai(self):
#         def sort_cards(cards):
#             for i in range(17):
#                 cards[i] = int(card_prepare().card_value[cards[i]])
#             cards.sort()
#             for i in range(17):
#                 cards[i] = card_prepare().value_card[str(cards[i])]
#             return cards
#
#         for i in range(17):
#             self.wj1.append(self.cards[2 * i])
#             self.wj2.append(self.cards[2 * i + 1])
#         self.dipai = [self.cards[-3], self.cards[-2], self.cards[-1]]
#         sort_cards(self.wj1)
#         sort_cards(self.wj2)
#         return self.wj1, self.wj2, self.dipai


class current_combination:
    def __init__(self, cards):
        self.cards = cards
        self.a = dou_2.legal_action(self.cards, "").action_movement()
        self.a2 = sorted(list(self.a.keys()), key=len, reverse=True)
        # self.a2 = dict(sorted(self.a.items(), key=lambda item: len(item[0]), reverse=True))
        self.p_combin = []
        self.hand_count = Counter(cards)

    def find_combinations(self):
        def judge_current_combination(current_combination):
            s = 0
            for i in range(len(current_combination)):
                s += len(current_combination[i])
            if s == len(self.cards):
                return True
            else:
                return False

        def find_combinations(actions, current_combination, hand_count, index, l):
            """查找所有合法的出牌动作组合"""
            if index == len(actions) or l == len(self.cards):
                if judge_current_combination(current_combination):
                    self.p_combin.append(current_combination)
                return

            hand_count1 = copy.deepcopy(hand_count)
            count1 = Counter(actions[index])
            f = True
            for card, count in count1.items():
                hand_count1[card] = hand_count1[card] - count
                if hand_count1[card] < 0:
                    f = False
                    break
            if f:
                # 选择当前动作
                find_combinations(actions, current_combination + [actions[index]], hand_count1, index + 1,
                                  l + len(actions[index]))
            # 不选择当前动作
            find_combinations(actions, current_combination, hand_count, index + 1, l)

        find_combinations(self.a2, [], self.hand_count, 0, 0)
        return self.p_combin


class point_value1:
    def __init__(self, card):
        self.card = card
        self.a = current_combination(self.card).find_combinations()
        self.value = {}

    def find_value1(self):
        for cards in self.a:
            v = 0
            ss = ''
            for card1 in cards:
                try:
                    v = v + card_type[card1][-1]
                except:
                    v = v + card_type1[card1][-1]
                    # print(card1)

                ss += card1
                ss += '.'
            self.value[ss] = v
        # self.value = dict(sorted(self.value.items(), reverse=True))
        self.value = dict(sorted(self.value.items(), key=lambda item: item[1], reverse=True))
        return list(self.value.values())[0], self.value


class point_value23:
    def __init__(self, card):
        self.card = card
        self.a = dict(Counter(self.card))

    def find_value2(self):
        value = 0
        if self.a.get("A"):
            p = self.a["A"]
            value += p * 0.5
        if self.a.get("2"):
            p = self.a["2"]
            value += p * 0.67
        if self.a.get("B"):
            value += 1
        if self.a.get("R"):
            value += 1.3
        return value * 0.25

    def find_value3(self):
        s = {key: value for key, value in self.a.items() if value > 2}
        if s:
            # dic_34 = {1: 0.2, 2: 0.5, 3: 0.9, 4: 1.4, 5: 1.4}
            dic_3 = {0: 0, 1: 0.1, 2: 0.2, 3: 0.4, 4: 0.6, 5: 0.7, 6: 0.8}
            dic_4 = {0: 0, 1: 0.4, 2: 0.8, 3: 1.1, 4: 1.4, 5: 1.6}
            s3 = {key: value for key, value in s.items() if value == 3}
            s4 = {key: value for key, value in s.items() if value == 4}
            # value = dic_34[len(s)]
            value3 = dic_3[len(s3)]
            value4 = dic_4[len(s4)]
            value = value3 + value4
        else:
            value = 0
        return value


class point_value4:
    def __init__(self, cards):
        self.cards = cards
        self.hand_count = list(Counter(cards))

    def find_value4(self):
        k = len(self.hand_count)
        v = 0
        if k == 14:
            if self.hand_count.count("B") * self.hand_count.count("R") == 0:
                if self.hand_count.count("B") == 1:
                    v = 0.3
                else:
                    v = 0.6
            else:
                v = 0.4
        if k == 15:
            v = 0.7
        return v


class total_point:
    def __init__(self, card):
        self.card = card

    def exact_point(self):
        a = point_value1(self.card).find_value1()[0] / 11 + point_value23(self.card).find_value2() + point_value23(
            self.card).find_value3() + point_value4(self.card).find_value4()
        # print(a)
        if a < 17 / 10:
            a = (10 / 17) ** 2 * a ** 3
        return a


def expoint(a):
    if a < 0.3:
        return 0
    elif 0.3 <= a < 0.7:
        return random.randint(0, 1), a
    elif 0.7 <= a < 1.3:
        return 1
    elif 1.3 <= a < 1.7:
        return random.randint(1, 2), a
    elif 1.7 <= a < 2.3:
        return 2
    elif 2.3 <= a < 2.7:
        return random.randint(2, 3), a
    else:
        return 3


def possiable_playable_cards(p1):
    ss = point_value1(p1).find_value1()[1]
    key_ss = list(ss.keys())
    s = []
    if len(key_ss) < 3:
        for i in range(len(key_ss)):
            s1 = key_ss[i].split(".")
            del s1[-1]
            s += s1
        else:
            for i in range(3):
                s1 = key_ss[i].split(".")
                del s1[-1]
                s += s1

    s = set(s)
    s = list(s)
    return s


# card = ['3', '3', '3', '4', '4', '4', '5', '5', '5', '6', '6', '6', '8', '9', 'J', '2', '2']
# point_value1(card).find_value1()
