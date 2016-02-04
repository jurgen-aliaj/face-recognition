#!/usr/bin/env python
#!/usr/bin/env python
import cPickle as pickle
import numpy as np
import scipy
from scipy import misc
import sys
import os

def main(a, b, c):

	face = 1 if a == 'face' else 0
	phase = b
	k = c

	training = []

	for i in list(os.walk('training'))[0][2]:
		im = np.asarray(misc.imread('training/' + i)).flatten()
		label = i.split('.')[0].split('_')[1 - face]
		training.append([im, label, i])

	validation = []

	for i in list(os.walk('validation'))[0][2]:
		im = np.asarray(misc.imread('validation/' + i)).flatten()
		label = i.split('.')[0].split('_')[1 - face]
		validation.append([im, label, i])

	testing = []

	for i in list(os.walk('testing'))[0][2]:
		im = np.asarray(misc.imread('testing/' + i)).flatten()
		label = i.split('.')[0].split('_')[1 - face]
		testing.append([im, label, i])

	if phase == 'validation':
		for i in range(len(validation)):
			top = top_k(validation[i][0], training, k)
			for j in range(1, 601):
				validation[i].append(majority_label(top[:j]))
		performance = []
		for i in range(1, 601):
			performance.append(find_accuracy(validation, i))
		return performance
	elif phase == 'testing':
		for i in range(len(testing)):
			top = top_k(testing[i][0], training, k)
			for j in range(1, 601):
				testing[i].append(majority_label(top[:j]))
		performance = []
		for i in range(1, 601):
			performance.append(find_accuracy(testing, i))
		return performance
	else:
		for i in range(len(training)):
			top = top_k(training[i][0], training, k)
			for j in range(1, 601):
				training[i].append(majority_label(top[:j]))
		performance = []
		for i in range(1, 601):
			performance.append(find_accuracy(training, i))
		return performance
			
def top_k(im, L, k):
	top = []
	for i in L:
		top.append([dif(im, i[0]), i[1], i[2]])
	top.sort(key=lambda x: x[0])
	return top

def majority_label(L):
	lst = []
	for i in L:
		lst.append(i[1])
	L = lst
	return max(((i, L.count(i)) for i in set(L)), key = lambda x: x[1])[0]

def print_failures(L):
	print [x for x in L if x[1] != x[-1]]

def find_accuracy(L, i):
	return len([x for x in L if x[1] == x[i + 2]])/float(len(L))

def dif(x, y):
	x = x.astype(float)
	y = y.astype(float)
	return np.sqrt(np.sum((x-y)**2))

if __name__ == '__main__':

	data = {'training': [], 'testing': [], 'validation': []}

	data['training'] = main('face', 'training', '1')
	data['testing'] = main('face', 'testing', '1')
	data['validation'] = main('face', 'validation', '1')

	with open('results.p', 'wb') as f:
		pickle.dump(data, f)
