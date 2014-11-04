from pattern.web import Wikia, URL, GET, json, cache
from operator import itemgetter

class MyWikia(Wikia):
    def cats(self, namespace=0, start=None, acmin=1, count=100, cached=True, **kwargs):
        """ Returns an iterator over all article titles (for a given namespace id).
        """
        kwargs.setdefault("unicode", True)
        kwargs.setdefault("throttle", self.throttle)
        # Fetch article titles (default) or a custom id.
        id = kwargs.pop("_id", "title")
        id = "*"
        # Loop endlessly (= until the last request no longer yields an "apcontinue").
        # See: http://www.mediawiki.org/wiki/API:Allpages
        while start != -1:
            url = URL(self._url, method=GET, query={
                     "action": "query",
                       "list": "allcategories",
                     "acfrom": start or "",
                    "aclimit": min(count, 500),
                    "acprop": "size",
                    "acmin": max(1, acmin),
                     "format": "json"
            })
            data = url.download(cached=cached, **kwargs)
            data = json.loads(data)
            for x in data.get("query", {}).get("allcategories", {}):
                # print(x)
                if x.get(id):
                    # yield x[id]
                    x['name'] = x.pop('*')
                    yield x

            start = data.get("query-continue", {}).get("allcategories", {})
            start = start.get("accontinue", start.get("acfrom", -1))
        raise StopIteration

"""
w = Wikia(domain='lostpedia')
for i, title in enumerate(w.index(start='d', throttle=1.0, cached=True)):
    if i >= 3:
        break
    a = w.search(title)
    # print repr(article.title)
    print "Title=%s\nCategories=%s\nLinks=%s\nMedia=%s" \
      % (a.title, a.categories, a.links, a.media)
"""

w = MyWikia(domain='lostpedia')
cats = []
for cat in w.cats(acmin=100, count=500, throttle=1.0, cached=True):
    cname = cat['name'].lower()
    if cname.find("image") == -1 and cname.find("file") == -1:
        cats.append(cat)
cats.sort(key=itemgetter("size", "subcats"), reverse=True)
for c in cats:
    print"Cat: %s (%s)" % (c["name"], c["size"])

