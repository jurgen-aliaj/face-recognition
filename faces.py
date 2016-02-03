#!/usr/bin/env python
import cPickle as pickle
import numpy as np
import scipy
from scipy import misc
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.cm as cm

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
			prediction = majority_label(top[:k])
			validation[i].append(prediction)
		return find_accuracy(validation)
	elif phase == 'testing':
		print '\nFIVE EXAMPLES OF FAILURE CASES\n'
		count = 0
		for i in range(len(testing)):
			top = top_k(testing[i][0], training, k)
			prediction = majority_label(top[:k])
			testing[i].append(prediction)
			if prediction != testing[i][1] and count < 5:
				print 'Error #' + str(count + 1) + ':\n'
				print 'original image: ' + testing[i][2]
				print 'predicted label: ' + testing[i][-1] + '\n'
				print '5 nearest neighbours: '
				print 'first: ' + top[0][2] + ' norm: ' + str(top[0][0])
				print 'second: ' + top[1][2] + ' norm: ' + str(top[1][0])
				print 'third: ' + top[2][2] + ' norm: ' + str(top[2][0])
				print 'fourth: ' + top[3][2] + ' norm: ' + str(top[3][0])
				print 'fifth: ' + top[4][2] + ' norm: ' + str(top[4][0]) + '\n'
				count += 1
		return find_accuracy(testing)
	else:
		for i in range(len(training)):
			top = top_k(training[i][0], training, k)
			prediction = majority_label(top[:k])
			training[i].append(prediction)
		return find_accuracy(training)

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
	
def find_accuracy(L):
	return len([x for x in L if x[1] == x[-1]])/float(len(L))		
	
def dif(x, y):
	x = x.astype(float)
	y = y.astype(float)	
	return np.sqrt(np.sum((x-y)**2))
	
if __name__ == '__main__':
	
	if len(sys.argv) != 4:
		print 'Usage: ./faces.py face/gender training/validation/testing k, example: ./faces.py gender validation 2'
		sys.exit()
	
	phase = sys.argv[2]
	
	if phase != 'training' and  phase != 'testing' and phase != 'validation':
		print 'Usage: ./faces.py face/gender training/validation/testing k, example: ./faces.py face training 10'
		sys.exit()

	try:
		k = int(sys.argv[3])
	except:
		print 'k must be a positive integer at most 600.'
		sys.exit()

	if k > 600 or k < 1:
		print 'k must be a positive integer at most 600.'
		sys.exit()

	face = sys.argv[1]
	
	if face != 'face' and face != 'gender':
		print 'Usage: ./faces.py face/gender training/validation/testing k, example: ./faces.py gender testing 2'
		sys.exit()

	print 'accuracy: ' + str(main(face, phase, k))

	with open('results.p', 'rb') as f:
		data = pickle.load(f)

	K = range(1, 601)

	blue_line = mlines.Line2D([], [], color='blue', label='training')
	red_line = mlines.Line2D([], [], color='red', label='testing')
	green_line = mlines.Line2D([], [], color='green', label='validation')
	plt.legend(handles=[blue_line, red_line, green_line])

	plt.plot(K, data['testing'], 'r', K, data['validation'], 'g', K, data['training'], 'b')
	plt.axis([-10, 610, 0, 1.03])
	plt.xlabel('k')
	plt.ylabel('performance')
	plt.title('Nearest Neighbour Performance for Various K')
	plt.show()
