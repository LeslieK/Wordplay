import re

def nextWord():
	with open("sowpods.txt") as f:
		while True:
			word = f.readline().replace("\n", '')
			if not word:
				break
			yield word


def isUU(word):
	return "UU" in word

def isQnotU(word):
	return "Q" in word and "QU" not in word

def isVowelsInOrder(word):
	'''returns match object'''
	vowels_in_order = re.compile(r'.*A.*E.*I.*O.*U.*Y')
	return vowels_in_order.search(word)

def isAllVowels(word):
	'''return word if contains all vowels'''
	vowels = set()
	for i in range(len(word)):
		if word[i] in set(["A", "E", "I", "O", "U", "Y"]):
			vowels.add(word[i])
	return len(vowels) == 6

def LongestRepeatedString(word):
	'''returns longest repeated string'''
	sa = SuffixArray(word) # sorted suffix array
	maxlen = 1
	res = []
	# find longest repeated string
	for i in range(1, len(word)):
		lrs_length = sa.lcp(i)
		if lrs_length > maxlen:
			maxlen = lrs_length
			res = [sa.select(i)[:maxlen]]
		elif lrs_length == maxlen:
			# found another lrs instance in this word
			res.append(sa.select(i)[:maxlen])
	return res

def isAnagram(word, ana_dict):
	'''return True if word is anagram of a word in dict'''
	return ''.join(sorted(list(word))) in ana_dict

def doubleLetters(word):
	doubles = []
	for i in range(1, len(word)):
		if word[i - 1] == word[i]:
			doubles.append(word[i])
	return set(doubles)

def letterFreq(word):
	'''find freq of letter in word'''
	res = [] # a list of tuples: [(letter, freq), ...]
	for i in range(len(word)):
		res.append((word[i], word.count(word[i])))
	return res

def updateLetterFreq(letter_freq_dict, word, pairs):
	'''[(letter, freq), (letter2, freq2), ...]'''
	for t in pairs:
		letter = t[0]
		freq = t[1]
		if letter in letter_freq_dict:
			if freq > letter_freq_dict[letter][0]:
				letter_freq_dict[letter][0] = freq
				letter_freq_dict[letter][1] = set([word])
			elif freq == letter_freq_dict[letter][0]:
				letter_freq_dict[letter][1].add(word)
		else:
			letter_freq_dict[letter] = [freq, set([word])]
	return letter_freq_dict

def longest_subpalindrome_slice(text):
    '''Return (i, j) such that text[i:j] is the longest palindrome in text.'''
    # I stole this from Peter Norvig's code presented in Udacity CS253
    if text == '':
        return ((0, 0))
    results = []
    for start in range(len(text)):
        for end in (start, start+1):
            results.append(grow(text, start, end))
    return max(results, key=length)

def grow(text, start, end):
    while (start > 0 and end < len(text) and text[start-1] == text[end]):
        start -= 1
        end += 1
    return (start, end)

def length(slice):  # slice is (start, end)
        start, end = slice
        return end - start


# use suffix array to find longest repeated string
class Suffix(object):
	'''a string suffix'''
	def __init__(self, s, offset, rotated):
		self.offset = offset
		self.N = len(s)
		self.s = s
		self.rotated = rotated

	def __getitem__(self, i):
		if not self.rotated:
			return self.s[i + self.offset]
		else:
			return self.s[(i + self.offset) % self.N]

	def __getslice__(self, i, j):
		if not self.rotated:
			return self.s[i + self.offset:j + self.offset]
		else:
			return self.s[(i + self.offset) % self.N: (j + self.offset) % self.N]

	def length(self):
		if not self.rotated:
			return self.N - self.offset
		else:
			return self.N

	def __len__(self):
		if not self.rotated:
			return self.N - self.offset
		else:
			return self.N

	def __cmp__(self, that):
		'''compare two suffix objects'''
		if not self.rotated:
			maxoffset = max(self.offset, that.offset)
			shortest_string = self.N - maxoffset
		else:
			shortest_string = self.N
		for i in range(shortest_string):
			if self[i] < that[i]:
				return -1
			elif self[i] > that[i]:
				return 1
		return 0

	def __repr__(self):
		if not self.rotated:
			return self.s[self.offset:]
		else:
			return self.s[self.offset:] + self.s[:self.offset]

class SuffixArray(object):
	''' an array of string suffixes'''
	def __init__(self, text, sort=True, rotated=False):
		'''build a suffix array of (random) text'''
		self.text = text
		self.N = len(text)
		self.suffixes = [Suffix(text, i, rotated=rotated) for i in range(self.N)]
		
		if sort:
			self.suffixes.sort()
			#q3 = Quick3string(self.suffixes)
			#self.suffixes = q3.sort()

	def __getitem__(self, i):
		'''returns a suffix object'''
		return self.suffixes[i]

	def length(self):
		'''length of original text'''
		return self.N

	def select(self, i):
		'''return suffix string for suffix in suffixArray[i]'''
		return self.text[self[i].offset:]

	def index(self, i):
		'''index in original text where suffix i begins'''
		return self[i].offset

	def lcp(self, i):
		'''return longest common prefix between suffix[i] and suffix[i-1]'''
		assert(i > 0)
		# suffix objects
		min_length = min(self[i].length(), self[i - 1].length())
		for j in range(min_length):
			if self.select(i)[j] != self.select(i-1)[j]:
				return j
		return min_length

	def rank(self, key):
		'''number of suffixes strictly less than key'''
		# binary search
		lo = 0
		hi = self.N - 1
		while (lo <= hi):
			mid = lo + (hi - lo)/2
			if key < self.select[mid]:
				hi = mid - 1
			elif key > self.select[mid]:
				lo = mid + 1
			else:
				return mid
		# no match
		return lo

def longest_palindromes(pal_dict):
	'''return longest palindromes in dictionary'''
	pal_list = sorted(pal_dict.items(), key=lambda x: len(x[1]), reverse=True)
	maxlen = len(pal_list[0][1])
	longest_pals = set([(pal_list[0])])
	for key, pal in pal_list:
		if len(pal) == maxlen:
			longest_pals.add(frozenset([(key, pal)]))
		else: 
			return longest_pals
			
def most_freq_letters(letter_freq_dict):
	'''return letters that are the most frequent'''
	maxfreqdict = {}
	freq_list = sorted(letter_freq_dict.items(), key=lambda x: x[1][0], reverse=True)
	maxfreq = freq_list[0][1][0]
	for letter, f in freq_list: # f is [n, set([word, word, word])]
		if f[0] == maxfreq:
			maxfreqdict[letter] = f
		else:
			return maxfreqdict

def longest_anagram(ana_dict):
	'''return longest word/anagram'''
	maxlen = 0
	for key in ana_dict:
		if len(key) > maxlen and len(ana_dict[key]) > 1:
			maxlen = len(key)
			word = key
	return word, ana_dict[word], len(word)

def maxRepeatedString(lrs_dict):
	'''return longest word/lrs'''
	# lrs_dict is {word: [lrs, lrs, ...]}
	maxdict = {}
	lrs_list = sorted(lrs_dict.items(), key=lambda x: len(x[1][0]), reverse=True)
	maxlen = len(lrs_list[0][1][0])
	for t in lrs_list:
		word = t[0]
		firstlrs = t[1][0]
		if len(firstlrs) == maxlen:
			maxdict[word] = t[1]
		else:
			break
	return maxdict