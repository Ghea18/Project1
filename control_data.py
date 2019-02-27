data = {}
def add(name, content):
    data[name] = content
def rem(name):
    del data[name]
def all():
    return data