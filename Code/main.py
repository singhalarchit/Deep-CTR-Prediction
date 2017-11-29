# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:13:22 2017

@author: Archit
"""

#! /usr/bin/env python
import os
import argparse
import datetime
import torch
import model
import train

parser = argparse.ArgumentParser(description='CTR Predictor')
# learning
parser.add_argument('-lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
parser.add_argument('-epochs', type=int, default=27000, help='number of epochs for train [default: 256]')
parser.add_argument('-log-interval',  type=int, default=1000,   help='how many steps to wait before logging training status [default: 1]')
parser.add_argument('-plot-interval',  type=int, default=500,   help='how many steps to wait before plotting training status [default: 1]')
#parser.add_argument('-test-interval', type=int, default=100, help='how many steps to wait before testing [default: 100]')
parser.add_argument('-save-interval', type=int, default=1000, help='how many steps to wait before saving [default:500]')
parser.add_argument('-save-dir', type=str, default='../Snapshots', help='where to save the snapshots')
parser.add_argument('-plot-dir', type=str, default='../Plots', help='where to save the plots')
parser.add_argument('-factor', type=int, default=1, help='factor for feature embeddings')
parser.add_argument('-imbalance-factor', type=int, default=5, help='class imbalance factor for training')
# data 
#parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch' )
# model
#parser.add_argument('-dropout', type=float, default=0.1, help='the probability for dropout [default: 0.1]')
#parser.add_argument('-max-norm', type=float, default=3.0, help='l2 constraint of parameters [default: 3.0]')
#parser.add_argument('-embed-dim', type=int, default=128, help='number of embedding dimension [default: 128]')
#parser.add_argument('-kernel-num', type=int, default=100, help='number of each kind of kernel')
#parser.add_argument('-kernel-sizes', type=str, default='2,3,4,5', help='comma-separated kernel size to use for convolution')
#parser.add_argument('-hidden-dim', type=int, default=128, help='number of hidden dimension [default: 256]')
#parser.add_argument('-num-layers', type=int, default=1, help='number of hidden layers in RNN [default: 1]')
#parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')
# device
#parser.add_argument('-device', type=int, default=-1, help='device to use for iterate data, -1 mean cpu [default: -1]')
parser.add_argument('-no-cuda', action='store_true', default=False, help='disable the gpu' )
# option
parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')
#parser.add_argument('-predict', type=str, default=None, help='predict the sentence given')
#parser.add_argument('-test', action='store_true', default=False, help='train or test')
args = parser.parse_args()


# update args and print
args.cuda = (not args.no_cuda) and torch.cuda.is_available(); del args.no_cuda
args.save_dir = os.path.join(args.save_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
args.plot_dir = os.path.join(args.plot_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

print("\nParameters:")
for attr, value in sorted(args.__dict__.items()):
    print("\t{}={}".format(attr.upper(), value))


# model
if args.snapshot is None:
    model = model.LR(args.factor)
else:
    print('\nLoading models from [%s]...' % args.snapshot)
    try:
        model = torch.load(args.snapshot + 'model.pt')
    except:
        print("Sorry, The snapshot(s) doesn't exist."); exit()

if args.cuda:
    model = model.cuda()

#train.cross_validation(args, model)


date = '2017-11-29_13-42-58'
lr = '1e-05'
steps = '27000'
filename = '../Snapshots/' + date + '/lr_' + lr + '/model_steps' + steps + '.pt'
model = torch.load(filename)
correct, wrong, accuracy, auc = train.evaluate(args, model)
print 'Correct: ' + str(correct) + ' Wrong: ' + str(wrong) + ' Accuracy: ' + str(accuracy) + ' AUC: ' + str(auc)
#correct, wrong, accuracy, auc = train.evaluatefull(args, model)
#print 'Correct: ' + str(correct) + ' Wrong: ' + str(wrong) + ' Accuracy: ' + str(accuracy) + ' AUC: ' + str(auc)


'''
# train or predict
if args.predict is not None:
    label = train.predict(args.predict, cnn, text_field, label_field, args.cuda)
    print('\n[Text]  {}\n[Label] {}\n'.format(args.predict, label))
elif args.test:
    try:
        train.eval(test_iter, cnn, args) 
    except Exception as e:
        print("\nSorry. The test dataset doesn't  exist.\n")
else:
    print()
    try:
        train.train(train_iter, dev_iter, cnn, args)
    except KeyboardInterrupt:
        print('-' * 89)
        print('Exiting from training early')
'''
