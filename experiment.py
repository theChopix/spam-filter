class Number:

    def __init__(self, num):
        self.num = num

    def sum(self):
        n = self.num + 1
        print(n)


class Experiment:

    def __init__(self):
        self.afilter = Number(1)
        self.bfilter = Number(2)
        self.cfilter = Number(3)

    def printf(self):
        filters = [getattr(self, attr) for attr in dir(self) if attr.endswith("filter")]
        for filter in filters:
            filter.sum()


if __name__ == '__main__':
    exp = Experiment()
    exp.printf()

