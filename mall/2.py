class TomatoesAndEgg:
    def __init__(self):
        self.data = '番茄炒蛋'

    def getData(self):
        return self.data

class SugarAndCucumber:
    def __init__(self):
        self.data = '白糖拌黄瓜'

    def getData(self):
        return self.data

class CookFactory:
    def cook_te(self):
        return TomatoesAndEgg()

    def cook_sc(self):
        return SugarAndCucumber()

if __name__ == '__main__':
    cook = CookFactory()

    man = cook.cook_te()
    woman = cook.cook_sc()

    data_man = man.getData()
    data_woman = woman.getData()

    print(data_man)
    print(data_woman)