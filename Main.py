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
    BACKGROUND = BLACK

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
        self.max_value = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD)/ len(lst)) #this divides the available screen size between each bar equally
        self.block_height = round((self.height - self.TOP_PAD)/(self.max_val - self.min_val)) #this is so that each bar can be relative to its size
        self.start_x = self.SIDE_PAD // 2
