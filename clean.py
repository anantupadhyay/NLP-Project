import re
import itertools

def replace_escape_characters(foo):
	idx = 1
	while(idx!=-1):
		idx = foo.find('\n')
		#print foo[idx-1]
		if((foo[idx-1]==' ' and foo[idx-2] == '.') or foo[idx-1]=='.'):
			foo = foo.replace('\n', ' ')
		if(foo[idx-1]==' ' and foo[idx-2]!='.'):
			foo = foo.replace(' \n', '. ')
		elif(foo[idx-1]!=' ' and foo[idx-1]!='.'):
			foo = foo.replace('\n', '. ')
	idx = 1
	while(idx != -1):
		#print idx
		idx = foo.find('\t')
		foo = foo.replace('\t', ' ')

	print (foo)

	#foo = re.sub('\. .', ". ", foo)
	foo = re.sub(' +',' ', foo)
	foo = foo.replace(" .", ".")
	foo = re.sub(r'\.+', ".", foo)						# replacing '...*' with '.'
	foo = re.sub(r'\?+', "?", foo)						# replacing '???*' with '?'
	foo = re.sub(r'\!+', "!", foo)						# replacing '!*' with '!'
	#foo = re.sub(r'\ .', ".", foo)
	#print foo	
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

def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text
 
# emojis = [':-J', '=^_^=', ':-o', '=-D', '>_<', '(*_*)', '>_<*', '=)', '=(', ':-p', ':p', '=D',
# 				':-/', ':/', '>-:o', '>:o', 'B)', 'B-)', '8-|', '8|', 'O:)', 'O:-)', '<3', ':)', ':D',
# 				':(', ':-)', ':-(', ':P']

#load the document
filename = 'sample.txt'
text = load_doc(filename)
# clean_text = cleaner_function(text)
# print('_'*100)
clean_text = replace_escape_characters("this property is like a guest house not a townhouse no room services avaialble no proper breakfast provided cold tea. I was given two separate bed instead of a king size one. There was construction going on just above my room which made it impossible to stay in the room. There were no water bottles in the room. There was no ac remote and when one was given it was not working either. The toilet seat was dirty. The most pathetic experience ever. Horrible experience full night i sleep in without electricity no fan no ac working please resolve other wise i never stay in oyo and share in my page about oyo horrible hotels. i asked them for a double quilt as i had two single but the reception guy said we dont keep extra. in lunch ordered shahi thali with , green chicken, but gavwe paneer. idnt gave anything from that. Hot water was available. thisssss is testtt stringgggggg. I did not check in, n yet the booking says I did. Will just anyone go n have a simple hygiene n cleaning audit. ? From the entrance door- big red color - misaligned. ift floor matt has enough dirt with bad odour comes from the reception lobby till the room. hecked in 205, bedsheets were dirty with mark on the pillow covers. athrooms flush is falling apart, shower curtain are stained badly.then shifted to room number 305, same issue there also but somehow compromised as we were very tried. In room , they should provide glass, tea cup and electric kettle. they should also provide food menu card , room service number, operator numbers. the hotel was awsm :). this is no t \n my.\n \n\n\n\n work\t\ttada")
print (clean_text)
