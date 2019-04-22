class PhoneStore:
    def __init__(self):
        self.factory=PhoneFactory()

    def sellPhone(self,phone_type):
        return self.factory.createPhone(phone_type)

class PhoneFactory:
    def createPhone(self,phone_type):
        if phone_type=='华为mate20':
            return HwMate20()
        elif phone_type=='iphone xs':
            return IphoneXs()
        elif phone_type=='oppo R17':
            return OppoR17()

class Phone:
    def call(self):
        print('打电话...')
    def watch(self):
        print('看视频...')
    def photo(self):
        print('拍照...')
    def game(self):
        print('玩游戏...')

class HwMate20(Phone):
    pass
class IphoneXs(Phone):
    def __str__(self):
        return 'iphone xs'
class OppoR17(Phone):
    pass

store = PhoneStore()
print(store.sellPhone('华为mate20'))