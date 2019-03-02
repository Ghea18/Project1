class Data_control():
    """docstring for Data_control"""
    def __init__(self):
        super(Data_control, self).__init__()   
        self.data = {}
    def add(self, name, content):
        self.data[name] = content
    def rem(self, name):
        del self.data[name]
    def all(self):
        return self.data