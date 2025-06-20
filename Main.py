import pygame
import random #Use it to initialise the initial list to sort

pygame.init()

#Instead of using global variables and not being able to port our functions to another program we are creating a class
class DrawInformation():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0) #these are in RGB
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128,128,128)
    BACKGROUND = WHITE

    #We will be making the blocks all in slightly different colours so we can see them

    GRADIENTS = [(128,128,128), (160,160,160), (192,192,192)] #Different shades of grey

    FONT = pygame.font.SysFont("comicsans", 30)
    LARGE_FONT = pygame.font.SysFont("comicsans", 40)
    SIDE_PAD = 100 #100px of padding from the left and right hand side so that the bars aren't touching the ends of the window
    TOP_PAD = 150
    #These are constants that are typically used in gui libraries such as pygame, this makes it easier for us to access colours and understand our program

    def __init__(self, width, height, lst): #lst will be the list we want to sort
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height)) #This is how we create a window in pygame, will be accessed pretty much everywhere in the program
        pygame.display.set_caption("Sorting-Algorithms-Visualiser")

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD)/ len(lst)) #this divides the available screen size between each bar equally
        self.block_height = round((self.height - self.TOP_PAD)/(self.max_val - self.min_val)) #this is so that each bar can be relative to its size
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND)

    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - descending", 1, draw_info.BLACK) #the 1 is essentially the sharpness of the line
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,5))

    sorting = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 35))

    draw_list(draw_info)
    pygame.display.update()

#Function to draw our bars onto the display
def draw_list(draw_info):

    for i, val in enumerate(draw_info.lst):
        #i will be index we get from enumerate, start_x tells us where to start on screen, so adding to it i * block width will give us the locations of the next blocks
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height  - ((val - draw_info.min_val) * draw_info.block_height) #We will figure out the height of the rectangle then subtract from the height of the screen cause in pygame y=0 is on the top left and it increases as we go down the screen

        colour = draw_info.GRADIENTS[i % 3] #each element beside each other will be in a different gray

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))
#n will be number of values we want in our list
def generate_starting_list(n, min_val, max_val):
    lst = []

    for i in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    # creating our pygame event loop

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1000, 600, lst)

    draw(draw_info)
    sorting = False
    ascending = True

    pygame.display.update() #renders the display
    while run:
        clock.tick(60) #max number of times the loop can run per second, kinda like fps
        draw(draw_info)
        #Gives us all the events that occured since the last loop, it will give it to us in the event variable
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_r: #if we press r it will reset our list
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.k_d and sorting == False:
                ascending = False
    pygame.quit()

#Just makes sure we are running the module directly before running the main function
if __name__ == "__main__":
    main()

