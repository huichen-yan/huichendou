from huichen_dou import dou_2
import copy
from huichen_dou.doudizhu_2 import collect1
# from huichen_dou.doudizhu_2 import collect2



class Game:
    def __init__(self, name, card):
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
        self.former_card = " "
        self.value = [0, 0]
        self.dicc = {}
        self.inf0 = {"name": self.name0, "card": copy.deepcopy(self.card0), "code": copy.deepcopy(self.code0),
                     "playable_cards": []}
        self.inf1 = {"name": self.name1, "card": copy.deepcopy(self.card1), "code": copy.deepcopy(self.code1),
                     "playable_cards": []}
        # self.inf0 = {"card": copy.deepcopy(self.card0), "code": copy.deepcopy(self.code0), "playable_cards": [], "Opponent playing record": [],
        #              "Opponent remain card": copy.deepcopy(self.card1)}
        # self.inf1 = {"card": copy.deepcopy(self.card1), "code": copy.deepcopy(self.code1), "playable_cards": [], "Opponent playing record": [],
        #              "Opponent remain card": copy.deepcopy(self.card0)}

    def play(self):
        def run(name, action, code, card, i):
            if i > 0 and self.former_card != "pass":
                playable_cards = dou_2.playable(action, self.card_type, self.former_card).card()
            else:
                playable_cards = [card11 for card11 in action]
            # print(playable_cards)
            # if i % 2 == 0:
            #     self.inf0["playable_cards"] = playable_cards
            #     self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i, self.dicc).a_b_choose_card()
            #     self.dicc = self.dicc[chosen_card]
            #
            # else:
            #     self.inf1["playable_cards"] = playable_cards
            #     self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i, self.dicc).a_b_choose_card()
            #     self.dicc = self.dicc[chosen_card]
            #     # chosen_card = collect1.way_to_play_card(playable_cards).randomly()

            if len(playable_cards) == 1 or len(action) == 1:
                chosen_card = playable_cards[0]

            else:
                if i % 2 == 0:
                    playable_cards = sorted(playable_cards, key=len, reverse=True)
                    self.inf0["playable_cards"] = playable_cards
                    self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                                                             self.dicc).a_b_choose_card()
                    # if action.get('555QQ'):
                    #     chosen_card = '555QQ'
                    # else:
                    #     self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                    #                                              self.dicc).a_b_choose_card()

                    # chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i).a_b_choose_card()[1]
                else:
                    self.inf1["playable_cards"] = playable_cards
                    self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                                                             self.dicc).a_b_choose_card()

                    # chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i).a_b_choose_card()[1]
                # chosen_card = collect1.way_to_play_card(playable_cards).randomly()

            print(f"{name} choose {chosen_card}")

            self.dicc = self.dicc[chosen_card]

            self.former_card = chosen_card

            if chosen_card != "pass":
                code, card, action = dou_2.pre(code, action, chosen_card).mins()
            print(f"{name} still remain {card}")

            if i % 2 == 0:
                self.inf0["card"] = card
                self.inf0["code"] = code
                # self.inf1["Opponent playing record"].append(chosen_card)
                # self.inf1["Opponent remain card"] = card
            else:
                self.inf1["card"] = card
                self.inf1["code"] = code
                # self.inf0["Opponent playing record"].append(chosen_card)
                # self.inf0["Opponent remain card"] = card
            return card, name, code, action

        i = 0
        while True:
            # if i > 0:
            #     break
            if i % 2 == 0:
                self.card0, self.name0, self.code0, self.action0 = run(self.name0, self.action0,
                                                                       self.code0, self.card0,
                                                                       i)

            else:
                self.card1, self.name1, self.code1, self.action1 = run(self.name1, self.action1,
                                                                       self.code1, self.card1,
                                                                       i)
            if self.card0 == []:
                print("p1 win!!!")
                self.value[0] = 1
                self.value[1] = -1
                break
            elif self.card1 == []:
                print("p2 win!!!")
                self.value[1] = 1
                self.value[0] = -1
                break
            else:
                i += 1
            # print(f"p1 information {self.inf0}")
            # print(f"p2 information {self.inf1}")