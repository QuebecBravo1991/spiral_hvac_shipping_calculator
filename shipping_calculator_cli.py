# import pandas library as pd
import pandas as pd
import time

TRAILER_HEIGHT = 98
TRAILER_WIDTH = 92
TRAILER_DEPTH = 10000000

class Spiral_Pipe:
    def __init__(self, diameter,  length, gauge) -> None:
       self.diameter = diameter
       self.length = length
       self.gauge = gauge

    def __str__(self):
        return f"Diameter: {self.diameter} Length: {self.length} Gauge: {self.gauge}"

def read_file():
    while True:
        # get the file name
        print("Please input the name of the file you wish to caclulate from: ")
        file_name = input()
        # create data frame from the file
        try:
            data_frame = pd.read_excel(repr(file_name[1:-1])[1:-1], sheet_name='Estimate')
            return data_frame
        except FileNotFoundError:
            print("\nNo such file found. Did you spell it right? Is it in the right folder?\n")


def collect_pipe(data_frame):
    names = data_frame.iloc[:, 2]
    names_length = len(names)
   
    pipes = []

    for i in range(names_length):
        current_cell = names[i]

        if type(current_cell) != str:
            continue

        if ("Spiral Pipe" in current_cell):
            # find the diameter of the pipe
            inch_index = current_cell.index('"')
            diameter = int(current_cell[:inch_index])

            # find the length
            length = round_up_to_5(data_frame.iloc[i, 0]) 

            # find the gauge
            ga_index = current_cell.index('ga')
            gauge = int(current_cell[ga_index - 2:ga_index]) 
   
            # create a pipe for each stick
            i = length
            while (i > 5):
                pipe = Spiral_Pipe(diameter, 10, gauge)
                pipes.append(pipe)
                i -= 10
            if i == 5:
                pipe = Spiral_Pipe(diameter, 5, gauge)
                pipes.append(pipe)

    return pipes

def round_up_to_5(num):
    ret_val = num

    # round up to whole number and convert to integer
    if (ret_val % 1 != 0):
        ret_val += 1
    ret_val = int(ret_val)

    # round up to multiple of 5
    while (ret_val % 5 != 0):
        ret_val += 1

    return ret_val

def sort_pipe(pipes):
    ret_val = []


    while pipes:
        max = pipes[0]
        
        for pipe in pipes:
            if (getattr(pipe, "diameter") > getattr(max, "diameter")):
                max =  pipe


        ret_val.append(max)
        pipes.remove(max)

    return ret_val

def pack_pipe(pipes):
    # dimensions x y z / width , height, depth
    dimensions = [0, 0, 0]
    

    level_width = 0
    layer_height = 0

    while pipes:
        current_diameter = getattr(pipes[0], "diameter")
        current_length = getattr(pipes[0], "length")
        
        if (level_width + current_diameter <= TRAILER_WIDTH):
            level_width += current_diameter
            
            if layer_height == 0:
                layer_height = current_diameter
            if dimensions[1] == 0:
                dimensions[1] = current_diameter
            if dimensions[0] < level_width:
                dimensions[0] = level_width
            if dimensions[2] == 0:
                dimensions[2] = current_length
        elif (layer_height + current_diameter <= TRAILER_HEIGHT):
            layer_height += current_diameter
            if layer_height > dimensions[1]:
                dimensions[1] = layer_height
            level_width = current_diameter
        elif (dimensions[2] + current_length <= TRAILER_DEPTH):
            if dimensions[2] % 10 != 0:
                dimensions[2] += 5
            else :
                dimensions[2] += current_length
            layer_height = 0
            level_width = current_diameter
        else :
            raise Exception("Looks like you need more than one trailer! This feature is currently not supported!")

        greatest_nestable_diameter = current_diameter
        
        nestable = True

        while nestable:
            found_nestable_pipe = False
            for pipe in pipes:
                if getattr(pipe, "diameter") < greatest_nestable_diameter:
                    greatest_nestable_diameter = getattr(pipe, "diameter")
                    pipes.remove(pipe)
                    found_nestable_pipe = True
                    break
            if found_nestable_pipe == False:
                nestable = False
    
        pipes.pop(0)

    print("The width is: " + str(dimensions[0]) + "\" The height is: " + str(dimensions[1])  + "\" The depth is " + str(dimensions[2]) + "\'")


def print_pipe(pipes):
    print("\n The following pipe(s) were found: ")

    for pipe in pipes:
        print(pipe)

    print()



data_frame = read_file()
pipes = collect_pipe(data_frame)
pipes = sort_pipe(pipes)
print_pipe(pipes)
pack_pipe(pipes)


while True:
    time.sleep(2)
