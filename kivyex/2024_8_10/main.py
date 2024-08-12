from random import randint


class Cell:
    # Each cell has a number and a sampler value
    def __init__(self, cell_num, value):
        self.cell_num = cell_num
        self.value = value


class SamplerBox:
    # Each box measures 12 samplers
    def __init__(self, box_num):
        self.box_num = box_num
        self.cells = []
        for i in range(1, 13):
            # Some fake random data
            self.cells.append( Cell(i + ((box_num-1)*12), randint(0, 200)/100.0))


# Populate a list of with 20 boxes
all_boxes = []
for i in range(1,21):
    all_boxes.append(SamplerBox(i))

# Prints examples
print("Box\t\tCell\t\tVal")
for box in all_boxes:
    for cell in box.cells:
        print(f'{box.box_num}\t\t{cell.cell_num}\t\t{cell.value}')