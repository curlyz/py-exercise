# Code for correting vietnamese syntax
# Visit https://en.wikipedia.org/wiki/Vietnamese_phonology

"""
	ngang "level"	A1	mid level	˧ (33)	(no mark)	ba ('three')
	huyền "deep"	A2	low falling (breathy)	˨˩ (21) or (31)	`	bà ('lady')
	sắc "sharp"	B1	mid rising, tense	˧˥ (35)	´	bá ('governor')
	nặng "heavy"	B2	mid falling, glottalized, short	˧ˀ˨ʔ (3ˀ2ʔ) or ˧ˀ˩ʔ (3ˀ1ʔ)	 ̣	bạ ('at random')
	hỏi "asking"	C1	mid falling(-rising), harsh	˧˩˧ (313) or (323) or (31)	 ̉	bả ('poison')
	ngã "tumbling"	C2
"""
# thứ tự : sắc huyền hỏi ngã nặng ngang
_characterTone = {
	'a':'áàảãạa',
	'ă':'ắằẳẵặă',
	'â':'ấầẩẫậâ',
	'u':'úùủũụu',
	'ư':'ứừửữựư',
	'o':'óòỏõọo',
	'ô':'ốồổỗộô',
	'ơ':'ớờởỡợơ',
	'i':'íìỉĩịi',
	'e':'éèẻẽẹe',
	'ê':'ếềểễệê',
	'y':'ýỳỷỹỵy'
}
_characterTonemap = {
	'a':'áàảãạa',
	'ă':'ắằẳẵặă',
	'â':'ấầẩẫậâ',
	'u':'úùủũụu',
	'ư':'ứừửữựư',
	'o':'óòỏõọo',
	'ô':'ốồổỗộô',
	'ơ':'ớờởỡợơ',
	'i':'íìỉĩịi',
	'e':'éèẻẽẹe',
	'ê':'ếềểễệê',
	'y':'ýỳỷỹỵy'
}

_consonant = ['ch','gh','kh','ng','ngh','nh','ph','th','tr','gi','qu']
_consonant.extend(['b','c','d','đ','g','h','k','l','m','n','p','q','r','s','t','v','x','y'])

_vowel = ['a','ă','â','e','ê','i','o','ô','ơ','u','ư','y']

# Main function ( function doesn't start with '_' )
def correctSentence(sentence):
	#sentence = pos_tag(sentence) #[('Đây', 'P'), ('là', 'V'), ('Thảo', 'Np'), (',', 'CH'), ('thào', 'V'), ('l', 'N'), ('.', 'CH')]
	sentence = sentence.split(' ')
	newSentence = [] # list để có method join
	#print(sentence)
	for element in sentence :
		if True :
			# cái này là chữ nè , xét nó
			# 1 , xác định 3 thành phần của từ * left , center , right
			left , center , right = _wordPartition(element)
			if len(center) == 0 :
				newSentence.append(left+center+right)
				continue
			# 2 , xác định dáu và vị trí của dấu của center
			tone , position = _getTone(center) # trả về loại dấu và vị trí	eg : ["sharp" , 0]
			# 3 , xác định vị trí của dấu chính xác chưa
			if len(right) == 0 :
				if len(center) <= 2 :
					correctPos = 0
				elif len(center) > 2 :
					correctPos = 1
			elif len(right) > 0 : # thuyền , thằng , thoải, thỏa , thiềng , thính , ? cái rule này đúng k
				correctPos = len(center) - 1

			#print('\tCorrentPos' , correctPos)

			# 4 , xóa dấu từ đó
			character = center[position]
			for x , y in _characterTone.items(): # x là chữ đã xóa dấu , y là chưa xóa dấu
				if character in y:
					character = x
					break # tiết kiệm điện
			center = center.replace(center[position] , character)
			#print('\tNoToneCenter' , center)
			# 5 , đặt dấu cho đúng
			character = center[correctPos] # kí tự sẽ bị đổi dấu
			character = _setTone(character , tone)
			center = center.replace(center[correctPos] , character)
			#print('\tNewToneCenter' , character , center)
			newSentence.append(left + center + right)

		#newSentence = ' '.join(newSentence)
	print('\n[{original} --> {converted}]'.format(
		original = ' '.join(sentence),
		converted = ' '.join(newSentence)
	))

	return ' '.join(newSentence)



# Helper function ( function that is only used by main function)
# It will start with ('_')
# Functions, Variables that starts with '_' will not be import when using "from library import *"
def _wordPartition(word):
	"""
		Seperate a word into 3 parts , return as list
	"""
	left , center , right = ['' for _ in range(3)]
	lWord = word.lower()
	for i in range(len(_consonant)):
		if lWord.find(_consonant[i]) == 0 :
			left = word[0:len(_consonant[i])]
			break


	for i in range(len(left),len(word)):
		char = word[i].lower()

		_isVowel = False
		for x,y in _characterTone.items():
			if  char in y :
				_isVowel = True
				break
		#print('Char' , char , _isVowel)
		if not _isVowel:
			center = word[len(left):i]
			right = word[i:]
			break
		if i == len(word) - 1 and _isVowel == True:
			center = word[len(left):]
			right = ''
	#print('_wordPartition' ,word ,  [left , center , right])
	return [left , center , right]

def _getTone(word):
	tone = 5
	for position in range(len(word)):

		character = word[position].lower()
		for x , y in _characterTone.items():
			if character in y[:-1]:
				tone = y.find(character)
				return tone , position
	return 5 , 0



def _setTone(word , tone):
	return _characterTone[word][tone]

correctSentence('Thuỷ Thíêu gì hk ta ?')
