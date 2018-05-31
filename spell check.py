# -*- coding: utf-8 -*-

from gingerit.gingerit import GingerIt

text = "the got busi working .the got busi working. the got busi working. the got busi working . the got busi working .the got busi working. the got busi working. the got busi working ."
#text = "Klüft skräms inför på fédéral électoral große"

parser = GingerIt()
print parser.parse(text)['result'], '\n'

#print text


from googletrans import Translator
translator = Translator()

txt = "Klüft skräms inför på fédéral électoral große stüff"
spell = translator.translate(txt, dest='en')
op = (spell.text).encode("utf-8")
print op
