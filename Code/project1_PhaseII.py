import random
import time
random.seed(10)
from mpmath import *
st = time.time()

# cooling_factors=[0.7,0.75,0.8,0.85,0.9,0.95,0.97]
f = open("test.txt", "r")
input_file = f.readline()
input_file_line_elements = input_file.split()
number_of_cells = input_file_line_elements[0]
number_of_connections = input_file_line_elements[1]
row = int(input_file_line_elements[2])
column = int(input_file_line_elements[3])
input_file1 = f.readlines()
lst4 = []
s = 1
for s in input_file1:
    lst3 = []
    ele = s.split()
    for h in range(1, len(ele)):
        lst3.append(ele[h])
    lst4.append(lst3)
grid = [['--' for i in range(column)] for j in range(row)]
cells = []
for i in range(int(number_of_cells)):
    cells.append([i, 0, 0])
for cell in cells:
    cell_row = random.randint(0, row - 1)
    cell_column = random.randint(0, column - 1)
    if grid[cell_row][cell_column] == '--':
        cell[1] = cell_row
        cell[2] = cell_column
        grid[cell_row][cell_column] = cell
    else:
        while grid[cell_row][cell_column] != '--':
            cell_row = random.randint(0, row - 1)
            cell_column = random.randint(0, column - 1)
        cell[1] = cell_row
        cell[2] = cell_column
        grid[cell_row][cell_column] = cell
print("initial placement")
for i in range(row):
    for j in range(column):
        if grid[i][j] != '--':
            [c, x, y] = grid[i][j]
            print(c, end=' ')
        else:
            print('--', end=' ')
    print()
print()
wl = 0

for i in lst4:
    co_x = []
    co_y = []
    for j in range(len(i)):
        [c, x, y] = cells[int(i[j])]
        co_x.append(x)
        co_y.append(y)
    wl = wl + (max(co_x) - min(co_x)) + (max(co_y) - min(co_y))
print("wire length: ", wl)

f.close()

initial_wl = wl

initial_temp = 500 * initial_wl
final_temp = 0.000005 * initial_temp / float(number_of_connections)
current_temp = initial_temp
next_temp = 0.7 * current_temp
moves_per_temp = 10 * int(number_of_cells)
# moves_per_temp = int(10)
count_moves = 0

# print("cells before ", cells)
while current_temp > final_temp:
    # picking 2 random cells

    cr1 = random.randint(0, row - 1)
    cc1 = random.randint(0, column - 1)
    cr2 = random.randint(0, row - 1)
    cc2 = random.randint(0, column - 1)

    cell1 = grid[cr1][cc1]
    cell2 = grid[cr2][cc2]

    # print(cell1, " , ", cell2)

    if (cell1[0] != '-') and (cell2[0] != '-'):     # if both cells not empty
        temp_x = grid[cr1][cc1][1]
        temp_y = grid[cr1][cc1][2]

        grid[cr1][cc1][1] = grid[cr2][cc2][1]
        grid[cr1][cc1][2] = grid[cr2][cc2][2]

        grid[cr2][cc2][1] = temp_x
        grid[cr2][cc2][2] = temp_y

        cell = grid[cr1][cc1]
        grid[cr1][cc1] = grid[cr2][cc2]
        grid[cr2][cc2] = cell

    elif (cell1[0] == '-') and (cell2[0] != '-'):     # if 1st cell empty and 2nd cell not empty
        grid[cr2][cc2][1] = cr1
        grid[cr2][cc2][2] = cc1

        cell = grid[cr1][cc1]
        grid[cr1][cc1] = grid[cr2][cc2]
        grid[cr2][cc2] = cell

    elif (cell1[0] != '-') and (cell2[0] == '-'):     # if 1st cell is not empty and 2nd cell is empty
        grid[cr1][cc1][1] = cr2
        grid[cr1][cc1][2] = cc2

        cell = grid[cr1][cc1]
        grid[cr1][cc1] = grid[cr2][cc2]
        grid[cr2][cc2] = cell

    swapped_wl = 0

    for i in lst4:
        co_x = []
        co_y = []
        for j in range(len(i)):
            # for k in range(len(cells)):
            [c, x, y] = cells[int(i[j])]
            # print(c == int(i[j]))
            # if c == int(i[j]):
            co_x.append(x)
            co_y.append(y)

        # print(co_x, co_y)
        # print("min x ", min(co_x), "  min y ", min(co_y))
        # print("max x ", max(co_x), "  max y ", max(co_y))
        swapped_wl = swapped_wl + (max(co_x) - min(co_x)) + (max(co_y) - min(co_y))

    # print(swapped_wl)

    delta_wl = swapped_wl - wl
    p = random.uniform(0, 1)
    e = exp(- (delta_wl / current_temp))
    wl_arr = []
    # print("probability to accept ", p)

    # scheduling temperature
    if delta_wl < 0:
        wl = swapped_wl

    elif p < e:
        wl = swapped_wl
    else:   # swap again to undo the swap
        cell1 = grid[cr1][cc1]
        cell2 = grid[cr2][cc2]
        if (cell1[0] != '-') and (cell2[0] != '-'):     # if both cells not empty
            temp_x = grid[cr1][cc1][1]
            temp_y = grid[cr1][cc1][2]

            grid[cr1][cc1][1] = grid[cr2][cc2][1]
            grid[cr1][cc1][2] = grid[cr2][cc2][2]

            grid[cr2][cc2][1] = temp_x
            grid[cr2][cc2][2] = temp_y

            cell = grid[cr1][cc1]
            grid[cr1][cc1] = grid[cr2][cc2]
            grid[cr2][cc2] = cell

        elif (cell1[0] == '-') and (cell2[0] != '-'):     # if 1st cell empty and 2nd cell not empty
            grid[cr2][cc2][1] = cr1
            grid[cr2][cc2][2] = cc1

            cell = grid[cr1][cc1]
            grid[cr1][cc1] = grid[cr2][cc2]
            grid[cr2][cc2] = cell

        elif (cell1[0] != '-') and (cell2[0] == '-'):     # if 1st cell is not empty and 2nd cell is empty
            grid[cr1][cc1][1] = cr2
            grid[cr1][cc1][2] = cc2

            cell = grid[cr1][cc1]
            grid[cr1][cc1] = grid[cr2][cc2]
            grid[cr2][cc2] = cell

    if count_moves >= moves_per_temp:
        count_moves = 0
        current_temp = next_temp
        next_temp = 0.95 * current_temp
    else:
        count_moves = count_moves + 1

print()
#print("array of wl", wl_arr)
print("final placement: ")
for i in range(row):
    for j in range(column):
        if grid[i][j] != '--':
            [c, x, y] = grid[i][j]
            print(c, end=' ')
        else:
            print('--', end=' ')
    print()
print()
print("wire length: ", wl)
print("Binary placement: ")
for i in range(row):
    for j in range(column):
        if grid[i][j] != '--':
            [c, x, y] = grid[i][j]
            print(1, end=' ')
        else:
            print(0, end=' ')
    print()

et = time.time()
elapsed_time = et - st
print("Execution time: ", elapsed_time, "seconds")
