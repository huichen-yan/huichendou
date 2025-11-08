import random
from huichen_dou import dou_2
import copy
from huichen_dou.doudizhu_2.anget.deep_agent import landlord_choose_action as la
from huichen_dou.doudizhu_2.anget.deep_agent import farmer_choose_action as fa


cards = ['5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', 'T', 'T',
         'T', 'T', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A', '2', '2', '2', '2',
         'B', 'R']


class Game:
    def __init__(self, name, card, point):
        self.name0 = name[0]
        self.card0 = card[0]
        self.name1 = name[1]
        self.card1 = card[1]
        self.code0 = dou_2.legal_action(self.card0, '').code
        self.code1 = dou_2.legal_action(self.card1, '').code
        self.action0 = dou_2.legal_action(self.card0, '').action_movement()
        self.action1 = dou_2.legal_action(self.card1, '').action_movement()
        self.card_value = dou_2.card_prepare().card_value
        self.card_type = dou_2.enter_card_type().card_type
        self.former_card = ""
        self.value = [0, 0]
        self.dicc = {}
        self.point = point
        self.act = []
        # self.inf0 = {"name": self.name0, "card": copy.deepcopy(self.card0), "code": copy.deepcopy(self.code0),
        #              "playable_cards": [], "role": "landload"}
        # self.inf1 = {"name": self.name1, "card": copy.deepcopy(self.card1), "code": copy.deepcopy(self.code1),
        #              "playable_cards": [], "role": "framer"}
        self.cc0 = ""
        self.cc1 = ''
        self.inf0 = {"card": copy.deepcopy(self.card0), "code": copy.deepcopy(self.code0), "playable_cards": [],
                     "Opponent_playing_record": [],
                     "Opponent_remain_card": copy.deepcopy(self.card1), "role": "landlord"}
        self.inf1 = {"card": copy.deepcopy(self.card1), "code": copy.deepcopy(self.code1), "playable_cards": [],
                     "Opponent_playing_record": [],
                     "Opponent_remain_card": copy.deepcopy(self.card0), "role": "framer"}
        self.card0_opp = copy.deepcopy(cards)
        self.card1_opp = copy.deepcopy(cards)
        for card_ in self.card0:
            self.card0_opp.remove(card_)
        for card_ in self.card1:
            self.card1_opp.remove(card_)

    def play(self):
        def run(name, action, code, card, i):
            if i > 0 and self.former_card != "pass":
                playable_cards = dou_2.playable(action, self.card_type, self.former_card).card()
            else:
                # playable_cards = get_cards.possiable_playable_cards(card)
                playable_cards = [card11 for card11 in action]
                # if len(card) > 10:
                #     playable_cards = get_cards.possiable_playable_cards(card)
                # else:
                #     playable_cards = [card11 for card11 in action]
            s1 = False
            for item in playable_cards:
                if len(item) == len(card):
                    chosen_card = item
                    s1 = True
                    break
            if not s1:
                if i % 2 == 0:
                    if len(playable_cards) == 1:
                        chosen_card = playable_cards[0]
                    else:
                        # chosen_card = random.choice(playable_cards)
                        chosen_card = la(self.card0, self.card1, self.card0_opp, self.former_card, self.cc0,
                                         playable_cards, self.act)

                else:
                    if len(playable_cards) == 1:
                        chosen_card = playable_cards[0]
                    else:
                        chosen_card = fa(self.card1, self.card0_opp, self.cc1, self.former_card, self.card0,
                                         playable_cards, self.act)
                        # chosen_card = random.choice(playable_cards)

            self.act.append(chosen_card)

            print(f"{name} choose {chosen_card}")

            self.former_card = chosen_card

            if chosen_card != "pass":
                code, card, action = dou_2.pre(code, action, chosen_card).mins()
            print(f"{name} still remain {card}")

            if i % 2 == 0:
                self.inf0["card"] = card
                self.inf0["code"] = code
                self.inf1["Opponent_playing_record"].append(chosen_card)
                self.inf1["Opponent_remain_card"] = card
                if chosen_card != "pass":
                    self.cc1 += chosen_card
                    s0 = dou_2.code_(self.card1_opp).code_cards()
                    _, self.card1_opp, __ = dou_2.pre(s0, '', chosen_card).mins()

            else:
                self.inf1["card"] = card
                self.inf1["code"] = code
                self.inf0["Opponent_playing_record"].append(chosen_card)
                self.inf0["Opponent_remain_card"] = card
                if chosen_card != "pass":
                    self.cc0 += chosen_card
                    s1 = dou_2.code_(self.card0_opp).code_cards()
                    _, self.card0_opp, __ = dou_2.pre(s1, '', chosen_card).mins()
            return card, name, code, action

        i = 0
        while True:
            # if i > 0:
            #     break
            if i % 2 == 0:

                self.card0, self.name0, self.code0, self.action0 = run(self.name0, self.action0,
                                                                       self.code0, self.card0,
                                                                       i)
                if not self.card0:
                    print(f"{self.name0} landlord win!!!")
                    break


            else:
                self.card1, self.name1, self.code1, self.action1 = run(self.name1, self.action1,
                                                                       self.code1, self.card1,
                                                                       i)
                if len(self.card1) <= self.point:
                    print(f"{self.name1} framer win!!!")
                    break
            i += 1
            # if i > 3:
            #     print("tech break")
            #     break

            # if self.card0 == []:
            #     print("p1 win!!!")
            #     self.value[0] = 1
            #     self.value[1] = -1
            #     break
            # elif self.card1 == []:
            #     print("p2 win!!!")
            #     self.value[1] = 1
            #     self.value[0] = -1
            #     break
            # else:
            #     i += 1
