import underthesea
# helper function that fix wrong location of intonation
sac = 	'áắấúứóốớíéếý'
huyen = 'àằầùừòồờìèềỳ'
hoi = 	'ảẳẩủửỏổởỉẻểỷ'
nga = 	'ãẵẫũữõỗỡĩẽễỹ'
nang = 	'ạặậụựóộợịẹệỵ'
ngang = 'aăâuưoôơieêy'
intonations = [sac,huyen,hoi,nga,nang]
char_map = [ None for _ in range(len(sac)) ]
for x in range(len(char_map)):
	char_map[x] = [ngang[x] , [i[x] for i in intonations]]

def getIntonatedCharacter ( char , inton):
	if inton == 0 :
		return char
	pos = ngang.find(char)

	return intonations[inton-1][pos]

def identifyIntonation(word):
	for character in word :
		for _intonation in intonations:
			for ex in _intonation:
				if character == ex :
					return intonations.index(_intonation) +1
	return 0

syllabel = 'qwrpsdđghjktlmnbvcxz' + 'qwrytpsdđghjklmnbvcxz'.upper()
def correctIntonation(string):
	words = string.split(' ')
	for x in range(len(words)):
		word = words[x]
		left_syllabel = 0
		right_syllabel = len(word)
		for i in range(len(word)):
			if word[i] not in syllabel :
				left_syllabel = i
				break
		for i in range(len(word)-1,left_syllabel-1,-1):
			if word[i] not in syllabel :
				right_syllabel = i+1
				break
		inton = word[left_syllabel:right_syllabel]

		lInton = len(inton)
		_intonType = identifyIntonation(inton)

		# ngang hóa
		_convertedInton = ''
		for char in inton :
			# find
			found = False
			for i in char_map:
				if char in i[1]:
					_convertedInton += i[0]
					found = True
					break
			if found == False:
				_convertedInton += char

		# intonationing
		if len(inton) in [1,2]:
			pos = 0
		if len(inton) in [3]:
			pos = 2


		# inton
		_newInton = _convertedInton.replace(_convertedInton[pos] , getIntonatedCharacter(_convertedInton[pos] , _intonType))
		word = word.replace(inton,_newInton)
		words[x] = word
	return ' '.join(words)
