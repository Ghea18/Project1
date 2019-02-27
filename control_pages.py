pages = {}
active = "";
def add(name, url):
    pages[name] = url
def rem(name):
    del pages[name]
def atv(page):
    pages["page_active"] = page
def all():
    return pages