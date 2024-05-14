import pandas as pd
import json
import os

ij1 = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\15thcensus872unit_1033.json"
ij2 = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\michigancensus00reel974_0114.json"
ij3 = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\michigancensus00reel974_0221.json"
ij4 = r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\newyorkcensus00reel1415rs_0920.json"

list_of_lists = []


for ij in [ij1, ij2, ij3, ij4]:
    reel_filename = 'images.tar'
    image_filename = os.path.splitext(os.path.basename(ij))[0] + ".png"

    with open(ij, 'r') as j:
        corners = json.load(j)

    columns_and_rows = corners['corners']

    for col_index in range(len(columns_and_rows) - 2):
        for row_index in range(len(columns_and_rows[0]) - 1):
            x1, y1 = columns_and_rows[col_index][row_index]
            x2, y2 = columns_and_rows[col_index+1][row_index]
            x3, y3 = columns_and_rows[col_index][row_index+1]
            x4, y4 = columns_and_rows[col_index+1][row_index+1]

            list_of_lists.append([reel_filename, image_filename, f"r{row_index+1}c{col_index+1}", x1, y1, x2, y2, x3, y3, x4, y4])


df = pd.DataFrame(list_of_lists, columns=['reel_filename', 'image_filename', 'snip_name', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])

df.to_csv(r"C:\Users\Jackson Roubidoux\RLL\repos\RLL_Snippet_Generator\tests\resources\images.tsv", sep='\t', index=False)
