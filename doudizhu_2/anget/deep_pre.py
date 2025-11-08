import numpy as np
import torch
from huichen_dou import dou_2


def c2a(card):
    if card == "pass" or not card:
        c_ = np.zeros(54, dtype=np.int8)
    else:
        code = dou_2.code_(card).code_cards()
        for i in range(13):
            code[i].reverse()
        c = []
        for i in range(13):
            for j in range(4):
                c.append(code[i][j])
        c.append(code[13])
        c.append(code[14])
        c_ = np.array(c)
    return c_


def process_action_seq(seq, l=15):
    """
    A utility function encoding historical moves. We
    encode 15 moves. If there is no 15 moves, we pad
    with zeros.
    """
    seq = seq[-l:].copy()
    if len(seq) < l:
        empty_sequence = [[] for _ in range(l - len(seq))]
        empty_sequence.extend(seq)
        seq = empty_sequence
    return seq


def action_seq_l2a(action_seq_list):
    """
    A utility function to encode the historical moves.
    We encode the historical 15 actions. If there is
    no 15 actions, we pad the features with 0. Since
    three moves is a round in DouDizhu, we concatenate
    the representations for each consecutive three moves.
    Finally, we obtain a 5x162 matrix, which will be fed
    into LSTM for encoding.
    """
    action_seq_array = np.zeros((len(action_seq_list), 54))
    for row, list_cards in enumerate(action_seq_list):
        action_seq_array[row, :] = c2a(list_cards)
    action_seq_array = action_seq_array.reshape(5, 162)
    return action_seq_array


# s = ["666",'222','333','444','777','9TJQK']
#
#
# z = action_seq_l2a(process_action_seq(s))
#
# z_batch = np.repeat(z[np.newaxis, :, :],20, axis=0)
# print(z_batch)

def load_model_(position, model_path):
    # from douzero.dmc.models import model_dict
    from huichen_dou.model.models import model_dict
    model = model_dict[position]()
    model_state_dict = model.state_dict()
    if torch.cuda.is_available():
        pretrained = torch.load(model_path, map_location='cuda:0')
    else:
        pretrained = torch.load(model_path, map_location='cpu')
    pretrained = {k: v for k, v in pretrained.items() if k in model_state_dict}
    model_state_dict.update(pretrained)
    model.load_state_dict(model_state_dict)
    if torch.cuda.is_available():
        model.cuda()
    model.eval()
    return model

class DeepAgent_:
    def __init__(self, model, z, x):
        self.model = model
        self.z = z
        self.x = x

    def act(self, playable_cards):
        z_batch = torch.from_numpy(self.z).float()
        x_batch = torch.from_numpy(self.x).float()
        if torch.cuda.is_available():
            z_batch, x_batch = z_batch.cuda(), x_batch.cuda()
        y_pred = self.model.forward(z_batch, x_batch, return_value=True)['values']
        y_pred = y_pred.detach().cpu().numpy()
        best_action_index = np.argmax(y_pred, axis=0)[0]

        best_action = playable_cards[best_action_index]
        best_action_confidence = y_pred[best_action_index]
        # print(best_action, best_action_confidence, y_pred)
        # print(y_pred)
        return best_action, best_action_confidence




