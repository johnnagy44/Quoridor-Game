from dataclasses import dataclass

@dataclass
class Player:
    
    r: int
    c: int
    walls: int = 10
    is_ai: bool = False
    id: int = 0
    name: str=""

    def pos(self):
        return (self.r, self.c)
