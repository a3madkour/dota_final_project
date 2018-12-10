
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from parseData import readHeroes
from collections import Counter
import random


def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])



def encode(seq):
    seq = seq.split(',')
    seq = seq[3:]
    coded_seq = []
    string = ''
    for el in seq:
        if el == 'BAN':
            string+= el+'_'
        elif el == 'PICK':
            string+= el+'_'
        elif el == 'ALLY_TEAM':
            string+= el+'_'
        elif el == 'ENEMY_TEAM':
            string+= el+'_'
        else:
            hero_id = int(el.replace('\n',''))
            string+=str(hero_id)
            coded_seq.append(string)
            string = ''
    return coded_seq

#BAN= 0
#PICK= 1
#ALLY_TEAM = 2
#ENEMY_TEAM = 3
#HERO = HERO_ID+3
#
# def encode(seq):
#     seq = seq.split(',')
#     seq = seq[3:]
#     coded_seq = []
#     for el in seq:
#         if el == 'BAN':
#             coded_seq.append('0')
#         elif el == 'PICK':
#             coded_seq.append('1')
#         elif el == 'ALLY_TEAM':
#             coded_seq.append('2')
#         elif el == 'ENEMY_TEAM':
#             coded_seq.append('3')
#         else:
#             hero_id = int(el.replace('\n',''))
#             coded_seq.append(str(hero_id +3))
#     coded_seq.append('\n')
#     return coded_seq
#
# def decode(seq):
#     decoded_seq = ''
#     coded_seq = []
#     for el in seq:
#         if el == '0':
#             coded_seq.append('BAN')
#         elif el == '1':
#             coded_seq.append('PICK')
#         elif el == '2':
#             coded_seq.append('ALLY_TEAM')
#         elif el == '3':
#             coded_seq.append('ENEMY_TEAM')
#         elif el == '\n':
#             continue
#         else:
#             hero_id = int(el.replace('\n',''))
#             coded_seq.append(str(hero_id -3))
#     coded_seq.append('\n')
#     return coded_seq
#
if __name__ == '__main__':
    # filename = '82262664_2_trunc_seqsX.csv'
    filename = '87278757_2_trunc_seqsX.csv'
    seqs =[]
    with open(filename) as f:
        seqs = f.readlines()
    seqs = seqs[1:]
    train_seqs = seqs[:int(len(seqs)/2)]
    test_seqs = seqs[int(len(seqs)/2):]
    coded_seqs = []
    for seq in train_seqs:
        coded_seq = encode(seq)
        coded_seqs.append(coded_seq)

    coded_seqs = [item for sublist in coded_seqs for item in sublist]
    order = 4
    grams = find_ngrams(coded_seqs,order)
    gram_dict = {}
    # generate entries for things not in the data
    for gram in grams:
        key = gram[:order-1]
        prediction = gram[order-1]
        if key not in gram_dict:
            gram_dict[key] = []
        gram_dict[key].append(prediction)

    predictions = []
    ground_truth = []
    for seq in test_seqs:
        coded_seq = encode(seq)
        inp = tuple(coded_seq[-(order+1):-2])
        if inp in gram_dict:
            pred = (random.sample(gram_dict[inp],1)[0])
        else:
            pred = '-1'
        truth = coded_seq[-2]
        predictions.append(pred)
        ground_truth.append(truth)

    predictions = np.array(predictions)
    ground_truth = np.array(ground_truth)
    print(np.sum(predictions == ground_truth)/len(ground_truth))

