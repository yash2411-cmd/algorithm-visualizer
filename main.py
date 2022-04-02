# visualizing the sorting algorithms with the help of pygame and python -version 3.10.01
# from signal import default_int_handler
# import pygame
import math
import pygame, sys
from pygame.locals import*
import random #to generate the random list for sorting
pygame.init()

# pygame window setup:
class windowSetup:
    black =0,0,0
    blue= 20, 52, 164
    yellow= (255,255,0)
    white= 255,255,255
    green = 0,255,0
    red= 255,0,0
    grey=128,128,128
    background_color=111,187,211
    side_pad= 100
    t_pad= 150
    bar_colors = [grey,(160,160,160),(192,192,192)]
    FONT = pygame.font.SysFont("times",20)
    large_FONT = pygame.font.SysFont("times",30)

    def __init__(self,width, height,lst):
        self.width= width
        self.height= height
        self.window = pygame.display.set_mode((width,height)) # setting the outlet of pygame windows passing the width and height as a tuple
        pygame.display.set_caption("Sorting Algorithms Visualizer")
        self.set_list(lst)
    def set_list(self,lst):
        self.lst= lst
        
        self.min_val= min(lst) #gives the minimum of the list 
        self.max_val= max(lst) # gives the max value of the list 
        
        self.bar_width= round(self.width - self.side_pad) / len(lst) #determines the width of each bar 
        self.bar_height= math.floor((self.height- self.t_pad)/(self.max_val- self.min_val)) # determines the height of each bar (the greater the range the smaller the hieght)
        self.start_x= self.side_pad//2 # where the first bar will be drwwn

    # width of the bars will be decided by the range of list that we have 
    #height of the bars will be decided by the values in the list we have
# displaying the canvas 
def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.background_color)

    tittle= draw_info.large_FONT.render(f"{algo_name} - {'Ascending'if ascending else 'Dscending'}",1,draw_info.red)
    draw_info.window.blit(tittle,(draw_info.width/2- tittle.get_width()/2,5)) # making the text display in th centre on the window
    
    controls= draw_info.FONT.render("R -Reset || SPACE -Start Sorting || A -Ascending || D -Dscending",1,draw_info.black)
    draw_info.window.blit(controls,(draw_info.width/2- controls.get_width()/2,45)) # making the text display in th centre on the window
    
    sorting= draw_info.FONT.render("I -Insertion Sort || B- Bubble Sort || M -Merge Sort",1,draw_info.black)
    draw_info.window.blit(sorting,(draw_info.width/2- sorting.get_width()/2,75)) # making the text display in th centre on the window
    
    draw_list(draw_info)
    pygame.display.update()

# drawingn the bars representing all the list elements by width and height
def draw_list(draw_info,color_post={},clear_bg= False):
    lst = draw_info.lst
     
    if clear_bg:   # clearing rectangles after sorts and rendering the text again n again n the frame
        clear_rect= (draw_info.side_pad//2,draw_info.t_pad,draw_info.width - draw_info.side_pad,draw_info.height -draw_info.t_pad)
        pygame.draw.rect(draw_info.window, draw_info.background_color, clear_rect)
     
    for i, val in enumerate(lst):
        x= draw_info.start_x + i* draw_info.bar_width
        y= draw_info.height -(val- draw_info.min_val) * draw_info.bar_height
        
        #defining the colors for bars 
        color= draw_info.bar_colors[i%3]
        if i in color_post:
            color= color_post[i]
        # making the rectangles with the given dimensions 
        pygame.draw.rect(draw_info.window,color,(x,y, draw_info.bar_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
# function to create a random list with the specified length and max and min range
def generate_list(n,min_val,max_val):
    lst=[]
    for _ in range(n):
        val= random.randint(min_val,max_val)
        lst.append(val)
    return lst

# implementation of bubble sort 
def bubble_sort(draw_info,ascending = True):
    lst = draw_info.lst # making variable short for easy use
    
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1= lst[j]
            num2= lst[j+1]

            if (num1> num2 and ascending) or (num1< num2 and not ascending):
                lst[j],lst[j+1]= lst[j+1],lst[j]    # swapping the bars for the aconditions acc to ascending and dscending 
                
                # updating the bar list on the screen after each swap has done 
                draw_list(draw_info,{j:draw_info.blue,j+1:draw_info.yellow},True)
                yield True # iterater or generater for storing the current state of function
    return lst 

# implementation of insertion sorting 
def insertion_sort(draw_info,ascending= True):
    lst= draw_info.lst

    for i in range(1,len(lst)):
        curr= lst[i]
        while True:
            ascending_sort= i>0 and lst[i-1]> curr and ascending
            dscending_sort= i>0 and lst[i-1]< curr and not ascending

            if not ascending_sort and not dscending_sort:
                break
            lst[i]= lst[i-1]
            i-=1
            lst[i]=curr
            
            # updating the bar list on the screen after each swap has done 
            draw_list(draw_info,{i-1:draw_info.blue, i: draw_info.yellow},True)
            yield True
    return lst

def merge_sort(draw_info,ascending= True):
    lst = draw_info.lst
    if(len(lst)>1):
        mid = len(lst)//2
        left_lst= lst[:mid]
        right_lst= lst[mid:]

        # recursilvely calling merge sort
        merge_sort(left_lst)
        merge_sort(right_lst)

        # merging :
        i= 0 # left most element of left_lst
        j= 0 # left most element of right_lst
        k= 0 # merged list index counter
        while (i<len(left_lst) and j<len(right_lst)):
            if(left_lst[i]<=right_lst[j]):
                lst[k]=left_lst[i]
                i+=1
                # /k+=1
                
            else:
                lst[k] = right_lst[j]
                j+=1
                
            k+=1
      
        # merging the left and right sorted lists:
        while i<len(left_lst):
            lst[k]= left_lst[i]
            
            i+=1
            k+=1
        while j<len(right_lst):
            lst[k]= right_lst[j]     
            
            j+=1
            k+=1
        
        draw_list(draw_info,{i:draw_info.yellow},True)
        yield True
        pygame.display.update()
    pygame.display.update()
    

    return  lst

    
# main that allows us to set up the buttons and render the screen 
def main():
    run = True
    clock = pygame.time.Clock()
    n= 20
    min_val= 1
    max_val= 100

    sorting= False
    ascending = True
    dscending = True
    sorting_algo= bubble_sort
    sorting_algo_name= "Bubble Sort"
    sorting_algo_generate= None
    lst= generate_list(n,min_val,max_val)
    draw_info= windowSetup(800,600,lst) 

    while run:
        clock.tick(30) # fps max number of time the loop can run in a second
        # handling via generator if the algo is in sorting then draw the bars on th screen otherwise break the loop and except the iteration stop
        if sorting:
            try:
                next(sorting_algo_generate)
            except StopIteration:
                sorting= False
        else:
            draw(draw_info,sorting_algo_name,ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # when the red cross hits then the loop will terminate and the program will close
                run = False
            # checking for the keypress on keyboard
            if event.type != pygame.KEYDOWN:
                continue
            # if the r key or the keyboard is pressed then it will reset the list and generates new bars
            elif event.key == pygame.K_r:
                lst= generate_list(n,min_val,max_val)
                draw_info.set_list(lst) # agian passing the new lst to the draw function 

            # buttons genertaed for user to switch between algos and method
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generate= sorting_algo(draw_info,ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algo= insertion_sort
                sorting_algo_name= "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algo= bubble_sort
                sorting_algo_name= "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algo= merge_sort
                sorting_algo_name= "Merge Sort"
                     

    pygame.quit()


if __name__== "__main__":
    main()

