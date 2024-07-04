import DxfDrawMaker
from DocDxf import MakeDocDxf
from XlsxInfoExtraction import XlsxInfoExtraction
from DrawTables import DrawTableFromDf

# Generating The Dxf file, that will get all table prints.
doc_dxf = MakeDocDxf()

# Xlsx initial doc
# directory_path = r''
xlsx_file_name = r'eixos1-a-b-c-d.xlsx'
# initial_xlsx_path = os.path.join(directory_path, xlsx_file_name)

# Load the initial file xlsx
doc_xlsx = XlsxInfoExtraction(xlsx_file_name)

# format_and_text is in format:
# [(dict_cell_format, cell_text, Merged_cells, values_with_border), ...]
format_and_text = doc_xlsx.get_row_format_and_text(1, 'Plan1')
"""for cells_infos in format_and_text:
    print(cells_infos)
    for cell_info in cells_infos:
        print(cell_info)"""

# Extracting df from the specified sheet of the xlsx file
df = doc_xlsx.df_from_sheet_in_xlsx('Plan1', 1)


# ------------------------------------ Draw the elements on dxf ----------------------------------------------
# Load the object DrawOnDxf with the DxfDoc
draw_on_dxf_doc = DxfDrawMaker.DrawOnDxf(doc_dxf)

# Calc and Draw a rectangle in doc_dxf
rectangle_ext_polyline_coords = draw_on_dxf_doc.set_rectangle_polyline_coords(1000, 1000, 5700, 5000)
draw_on_dxf_doc.draw_lines(rectangle_ext_polyline_coords, 'Frame')


# Draw Table
inst_table = DrawTableFromDf(doc_dxf, 1250, 1250, df)
inst_table.set_table_variables(cell_height=70, cell_width=140, lines_same_height=False, columns_same_width=False)

# Set Mulipliers for lines and columns (No need for equal size lines and columns)
# The lines index go from : 1 to (len(df) + 1 (if: add_on_bottom) + 1 (if: add_on_top))
inst_table.set_colums_and_lines_multiplier_sizes([1, 5, 6, 10], ['Elev.', 'Eixos'],
                                                 line_height_mult=2.0, column_width_mult=2.0)

inst_table.set_column_names_variables(add_on_bottom=True, add_on_top=True)

# Calculate sizes of the table (width and heigth)
inst_table.calculate_table_sizes()

inst_table.draw_table_lines()

inst_table.set_df_text_attribs(layer="texto")
inst_table.write_df_info()


# Save the file
doc_dxf.save_dxf(r'UTAs.dxf')

print('Done1')
