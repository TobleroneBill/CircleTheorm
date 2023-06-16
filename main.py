# Will show if a point opposite a diameter is always a right angle
import pygame
import math
import asyncio

# pygame template
WIDTH, HEIGHT = 500,500
flags = pygame.SRCALPHA
window = pygame.display.set_mode((WIDTH,HEIGHT),flags=flags)
pygame.display.set_caption("Circle Theorm's")
clock = pygame.time.Clock()
focused = True
bgColors= (
    (17, 0, 158),   # Dark Blue
    (73, 66, 228),
    (134, 150, 254),
    (196, 176, 255) # light faint purple
)

# side of c2
def pythag(p1,p2):
    a = p1[0] - p2[0]
    b = p1[1] - p2[1]
    return math.sqrt(a**2+b**2)

def IncrementTowards(a, b):
    if (a < b):
        return a + 1
    if (a > b):
        return a - 1
    return a

class BG:
    def __init__(self):
        self.activeColor = bgColors[0]
        self.next = 1
        self.timeMultiplier = 5
        self.time = 0
    
    def update(self):
        self.time +=1
        if self.time % self.timeMultiplier == 0:
            self.time = 0
            if self.activeColor != bgColors[self.next]:
                self.activeColor = (
                IncrementTowards(self.activeColor[0],bgColors[self.next][0]),
                IncrementTowards(self.activeColor[1],bgColors[self.next][1]),
                IncrementTowards(self.activeColor[2],bgColors[self.next][2]),
                )
                return
            else:
                self.next +=1
                if self.next >= len(bgColors)-1:
                    self.next = 0
        
    def Draw(self):
        self.update()
        window.fill(self.activeColor)

class input:
    def __init__(self,player):
        self.activeplayer = player

    def SetPlayer(self,player):
        self.activeplayer = player

    def input(self):
        if self.activeplayer == None:
            return
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pass
            

        if self.keys[pygame.K_LEFT]:
            self.activeplayer.Left()

        if self.keys[pygame.K_RIGHT]:
            self.activeplayer.Right()
            
class point:
    a = (0,250) 
    b = (500,250)

    def __init__(self):
        self.angle = 0  # radians
        self.len = 250  # makes it easier to reference
        self.pos = self.getPos()   # calculated Pos
        self.speed = 1
        
    def Left(self):
        self.angle += math.radians(self.speed)
        self.pos = self.getPos()
        if self.angle > math.radians(360):
            self.angle = 0

    def Right(self):
        self.angle -= math.radians(self.speed)
        self.pos = self.getPos()
        if self.angle < -math.radians(360):
            self.angle = 0

    def getPos(self):
        x = math.cos(self.angle) * self.len
        y = math.sin(self.angle) * self.len
        return (250 + x,250 + y)



    def DrawRightAngle(self):
        p1 = (self.pos[0],250)
        
        # solve for angle C
        c = self.pos

        # Angle - SSS formula
        # Cos(c) = (a^2 + b^2 -  c^2) / 2*(a*b)
        # c = cos-1(a^2 + b^2 -  c^2) / 2*(a*b)
    
        # ab is window x to x + size
        ab = 500    # c
        # pythag
        ac = pythag(point.a,c)    # b
        bc = pythag(point.b,c)    # a
        
        # letters are opposite sides in equation
        # c = cos-1(bc^2 + ac^2 -  ab^2) / 2*(bc*ac)
        
        part1 = ((bc**2 + ac**2) - ab **2)
        part2 = part1 / 2 * (bc * ac)
        acbAngle = math.acos(part2)

        # this really is always 90 degrees :0
        # print(math.degrees(acbAngle))

        # end pt - start pt

        scalar = 0.2

        middle = (((point.b[0] - self.pos[0]) + (point.a[0] - self.pos[0])),(point.b[1] - self.pos[1]) + (point.a[1] - self.pos[1])) 

        polypoints = (
            self.pos,
            (self.pos[0] + scalar * (point.b[0]   - self.pos[0]),self.pos[1] + scalar * (point.b[1]   - self.pos[1])),
            (self.pos[0] + scalar * middle[0],self.pos[1] + scalar * middle[1]),
            (self.pos[0] + scalar * (point.a[0] - self.pos[0]),self.pos[1] + scalar * (point.a[1] - self.pos[1])),
        )

        #Lines
        pygame.draw.line(window,(255,255,255),p1,self.pos,7)
        pygame.draw.line(window,(0,0,0),self.pos,p1,5)

        alphaDraw = pygame.Surface((500,500),pygame.SRCALPHA)
        alphaDraw.set_alpha(128)
        pygame.draw.polygon(alphaDraw,(72, 198, 57),polypoints)
        
        #text
        FDegrees = pygame.font.Font(pygame.font.get_default_font(),36)
        text = FDegrees.render(F'{round(math.degrees(acbAngle))}°',False,(255,255,255))

        FFormula = pygame.font.Font(pygame.font.get_default_font(),18)
        FormulaText = FFormula.render(F'c = cos-1(a^2 + b^2 - c^2) / 2*(a*b)',False,(255,255,255))

        FESCtext = pygame.font.Font(pygame.font.get_default_font(),12)
        ESCtext = FESCtext.render(F'Left/Right to move',False,(255,255,255))

        alphaDraw.blit(text,(228,200))
        alphaDraw.blit(FormulaText,(115,275))
        alphaDraw.blit(ESCtext,(0,0))

        window.blit(alphaDraw,(0,0))

        pygame.draw.line(window,(255,255,255),self.pos,point.a,3)
        pygame.draw.line(window,(255,255,255),self.pos,point.b,3)
        pygame.draw.line(window,(255,255,255),self.pos,(250,250),5)

    # Draw angle, point and connecting lines to make right angle
    def Draw(self):
        self.DrawRightAngle()

#  setup
pygame.init()
Circlepos = (WIDTH//2,HEIGHT//2)
player = point()
manager = input(player)
bg = BG()

# a to b
Diameter = (
    (0,250),
    (500,250)
            )

def Draw():
    bg.Draw()
    player.Draw()
    pygame.draw.line(window,(228, 73, 66),Diameter[0],Diameter[1],5)
    pygame.draw.circle(window,(228, 73, 66),Circlepos,10)
    pygame.draw.circle(window,(66, 228, 73),Circlepos,250,5)
    pygame.draw.circle(window,(255, 0, 171),player.pos,5)

async def main():
    gaming = True
    focused = True
    afk = pygame.Surface((500,500),pygame.SRCALPHA)
    afk.set_alpha(128)
    
    while gaming:
        window.fill((0,0,0))
        Draw()
        manager.input()
        if not focused:
            afk.fill((0,0,0))
            window.blit(afk,(0,0))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.ACTIVEEVENT:
                if event.gain:
                    focused = True
                else:
                    focused = False
        clock.tick(60)  # Limit the frame rate to 60 FPS
        await asyncio.sleep(0) 

asyncio.run(main())