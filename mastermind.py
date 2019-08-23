import pygame, pygame.freetype, sys, random, time

#Colors       (R  ,G  ,B  )
#can be used in the secret code and guesses
RED         = (227,2  ,2  )
GREEN       = (30 ,217,55 )
BLUE        = (21 ,115,237)
YELLOW      = (240,252,13 )
PINK        = (252,35 ,158)
BROWN       = (125,55 ,76 )
#Used for responses to guesses
BLACK       = (0  ,0  ,0  )
WHITE       = (255,255,255)
#for GUI use
GRAY        = (128,128,128)
DARKERBROWN = (158,100,100)
DARKERGREEN = (23, 179, 44)

#Coordinate values
ROW_HEIGHT=72
CIRCLE_GAP = 80
INITIAL_CIRCLE_X = 160
INITIAL_CIRCLE_Y = 36
CIRCLE_RADIUS = 25

#Class to reperesent one circle
class Circle:
    def __init__(self,color,x,y):
        self.color=color
        self.coordinate = x,y
        self.radius = CIRCLE_RADIUS
        self.rect=pygame.draw.circle(DISPLAYSURF,color,self.coordinate,self.radius)
    
    def toggle_color(self):
        toggle_dict = {RED:GREEN, GREEN:BLUE, BLUE:YELLOW, YELLOW:PINK,
                       PINK:BROWN,BROWN:RED}
        color=toggle_dict[self.color]
        self.color=color
        self.rect=pygame.draw.circle(DISPLAYSURF,self.color,self.coordinate,
                                     self.radius)
            
def get_random_secret_code(listofcolors):
    return tuple(random.choices(listofcolors,k=4))

def draw_grid():
    '''Draws a grid of black lines onto background. x,y coordinates are 
    hardcoded'''
    #Horizontal lines
    for i in range(11):
        pygame.draw.lines(DISPLAYSURF,BLACK,True,[(0,i*ROW_HEIGHT),(450,i*ROW_HEIGHT)])
    #Vertical line
    pygame.draw.line(DISPLAYSURF,BLACK,(100,0),(100,792))

def draw_row(colors,attemptsleft):
    '''Draws a row of inputted colors in location based on no of attempts left'''
    for i,color in enumerate(colors):
        pygame.draw.circle(DISPLAYSURF,color,(INITIAL_CIRCLE_X+(i*CIRCLE_GAP),
                           INITIAL_CIRCLE_Y+(attemptsleft*ROW_HEIGHT)),
                           CIRCLE_RADIUS)

def check_solution(guess,SECRETCODE):
    response=[]
    #make copies of guess and secretcode to prevent aliasing
    SECRETCODE=list(SECRETCODE)
    guess = guess[:]
    for i,color in enumerate(guess):
        if SECRETCODE[i]==color:
            #correct color and position
            #override values since they have been considered once
            SECRETCODE[i]=None
            guess[i]=None
            response.append(BLACK)
    for i,color in enumerate(guess):
        if color == None:
            #overriden value
            pass
        elif color in SECRETCODE:
            #right color in wrong position
            guess[i]=None
            x=SECRETCODE.index(color)
            SECRETCODE[x]=None
            response.append(WHITE)
    return response
    
def draw_hidden_code():
    '''Draws hidden code row to begin game'''
    #Draw 4 gray circles
    for i in range(4):
        pygame.draw.circle(DISPLAYSURF,GRAY,(INITIAL_CIRCLE_X+(i*CIRCLE_GAP),
                                              INITIAL_CIRCLE_Y),CIRCLE_RADIUS)
    #Draw question marks on circles
    fontObj=pygame.freetype.SysFont('comicsansms',28,bold=True)
    for i in range(4):
        fontObj.render_to(DISPLAYSURF,(155+(i*CIRCLE_GAP),26),'?')
        
    
def show_hidden_code(code):
    '''Displays the hidden secret code'''
    for i,color in enumerate(code): 
        pygame.draw.circle(DISPLAYSURF,color,(INITIAL_CIRCLE_X+(i*CIRCLE_GAP),
                                              INITIAL_CIRCLE_Y),CIRCLE_RADIUS)
        pygame.display.update()
        
def victory_animation(background,SECRETCODE):
    '''Plays winning animation. Trigger when code is guessed correctly'''
    show_hidden_code(SECRETCODE)
    time.sleep(1)
    
    #Reset screen
    DISPLAYSURF.blit(background,(0,0))
    
    #Draw victory image and text on screen
    imageSurf = pygame.image.load('assets/einstein.png')
    imageSurf.convert_alpha()
    DISPLAYSURF.blit(imageSurf,(0,200))
    fontObj=pygame.freetype.SysFont('comicsansms',40,bold=True)
    fontObj.render_to(DISPLAYSURF,(135,50),'GENIUS!')
    fontObj=pygame.freetype.SysFont('comicsansms',26,bold=True)
    fontObj.render_to(DISPLAYSURF,(77,110),"You've cracked the code!")
    pygame.display.update()
    
    #Play sound effect
    pygame.mixer.music.load('assets/victory.mp3')
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
    
def losing_animation(background,SECRETCODE):
    '''Plays losing animation. Trigerred when player runs out of attempts'''
    show_hidden_code(SECRETCODE)
    time.sleep(2)
    #Reset screen
    DISPLAYSURF.blit(background,(0,0))
    #Display text
    fontObj=pygame.freetype.SysFont('comicsansms',40,bold=True)
    fontObj.render_to(DISPLAYSURF,(95,50),'You just lost!')
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()
    
def draw_response(response,attempts_left):
    '''Turns pre-shuffled response list to drawings. Draws circles in correct position based on how many attempts left'''
    #Draw brown box
    pygame.draw.rect(DISPLAYSURF,DARKERBROWN,(8,12+(attempts_left*ROW_HEIGHT),85,51))
    #Draw colored response dots
    responseCoordinates = [(33,48+(attempts_left*ROW_HEIGHT)),(33,24+(attempts_left*ROW_HEIGHT)),
                           (66,48+(attempts_left*ROW_HEIGHT)),(66,24+(attempts_left*ROW_HEIGHT))]
    for color,coordinate in zip(response,responseCoordinates):
        pygame.draw.circle(DISPLAYSURF,color,coordinate,10)

def new_submit_box(attemptsleft,color=GREEN):
    '''Create a new submit box. Location based on num of attempts left. Default color green'''
    attempt = 10 - attemptsleft
    submitbox = pygame.draw.rect(DISPLAYSURF,color,(8,732-(72*attempt),85,51))
    #Text label for the submit box
    fontObj=pygame.freetype.SysFont('Arial',25)
    fontObj.render_to(DISPLAYSURF,(11,25+(attemptsleft*ROW_HEIGHT)),'SUBMIT',WHITE)
    pygame.display.update()
    return submitbox
    

def new_active_row(attemptsleft,colors=[RED,RED,RED,RED]):
    '''Create a new active row based on num of attempts left'''
    activerow=[]
    for i,color in enumerate(colors):
        circle=Circle(color,INITIAL_CIRCLE_X+(i*CIRCLE_GAP),INITIAL_CIRCLE_Y+(attemptsleft*ROW_HEIGHT))
        activerow.append(circle)
    return activerow
    
    
def main():
    pygame.init()
    #Crate a display with background
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((450,792))
    pygame.display.set_caption('Mastermind - The code breaking game')
    background = pygame.image.load('assets/woodbackground.png')
    DISPLAYSURF.blit(background,(0,0))
    
    #FPS clock
    FPSClock = pygame.time.Clock()
    
    #create black lined grid
    draw_grid()
    
    #Initialize game variables
    attempts_left = 10
    FPS = 60
    
    #create secret code
    COLORS = [RED,GREEN,BLUE,YELLOW,PINK,BROWN]
    SECRETCODE = get_random_secret_code(COLORS)

    draw_hidden_code()
    
    #Create submit box
    submitbox = new_submit_box(attempts_left)
    
    #Create lists to store guesses
    guessHistory = []

    #Create an interactive row where you can toggle colors.
    activerow = new_active_row(attempts_left)
    
    #Main game loop
    while True:
        moved = False
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                moved = True
            elif event.type == pygame.MOUSEBUTTONUP:
                clickx,clicky = event.pos
                clicked = True
            
            #Handle mouse movement over submit box
            if moved:
                if submitbox.collidepoint(mousex,mousey):
                    submitbox = new_submit_box(attempts_left,color=DARKERGREEN)
                else:
                    submitbox = new_submit_box(attempts_left,color=GREEN)
            
            #Handle clicks
            if clicked:
                if submitbox.collidepoint(clickx,clicky):
                    #Submit button is clicked
                    activecolors = [circle.color for circle in activerow]
                    response=check_solution(activecolors,SECRETCODE)
                    guessHistory.append(tuple(activecolors))
                    submitbox=new_submit_box(attempts_left)
                    draw_response(response,attempts_left)
                    attempts_left-=1
                    if response.count(WHITE)==4:
                        show_hidden_code(SECRETCODE)
                        victory_animation(background,SECRETCODE)
                    if attempts_left==0:
                        show_hidden_code(SECRETCODE)
                        losing_animation(background,SECRETCODE)                    
                    activerow = new_active_row(attempts_left,guessHistory[-1])
                else:
                    #Check for clicks on active row circles
                    for circle in activerow:
                        if circle.rect.collidepoint(clickx,clicky):
                            circle.toggle_color()
                    
        pygame.display.update()
        FPSClock.tick(FPS)         

if __name__=='__main__':
    main()