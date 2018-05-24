# from gingerit.gingerit import GingerIt

# text = "the got busi working"

# parser = GingerIt()
# print parser.parse(text)['result']

# print text


from googletrans import Translator
translator = Translator()

txt = "they got busy workin"
spell = translator.translate(txt, dest='en')
print spell.text

# import coreference_resolution as cr 

# text = "The got busi in wrk"

# op = cr.correct_spell(text)
# print op