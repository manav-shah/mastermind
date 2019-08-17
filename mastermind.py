import pygame, sys, random, time, pygame.freetype

#Colors       (R  ,G  ,B  )
#can be used in the secret code and guesses
RED         = (227,2  ,2  )
GREEN       = (30 ,217,55 )
BLUE        = (21 ,115,237)
YELLOW      = (240,252,13 )
PINK        = (252,35 ,158)
BROWN       = (125,55 ,76 )
#can be used for responses to guesses
BLACK       = (0  ,0  ,0  )
WHITE       = (255,255,255)
#for miscellaneous GUI uses
GRAY        = (128,128,128)
DARKERBROWN = (158,100,100)
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
        pygame.display.update(self.rect)
            
def get_random_secret_code(listofcolors,number):
    return tuple(random.choices(listofcolors,k=number))

def check_solution(code):
    secretcode=list(SECRETCODE)
    code=code[:]
    response=[]
    isexactmatch=[]
    print(code,secretcode)
    for i in range(4):
        if code[i]==secretcode[i]:
            response.append(WHITE)
            isexactmatch.append(True)
        else:
            isexactmatch.append(False)
    code = [code[i] for i in range(4) if isexactmatch[i]==False]
    secretcode = [secretcode[i] for i in range(4) if isexactmatch[i]==False]
    for color in set(code):
        n = min(code.count(color),secretcode.count(color))
        for i in range(n):
            response.append(BLACK)
    random.shuffle(response)
    return response
            
def draw_grid():
    '''Draws a grid of black lines onto background. x,y coordinates are hardcoded'''
    for i in range(11):
        pygame.draw.lines(DISPLAYSURF,BLACK,True,[(0,i*ROW_HEIGHT),(450,i*ROW_HEIGHT)])
    pygame.draw.line(DISPLAYSURF,BLACK,(100,0),(100,792))
    
def show_secret_code(code):
    '''Displays the secret code'''
    for i,color in enumerate(code): 
        pygame.draw.circle(DISPLAYSURF,color,(130+(30*(i+1))+(i*50),36),25)
        pygame.display.update()
        
def victory_animation(background):
    show_secret_code(SECRETCODE)
    pygame.display.update()
    time.sleep(1.2)
    DISPLAYSURF.blit(background,(0,0))
    imageSurf = pygame.image.load('assets\\einstein.png')
    imageSurf.convert_alpha()
    DISPLAYSURF.blit(imageSurf,(0,200))
    fontObj=pygame.freetype.SysFont('comicsansms',40,bold=True)
    fontObj.render_to(DISPLAYSURF,(135,50),'GENIUS!')
    fontObj=pygame.freetype.SysFont('comicsansms',26,bold=True)
    fontObj.render_to(DISPLAYSURF,(77,110),"You've cracked the code!")
    pygame.display.update()
    pygame.mixer.music.load('assets\\victory.mp3')
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
    
def losing_animation(background):
    show_secret_code(SECRETCODE)
    pygame.display.update()
    time.sleep(0.5)
    DISPLAYSURF.blit(background,(0,0))
    fontObj=pygame.freetype.SysFont('comicsansms',40,bold=True)
    fontObj.render_to(DISPLAYSURF,(95,50),'You just lost!')
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()
    
def draw_response(response,attempts_left):
    '''Turns pre-shuffled response list to drawings. Draws circles in correct position based on how many attempts left'''
    attempt=10-attempts_left
    pygame.draw.rect(DISPLAYSURF,DARKERBROWN,(8,732-(72*attempt),85,51))
    responseCoordinates = [(33,48+(72*attempts_left)),(33,24+(72*attempts_left)),(66,48+(72*attempts_left)),(66,24+(72*attempts_left))]
    for color,coordinate in zip(response,responseCoordinates):
        pygame.draw.circle(DISPLAYSURF,color,coordinate,10)
    pygame.display.update()
    time.sleep(1)

def draw_row(colors,attemptsleft):
    for i,color in enumerate(colors):
        pygame.draw.circle(DISPLAYSURF,color,((130+(30*(i+1))+(i*50)),36+(attemptsleft*72)),25)

def screen_refresh(guessHistory,responseHistory,background):
    DISPLAYSURF.blit(background,(0,0))
    draw_grid()
    for index,guess in enumerate(guessHistory):
        position=10-index
        draw_row(guess,position)
    for index,response in enumerate(responseHistory):
        position=10-index
        draw_response(response,position)

def move_to_next_line(guessHistory,attemptsleft):
    latestcolors = guessHistory[-1]
    draw_row(latestcolors,attemptsleft)

def new_submit_box(submitbox,attemptsleft):
    attempt = 11 - attemptsleft
    submitbox = pygame.draw.rect(DISPLAYSURF,GREEN,(8,732-(72*attempt),85,51))
    #Text label for the submit box
    font=pygame.font.SysFont('Arial',25)
    text = font.render('SUBMIT',True,WHITE)
    DISPLAYSURF.blit(text,(11,25+((attemptsleft-1)*72)))
    return submitbox
    

def new_active_row(activerow,attemptsleft):
    del activerow[:]
    for i in range(4):
        circle=Circle(RED,(130+(30*(i+1))+(i*50)),36+((attemptsleft)*72),25)
        activerow.append(circle)
    
    
FPS = 100
COLORS = [RED,GREEN,BLUE,YELLOW,PINK,BROWN]
#SECRETCODE = get_random_secret_code(COLORS,4)
SECRETCODE = (PINK,PINK,BLUE,GREEN)
    

def main():
    attempts_left = 10
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
    
    
    #create black lined grid
    draw_grid()
    
    
    #Create a submit box 
    submitbox = pygame.draw.rect(DISPLAYSURF,GREEN,(8,732,85,51))
    #Text label for the submit box
    font=pygame.font.SysFont('Arial',25)
    text = font.render('SUBMIT',True,WHITE)
    DISPLAYSURF.blit(text,(11,745))
    
    #Create lists to store guesses and response history
    guessHistory = []
    responseHistory = []
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
                for circle in activerow:
                    if circle.rect.collidepoint(clickx,clicky):
                        circle.toggle_color()
                if submitbox.collidepoint(clickx,clicky):
                    #Submit button is clicked
                    activecolors = [circle.color for circle in activerow]
                    response=check_solution(activecolors)
                    guessHistory.append(activecolors)
                    responseHistory.append(response)
                    submitbox=new_submit_box(submitbox,attempts_left)
                    draw_response(response,attempts_left)
                    attempts_left-=1
                    if attempts_left==0:
                        show_secret_code(SECRETCODE)
                        losing_animation(background)
#                    screen_refresh(guessHistory,responseHistory,background)
                    if response.count(WHITE)==4:
                        show_secret_code(SECRETCODE)
                        victory_animation(background)
                    new_active_row(activerow,attempts_left)
            
            #Handle mouse movement over submit box
            if submitbox.collidepoint(mousex,mousey):
                submitbox=submitbox = pygame.draw.rect(DISPLAYSURF,DARKERGREEN,submitbox)
                DISPLAYSURF.blit(text,(11,745-(72*(10-attempts_left))))
            else:
                submitbox=submitbox = pygame.draw.rect(DISPLAYSURF,GREEN,submitbox)
                DISPLAYSURF.blit(text,(11,745-(72*(10-attempts_left))))
            
                    
        pygame.display.update()
        FPSClock.tick(FPS)
                

if __name__=='__main__':
    main()