class Person:
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

class Male(Person):
    def __init__(self,name):
        self.name = name

        print ('Hello Mr.%s'%self.name)

class Feamle(Person):
    def __init__(self,name):
        self.name = name
        print ('Hello Miss.%s'%self.name)

class Factory:
    def getPerson(self,name,gender):
        if gender == 'M':
            return Male()
        if gender == 'F':
            return Feamle()

if __name__ == '__main__':
    factory = Factory()
    person = factory.getPerson('Chetan','M')
    print(person)