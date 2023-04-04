import point

class prime_elliptic_curve:
    def __init__(self, p:int, a:int, b:int, G:point.point, keysize: int, name: str):
        self.a = a
        self.b = b
        self.p = p 
        self.G = G
        self.keysize = keysize
        self.name = name