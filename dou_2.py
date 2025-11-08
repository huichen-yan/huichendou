import json
import numpy as np
from collections import Counter


class enter_card_type:
    def __init__(self):
        with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_1.json") as f:
            self.card_type = json.load(f)

    def c3(self):
        with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_2.json") as f:
            card_type2 = json.load(f)
        with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_3.json") as f:
            card_type3 = json.load(f)
        self.card_type.update(card_type2)
        self.card_type.update(card_type3)
        return self.card_type


class card_prepare:
    def __init__(self):
        self.card = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2", "B", "R"]
        self.value_card = {}
        self.card_value = {}
        for i in range(len(self.card)):
            self.value_card[i] = self.card[i]
            self.card_value[self.card[i]] = i


class code_:
    def __init__(self, card):
        self.card = card
        self.card_value = card_prepare().card_value
        self.code = []

    def code_cards(self):
        self.code = []
        for i in range(15):
            self.code.append([])
            for j in range(4):
                self.code[i].append(0)
        c = dict(Counter(self.card))
        for item in c:
            p = int(self.card_value[item])
            sum1 = c[item]
            for i in range(sum1):
                self.code[p][i] = 1

        # for i in range(len(self.card)):
        #     if self.card.count(self.card[i]) == 0:
        #         continue
        #     else:
        #         if i > 0 and self.card[i] == self.card[i - 1]:
        #             continue
        #         else:
        #             t = self.card_value[self.card[i]]
        #             for j in range(self.card.count(self.card[i])):
        #                 self.code[int(t)][j] = 1
        if self.code[13][0] == 1:
            self.code[13] = 1
        else:
            self.code[13] = 0
        if self.code[14][0] == 1:
            self.code[14] = 1
        else:
            self.code[14] = 0
        for i in range(13):
            self.code[i].reverse()
        return self.code

    def code_one_vector(self):
        code = self.code_cards()
        code_one = []
        for i in range(13):
            for j in range(4):
                code_one.append(code[i][j])
        for i in range(13, 15):
            code_one.append(code[i])
        return code_one


class show_code:
    def __init__(self, code):
        self.card1 = card_prepare().card
        self.code = code
        self.show = []

    def show_card(self):
        for i in range(13):
            if sum(self.code[i]) > 0:
                for j in range(sum(self.code[i])):
                    self.show.append(self.card1[i])
        for i in range(13, 15):
            if self.code[i] == 1:
                self.show.append(self.card1[i])
        return self.show


class legal_action:
    def __init__(self, card, former_action):
        self.card = card
        self.former_action = former_action
        # self.card_type = enter_card_type().card_type
        self.code = code_(self.card).code_cards()
        self.action = []

    def action_movement(self):
        def action_movement_(card_type, code):
            action = {}
            for card0 in card_type:
                card0_code = code_(card0).code_cards()
                t = 1
                for i in range(len(code) - 2):
                    sum1 = sum(code[i])
                    sum0 = sum(card0_code[i])
                    if sum1 - sum0 < 0:
                        t = -1
                        break
                if code[-1] - card0_code[-1] < 0 or code[-2] - card0_code[-2] < 0:
                    t = -1
                if t == 1:
                    action[card0] = card_type[card0]
            return action

        if self.former_action:
            return action_movement_(self.former_action, self.code)
        else:

            ss = judge_plane(self.card).judge_plane()
            # print(ss)
            if ss[1]:
                # with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_3.json") as f:
                #     tt = json.load(f)
                tt = enter_card_type().c3()
                return action_movement_(tt, self.code)
            else:
                card_type = enter_card_type().card_type
                action = action_movement_(card_type, self.code)
                if ss[0]:
                    with open(r"C:\Users\86131\Desktop\python online\huichen_dou\hc_card_type_2.json") as f:
                        tt = json.load(f)
                    a = action_movement_(tt, self.code)
                    action.update(a)
                return action
            # return action_movement_(card_type, self.code)


class playable:
    def __init__(self, action, card_type, former_card):
        self.action = action
        self.card_type = card_type
        self.former_card = former_card

    def card(self):
        if self.former_card == "BR":
            playable_cards1 = []
        elif self.card_type[self.former_card][0] == "bomb":
            playable_cards1 = [card11 for card11 in self.action if
                               self.card_type[self.former_card][0] == self.card_type[card11][0]
                               and int(self.card_type[card11][1]) > int(self.card_type[self.former_card][1])
                               or self.card_type[card11][0] == "rocket"]
        else:
            playable_cards1 = [card11 for card11 in self.action if
                               self.card_type[self.former_card][0] == self.card_type[card11][0]
                               and int(self.card_type[card11][1]) > int(self.card_type[self.former_card][1])
                               or self.card_type[card11][0] == "bomb" or self.card_type[card11][
                                   0] == "rocket"]

        playable_cards1.append("pass")

        return playable_cards1


class pre:
    def __init__(self, code, action, chosen_card):
        self.code = code
        self.card = ""
        self.action = action
        self.chosen_card = chosen_card

    def mins(self):
        chosen_card_code = code_(self.chosen_card).code_cards()
        for s in range(13):
            for j in range(4):
                self.code[s][j] -= chosen_card_code[s][j]
        for s in range(13, 15):
            self.code[s] -= chosen_card_code[s]
        self.card = show_code(self.code).show_card()
        self.code = code_(self.card).code_cards()
        if self.action:
            self.action = legal_action(self.card, self.action).action_movement()

        return self.code, self.card, self.action


class judge_plane:
    def __init__(self, card):
        self.card = card
        self.code = code_(card).code_cards()

    def j_3(self):
        s = []
        for i in range(12):
            if self.code[i][1] == 1:
                s.append(i)
        if len(s) < 3:
            return [False, False]
        else:
            for j in range(len(s) - 2):
                if s[j + 1] - s[j] == 1 and s[j + 2] - s[j + 1] == 1:
                    return [True, False]
        return [False, False]

    def judge_plane(self):
        s = []
        for i in range(12):
            if self.code[i][1] == 1:
                s.append(i)
        if len(s) < 5 and len(self.card) < 20:
            return self.j_3()
        else:
            for k in range(len(s) - 2):
                if s[k] + 2 == s[k + 1] + 1 == s[k + 2]:
                    for j in range(len(s) - 4):
                        if s[j] + 4 == s[j + 1] + 3 == s[j + 2] + 2 == s[j + 3] + 1 == s[j + 4]:
                            return [True, True]
                    return [True, False]
        return [False, False]


class get_batch:
    def __init__(self, card, num_legal_action):
        self.card = card
        # self.code = code_(card).code_cards()
        self.num_legal_action = num_legal_action

    def batch(self):
        if self.card == "pass" or not self.card:
            c_ = np.zeros(54, dtype=np.int8)
        else:
            code = code_(self.card).code_cards()
            for i in range(13):
                code[i].reverse()
            c = []
            for i in range(13):
                for j in range(4):
                    c.append(code[i][j])
            c.append(code[13])
            c.append(code[14])
            c_ = np.array(c)
        c_batch = np.repeat(c_[np.newaxis, :], self.num_legal_action, axis=0)
        return c_batch

"""

"""
class c_card:
    def __init__(self, card, max_num, num1):
        self.card = card
        self.max_num = max_num
        self.num1 = num1

    def _get_one_hot_(self):
        one_hot1 = np.zeros(self.max_num)
        if len(self.card) > 0:
            one_hot1[len(self.card) - 1] = 1
        one_hot1_ = np.repeat(one_hot1[np.newaxis, :], self.num1, axis=0)
        return one_hot1_

    def _one_hot_bomb_(self):
        one_hot = np.zeros(15)
        if len(self.card) < 2:
            one_hot[0] = 1
        else:
            if self.card[-1] == "R" and self.card[-2] == "B":
                one_hot[1] = 1
            else:
                one_hot[0] = 1
        one_hot_ = np.repeat(one_hot[np.newaxis, :], self.num1, axis=0)
        return one_hot_


if __name__ == "__main__":
    # print(enter_card_type().card_type)
    # ss = 1
    p1 = ['8', '9', '9', 'T', 'T', 'T', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'A', 'A', '2', '2', 'R']
    print(code_(p1).code_one_vector())
    # ss = legal_action(p1, "").action_movement()
    # print(ss)
    # print(len(ss))
