import csv
import json
from math import log
from collections import Counter
import random

def main():
	correct = 0
	attempted = 0

	proportions = dict([('TX', 0.173), ('MA', 0.245), ('FL', 0.154), ('OR', 0.176), ('OH', 0.078), ('CO', 0.022), ('GA', 0.129), ('WA', 0.021), ('CA', 0.0002)])

	f = open('proportions_train_unclustered.json')
	data = json.load(f)
	data_array = []
	for key in data:
		data_array.append(data[key])
	f.close()

	with open('features_test.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		first = True
		for row in spamreader:
			if first:
				first = False
				continue

			features = row[0].split(',')
			options = Counter()

			for i in range(len(data_array)):
				if not features[i+1]: continue

				for option in data_array[i]:
					if data_array[i][option] == 0: continue
					options[option] += log(1 + data_array[i][option])

			for option in options:
				options[option] = proportions[option] * options[option]

			choices = options.most_common()
			choice = 'MA'

			if choices != []:
				choice = choices[0][0]

			#choice = random.choice(list(proportions.keys()))	random baseline
			#choice = 'MA'										most common baseline

			##countstates = Counter(proportions)				multiple guesses baseline
			##choices = countstates.most_common()
			#rank = Counter()									multiple guesses
			#for i in range(len(choices)):
			#	rank[choices[i][0]] = i
			#correct += rank[features[0]]

			if choice == features[0]: correct += 1
			attempted += 1

	return correct / attempted
