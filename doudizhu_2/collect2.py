import random
import copy
from huichen_dou import dou_2
from threading import Thread
import queue


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
                    else:
                        my_inf['playable_cards'] = dou_2.playable(ac, card_type, former_card).card()
                        playable_cards = my_inf['playable_cards']

                else:
                    playable_cards = my_inf['playable_cards']
                k = len(playable_cards)

                for i in range(0, k, 2):

                    my_inf1 = copy.deepcopy(my_inf)
                    my_inf2 = copy.deepcopy(my_inf)
                    if playable_cards[i] != "pass":
                        my_inf1["code"], my_inf1["card"], k0 = dou_2.pre(my_inf1["code"], "", playable_cards[i]).mins()

                    if i + 1 < k:
                        if playable_cards[i + 1] != "pass":
                            my_inf2["code"], my_inf2["card"], k0 = dou_2.pre(my_inf2["code"], "",
                                                                             playable_cards[i + 1]).mins()
                        result_queue = queue.Queue()
                        # dicc1, value1, ac_opp = a_b(opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1, dicc)
                        # dicc2, value2, ac_opp2 = a_b(opp_inf_, my_inf2, card_type, playable_cards[i + 1], iter + 1, dicc)
                        Thread(target=a_b, args=(result_queue, opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1, dicc)).start()
                        Thread(target=a_b, args=(result_queue, opp_inf_, my_inf2, card_type, playable_cards[i+1], iter + 1, dicc)).start()
                        if result_queue.empty:
                            a = result_queue.get()
                        if result_queue.empty:
                            b = result_queue.get()
                        dicc[playable_cards[i]] = dicc1
                        dicc[playable_cards[i + 1]] = dicc2
                        value_list.append(-value1)
                        value_list.append(-value2)
                        if value_list[-1] == 1 or value_list[-2] == 1:
                            if value_list[-1] == 1:
                                best_move = playable_cards[i + 1]
                                ss = 1
                                break
                            else:
                                best_move = playable_cards[i]
                                ss = 1
                                break
                    else:
                        dicc1, value1, ac_opp = a_b(opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1, dicc)
                        value_list.append(-value1)
                        dicc[playable_cards[i]] = dicc1
                        # alpha-beta cut
                        if value_list[-1] == 1:
                            best_move = playable_cards[i]
                            ss = 1
                            break

                    print(i)

                # for i in range(k):
                #
                #     my_inf1 = copy.deepcopy(my_inf)
                #     if playable_cards[i] != "pass":
                #         my_inf1["code"], my_inf1["card"], k0 = dou_2.pre(my_inf1["code"], "", playable_cards[i]).mins()
                #     dicc1, value1, ac_opp = a_b(opp_inf_, my_inf1, card_type, playable_cards[i], iter + 1, dicc)
                #     value_list.append(-value1)
                #     dicc[playable_cards[i]] = dicc1
                #     # alpha-beta cut
                #     if value_list[-1] == 1:
                #         best_move = playable_cards[i]
                #         ss = 1
                #         break

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
