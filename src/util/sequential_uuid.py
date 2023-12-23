class SequentialID:
    def __init__(self, name: str = "default"):
        self.counter = 0
        self.name = name

    def generate_name(self):
        res = f'{self.name}__{str(self.counter)}'
        self.increase_counter()
        return res

    def increase_counter(self):
        self.counter += 1
