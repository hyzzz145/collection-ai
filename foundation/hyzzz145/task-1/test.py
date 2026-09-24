class a():
    def __init__(self,hp):
        self.hp = hp
m = a(3)
b = []
c = []
b[0] = m
c.append(m)
b[0].hp += 3
print(b[0].hp)
print(c[0].hp)