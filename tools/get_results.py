#!/usr/bin/env python
from faces import main
import cPickle as pickle
import sys
import os

data = {'training': [], 'testing': [], 'validation': []}

for k in range(1, 601):
	print k
	data['training'].append(main('training', k))
	data['testing'].append(main('testing', k))
	data['validation'].append(main('validation', k))

with open('results.p', 'wb') as f:
	pickle.dump(data, f)
