import string
import WordplayUtils 

# lists of words
doubleU = []
QnotU = []
doubleLetters = set()
vowelsInOrder = []
all_vowels = []

letter_freq_dict = {} # letter: [n, set-of-words]
lrs_dict = {} # word: {lrs1, lrs2, ...}
pal_dict = {} # word: long_pal
ana_dict = {} # key: [anagram1, anagram2, ...]

WORDS = WordplayUtils.nextWord()

for word in WORDS:
	# longest palindrome:
	i, j = WordplayUtils.longest_subpalindrome_slice(word)
	if j - i > 1:
		pal_dict[word] = word[i:j]
	
	if WordplayUtils.isUU(word):
		doubleU.append(word)
	
	if WordplayUtils.isQnotU(word):
		QnotU.append(word)

	# find all letters that are doubled
	doubleLetters = doubleLetters.union(WordplayUtils.doubleLetters(word))

	# all vowels in order 
	if WordplayUtils.isVowelsInOrder(word):
		vowelsInOrder.append(word)

	# all vowels in any order
	if WordplayUtils.isAllVowels(word):
		all_vowels.append(word)

	# find anagrams
	key = ''.join(sorted(list(word)))
	if WordplayUtils.isAnagram(word, ana_dict):
		ana_dict[key].append(word)
	else:
		ana_dict[key] = [word]

	# frequency of letter in word
	list_of_letter_freq_pairs = WordplayUtils.letterFreq(word)
	letter_freq_dict = WordplayUtils.updateLetterFreq(letter_freq_dict, word, list_of_letter_freq_pairs)

	# finds longest repeated string(s)
	LRSlist = WordplayUtils.LongestRepeatedString(word)
	if len(LRSlist) > 0:
		lrs_dict[word] = LRSlist


# letters that are not doubled
set_of_nondoubleLetters = set(string.ascii_uppercase) - doubleLetters

print 'longest repeated string is:\n {}\n'.format(WordplayUtils.maxRepeatedString(lrs_dict))
print 'words that contain "UU":\n {}\n'.format(doubleU)
print 'words with Q not followed by U:\n {}\n'.format(QnotU)
print 'letters that are not doubled:\n {}\n'.format(set_of_nondoubleLetters)
print 'longest palindromes are:\n {}\n'.format(WordplayUtils.longest_palindromes(pal_dict))
print 'most frequent letter(s) and the words they are in:\n {}\n'.format(WordplayUtils.most_freq_letters(letter_freq_dict)) 
print 'longest anagrams are:\n {}\n'.format(WordplayUtils.longest_anagram(ana_dict))
print 'words that contain all vowels in order:\n {}\n'.format(vowelsInOrder)

print 'words that contain all vowels in any order:\n {}\n'.format(all_vowels)
print 'max frequency of each letter:\n {}\n'.format(sorted(letter_freq_dict.items()))