from effect import Effect
#卡牌主类
class Card():
    def __init__(self,suit:str,rank:int,act_time:int,effect:Effect)->None:
        #花色
        self.suit = suit
        #点数
        self.rank = rank
        #触发时间，0代表现在
        self.act_time = act_time

#基本牌
class Basic_card(Card):
    def __init__(self, suit, rank, act_time, effect):
        super().__init__(suit, rank, act_time, effect)

class sha(Basic_card):
    def __init__(self, suit, rank, act_time):
        super().__init__(suit, rank, act_time, Effect.sha(self))
