import numpy as np
from huichen_dou import dou_2
from huichen_dou.doudizhu_3.anget import deep_pre


def landlord_choose_action(card0,card1,card2,card0_opp,former_card,cc1,cc2,playable_cards,playing_record):
    my_handcards_batch = dou_2.get_batch(card0, len(playable_cards)).batch()
    other_handcards_batch = dou_2.get_batch(card0_opp, len(playable_cards)).batch()
    last_action_batch = dou_2.get_batch(former_card, len(playable_cards)).batch()
    landlord_up_played_cards_batch = dou_2.get_batch(cc1, len(playable_cards)).batch()
    landlord_down_played_cards_batch = dou_2.get_batch(cc2, len(playable_cards)).batch()
    landlord_up_num_cards_left_batch = dou_2.c_card(card1, 17, len(playable_cards))._get_one_hot_()
    landlord_down_num_cards_left_batch = dou_2.c_card(card2, 17, len(playable_cards))._get_one_hot_()
    bomb_num_batch = dou_2.c_card(card0, 1, len(playable_cards))._one_hot_bomb_()

    my_action_batch = np.zeros(my_handcards_batch.shape)
    j = 0
    for a in playable_cards:
        my_action_batch[j, :] = dou_2.get_batch(a, 1).batch()
        j = j + 1
    x_batch = np.hstack((
        my_handcards_batch,
        other_handcards_batch,
        last_action_batch,
        landlord_up_played_cards_batch,
        landlord_down_played_cards_batch,
        landlord_up_num_cards_left_batch,
        landlord_down_num_cards_left_batch,
        bomb_num_batch,
        my_action_batch
    ))
    z = deep_pre.action_seq_l2a(deep_pre.process_action_seq(playing_record))
    z_batch = np.repeat(z[np.newaxis, :, :], len(playable_cards), axis=0)

    model = deep_pre.load_model_(position="landlord",
                                 model_path=r"C:\Users\86131\Desktop\python online\baselines\douzero_WP\landlord.ckpt")

    ss = deep_pre.DeepAgent_(x=x_batch, z=z_batch, model=model).act(playable_cards)[0]
    return ss


def landlord_up_choose_action(card0,card1,card2,card1_opp,cc0,cc2,former_card_1,former_card_2,playable_cards,playing_record):
    my_handcards_batch = dou_2.get_batch(card1, len(playable_cards)).batch()
    other_handcards_batch = dou_2.get_batch(card1_opp, len(playable_cards)).batch()
    landlord_played_cards_batch = dou_2.get_batch(cc0, len(playable_cards)).batch()
    teammate_played_cards_batch = dou_2.get_batch(cc2, len(playable_cards)).batch()
    last_action_batch = dou_2.get_batch(former_card_1, len(playable_cards)).batch()
    last_landlord_action_batch = last_action_batch
    last_teammate_action_batch = dou_2.get_batch(former_card_2, len(playable_cards)).batch()
    landlord_num_cards_left_batch = dou_2.c_card(card0, 20, len(playable_cards))._get_one_hot_()
    teammate_num_cards_left_batch = dou_2.c_card(card2, 17, len(playable_cards))._get_one_hot_()
    bomb_num_batch = dou_2.c_card(card1, 1, len(playable_cards))._one_hot_bomb_()
    my_action_batch = np.zeros(my_handcards_batch.shape)
    j = 0
    for a in playable_cards:
        my_action_batch[j, :] = dou_2.get_batch(a, 1).batch()
        j = j + 1
    x_batch = np.hstack((
        my_handcards_batch,
        other_handcards_batch,
        landlord_played_cards_batch,
        teammate_played_cards_batch,
        last_action_batch,
        last_landlord_action_batch,
        last_teammate_action_batch,
        landlord_num_cards_left_batch,
        teammate_num_cards_left_batch,
        bomb_num_batch,
        my_action_batch
    ))
    z = deep_pre.action_seq_l2a(deep_pre.process_action_seq(playing_record))
    z_batch = np.repeat(z[np.newaxis, :, :], len(playable_cards), axis=0)
    model = deep_pre.load_model_(position='farmer',
                                 model_path=r"C:\Users\86131\Desktop\python online\baselines\douzero_WP\landlord_up.ckpt")
    return deep_pre.DeepAgent_(x=x_batch, z=z_batch, model=model).act(playable_cards)[0]


def landlord_down_choose_action(card0,card1,card2,card2_opp,cc0,cc1,former_card_1,former_card_2,playable_cards,playing_record):
    my_handcards_batch = dou_2.get_batch(card2, len(playable_cards)).batch()
    other_handcards_batch = dou_2.get_batch(card2_opp, len(playable_cards)).batch()
    landlord_played_cards_batch = dou_2.get_batch(cc0, len(playable_cards)).batch()
    teammate_played_cards_batch = dou_2.get_batch(cc1, len(playable_cards)).batch()
    last_action_batch = dou_2.get_batch(former_card_1, len(playable_cards)).batch()
    last_landlord_action_batch = dou_2.get_batch(former_card_2, len(playable_cards)).batch()
    last_teammate_action_batch = last_action_batch
    landlord_num_cards_left_batch = dou_2.c_card(card0, 20, len(playable_cards))._get_one_hot_()
    teammate_num_cards_left_batch = dou_2.c_card(card1, 17, len(playable_cards))._get_one_hot_()
    bomb_num_batch = dou_2.c_card(card2, 1, len(playable_cards))._one_hot_bomb_()
    my_action_batch = np.zeros(my_handcards_batch.shape)
    j = 0
    for a in playable_cards:
        my_action_batch[j, :] = dou_2.get_batch(a, 1).batch()
        j = j + 1
    x_batch = np.hstack((
        my_handcards_batch,
        other_handcards_batch,
        landlord_played_cards_batch,
        teammate_played_cards_batch,
        last_action_batch,
        last_landlord_action_batch,
        last_teammate_action_batch,
        landlord_num_cards_left_batch,
        teammate_num_cards_left_batch,
        bomb_num_batch,
        my_action_batch
    ))
    z = deep_pre.action_seq_l2a(deep_pre.process_action_seq(playing_record))
    z_batch = np.repeat(z[np.newaxis, :, :], len(playable_cards), axis=0)
    model = deep_pre.load_model_(position='farmer',
                                 model_path=r"C:\Users\86131\Desktop\python online\baselines\douzero_WP\landlord_down.ckpt")
    return deep_pre.DeepAgent_(x=x_batch, z=z_batch, model=model).act(playable_cards)[0]
