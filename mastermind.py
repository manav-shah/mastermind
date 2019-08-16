import pygame, sys, random

#Colors  (R  ,G  ,B  )
RED =    (227,2  ,2  )
GREEN =  (30 ,217,55 )
BLUE =   (21 ,115,237)
YELLOW = (240,252,13 )
PINK =   (252,35 ,158)
BROWN =  (125,55 ,76 )
BLACK =  (0  ,0  ,0  )
WHITE =  (255,255,255)
GRAY =   (128,128,128)

#for submit button only
DARKERGREEN = (23, 179, 44)


#Coordinate values
ROW_HEIGHT=72

#Class to reperesent one circle
class Circle:
    def __init__(self,color,x,y,radius):
        self.color=color
        self.coordinate = x,y
        self.radius = radius
        self.rect=pygame.draw.circle(DISPLAYSURF,color,self.coordinate,self.radius)
    
        
    def toggle_color(self):
        toggle_dict = {RED:GREEN, GREEN:BLUE, BLUE:YELLOW, YELLOW:PINK,PINK:BROWN,BROWN:RED}
        color=toggle_dict[self.color]
        self.color=color
        self.rect=pygame.draw.circle(DISPLAYSURF,color,self.coordinate,self.radius)
        pygame.display.update()
            

def get_random_secret_code(listofcolors,number):
    return tuple(random.choices(listofcolors,k=number))

def has_won(row,SECRETCODE):
    if tuple(row)==SECRETCODE:
        return True
    return False

def draw_grid():
    '''Draws a grid of black lines onto background. x,y coordinates are hardcoded'''
    for i in range(11):
        pygame.draw.lines(DISPLAYSURF,BLACK,True,[(0,i*ROW_HEIGHT),(450,i*ROW_HEIGHT)])
    pygame.draw.line(DISPLAYSURF,BLACK,(100,0),(100,792))
    
def show_secret_code(code):
    '''Displays the secret code'''
    for i,color in enumerate(code): 
        pygame.draw.circle(DISPLAYSURF,color,(130+(30*(i+1))+(i*50),36),25)
        
def foo(bg):
    DISPLAYSURF.blit(bg,pygame.Rect(100,0,350,72))  

 
FPS = 30
COLORS = [RED,GREEN,BLUE,YELLOW,PINK,BROWN]
SECRETCODE = get_random_secret_code(COLORS,4)
    

def main():
    
    pygame.init()
    #Crate a display with background
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((450,792))
    pygame.display.set_caption('Mastermind - The code breaking game')
    background = pygame.image.load('assets\\woodbackground.png')
    DISPLAYSURF.blit(background,(0,0))
    
    #FPS clock
    global FPSClock
    FPSClock = pygame.time.Clock()
    
    #Create a submit box 
    submitbox = pygame.draw.rect(DISPLAYSURF,GREEN,(8,732,85,51))
    #Text label for the submit box
    font=pygame.font.SysFont('Arial',25)
    text = font.render('SUBMIT',True,WHITE)
    DISPLAYSURF.blit(text,(11,745))
    
    #create black lined grid
    draw_grid()
    
    #testing
    x=Circle(RED,30,30,25)
    show_secret_code(SECRETCODE)
    
    #Create interactive row
    activerow = []
    for i in range(4):
        circle=Circle(RED,(130+(30*(i+1))+(i*50)),756,25)
        activerow.append(circle)
    
    while True:
        for event in pygame.event.get():
            mousex,mousey=0,0
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                print(mousex,mousey)
            elif event.type == pygame.MOUSEBUTTONUP:
                clickx,clicky = event.pos
                if x.rect.collidepoint(clickx,clicky):
                    x.toggle_color()
                for circle in activerow:
                    if circle.rect.collidepoint(clickx,clicky):
                        circle.toggle_color()
                if submitbox.collidepoint(clickx,clicky):
                    submitbox=submitbox = pygame.draw.rect(DISPLAYSURF,DARKERGREEN,(8,732,85,51))
                    
                    #do stuff
            
            #Handle mouse over submit box
            if submitbox.collidepoint(mousex,mousey):
                submitbox=submitbox = pygame.draw.rect(DISPLAYSURF,DARKERGREEN,(8,732,85,51))
                DISPLAYSURF.blit(text,(11,745))
            else:
                submitbox=submitbox = pygame.draw.rect(DISPLAYSURF,GREEN,(8,732,85,51))
                DISPLAYSURF.blit(text,(11,745))
            
                    
        pygame.display.update()
        FPSClock.tick(FPS)
                

if __name__=='__main__':
    main()



