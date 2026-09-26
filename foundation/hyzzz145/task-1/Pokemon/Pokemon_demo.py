import random
import time
import copy
import sys

#made by deepseek
#-------------------------------------------------------------------
def lucky_bar(prob, label="事件", width=40, duration=0.8, fps=40):

    print(f"{label} 概率抽奖")
    pause(pause_t*4)
    hit = random.random() <= prob
    green = max(1, round(prob * width))
    target = random.randint(0, green - 1) if hit else random.randint(green, width - 1)

    total = int(duration * fps)
    for i in range(total + 1):
        t = i / total
        if i == total:
            pos = target
        else:
            amp = (width / 2) * (1 - t) ** 2
            pos = int(target + amp * random.uniform(-1, 1))
            pos = max(0, min(width - 1, pos))

        bar = "█" * green + "░" * (width - green)
        line = list(" " * width)
        line[pos] = "▲"
        sys.stdout.write(f"\r  [{bar}]\n\r  {''.join(line)}\033[1A")
        sys.stdout.flush()
        time.sleep(1 / fps)

    sys.stdout.write(f"\r  [{bar}]\n\r  {''.join(line)}\n")
    print(f"  {'✨ 命中' if hit else '✖ 未中'}：{label}")
    pause(pause_t*5)
    return hit
#--------------------------------------------------------------

#延迟函数
def pause(t:float):
    time.sleep(t)
#战斗延迟
def pause_battle(t:float):
    for _ in range(5):
        pause(t/5)
        print(".",end="  ")
    print("")
pause_t = 0.8
        

#宝可梦类
class Pokemon():
    def __init__(self,name:str,hp:int,attack_value:int,defend_value:int,dodge_rate:int,chinese:str):
        self.max_hp = hp
        self.hp = hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dodge_rate = dodge_rate
        self.name = name
        self.chinese = chinese
        self.is_dizzy = 0
        #烧伤
        self.is_fired = 0
        #火蓄力
        self.flame_count = 0
        #护盾
        self.defend_rate = 0
        #中毒
        self.is_poisoning = 0
        #麻痹
        self.is_paralyzed = 0
        #寄生种子
        self.is_seed = 0
        #所属阵营
        self.belong = None
            
    #攻击伤害计算
    def attack(self,op_character:Pokemon,base_attack_value:int)->int:
        #躲闪计算
        is_dodge = 0
        #random.randint(1,100) <= op_character.dodge_rate:
        if lucky_bar(op_character.dodge_rate/100,'能否闪躲'):
            pause(pause_t)
            print(f"{op_character.belong} {op_character.chinese} 成功闪避！")
            is_dodge = 1

        #元素被克
        #这里 -1 代表被对方克制，1 代表克制对方
        is_counter = 0
        if self.element_id == 1:
            if op_character.element_id == 3:
                is_counter = 1
            elif op_character.element_id == 2:
                is_counter = -1
        elif self.element_id == 2:
            if op_character.element_id == 1:
                is_counter = 1
            elif op_character.element_id == 3:
                is_counter = -1
        elif self.element_id == 3:
            if op_character.element_id == 2:
                is_counter = 1
            elif op_character.element_id == 4:
                is_counter = -1
        elif self.element_id == 4:
            if op_character.element_id == 3:
                is_counter = 1
            elif op_character.element_id == 1:
                is_counter = -1

            
        '''
        is_counter = 0
        if (self.element_id - op_character.element_id) % 2 != 0:
            if self.element_id - op_character.element_id == 1 or self.element_id - op_character.element_id == -3:
                is_counter = 1
            else:
                is_counter = -1
        '''
        #攻击力的计算
        attack = base_attack_value
        if is_counter == 1:
            pause(pause_t)
            print("属性伤害翻倍")
            attack *= 2
        elif is_counter == -1:
            pause(pause_t)
            print("属性伤害减半")
            attack /= 2
        attack = max(0,attack - op_character.defend_value)
        if self.defend_rate:
            pause(pause_t)
            print(f"护盾吸收 {op_character.defend_rate}%")
            attack *= (100 - op_character.defend_rate)
            attack /= 100
        if is_dodge:
            attack = 0
        if op_character.is_fired:
            pause(pause_t)
            print(f"{op_character.belong} {op_character.chinese} 受到 10 点额外烧伤 {3 - op_character.is_fired * 2}/2")
            attack += 10
            op_character.is_fired -= 0.5
        if attack != 0:
            if self.element_id == 2:
                attack *= 1 + 0.1 * self.passive_skill()

        return attack
    #伤害扣除
    def reduce_hp(self,num:int,object:Pokemon):
        #水被动
        if num != 0 and object.element_id == 3:
            object.passive_skill(num)
        object.hp -= num
        pause(pause_t)
        print(f"{object.belong} {object.chinese} 受到了 {num} 点伤害！剩余 HP：{object.hp}/{object.max_hp}")
        #电被动
        if num != 0:
            if object.element_id == 4:
                object.passive_skill()


    #生命恢复
    def recover_hp(self,num:int):
        self.hp = min(self.max_hp,self.hp + num)
        pause(pause_t)
        print(f"{self.belong} {self.chinese} 生命值回复 {num}")

    #护盾增加
    def add_defend(self,num:int):
        self.defend_rate=min(100,self.defend_rate + num)
        pause(pause_t)
        print(f"{self.belong} {self.chinese} 护盾增加 {num}，目前护盾: {self.defend_rate}%")

    #闪避率增加
    def add_dodge(self,num:int):
        self.dodge_rate = min (100,self.dodge_rate + num)
        pause(pause_t)
        print(f"{self.belong} {self.chinese} 闪避率增加 {num}，目前闪避值：{self.dodge_rate}")

    #技能
    def skill_act(self,skill_num:int,op_character:Pokemon):
        if self.name == 'PikaChu':
            #十万伏特
            if skill_num == 1:
                self.reduce_hp(1.4 * self.attack(op_character,self.attack_value),op_character)
                #麻痹
                if lucky_bar(0.1,'十万伏特麻痹'):
                #random.random() <= 0.1:
                    pause(pause_t)
                    print(f"{op_character.belong} {op_character.chinese} 已被麻痹")
                    op_character.is_paralyzed = 1

            #电光一闪
            if skill_num == 2:
                self.reduce_hp(self.attack(op_character,self.attack_value),op_character)
                if lucky_bar(0.1,'电光一闪连续攻击'):
                #random.random() <= 0.1:
                    pause(pause_t)
                    print("**触发连续攻击**")
                    self.reduce_hp(self.attack(op_character,self.attack_value),op_character)
        if self.name == 'Bulbasaur':
            #种子炸弹
            if skill_num == 1:
                self.reduce_hp(self.attack(op_character,self.attack_value),op_character)
                #中毒
                if lucky_bar(0.1,'种子炸弹中毒'):
                #random.random() <= 0.1:
                    op_character.is_poisoning = 1
            #寄生种子
            if skill_num == 2:
                self.is_seed = 3
                pause(pause_t)
                print("寄生种子下回合生效")

        if self.name == 'Squirtle':
            #水枪
            if skill_num == 1:
                self.reduce_hp(1.4 * self.attack(op_character,self.attack_value),op_character)

            #护盾
            if skill_num == 2:
                self.add_defend(50)
                self.reduce_hp(self.attack(op_character,0),op_character)

        if self.name == 'Charmander':
            #火花
            if skill_num == 1:
                self.reduce_hp(self.attack(op_character,self.attack_value),op_character)
                #烧伤
                if lucky_bar(0.1,'烧伤'):
                #random.random() <= 0.1:
                    pause(pause_t)
                    print(f"{op_character.belong} {op_character.chinese} 成功被烧伤")
                    op_character.is_fired = 1
                
            #蓄能爆炎
            if skill_num == 2:
                if self.flame_count:
                    op_character.add_dodge(20)
                    self.reduce_hp(3 * self.attack(op_character,self.attack_value),op_character)
                    #烧伤
                    if lucky_bar(0.8,'烧伤'):
                    #random.random() < 0.8:
                        pause(pause_t)
                        print(f"{op_character.belong} {op_character.chinese} 成功被烧伤")
                        op_character.is_fired = 1
                    self.flame_count = 0
                else:
                    self.flame_count += 1
                    pause(pause_t)
                    print(f"{self.belong} {self.chinese}蓄能爆炎 已蓄能！")

            

#元素类
class WaterPokemon(Pokemon):
    def __init__(self, name, hp, attack_value, defend_value, dodge_rate,chinese):
        super().__init__(name, hp, attack_value, defend_value, dodge_rate,chinese)

    #类属性
    element = 'water'
    element_id = 3
    element_chinese = '水属性'
    def passive_skill(self,attack:int):
        if lucky_bar(0.5,'水属性被动'):
        #random.random() <= 0.5:
            pause(pause_t)
            print("水属性被动发动，伤害减免30%")
            attack *= 0.7

class FirePokemon(Pokemon):
    def __init__(self, name, hp, attack_value, defend_value, dodge_rate,chinese):
        super().__init__(name, hp, attack_value, defend_value, dodge_rate,chinese)
        self.passive_skill_num = 0
    #类属性
    element = 'fire'
    element_id = 2
    element_chinese = '火属性'
    
    def passive_skill(self)->int:
        pause(pause_t)
        print(f"{self.chinese} 被动启用")
        if self.passive_skill_num <= 4:
            self.passive_skill_num += 1
        print(f"当前层数 （{self.passive_skill_num}/4）")
        return self.passive_skill_num

class GrassPokemon(Pokemon):
    def __init__(self, name, hp, attack_value, defend_value, dodge_rate,chinese):
        super().__init__(name, hp, attack_value, defend_value, dodge_rate,chinese)
    #类属性
    element = 'grass'
    element_id = 1
    element_chinese = '草属性'
    def passive_skill(self):
        pause(pause_t)
        print(f"{self.chinese} 回合触发草属性被动")
        self.recover_hp(0.1 * self.max_hp)
class ElectricPokemon(Pokemon):
    def __init__(self, name, hp, attack_value, defend_value, dodge_rate,chinese):
        super().__init__(name, hp, attack_value, defend_value, dodge_rate,chinese)
        self.is_act = 0
    #类属性
    element = 'electric'
    element_id = 4
    element_chinese = '电属性'
    def passive_skill(self):
        self.is_act = 1



class Game():

    def __init__(self):
        pass
    def start(self):
        self.character = []
        #皮卡丘
        self.character.append(ElectricPokemon('PikaChu',80,35,5,30,"皮卡丘"))
        #妙蛙种子
        self.character.append(GrassPokemon('Bulbasaur',100,35,10,10,"妙蛙种子"))
        #杰尼龟
        self.character.append(WaterPokemon('Squirtle',80,25,20,20,"杰尼龟"))
        #小火龙
        self.character.append(FirePokemon('Charmander',80,35,15,10,"小火龙"))
        self.player_dizzy = []
        self.computere_dizzy = []
        self.player_paralyzed = []
        self.computere_paralyzed = []
        self.turn = 0
        self.run = 1
        self.character_choice()
        

    def character_choice(self):
        pause(pause_t)
        print("请选择 3 个宝可梦用于组成你的队伍：")
        pause(pause_t)
        for i in range(len(self.character)):
            print(f"{i+1}.  {self.character[i].chinese}({self.character[i].element_chinese})",end="  ")
            pause(pause_t/5)
        print("")
        pause(pause_t)
        self.choice = input("输入数字选择你的宝可梦：").split()
        self.player_pokemon = []
        for i in range(3):
            self.player_pokemon.append(copy.copy(self.character[int(self.choice[i]) - 1]))
        #阵营初始化
        for i in self.player_pokemon:
            i.belong = '你的'
        pause(pause_t)
        print("")
        #人机宝可梦发放
        random.shuffle(self.character)
        self.computere_pokemon = []
        for i in range(3):
            self.computere_pokemon.append(copy.copy(self.character[i]))
        #阵营初始化
        for i in self.computere_pokemon:
            i.belong = '对方的'
        self.game_looping()

    def game_looping(self)->bool:
        #判断结束函数
        def is_end(self):
            for i in self.computere_pokemon:
                if i.hp <= 0:
                    i.is_dizzy = 1
            for i in self.player_pokemon:
                if i.hp <= 0:
                    i.is_dizzy = 1
            if self.computere_pokemon[0].is_dizzy and self.computere_pokemon[1].is_dizzy and self.computere_pokemon[2].is_dizzy:
                if self.player_pokemon[0].is_dizzy and self.player_pokemon[1].is_dizzy and self.player_pokemon[2].is_dizzy:
                    return 'double'
                else:
                    return 'player'
            elif self.player_pokemon[0].is_dizzy and self.player_pokemon[1].is_dizzy and self.player_pokemon[2].is_dizzy:
                return 'computer'
            else:
                return False
        #显示函数
        def show(pokemon_list:list,dizzy_list:list,paralyzed_list:list):
            for i in range(3):
                pause(pause_t/4)
                print(f"{i+1}.{pokemon_list[i].chinese}({pokemon_list[i].element_chinese})",end="  ")
                #晕厥判定
                if pokemon_list[i].is_dizzy:
                    print("(已晕厥)")
                    if not i in dizzy_list:
                        dizzy_list.append(i)
                elif i in dizzy_list:
                    dizzy_list.remove(i)
                #麻痹判定
                elif pokemon_list[i].is_paralyzed:
                    print("(已麻痹)")
                else:
                    print(f"({pokemon_list[i].hp}/{pokemon_list[i].max_hp})")
                if pokemon_list[i].is_paralyzed:
                    pokemon_list[i].is_paralyzed -= 0.25
                    if not i in paralyzed_list:
                        paralyzed_list.append(i)
                elif i in paralyzed_list:
                    paralyzed_list.remove(i)
        #状态更新函数
        def updata(self):
            for i in self.player_pokemon:
                if i.element_id == 4:
                    i.is_act = 0 
            for i in self.computere_pokemon:
                if i.element_id == 4:
                    i.is_act = 0 

        #技能释放函数
        #玩家
        def player_skill(self):
            pause(pause_t)
            print(f"你的 {self.player_current_pokemon.chinese} 的技能：")
            pause(pause_t)
            print(f"1.{SKILL[self.player_current_pokemon.name][0]}")
            pause(pause_t)
            print(f"2.{SKILL[self.player_current_pokemon.name][1]}")
            pause(pause_t)
            self.skill_choice = int(input("选择一个技能进行攻击："))
            print("=====你的回合=====")
            pause(pause_t)
            print(f"{self.player_current_pokemon.belong} {self.player_current_pokemon.chinese} 使用了 {SKILL[self.player_current_pokemon.name][self.skill_choice - 1]}！")
            pause(pause_t)
            self.player_current_pokemon.skill_act(self.skill_choice,self.computere_current_pokemon)
            pause(pause_t)
            print("")
            pause(pause_t)
            if is_end(self):
                self.run = 0
        #人机
        def computere_skill(self):
            pause(pause_t)
            self.computere_skill_choice = random.randint(1,2)
            print(f"{self.computere_current_pokemon.belong} {self.computere_current_pokemon.chinese} 使用了 {SKILL[self.computere_current_pokemon.name][self.computere_skill_choice - 1]}！")
            self.computere_current_pokemon.skill_act(self.computere_skill_choice,self.player_current_pokemon)
            pause(pause_t)
            print("")
            pause(pause_t)
            print("")
            if is_end(self):
                self.run = 0

        #战斗循环
        while(self.run):
            #回合数
            self.turn += 1
            #更新
            updata(self)
            print(f"======{self.turn} Turn =====")
            pause(pause_t)
            #玩家角色选择显示
            print("请选择你的宝可梦：")
            pause(pause_t)
            show(self.player_pokemon,self.player_dizzy,self.player_paralyzed)
            '''
            for i in range(3):
                print(f"{i+1}.{self.player_pokemon[i].chinese}({self.player_pokemon[i].element_chinese})",end="  ")
                #玩家晕厥判定
                if self.player_pokemon[i].is_dizzy:
                    print("(已晕厥)")
                    if not i in self.player_dizzy:
                        self.player_dizzy.append(i)
                elif i in self.player_dizzy:
                    self.player_dizzy.remove(i)
                #玩家麻痹判定
                elif self.player_pokemon[i].is_paralyzed:
                    print("(已麻痹)")
                else:
                    print(f"({self.player_pokemon[i].hp}/{self.player_pokemon[i].max_hp})")
                if self.player_pokemon[i].is_paralyzed:
                    self.player_pokemon[i].is_paralyzed -= 0.25
                    if not i in self.player_paralyzed:
                        self.player_paralyzed.append(i)
                elif i in self.player_paralyzed:
                    self.player_paralyzed.remove(i)
                pause(0.1)
            '''
            pause(pause_t/4)
            print("4.查看所有角色HP")
            pause(pause_t)
            #玩家角色选择
            self.player_current_pokemon_num = -1
            self.player_current_pokemon_num = int(input("输入数字决定你的选择："))
            #选择 4 时，显示信息
            while self.player_current_pokemon_num == 4:
                pause(pause_t)
                print("======你自己======")
                show(self.player_pokemon,self.player_dizzy,self.player_paralyzed)
                pause(pause_t)
                print("======对方========")
                pause(pause_t)
                show(self.computere_pokemon,self.computere_dizzy,self.computere_paralyzed)
                self.player_current_pokemon_num = int(input("输入数字决定你的选择："))
            #完成显示信息循环后，赋值当前角色
            self.player_current_pokemon = self.player_pokemon[self.player_current_pokemon_num - 1]
            #判断所选角色是否晕厥
            while self.player_current_pokemon_num - 1 in self.player_dizzy:
                pause(pause_t)
                print(f"你的 {self.player_current_pokemon.chinese} 目前已晕厥！")
                pause(pause_t)
                self.player_current_pokemon_num = int(input("请输入数字重新选择你的宝可梦："))
                self.player_current_pokemon = self.player_pokemon[self.player_current_pokemon_num - 1]
            #判断角色是否麻痹
            while self.player_current_pokemon_num - 1 in self.player_paralyzed:
                pause(pause_t)
                print(f"你的 {self.player_current_pokemon.chinese} 目前已麻痹！")
                pause(pause_t)
                self.player_current_pokemon_num = int(input("请输入数字重新选择你的宝可梦："))
                self.player_current_pokemon = self.player_pokemon[self.player_current_pokemon_num - 1]
            pause(pause_t)
            print(f"你选择了 {self.player_current_pokemon.chinese}！")
            pause(pause_t)
            #电脑选择
            #电脑晕厥判断
            for i in range(3):
                #电脑晕厥更新
                if self.computere_pokemon[i].is_dizzy:
                    if not i in self.computere_dizzy:
                        self.computere_dizzy.append(i)
                elif i in self.computere_dizzy:
                    self.computere_dizzy.remove(i)
                #电脑麻痹更新
                if self.computere_pokemon[i].is_paralyzed:
                    if not i in self.computere_paralyzed:
                        self.computere_paralyzed.append(i)
                elif i in self.computere_paralyzed:
                    self.computere_paralyzed.remove(i)
            #电脑角色选择随机
            self.computere_current_pokemon_num = random.randint(0,2)
            self.computere_current_pokemon = self.computere_pokemon[self.computere_current_pokemon_num]
            #电脑扣除禁用
            while self.computere_current_pokemon_num in self.computere_dizzy or self.computere_current_pokemon_num in self.computere_paralyzed:
                self.computere_current_pokemon_num = random.randint(0,2)
                self.computere_current_pokemon = self.computere_pokemon[self.computere_current_pokemon_num]
            pause(pause_t)
            print(f"电脑选择了 {self.computere_current_pokemon.chinese}！")
            pause(pause_t)
            print("")

            #中毒判定
            for i in self.player_pokemon:
                if i.is_poisoning:
                    pause(pause_t)
                    print(f"{i.chinese} 受中毒影响，扣除了{int(0.1 * i.hp)}点伤害，当前HP：{i.hp - int(0.1 * i.hp)} ")
                    i.hp = i.hp - int(0.1 * i.hp)
            for i in self.computere_pokemon:
                if i.is_poisoning:
                    pause(pause_t)
                    print(f"{i.chinese} 受中毒影响，扣除了{int(0.1 * i.hp)}点伤害，当前HP：{i.hp - int(0.1 * i.hp)} ")
                    i.hp = i.hp - int(0.1 * i.hp)
                    
            pause(pause_t)
            #玩家技能
            #草被动
            for i in self.player_pokemon:
                if i.element_id == 1:
                    i.passive_skill()
            player_skill(self)
            #电被动
            if self.computere_current_pokemon.element_id == 4:
                if self.computere_current_pokemon.is_act:
                    pause(pause_t)
                    print(f"{self.computere_current_pokemon.chinese} 触发电属性被动")
                    #用于调试
                    #print("电脑电触发被动") 
                    computere_skill(self)
                    self.computere_current_pokemon.is_act = 0

            pause_battle(pause_t*7)
            '''
            print(f"你的 {self.player_current_pokemon.chinese} 的技能：")
            pause(0.2)
            print(f"1.{SKILL[self.player_current_pokemon.name][0]}")
            pause(0.1)
            print(f"2.{SKILL[self.player_current_pokemon.name][1]}")
            pause(0.5)
            self.skill_choice = int(input("选择一个技能进行攻击："))
            print("=====你的回合=====")
            pause(0.1)
            print(f"{self.player_current_pokemon.chinese} 使用了 {SKILL[self.player_current_pokemon.name][self.skill_choice - 1]}！")
            pause(0.3)
            pause(0.1)
            self.player_current_pokemon.skill_act(self.skill_choice,self.computere_current_pokemon)
            pause(0.1)
            if is_end(self):
                break
            print("")
            pause(0.2)
            '''
            print("=====对方回合=====")
            #人机技能
            #草被动
            for i in self.computere_pokemon:
                if i.element_id == 1:
                    i.passive_skill()
            #技能发动
            computere_skill(self)
            #电被动
            if self.player_current_pokemon.element_id == 4:
                if self.player_current_pokemon.is_act:
                    pause(pause_t)
                    print(f"{self.player_current_pokemon.chinese} 触发电属性被动")
                    player_skill(self)
            pause_battle(pause_t*7)
            #护盾扣除
            for i in self.computere_pokemon:
                if i.defend_rate != 0:
                    i.defend_rate = max(0,i.defend_rate - 30)
                    pause(pause_t)
                    print(f"电脑的{i.chinese} 护盾失去 30%")
                    print(f"目前护盾{i.defend_rate}")
            for i in self.player_pokemon:
                if i.defend_rate != 0:
                    i.defend_rate = max(0,i.defend_rate - 30)
                    pause(pause_t)
                    print(f"你的{i.chinese} 护盾失去 30%")
                    print(f"目前护盾{i.defend_rate}")
            '''
            pause(0.1)
            print(f"{self.computere_current_pokemon.chinese} 使用了 {SKILL[self.computere_current_pokemon.name][self.skill_choice - 1]}！")
            self.computere_current_pokemon.skill_act(random.randint(1,2),self.player_current_pokemon)
            pause(0.1)
            print("")
            pause(0.1)
            print("")
            '''

        if is_end(self) == 'player':
            pause(pause_t)
            print("恭喜你胜利")
            pause(pause_t)
            print("你的阵营如下：")
            show(self.player_pokemon,self.player_dizzy,self.player_paralyzed)
        elif is_end(self) == 'computer':
            pause(pause_t)
            print("可惜了，你的三个宝可梦倒下了")
            pause(pause_t)
            print("对方的阵营如下：")
            show(self.computere_pokemon,self.computere_dizzy,self.computere_paralyzed)
        else:
            print("平局了？？？")
            show(self.player_pokemon,self.player_dizzy,self.player_paralyzed)
            show(self.computere_pokemon,self.computere_dizzy,self.computere_paralyzed)


SKILL = {"PikaChu":['十万伏特','电光一闪'],
    "Bulbasaur":['种子炸弹','寄生种子'],
    "Squirtle":['水枪','护盾'],
    "Charmander":['火花','蓄能爆炎']}

a = Game()
a.start()