from huichen_dou import dou_2
import copy
import random
from huichen_dou.doudizhu_3.anget.deep_agent import landlord_choose_action as la, landlord_up_choose_action as lu, \
    landlord_down_choose_action as ld

cards = ['3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7', '8', '8',
         '8', '8', '9', '9', '9', '9', 'T', 'T', 'T', 'T', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K',
         'A', 'A', 'A', 'A', '2', '2', '2', '2', 'B', 'R']


class Game:
    def __init__(self, name, card, basic_score):
        self.name0 = name[0]
        self.card0 = card[0]
        self.name1 = name[1]
        self.card1 = card[1]
        self.name2 = name[2]
        self.card2 = card[2]
        self.code0 = dou_2.legal_action(self.card0, '').code
        self.code1 = dou_2.legal_action(self.card1, '').code
        self.code2 = dou_2.legal_action(self.card2, '').code
        self.action0 = dou_2.legal_action(self.card0, '').action_movement()
        self.action1 = dou_2.legal_action(self.card1, '').action_movement()
        self.action2 = dou_2.legal_action(self.card2, '').action_movement()
        self.basic_score = basic_score
        self.card_value = dou_2.card_prepare().card_value
        self.card_type = dou_2.enter_card_type().c3()
        self.former_card_2 = ""
        self.former_card_1 = ""
        self.playing_record = []
        self.inf0 = {"card": copy.deepcopy(self.card0), "code": copy.deepcopy(self.code0), "playable_cards": [],
                     "My_playing_record": [], "My_playing_card": "", "role": "landlord"}
        self.inf1 = {"card": copy.deepcopy(self.card1), "code": copy.deepcopy(self.code1), "playable_cards": [],
                     "My_playing_record": [], "My_playing_card": "", "role": "landlord_up"}
        self.inf2 = {"card": copy.deepcopy(self.card2), "code": copy.deepcopy(self.code2), "playable_cards": [],
                     "My_playing_record": [], "My_playing_card": "", "role": "landlord_down"}
        self.card0_opp = copy.deepcopy(cards)
        self.card1_opp = copy.deepcopy(cards)
        self.card2_opp = copy.deepcopy(cards)
        for card_ in self.card0:
            self.card0_opp.remove(card_)
        for card_ in self.card1:
            self.card1_opp.remove(card_)
        for card_ in self.card2:
            self.card2_opp.remove(card_)
    """
    0 is random agent
    1 is douzero agent
    """
    def play(self, landlord_agent="douzero agent", former_agent="douzero agent"):
        def run(name, action, code, card, i):
            if i > 0:
                if self.former_card_2 != "pass" or self.former_card_1 != "pass":
                    if self.former_card_1 != "pass":
                        playable_cards = dou_2.playable(action, self.card_type, self.former_card_1).card()
                    else:
                        playable_cards = dou_2.playable(action, self.card_type, self.former_card_2).card()
                else:
                    playable_cards = [card11 for card11 in action]
            else:
                playable_cards = [card11 for card11 in action]
            if i % 3 == 0:
                if landlord_agent == "douzero agent":
                    chosen_card = la(self.card0, self.card1, self.card2, self.card0_opp, self.former_card_1,
                                     self.inf1["My_playing_card"], self.inf2["My_playing_card"], playable_cards,
                                     self.playing_record)
                else:
                    chosen_card = random.choice(playable_cards)

            elif i % 3 == 1:
                if former_agent == "douzero agent":
                    chosen_card = lu(self.card0, self.card1, self.card2, self.card1_opp, self.inf0["My_playing_card"],
                                     self.inf2["My_playing_card"], self.former_card_1, self.former_card_2,
                                     playable_cards,
                                     self.playing_record)

                else:
                    chosen_card = random.choice(playable_cards)
            else:
                if former_agent == "douzero agent":
                    chosen_card = ld(self.card0, self.card1, self.card2, self.card2_opp, self.inf0["My_playing_card"],
                                     self.inf1["My_playing_card"], self.former_card_1, self.former_card_2,
                                     playable_cards,
                                     self.playing_record)
                else:
                    chosen_card = random.choice(playable_cards)


            self.playing_record.append(chosen_card)

            self.former_card_2 = self.former_card_1
            self.former_card_1 = chosen_card
            # print(f"{name} choose {chosen_card}")
            if chosen_card != "pass":
                code, card, action = dou_2.pre(code, action, chosen_card).mins()
                if self.card_type[chosen_card][0] == "bomb" or self.card_type[chosen_card][0] == "rocket":
                    self.basic_score = self.basic_score*2
            # print(f"{name} still remain {card}")
            if i % 3 == 0:
                self.inf0["card"] = card
                self.inf0["code"] = code
                self.inf0["My_playing_record"].append(chosen_card)
                if chosen_card != "pass":
                    self.inf0["My_playing_card"] += chosen_card
                    s1 = dou_2.code_(self.card1_opp).code_cards()
                    s2 = dou_2.code_(self.card2_opp).code_cards()
                    _, self.card1_opp, __ = dou_2.pre(s1, '', chosen_card).mins()
                    _, self.card2_opp, __ = dou_2.pre(s2, '', chosen_card).mins()
            elif i % 3 == 1:
                self.inf1["card"] = card
                self.inf1["code"] = code
                self.inf1["My_playing_record"].append(chosen_card)
                if chosen_card != "pass":
                    self.inf1["My_playing_card"] += chosen_card
                    s0 = dou_2.code_(self.card0_opp).code_cards()
                    s2 = dou_2.code_(self.card2_opp).code_cards()
                    _, self.card0_opp, __ = dou_2.pre(s0, '', chosen_card).mins()
                    _, self.card2_opp, __ = dou_2.pre(s2, '', chosen_card).mins()
            else:
                self.inf2["card"] = card
                self.inf2["code"] = code
                self.inf2["My_playing_record"].append(chosen_card)
                if chosen_card != "pass":
                    self.inf2["My_playing_card"] += chosen_card
                    s0 = dou_2.code_(self.card0_opp).code_cards()
                    s1 = dou_2.code_(self.card1_opp).code_cards()
                    _, self.card0_opp, __ = dou_2.pre(s0, '', chosen_card).mins()
                    _, self.card1_opp, __ = dou_2.pre(s1, '', chosen_card).mins()
            return card, name, code, action

        i = 0
        while True:
            if i % 3 == 0:
                self.card0, self.name0, self.code0, self.action0 = run(self.name0, self.action0,
                                                                       self.code0, self.card0,
                                                                       i)
            elif i % 3 == 1:
                self.card1, self.name1, self.code1, self.action1 = run(self.name1, self.action1,
                                                                       self.code1, self.card1,
                                                                       i)
            else:
                self.card2, self.name2, self.code2, self.action2 = run(self.name2, self.action2,
                                                                       self.code2, self.card2,
                                                                       i)
            if not self.card0:
                print(f"{self.name0} landlord win")
                score = self.basic_score
                break
            if not self.card1 or not self.card2:
                print(f"{self.name1} and {self.name2} farmer win")
                score = -self.basic_score
                break

            i += 1
        return score