import pygame as pt
import neat
import time
import random
import os
import pickle
time.sleep(5)
pt.font.init()
time.sleep(5)
WIN_WIDTH=500
WIN_HEIGHT=800
GEN=0
BIRD_IMGS=[pt.transform.scale2x(pt.image.load(os.path.join("imgs","bird1.png"))),
           pt.transform.scale2x(pt.image.load(os.path.join("imgs","bird2.png"))),
           pt.transform.scale2x(pt.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG=pt.transform.scale2x(pt.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG=pt.transform.scale2x(pt.image.load(os.path.join("imgs","base.png")))
BG_IMG=pt.transform.scale2x(pt.image.load(os.path.join("imgs","bg.png")))
STAT_FONT=pt.font.SysFont("comicsans",50)
bg_vel=5


class Bird:
    IMGS=BIRD_IMGS
    MAX_ROTATION=25
    ROT_VEL=20
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[0]
        self.is_jumping_flag=False

    def jump(self):
        self.vel= -8.5 #since the downward way is +ve thus moving up requires negative velocity
        self.tick_count=0
        self.height=self.y
        self.is_jumping_flag=True
        

    def is_jumping(self):
        return self.is_jumping_flag
    
    def move(self):
        self.tick_count+=1
        d=self.vel*self.tick_count+.5*3*(self.tick_count)**2    #s=ut+0.5at^2
        if d>=16:
            d=16
        if d<0:
            d-=2
        
        self.y=self.y+d

        if d<0 or self.y<self.height+50:
            if self.tilt<self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION
        else:
            if self.tilt>-90:
                self.tilt-=self.ROT_VEL

    def draw(self,win):
        self.img_count+=1
        if self.img_count<self.ANIMATION_TIME:          #starts with wings at UP pos
            self.img=self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:      #wings GOES LEVEL                                                   ##HERE
            self.img=self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*3:      #wing moves down
            self.img=self.IMGS[2]
        elif self.img_count<self.ANIMATION_TIME*4:      #wing moves LEVEL
            self.img=self.IMGS[1]
        elif self.img_count==self.ANIMATION_TIME*4+1:   #wing to UP pos ,thus this sequence represent a flap
            self.img=self.IMGS[0]
            self.img_count=0
        if self.tilt<=-80:                              #DURING DIVING THE WINGS REMAIN LEVEL AND DONT FLAP
            self.img=self.IMGS[1]
            self.img_count=self.ANIMATION_TIME*2        #RETURN TO LEVEL WING EVEN AT MOMENT OF JUMPING UP                   ##THERE

        #rotate bird around centre for tilting up and down
        rotated_images=pt.transform.rotate(self.img,self.tilt)
        new_rect=rotated_images.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_images,new_rect.topleft)

    def get_mask(self):
        return pt.mask.from_surface(self.img)

class Pipe:
    GAP=200
 
    VEL=bg_vel

    def __init__(self,x):
        self.x=x
        self.height=0
        self.top=0
        self.bottom=0
        self.PIPE_TOP=pt.transform.flip(PIPE_IMG,False,True)   #stores the pipe's position which comes from top
        self.PIPE_BOTTOM=PIPE_IMG                               #which comes from bottom
        self.passed=False
        self.set_height()                                        #defines how top our pipe is or how bottom it is or how tall it is

    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.bottom=self.height+self.GAP
    
    def move(self):
        self.x-=self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()                            # a mask is an approx list of all the pixels within the image.
        top_mask=pt.mask.from_surface(self.PIPE_TOP)
        bottom_mask=pt.mask.from_surface(self.PIPE_BOTTOM)

        top_offset=(self.x-bird.x,self.top-round(bird.y))        #offset value which is to be considered as a collision
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))

        b_point=bird_mask.overlap(bottom_mask,bottom_offset)      # gives the point if collides otherwise returns None
        t_point=bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:                                    # if collides
            return True
        return False

class Base:

    VEL=bg_vel                                      #SAME AS PIPE
    WIDTH=BASE_IMG.get_width()
    IMG=BASE_IMG

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.WIDTH

    def move(self):
        self.x1 -=self.VEL
        self.x2-=self.VEL

        if self.x1+self.WIDTH<0:                #queue one img after other 
            self.x1=self.x2+self.WIDTH

        if self.x2+self.WIDTH<0:                #when the forst image goes out of frame queue it back after the second one
            self.x2=self.x1+self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))

def draw_window(win,birds,pipes,base,score,gen):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)

    text=STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))

    text=STAT_FONT.render("GEN: "+str(gen),1,(255,255,255))
    win.blit(text,(10,10))

    text=STAT_FONT.render("Alive: "+str(len(birds)),1,(255,255,255))
    win.blit(text,(10,50))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pt.display.update()

def main(genomes,config):
    global GEN
    GEN+=1
    nets=[]
    ge=[]
    birds=[]  

    for _,g in genomes:                   #genome is a tupple(id,obj)
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness=0
        ge.append(g)
        

    base=Base(700)
    pipes=[Pipe(700)]
    clock=pt.time.Clock()
    win=pt.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    run=True
    score=0
    while run:
        clock.tick(30)
        
        global bg_vel
        if bg_vel<=10:
            bg_vel+=1
       

        for event in pt.event.get():
            if event.type==pt.QUIT:
                run=False
                pt.quit()
                quit()

        pipe_ind=0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].PIPE_TOP.get_width():
                pipe_ind=1

        else:
            run=False
            break
        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness+=0.1

            output=nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0]>=0.5:
                bird.jump()

        add_pipe=False

        add_pipe=False
        rem=[]
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness-=1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x<bird.x:
                    pipe.passed=True
                    add_pipe=True

            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)
            
            pipe.move()

        if add_pipe:
            score+=1 
            for g in ge:
                g.fitness+=5

            pipes.append(Pipe(550))
        
        for r in rem:
            pipes.remove(r)

        for x,bird in enumerate(birds):
            if bird.y+bird.img.get_height()>=730 or bird.y<0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

                if score>50:
                    break

                 

        base.move()
        draw_window(win,birds,pipes,base,score,GEN)

def save_winner_bird(winner,filename):
    with open(filename,'wb') as f:
        pickle.dump(winner,f)

def load_winner_bird(filename):
    with open(filename,'rb') as f:
        winner=pickle.load(f)
    return winner

def implement_winner_bird(winner,config):
    base = Base(700)
    pipes = [Pipe(700)]
    clock = pt.time.Clock()
    win = pt.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    bird = Bird(230, 350)
    nets = neat.nn.FeedForwardNetwork.create(winner, config)

    run = True
    score = 0

    while run:
        clock.tick(30)

        for event in pt.event.get():
            if event.type == pt.QUIT:
                run = False
                pt.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        bird.move()

        output = nets.activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
        if output[0] >= 0.5:
            bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
                break

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(550))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False

        base.move()
        draw_window(win, [bird], pipes, base, score, GEN)
      
def main_manual():
    bird = Bird(230, 350)
    base = Base(700)
    pipes = [Pipe(700)]
    clock = pt.time.Clock()
    win = pt.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    score = 0

    while run:
        clock.tick(30)

        for event in pt.event.get():
            if event.type == pt.QUIT:
                run = False
                pt.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        bird.move()

        keys = pt.key.get_pressed()
        if keys[pt.K_SPACE]:
            bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
                break

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(550))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False

        base.move()
        draw_window(win, [bird], pipes, base, score, GEN)

def train_birds(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                               neat.DefaultReproduction,
                               neat.DefaultSpeciesSet,
                               neat.DefaultStagnation,
                               config_path)

    p = neat.Population(config)

    # Add reporters to display the progress during training
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Set the number of generations to run the training
    num_generations = 50

    winner = p.run(main, num_generations)

    # Save the winner bird as a file
    save_winner_bird(winner, "winner_bird.pkl")

def play_manual():
    bird = Bird(230, 350)
    base = Base(700)
    pipes = [Pipe(700)]
    clock = pt.time.Clock()
    win = pt.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    score = 0
    game_over = False

    while run:
        clock.tick(30)

        for event in pt.event.get():
            if event.type == pt.QUIT:
                run = False
                pt.quit()
                quit()

        keys = pt.key.get_pressed()
        if keys[pt.K_SPACE]:
            bird.jump()

        if game_over and keys[pt.K_s]:
            # Restart the game when 's' key is pressed after game over
            bird = Bird(230, 350)
            base = Base(700)
            pipes = [Pipe(700)]
            score = 0
            game_over = False

        if not game_over:
            pipe_ind = 0
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

            bird.move()

            add_pipe = False
            rem = []
            for pipe in pipes:
                if pipe.collide(bird):
                    game_over = True
                    break

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(550))

            for r in rem:
                pipes.remove(r)

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                game_over = True

            base.move()
            draw_window(win, [bird], pipes, base, score, GEN)
        else:
            # Game Over Logic
            win.blit(BG_IMG, (0, 0))
            text = STAT_FONT.render("Game Over", 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, WIN_HEIGHT // 2 - text.get_height() // 2))
            text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, WIN_HEIGHT // 2 - text.get_height() // 2 + 50))
            text = STAT_FONT.render("Press 's' to Restart", 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, WIN_HEIGHT // 2 - text.get_height() // 2 + 100))
            pt.display.update()

    # After the loop exits, the program will terminate.

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
   
    # Uncomment the following line for training mode
    #train_birds(config_path)

    # Uncomment the following line to play manually
    #play_manual()

    # Uncomment the following lines to implement the winner bird
    winner_bird_filename = "winner_bird.pkl"
    winner_bird = load_winner_bird(winner_bird_filename)
    implement_winner_bird(winner_bird,config)

    pass

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)
