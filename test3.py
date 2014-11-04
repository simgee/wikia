##MODULE = 'C:\Documents and Settings\dfg\Desktop\dev\wikia\pattern-2.6\pattern'
##import sys
##if MODULE not in sys.path: sys.path.append(MODULE)
from pattern.web import Wikia

w = Wikia(domain='lostpedia')
a = w.article(query="ABC Medianet")
print repr(a.title)
print repr(a.categories)
