# import pandas library as pd
import pandas as pd

TRAILER_HEIGHT = 90
TRAILER_WIDTH = 98
TRAILER_DEPTH = 53

class Spiral_Pipe:
    def __init__(self, diameter,  length, gauge) -> None:
       self.diameter = diameter
       self.length = length
       self.gauge = gauge

    def __str__(self):
        return f"Diameter: {self.diameter} Length: {self.length} Gauge: {self.gauge}"

def read_file():
    # get the file name
    print("Please input the name of the file you wish to caclulate from: ")
    file_name = input()

    # create data frame from the file
    data_frame = pd.read_excel(file_name, sheet_name='Sheet1')
    
    return data_frame

def collect_pipe(data_frame):
    names = data_frame['Name']
    names_length = len(names)
   
    pipes = []

    for i in range(names_length):
        current_cell = names[i]

        if ("Spiral Pipe" in current_cell):
            # find the diameter of the pipe
            inch_index = current_cell.index('"')
            diameter = int(current_cell[:inch_index])

            # find the length
            length = round_up_to_5(data_frame.iloc[i]['Qty']) 

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

def print_pipe(pipes):
    print("The following pipe(s) were found: ")

    for pipe in pipes:
        print(pipe)



data_frame = read_file()
pipes = collect_pipe(data_frame)
print_pipe(pipes)


