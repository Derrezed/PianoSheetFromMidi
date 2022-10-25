class DataHolder:
    def __init__(self):
        self.keys = []
        self.keys_change_right = ""
        self.keys_change_left = ""

    def add_keys(self, data):
        self.keys.append(data)

    def add_keys_change_right(self, data):
        self.keys_change_right = data

    def add_keys_change_left(self, data):
        self.keys_change_left = data
