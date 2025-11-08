from huichen_dou import dou_2
import random
import copy
import collect1
import collect2
import time


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
                    # self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                    #                                          self.dicc).a_b_choose_card()
                    if action.get('555QQ'):
                        chosen_card = '555QQ'
                    else:
                        self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                                                                 self.dicc).a_b_choose_card()

                    # chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i).a_b_choose_card()[1]
                else:
                    self.inf1["playable_cards"] = playable_cards
                    self.dicc, v, chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i,
                                                             self.dicc).a_b_choose_card()

                    # chosen_card = collect1.a_b(self.inf0, self.inf1, self.card_type, i).a_b_choose_card()[1]
                # chosen_card = collect1.way_to_play_card(playable_cards).randomly()

            print(f"{name} choose {chosen_card}")
            # if i>0:
            #     self.dicc = self.dicc[chosen_card]
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


if __name__ == "__main__":
    # p1 = ["4", "7", "7", "J", "K", "B"]
    # p2 = ["3", "4", "4", "5", "5", "7", "T", "T", "K", "A", "A"]

    # p1 = ["6", "6", "Q", "K", "B"]
    # p2 = ["4", "5", "6", "7", "8", "T", "T", "Q", "2", "2"]
    #
    # p1 = ["4", "4", "4", "4", "6", "K", "K"]
    # p2 = ["3", "5", "A", "2", "2", "B", "R"]

    # p1 = ["4", "4", "5", "6", "6", "9", "Q", "2"]#445669Q2
    # p2 = ["8", "8", "T", "K"]

    # p1 = ["5", "5", '5', '9', 'J', 'Q', 'Q', 'A', '2']
    # p2 = ['3', '8', '9', 'T', 'A', 'A', 'A', 'B', 'R']

    # p1 = ["4", "6", "6", "7"]
    # p2 = ["5", "6", "6", "7"]

    # p1 = ["3", "4", "5", "5", "5", "9", "R"]
    # p2 = ["7", "8", "A", "A", "A", "B"]    #JJ斗地主5秒挑战

    # p1 = ["5", "9", "9", "T", "T", "A", "A"]
    # p2 = ["3", "3", "4", "4", "8", "9", "T", "T", "K", "B", "R"]

    # p1 = ["6", "7", "8", "9", "T", "J", "Q", "K", "K", "K", "R"]
    # p2 = ["6", "7", "8", "9", "T", "J", "Q", "K", "A", "A", "A"]
    p1 = ["K", "K", "A", "A", "2", '2', 'B', 'R']
    p2 = ["3", '3', '4', '4', '4', '4', '2', '2']

    start_time = time.time()
    Game(["p1", "p2"], [p1, p2]).play()
    finish_time = time.time()
    print(f"run time:{finish_time - start_time}")
