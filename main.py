import pygame as pg
import random
import os

pg.init()

screen = pg.display.set_mode((1920,1080))

clock = pg.time.Clock()
xpos=640
ypos=800

imgpath='assets/'
fruitnames=['blueberry','coco','orange','strawberry','watermelon']
points={'blueberry':3,'coco':1,'orange':2,'strawberry':2,'watermelon':2}
fruits=[]
caught=[]
empty=(0,0,0,0)
for i in range(len(fruitnames)):
    image= str(fruitnames[i]) + '.png'
    fruits.append(pg.image.load(os.path.join(imgpath,image)).convert())
    fruits[i].set_colorkey(empty)
bg=pg.image.load((os.path.join(imgpath,'background.png'))).convert()
basket=pg.image.load((os.path.join(imgpath,'basket.png'))).convert()
lg=pg.image.load((os.path.join(imgpath,'lifegone.png'))).convert()
sc=pg.image.load((os.path.join(imgpath,'sc.png')))
lc=pg.image.load((os.path.join(imgpath,'lost.png')))
bg.set_colorkey(empty)
basket.set_colorkey(empty)
lg.set_colorkey(empty)

numbers=[]
for i in range(9):
    image=str(i)+'.png'
    imgpath='assets/number'
    numbers.append(pg.image.load((os.path.join(imgpath,image))))
yloc=0
fallingfruits={}
fruit=random.choice(fruits)
xloc=random.randint(300,1400)
complete=False
loss=0
fruitrects=[]
def losses(l):
    global lg
    x=100
    y=120
    for i in range(1,4):
        x+=100
        if l >= i > 0:
            screen.blit(lg,(x,y))


scorepoints=0
def displayscore(point):
    point=str(point)
    xcoordin=1570
    ycoorin=190
    screen.blit(sc,(1350,150))
    for i in point:
        screen.blit(numbers[int(i)],(xcoordin,ycoorin))
        xcoordin+=30
def displaynum(num,x,y):
    for i in str(num):
        screen.blit(numbers[int(i)],(x,y))
        x+=25
def failcheck():
    global loss,fruitrects
    for i in fruitrects:
        if i.clipline():
            loss+=1
def fruitgen():
    global fruitcounter,fallingfruits
    if fruitcounter<=1:
        fruit=random.choice(fruits)
        xloc=random.randint(300,1400)
        mylis=[xloc,0]
        fallingfruits[fruit]=mylis
        fruitcounter+=1
def fruitfall():
    global fallingfruits,complete,loss,fruitrects
    for i in list(fallingfruits):
        if fallingfruits[i][1]<=1000:
            coords=tuple(fallingfruits[i])
            screen.blit(i,coords)
            fallingfruits[i][1] += 5
        if 805> fallingfruits[i][1]>=800:
            coords=tuple(fallingfruits[i])
            w,h=i.get_size()
            rectangle=pg.rect.Rect(coords,(w,h))
            if rectangle not in fruitrects:
                fruitrects.append(rectangle)
                print(fruitrects)

def ismove():
    global movingL,movingR,xpos
    if movingL:
        xpos-=20
        if xpos<=200:
            xpos=200
    if movingR:
        xpos+=20
        if xpos>=1500:
            xpos=1500
def end():
    screen.fill(empty)
    screen.blit(bg,(0,0))
    screen.blit(lc,(900,400))
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
        #screen.fill((0,0,0,0))
        screen.blit(bg, (0, 0))
        screen.blit(lc, (900, 400))
        displaynum(scorepoints,1080,525)
        pg.display.flip()
movingL,movingR=False,False
running=True
fruitcounter=0
fruitfalling=False
while running:
    if loss>=3:
        end()
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running=False
            if event.key==pg.K_RIGHT:
                movingR=True
            if event.key==pg.K_LEFT:
                movingL=True
        elif event.type == pg.KEYUP:
            if event.key==pg.K_RIGHT:
                movingR=False
            if event.key==pg.K_LEFT:
                movingL=False
    chance=random.randint(0,50)
    bassize=basket.get_size()
    basrect=pg.rect.Rect((xpos,ypos),bassize)

    if chance==1:
        fruitgen()
    for i in fallingfruits:
        num=list(fallingfruits).index(i)
        if fallingfruits[i][1]==1005:
            fallingfruits[i][1]+=5
            loss+=1
            fruitcounter-=1
            x, y = fallingfruits[i][0], fallingfruits[i][1]
            fallingfruits.pop(i)
            if fruitrects:
                fruitrects.pop(num)
            break
        if len(fruitrects)-1>=num and fruitrects:
            if fallingfruits[i][1]==1010 or fallingfruits[i][1]==1005:
                print('yes')
                fruitrects.pop(num)
                fruitcounter -= 1
                num-=1
            elif pg.Rect.colliderect(fruitrects[num], basrect):
                fallingfruits.pop(i)
                scorepoints += 5
                fruitcounter -= 1
                fruitrects.pop(num)
                break

    ismove()
    screen.blit(bg,(0,0))
    fruitfall()
    losses(loss)
    displayscore(scorepoints)
    screen.blit(basket,(xpos,ypos))
    pg.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)