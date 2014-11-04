##MODULE = 'C:\Documents and Settings\dfg\Desktop\dev\wikia\pattern-2.6\pattern'
##import sys
##if MODULE not in sys.path: sys.path.append(MODULE)
from pattern.web import Wikia

w = Wikia(domain='lostpedia')
a = w.article(query="Richard_Alpert")

for i, title in enumerate(w.index(start='a', throttle=1.0, cached=True)):     
     if i >= 3:
         break
     article = w.search(title)
     print repr(article.title)
