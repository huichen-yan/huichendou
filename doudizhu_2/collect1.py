import random
import copy
from huichen_dou import dou_2



class way_to_play_card:
    def __init__(self, inf):
        self.inf = inf

    def randomly(self):
        return random.choice(self.inf)
        # return random.choice(self.inf["playable_cards"])


# class a_b:
#     def __init__(self, inf0, inf1, card_type, iter):
#         self.inf0 = copy.deepcopy(inf0)
#         self.inf1 = copy.deepcopy(inf1)
#         self.card_type = card_type
#         self.iter = iter
#
#     def a_b_choose_card(self):
#         def a_b(my_inf, opp_inf, card_type, former_card, iter):
#             if not opp_inf['card']:
#                 return -1, None
#             if former_card:
#                 ac = dou_2.legal_action(my_inf["card"], '').action_movement()
#                 if former_card == "pass":
#                     my_inf['playable_cards'] = [card11 for card11 in ac]
#                     playable_cards = my_inf['playable_cards']
#                 else:
#                     my_inf['playable_cards'] = dou_2.playable(ac, card_type, former_card).card()
#                     playable_cards = my_inf['playable_cards']
#
#             else:
#                 playable_cards = my_inf['playable_cards']
#
#             value_list = []
#             ss = 0
#             my_inf_ = copy.deepcopy(my_inf)
#             opp_inf_ = copy.deepcopy(opp_inf)
#             for i in range(len(playable_cards)):
#                 # if iter == 1:
#                 #     print(playable_cards[i], iter)
#                 my_inf1 = copy.deepcopy(my_inf)
#                 if playable_cards[i] != "pass":
#                     my_inf1["code"], my_inf1["card"], k0 = dou_2.pre(my_inf1["code"], "", playable_cards[i]).mins()
#                     # k0, k1, k2 = dou_2.pre(my_inf["code"], "", playable_cards[i]).mins()
#                     # my_inf1["code"] = copy.deepcopy(k0)
#                     # my_inf1["card"] = copy.deepcopy(k1)
#                 value, ac_opp = a_b(opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1)
#                 value_list.append(-value)
#                 # print(-value, best_move, playable_cards[i], iter)
#                 # alpha-beta cut
#                 if value_list[-1] == 1:
#                     best_move = playable_cards[i]
#                     ss = 1
#                     break
#             # if value_list.count(1) == 0:
#             #     # print(len(value_list))
#             #     value = -1
#             #     best_move = random.choice(playable_cards)
#             # else:
#             #     s = value_list.index(1)
#             #     value = 1
#             #     best_move = playable_cards[s]
#             if ss == 1:
#                 value = 1
#             else:
#                 value = -1
#                 best_move = random.choice(playable_cards)
#                 # print(value_list, best_move, playable_cards[i], iter)
#             # if iter == 2:
#             #     print(value_list)
#             return value, best_move
#
#         if self.iter % 2 == 0:
#             return a_b(self.inf0, self.inf1, self.card_type, "", self.iter)
#         else:
#             return a_b(self.inf1, self.inf0, self.card_type, "", self.iter)

ss = 1

class a_b:
    def __init__(self, inf0, inf1, card_type, iter, dicc):
        self.inf0 = copy.deepcopy(inf0)
        self.inf1 = copy.deepcopy(inf1)
        self.card_type = card_type
        self.iter = iter
        self.dicc = dicc

    def a_b_choose_card(self):
        def a_b(my_inf, opp_inf, card_type, former_card, iter, dicc):
            if not self.dicc:
                if not opp_inf['card']:
                    if opp_inf['name'] == "p1":
                        return {"p1": 1, "p2": -1}, -1, None
                    else:
                        return {"p1": -1, "p2": 1}, -1, None
                value_list = []
                ss = 0
                opp_inf_ = copy.deepcopy(opp_inf)
                dicc = {}

                if former_card:
                    ac = dou_2.legal_action(my_inf["card"], '').action_movement()
                    if former_card == "pass":
                        my_inf['playable_cards'] = [card11 for card11 in ac]
                        playable_cards = my_inf['playable_cards']
                        playable_cards = sorted(playable_cards, key=len, reverse=True)
                    else:
                        my_inf['playable_cards'] = dou_2.playable(ac, card_type, former_card).card()
                        playable_cards = my_inf['playable_cards']
                        playable_cards = sorted(playable_cards, key=len, reverse=True)
                else:
                    playable_cards = my_inf['playable_cards']

                for i in range(len(playable_cards)):
                    my_inf1 = copy.deepcopy(my_inf)
                    if playable_cards[i] != "pass":
                        my_inf1["code"], my_inf1["card"], k0 = dou_2.pre(my_inf1["code"], "", playable_cards[i]).mins()
                    dicc1, value1, ac_opp = a_b(opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1, dicc)
                    value_list.append(-value1)
                    dicc[playable_cards[i]] = dicc1
                    # alpha-beta cut
                    if value_list[-1] == 1:
                        best_move = playable_cards[i]
                        ss = 1
                        break
                if ss == 1:
                    value = 1
                else:
                    value = -1
                    best_move = random.choice(playable_cards)
                return dicc, value, best_move

            else:
                if dicc.get("p1"):
                    return dicc, -1, None
                value_list = []
                ss = 0

                for card in dicc:
                    dicc1, value1, ac_opp = a_b(opp_inf, my_inf, card_type, card, iter + 1, dicc[card])
                    value_list.append(-value1)
                    if value_list[-1] == 1:
                        best_move = card
                        ss = 1
                        break
                if ss == 1:
                    value = 1
                else:
                    value = -1
                    best_move = random.choice(list(dicc.keys()))
                return dicc, value, best_move


        if self.iter % 2 == 0:
            return a_b(self.inf0, self.inf1, self.card_type, "", self.iter, self.dicc)
        else:
            return a_b(self.inf1, self.inf0, self.card_type, "", self.iter, self.dicc)


SS=1

# class AB:
#     def __init__(self, inf0, inf1, card_type, iter, dicc):
#         self.inf0 = copy.deepcopy(inf0)
#         self.inf1 = copy.deepcopy(inf1)
#         self.card_type = card_type
#         self.iter = iter
#         self.dicc = dicc
#
#     def a_b_choose_card(self):
#         if self.iter % 2 == 0:
#             return self.a_b_algo(self.inf0, self.inf1)
#         else:
#             return self.a_b_algo(self.inf1, self.inf0)
#
#     def a_b_algo(self, my_inf, opp_inf):
#         """核心决策算法"""
#         if not self.dicc:
#             return self.handle_no_dicc(my_inf, opp_inf)
#
#         return self.handle_with_dicc(my_inf, opp_inf)
#
#     def handle_no_dicc(self, my_inf, opp_inf):
#         """处理dicc为空的情况"""
#         if not opp_inf['card']:
#             return self.game_over(opp_inf['name'])
#
#         opp_inf_ = copy.deepcopy(opp_inf)
#         playable_cards = self.get_playable_cards(my_inf, "")
#
#         value_list = []
#         for card in playable_cards:
#             my_inf1 = copy.deepcopy(my_inf)
#             if card != "pass":
#                 my_inf1["code"], my_inf1["card"], _ = dou_2.pre(my_inf1["code"], "", card).mins()
#             dicc1, value1, _ = self.a_b_algo(opp_inf_, my_inf1)
#             value_list.append(-value1)
#
#             if value_list[-1] == 1:
#                 return {}, 1, card
#
#         return {}, -1, random.choice(playable_cards)
#
#     def handle_with_dicc(self, my_inf, opp_inf):
#         """处理dicc不为空的情况"""
#         if self.dicc.get("p1"):
#             return self.dicc, -1, None
#
#         value_list = []
#         for card in self.dicc:
#             dicc1, value1, _ = self.a_b_algo(opp_inf, my_inf, card, self.iter + 1, self.dicc[card])
#             value_list.append(-value1)
#
#             if value_list[-1] == 1:
#                 return self.dicc, 1, card
#
#         return self.dicc, -1, random.choice(list(self.dicc.keys()))
#
#     def game_over(self, name):
#         """游戏结束处理"""
#         return {"p1": 1 if name == "p1" else -1, "p2": -1 if name == "p1" else 1}, -1, None
#
#     def get_playable_cards(self, my_inf, former_card):
#         """获取可打牌"""
#         ac = dou_2.legal_action(my_inf["card"], '').action_movement()
#         if former_card == "pass":
#             playable_cards = sorted(ac, key=len, reverse=True)
#         else:
#             playable_cards = dou_2.playable(ac, self.card_type, former_card).card()
#             playable_cards = sorted(playable_cards, key=len, reverse=True)
#
#         my_inf['playable_cards'] = playable_cards
#         return playable_cards

