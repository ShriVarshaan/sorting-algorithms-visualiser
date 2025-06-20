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
        self.block_height = int((self.height - self.TOP_PAD)/(self.max_val - self.min_val)) #this is so that each bar can be relative to its size
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND)

    title = draw_info.LARGE_FONT.render(f"{algo_name}, {ascending}", 1,draw_info.BLACK)  # the 1 is essentially the sharpness of the line
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 0))

    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - descending", 1, draw_info.BLACK) #the 1 is essentially the sharpness of the line
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,45))

    sorting = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()

#Function to draw our bars onto the display
def draw_list(draw_info, colour_positions={}, clear_bg=False):

    #For clearing just the list and drawing our list with colours on top
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND, clear_rect)
    for i, val in enumerate(draw_info.lst):
        #i will be index we get from enumerate, start_x tells us where to start on screen, so adding to it i * block width will give us the locations of the next blocks
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height  - ((val - draw_info.min_val) * draw_info.block_height) #We will figure out the height of the rectangle then subtract from the height of the screen cause in pygame y=0 is on the top left and it increases as we go down the screen

        colour = draw_info.GRADIENTS[i % 3] #each element beside each other will be in a different gray

        if i in colour_positions:
            colour = colour_positions[i]

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))

    #We need to update our display as well
    if clear_bg:
        pygame.display.update()

#n will be number of values we want in our list
def generate_starting_list(n, min_val, max_val):
    lst = []

    for i in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst

def bubble_sort(draw_info, ascending):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if ascending:
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True #We are yielding this as we want to call this function each time a swap occurs
            else:
                if lst[j] < lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                    yield True
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


    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "bubble sort"
    sorting_algorithm_generator = None
    draw(draw_info, sorting_algo_name, ascending)

    pygame.display.update() #renders the display
    while run:
        #clock.tick(120) #max number of times the loop can run per second, kinda like fps
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
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
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
    pygame.quit()

#Just makes sure we are running the module directly before running the main function
if __name__ == "__main__":
    main()

