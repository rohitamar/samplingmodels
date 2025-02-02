import torch 
import torch.nn as nn

from models import NPLM, RNN, TransformerModel

with open('./dataset/data.txt') as f:
    data = f.read()
    vocab = sorted(set(data))
    ctoi = {x:i for i, x in enumerate(vocab)}
    itoc = {i:x for i, x in enumerate(vocab)}
    vocab_size = len(vocab)

rnn_model = RNN(vocab_size=vocab_size, 
                embed_size=64, 
                hidden_size=64
            ).to(device)
rnn_model.load_state_dict(torch.load("./saved_models/rnn_model.pt"))

transformer_model = TransformerModel(
                        vocab_size=vocab_size, 
                        d_model=64
                    ).to(device)
transformer_model.load_state_dict(torch.load("./saved_models/transformer_model.pt"))

nplm_model = NPLM(vocab_size=vocab_size, 
                  embed_size=64, 
                  hidden_size=64, 
                  block_size=32
             ).to(device)
nplm_model.load_state_dict(torch.load("./saved_models/nplm_model.pt"))

def num_parameters(model):
    total = 0
    for p in model.parameters():
        total += p.numel()
    return total

print(f"Transformer: {num_parameters(transformer_model)}")
print(f"RNN: {num_parameters(rnn_model)}")
print(f"NPLM: {num_parameters(nplm_model)}")

print(transformer_model)
print(rnn_model)
print(nplm_model)

from sampling import greedy_decode, random_decode, beam_search

with open('./dataset/data.txt') as f:
    data = f.read()
    vocab = sorted(set(data))
    ctoi = {x:i for i, x in enumerate(vocab)}
    itoc = {i:x for i, x in enumerate(vocab)}
    vocab_size = len(vocab)


device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Training on: ", device)

def encode(s):
    return [ctoi[x] for x in list(s)]

def decode(s):
    return "".join(itoc[x] for x in s)

print(decode(random_decode(transformer_model, encode(" "), 300, 32)))
print(decode(random_decode(nplm_model, encode("Then? and I crown, with land is it so"), 300, 32)))
print(decode(random_decode(rnn_model, encode(" "), 300, 32)))
