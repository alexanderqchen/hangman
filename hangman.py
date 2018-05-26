import requests

URL = "http://upe.42069.fun/jizyr"


most_common_letters = ['e', 't', 'o', 'i', 'a', 'n', 's', 'h', 'r', 'l', 'u', 'd', 'y', 'g', 'm', 'c', 'w', 'p', 'k', 'f', 'b', 'v', 'j', 'z', 'q', 'x']
f = open("20k.txt", "r")
dictionary = []
for line in f:
	dictionary.append(line.strip())

def getWords(state):
	words = state.split(' ')
	for i in range(len(words)):
		for c in words[i]:
			if c != '_' and not c.isalpha():
				words[i] = words[i].replace(c, '')
	return words


unused = [True]*26

def chooseLetter(words):
	letter_count = [0]*26
	for word in words:
		size = len(word)
		for w in dictionary:

			if len(w) == size:
				shouldContinue = False
				for i in range(size):
					if word[i] != w[i] and word[i] != '_':
						shouldContinue = True
						break

				if shouldContinue:
					continue

				for i in range(size):
					if word[i] == '_' and unused[ord(w[i]) - ord('a')]:
						letter_count[ord(w[i]) - ord('a')] += 1
	
	max_count = max(letter_count)

	max_letters = []

	for i, count in enumerate(letter_count):
		if count == max_count:
			max_letters.append(chr(i + ord('a')))

	for l in most_common_letters:
		if l in max_letters and unused[ord(l) - ord('a')]:
			unused[ord(l) - ord('a')] = False
			return l
	
	for l in most_common_letters:
		if unused[ord(l) - ord('a')]:
			unused[ord(l) - ord('a')] = False
			return l

def addWords(lyrics):
	words = lyrics.split()
	for i, word in enumerate(words):
		words[i] = word.strip()
	for i in range(len(words)):
		word = words[i]
		for c in word:
			if not c.isalpha():
				word = word.replace(c, '')
		words[i] = word
	
	for word in words:
		with open("20k.txt", "a") as myfile:
			myfile.write(word + "\n")


while(True):
	r = requests.get(url=URL)
	data = r.json()
	print(data)
	
	games = 0

	while(True):
		words = getWords(data['state'])

		guess = {}
		guess['guess'] = chooseLetter(words)
		print(guess['guess'])

		r = requests.post(url=URL, data=guess)
		data = r.json()
		print(data)

		games = data['games']

		if data['status'] == 'FREE' or data['status'] == 'DEAD':
			unused = [True]*26
			addWords(data['lyrics'])
			break

	if games == 100:
		break