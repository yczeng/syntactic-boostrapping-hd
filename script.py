import numpy as np
import os
import traceback

def generateStopWords(filepath):
	stopWords = set()
	with open(filepath) as text:
		for count, line in enumerate(text):	
			stopWords.add(line.replace("\n", ""))
	return stopWords

def addTreeBank(filePath, posVectors, environmentVectors, lexicalVectors, stopwords):
	text = open(filePath)

	parsedTree = ""
	for count, line in enumerate(text):
		if "(. .)" not in line and "(. ?)" not in line:
			parsedTree += line
			continue

		# the end of the parsedTree has been reached
		tokenized = list(filter(None, parsedTree.replace("\n", "").split(" ")))

		# saves words and their part of speech
		wordsToSave = {}
		for count, token in enumerate(tokenized):

			# if there is a lowercase letter, there's a word
			if any(letter.islower() for letter in token):
				pos = tokenized[count-1].replace("(", "").replace(" ", "")
				word = token.replace(")", "").replace(" ", "").lower()
				# print(pos, word)

				if word not in stopwords:
					wordsToSave[word] = pos
					if word not in environmentVectors:
						environmentVectors[word] = np.random.choice([-1, 1], size=10000)

		# print(wordsToSave)
		# addes context vectors * part of speech vector
		saveToLexical = wordsToSave.copy()
		for word in wordsToSave:

			if word not in lexicalVectors:
				lexicalVectors[word] = np.zeros(10000)

			saveToLexical.pop(word)
			for contextWord in saveToLexical:
				# generate random vectors for part of speech
				if saveToLexical[contextWord] not in posVectors:
					posVectors[saveToLexical[contextWord]] = np.random.choice([-1, 1], size=10000)

				lexicalVectors[word] += environmentVectors[contextWord] * posVectors[saveToLexical[contextWord]]

			saveToLexical[word] = wordsToSave[word]

		parsedTree = ""

	text.close()
	return posVectors, environmentVectors, lexicalVectors

def grabAnalogy(concept1, concept2, analogousTo, lexicalVectors, environmentVectors, numResults=1):
	f = lexicalVectors[concept1] * lexicalVectors[concept2]
	analogyResults = {}
	for word in environmentVectors:
		if word != analogousTo:
			analogyResults[word] = np.dot(environmentVectors[word],	environmentVectors[analogousTo] * f)

	# for key, value in analogyResults.items():
	#     if value > 4000:
	#         print(key, value)

	# print(analogyResults)
	results = []
	for i in range(numResults):
		word = max(analogyResults, key=analogyResults.get)

		results.append((word, analogyResults[word]))
		analogyResults.pop(word)

	return results

if __name__ == "__main__":
	stopWords = generateStopWords('stopwords.txt')
	posVectors = {}
	environmentVectors = {}
	lexicalVectors = {}

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# result = grabAnalogy('dog', 'cat', 'bark', lexicalVectors, environmentVectors)
	# print("Dog : Bark : : Cat :", result)

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/wsjExerpt.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# results = grabAnalogy('industrial', 'senior', 'average', lexicalVectors, environmentVectors, 4)
	# print("analogy of industrial:average is points:")
	# for result in results:
	# 	print(result)

	# count = 0
	# for folder in os.listdir("data/wsj"):
	# 	for file in os.listdir("data/wsj/" + str(folder)):
	# 		posVectors, environmentVectors, lexicalVectors = addTreeBank("data/wsj/" + str(folder) + "/" + file, posVectors, environmentVectors, lexicalVectors, stopWords)
	# 		print("done with", "data/wsj/" + str(folder) + "/" + file)

	# 		count += 1
	# 		if count == 3:
	# 			break

	# 	print("\n\nFOLDER", folder, "done\n\n")
		
	# 	break

	addTreeBank('data/bnc_1000_gold_trees_09', posVectors, environmentVectors, lexicalVectors, stopWords)

	results = {}
	f = lexicalVectors["composers"]

	for word in environmentVectors:
		results[word] = np.dot(environmentVectors[word], lexicalVectors["composers"] * posVectors["NN"])

	newResults = []
	for i in range(5):
		word = max(results, key=results.get)

		newResults.append((word, results[word]))
		results.pop(word)

	print(newResults)

	# [('melody', 11260.0), ('music', 10592.0), ('century', 10580.0), ('material', 10492.0), ('group', 10132.0)]

	# with open('output/vectors.txt', 'w') as writeLexicon:
	# 	for vector in lexicalVectors:
	# 		string = str(vector)
	# 		for number in lexicalVectors[vector]:
	# 			string += " " + str(number)
	# 		writeLexicon.write(string + "\n")

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/bnc_1000_gold_trees_09', posVectors, environmentVectors, lexicalVectors, stopWords)

	# print("Done loading treebanks!")
	# print("----------------------------------------------\n\n\n")
	# print("Format: concept1: idea1 :: concept2: idea2.")
	# print("\n\n\n----------------------------------------------")

	# keepRolling = True
	# transpose = False

	# while keepRolling:
	# 	concept1 = input("Please enter concept1: \n").lower()
	# 	idea1 = input("Please enter idea1: \n").lower()
	# 	concept2 = input("Please enter concept2: \n").lower()
	# 	numResults = input("How many results?\n")

	# 	try:
	# 		results = grabAnalogy(concept1, concept2, idea1, lexicalVectors, environmentVectors, int(numResults))
	# 		print(concept1 + ": " + idea1 + " :: " + concept2 + ": \n")
	# 		for result in results:
	# 			print(result)

	# 	except Exception:
	# 	    traceback.print_exc()
		
	# 	print("\n")