class TomatoesAndEgg:
    def __init__(self):
        self.data = '男士喜欢吃番茄'

    def getData(self):
        return self.data

class SugarAndCucumber:
    def __init__(self):
        self.data = '女士喜欢吃甜食'

    def getData(self):
        return self.data

def cook_factory(sex):
    if sex == 'man':
        food = TomatoesAndEgg
    elif sex == 'woman':
        food = SugarAndCucumber
    else:
        raise ValueError('请输入正确性别:()'.fromat(sex))
    return food()

if __name__ == '__main__':
    man = cook_factory('man')
    woman = cook_factory('woman')

    data_man = man.getData()
    data_woman = woman.getData()

    print(data_man)
    print(data_woman)