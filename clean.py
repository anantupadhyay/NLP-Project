import re
import itertools

def replace_escape_characters(foo):
	idx = 1
	while(idx!=-1):
		idx = foo.find('\n')
		#print idx
		if((foo[idx-1]==' ' and foo[idx-2] == '.') or foo[idx-1]=='.'):
			foo = foo.replace('\n', ' ')
		elif(foo[idx-1]==' ' and foo[idx-2]!='.'):
			foo = foo.replace(' \n', '. ')
	idx = 1
	while(idx != -1):
		#print idx
		idx = foo.find('\t')
		foo = foo.replace('\t', ' ')

	foo = re.sub(r'\.+', ".", foo)
	foo = re.sub(r'\. .', ". ", foo)
	foo = re.sub(' +',' ', foo)
	foo = foo.replace(" .", ".")
	foo = re.sub(r'\.+', ".", foo)						# replacing '...*' with '.'
	foo = re.sub(r'\?+', "?", foo)						# replacing '???*' with '?'
	foo = re.sub(r'\!+', "!", foo)						# replacing '!*' with '!'
	#foo = re.sub(r'\ .', ".", foo)
	print foo	
	return foo

# def cleaner_function(text):

# 	emoji_pattern = re.compile("["
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#         u"\U0001F680-\U0001F6FF"  # transport & map symbols
#         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                            "]+", flags=re.UNICODE)

# 	text = re.sub(r"\b([A-Za-z]+)'re\b", '\\1 are', text)	# changing "'re" to 'are'
# 	text = re.sub(r"\b([A-Za-z]+)'s\b", '\\1 is', text)		# changing "'s" to 'is'
# 	text = re.sub(r"\b([A-Za-z]+)'m\b", '\\1 am', text)		# changing "'am" to 'am'
# 	text = re.sub(r"\b([A-Za-z]+)'ve\b", '\\1 have', text)	# changing "'ve" to 'have'
# 	text = re.sub(r"\b([A-Za-z]+)'ll\b", '\\1 will', text)	# changing "'ll" to 'will'
# 	text = re.sub(r"\b([A-Za-z]+)n't\b", '\\1 not', text)	# changing "n't" to 'not'
# 	text = re.sub(r"\b([A-Za-z]+)'d\b", '\\1 had', text)	# changing "'d" to 'had'

# 	text = text.replace(" n ", " and ")						# Replacing 'n' with 'and'
# 	text = text.replace(" bcz ", " because ")				# replacing 'bcz' with 'because'
# 	text = text.replace(" ur ", " your ")					# replacing 'ur' with 'your'
# 	text = text.replace(" b4 ", " before ")					# relpacing 'b4' with 'before'
# 	text = text.replace(" awsm ", " awesome ")				# replacing 'awsm' with 'awesome'
	

# 	text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))		# replacing 'testtttt' with 'testt'
# 	text = (emoji_pattern.sub(r'', text))					# remove emoji pattern in text

# 	text_words = text.split()
# 	res_word = [word for word in text_words if word not in emojis]

# 	txt = ' '.join(res_word)
# 	print('*'*80)
# 	print(txt)
	
# 	print('-'*100)
# 	return txt

# def load_doc(filename):
# 	# open the file as read only
# 	file = open(filename, 'r')
# 	# read all text
# 	text = file.read()
# 	# close the file
# 	file.close()
# 	return text
 
# emojis = [':-J', '=^_^=', ':-o', '=-D', '>_<', '(*_*)', '>_<*', '=)', '=(', ':-p', ':p', '=D',
# 				':-/', ':/', '>-:o', '>:o', 'B)', 'B-)', '8-|', '8|', 'O:)', 'O:-)', '<3', ':)', ':D',
# 				':(', ':-)', ':-(', ':P']

# load the document
# filename = 'sample.txt'
# text = load_doc(filename)
# print text
# clean_text = cleaner_function(text)
# print('_'*100)
clean_text = replace_escape_characters("this is not \n my.\n \n\n\n\n work\t\ttada")
print (clean_text)
