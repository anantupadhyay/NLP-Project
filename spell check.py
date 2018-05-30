# -*- coding: utf-8 -*-

# from gingerit.gingerit import GingerIt

# text = "the got busi working .the got busi working. the got busi working. the got busi working . the got busi working .the got busi working. the got busi working. the got busi working ."
# text = "Klüft skräms inför på fédéral électoral große"

# parser = GingerIt()
# print parser.parse(text)['result']

# print text


from googletrans import Translator
translator = Translator()

txt = "Klüft skräms inför på fédéral électoral große stüff"
spell = translator.translate(txt, dest='en')
op = (spell.text).encode("utf-8")
print op

# import coreference_resolution as cr 

# text = "The got busi in wrk"

# op = cr.correct_spell(text)
# print op
