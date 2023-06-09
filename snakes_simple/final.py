import pygame
import random
import os
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, KEYDOWN, QUIT, K_s, K_x
from time import sleep
pygame.mixer.init()

                                                                                #colours
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
black=(0,0,0)
white=(255,255,255)
                                                                                     #constants
fps=60
s_width=700
s_height=700

size=10

b_x=[40,650]
b_y=[40,650]
range=8

clock=pygame.time.Clock()                                                           #clock

def welcome(game_win):      
    play("bg.mp3")                                                        #welcome screen
    exit_game=False
    while not exit_game:
        border(game_win)
        game_win.fill(black)
        text_screen(f"Welcome to Snakes",green,50,180,300,game_win)
        text_screen ("press 's' to start",green,20,280,400,game_win)
        save()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==KEYDOWN:
                if event.key==K_s:
                    game_loop(game_win)



                                                                        #functions for drawing borders and boundaries x=55 y=55 x=6
def border(game_win):
    pygame.draw.rect(game_win,green,[50,50,600,5])
    pygame.draw.rect(game_win,green,[650,50,5,600])
    pygame.draw.rect(game_win,green,[50,650,605,5])
    pygame.draw.rect(game_win,green,[50,50,5,600])

                                                                        #function for screen update
def save():
    pygame.display.update()

                                                                        #function for random food position
def food(game_win):
    x= random.randint(55,640)
    y=random.randint(55,640)
    return [x,y,10]

                                                                        #function for text on screen

def text_screen(text,color,fontsize,x,y,win):
    font=pygame.font.SysFont(None,fontsize)                             #taking default system font none=default font 
    Screen_text=font.render(text,True,color)
    win.blit(Screen_text,[x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def play(nsong):
    if type(nsong)==str:
        pygame.mixer.music.load(nsong)
        pygame.mixer.music.play()
    else: 
        pass

def game_loop(game_win):                        #game loop
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as f:
            f.write("0")
    
    with open("highscore.txt","r") as f:
        high_score=f.read()

    fx=food(game_win)[0] 
    fy=food(game_win)[1]
    fs=food(game_win)[2]

    exit_game=False
    game_over=False
    game_pause=False
    sn_x=300
    sn_y=300 
    # in_speed=3
    step=2                                                                                   #speed

    vel_x=step
    vel_y=0
    score=0

    snk_length=1
    snk_list=[] 


    m=5
    while not exit_game:
        if game_over==False:
            pygame.mixer.music.load("bg.mp3")
            pygame.mixer.music.play(-1)
        
        
        

        while  game_over==False:
            
            game_win.fill(black)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    game_over=True
                    exit_game=True

                if event.type==KEYDOWN:
                    if event.key==K_RIGHT :
                        vel_x=step
                        vel_y=0
                    elif event.key==K_LEFT:
                        vel_x=-step
                        vel_y=0
                    elif event.key==K_UP:
                        vel_y=-step
                        vel_x=0
                    elif event.key==K_DOWN:
                        vel_y=step
                        vel_x=0
    
            sn_y+=vel_y
            sn_x+=vel_x
            
            if abs((2*sn_x+10)/2-(2*fx+5)/2)<range and abs((2*sn_y+10)/2-(2*fy+5)/2)<range:
          
                fx=food(game_win)[0] 
                fy=food(game_win)[1]
                score+=1
                snk_length+=5
                pygame.mixer.Sound("eat.mp3").play()
                
                
                
                
               
            pygame.draw.rect(game_win,white,[fx,fy,fs,fs])

            sn_head=[]
            sn_head.append(sn_x)
            sn_head.append(sn_y)
            snk_list.append(sn_head)

            if len(snk_list)>snk_length+8:
                del snk_list[0]
            
            text_screen(f"Score:{score}",green,30,300,25,game_win)
            
            plot_snake(game_win,red,snk_list,size-2)
            pygame.draw.rect(game_win, blue,[sn_head[0], sn_head[1],size+2, size+2])
            if score>int(high_score):
                high_score=score
          
            if sn_x<50 or sn_x>650-size or sn_y<50 or sn_y>650-size:
                game_over=True
                pygame.mixer.Sound("over.mp3").play()
                sleep(0.5)
                play("gameover.mp3")
            for a,b in snk_list[0:len(snk_list)-3]:
                if sn_x==a and sn_y==b:
                    game_over=True
                    pygame.mixer.Sound("over.mp3").play()
                    sleep(0.5)
                    play("gameover.mp3")





            border(game_win)
            save()
            
            clock.tick(fps)
        
        if exit_game==True:
            break


        save()
        
        
        with open("highscore.txt",'w') as f:
            f.write(str(high_score))
    
        while m<=60:
            game_win.fill(black)
            text_screen(f"GAME OVER",green,m,210,300,game_win)
            text_screen(f"High score {high_score}",green,20,300,400,game_win)
            text_screen(f"Press 's' to replay",green,20,300,450,game_win)
            text_screen(f"Score:{score}",green,30,300,25,game_win)
            border(game_win)
            save()
            m+=5
            sleep(0.005)
            
        
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==K_s:
                    game_over=False
                    snk_length=1
                    snk_list=[]
                    sn_x=300
                    sn_y=300
                    score=0
                    m=5
                    
            if event.type==pygame.QUIT:
                exit_game=True
        

    pygame.quit()
    quit()

