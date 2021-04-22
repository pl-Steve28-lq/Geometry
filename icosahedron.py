from numpy import cos, sin, pi

import pygame
import pygame.display as display
import pygame.event as events
import pygame.draw as draws
from pygame.time import Clock


width = 400
height = 300
t = pi/10
v = 0
BLACK = (0,)*3
WHITE = (255,)*3
Scale = lambda x, y: (width*((1+x)/2+1/5), height*((1+y)/2+1/5))

V0 = (0, 0, 1)
V1 = (0, 0, -1)

U = tuple([(cos(2*pi*k/5), sin(2*pi*k/5), 1/2) for k in range(5)])
L = tuple([(cos(2*pi*k/5 + pi/5), sin(2*pi*k/5 + pi/5), -1/2) for k in range(5)])


def Transform(pos):
    ct, st = cos(t), sin(t)
    cv, sv = cos(v), sin(v)
    x, y, z = pos
    return (ct*x-st*y, cv*st*x+cv*ct*y+sv*z, sv*(st*x+ct*y)+cv*z)


def draw(screen):
    screen.fill(BLACK)
    
    def Line(P0, P1):
        x0, y0, z0 = Transform(P0)
        x1, y1, z1 = Transform(P1)
        m = (y0+y1)/2
        color = 20*(1+m), 60*(1+m)+100, 55*(1-m)
        draws.aaline(screen, tuple(map(lambda x: max(x, 0), color)), Scale(x0, z0), Scale(x1, z1))

    def Triangle(P0, P1, P2):
        pts = list(map(Transform, [P0, P1, P2]))
        x0, y0, z0 = Transform(P0)
        x1, y1, z1 = Transform(P1)
        x2, y2, z2 = Transform(P2)
        m = (y0+y1+y2)/3
        color = 20*(1+m), 60*(1+m)+100, 55*(1-m), 96


        px, _, py = zip(*pts)
        min_x, min_y = Scale(min(px), min(py))
        max_x, max_y = Scale(max(px), max(py))
        rect = pygame.Rect(min_x, min_y, max_x-min_x, max_y-min_y)

        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        draws.polygon(
            surf,
            tuple(map(lambda x: max(x, 0), color)),
            [(x-min_x, y-min_y) for x, y in [Scale(x0, z0), Scale(x1, z1), Scale(x2, z2)]]
        )
        screen.blit(surf, rect)
    
    for i in range(5):
        u = U[i]
        up = U[(i+1)%5]
        l = L[i]
        lp = L[(i+1)%5]
        lpp = L[(i-1)%5]
        
        Line(V0, u)
        Line(V1, l)
        Line(u, up)
        Line(l, lp)
        Line(u, l)
        Line(u, lpp)

        Triangle(V0, u, up)
        Triangle(V1, l, lp)
        Triangle(u, up, l)
        Triangle(l, lp, up)

    font = pygame.font.Font("NanumSquare.ttf", 17)
    text = font.render("https://github.com/pl-Steve28-lq", True, WHITE)
    rect = text.get_rect()
    rect.centerx = int(width*7/10)
    rect.y = int(height*7/5 - rect.size[1]*3/2)
    screen.blit(text, rect)

    
def start():
    global t, v
    
    pygame.init()
        
    screen = display.set_mode((int(width*7/5), int(height*7/5)))
    display.set_caption("Steve28 : Icosahedron")
    clock = Clock()

    running = True
    while running:
        clock.tick(30)
            
        for event in events.get():
            if event.type == pygame.QUIT:
                running = False

        draw(screen)
        display.flip()
        v += 0.01
        v %= 2*pi
        t += 0.015
        t %= 2*pi

    pygame.quit()

if __name__ == '__main__':
    start()
