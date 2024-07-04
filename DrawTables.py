from imports import *
from DxfDrawMaker import DrawOnDxf


class DrawTableFromDf:

    def __init__(self, dxfdoc, xi, yi, df=pd.DataFrame(), num_lines_add=0):
        self.dxfdoc = dxfdoc
        self.msp = dxfdoc.msp

        # Table info
        # Initial Positions
        self.xi = xi
        self.yi = yi

        # Iteration positions
        self.x_position = xi
        self.y_position = yi

        if not df.empty:
            self.df = df

        # Cell Variables
        self.cell_height = 70
        self.cell_width = 140

        # Table Characteristics
        self.lines_are_same_height = True
        self.columns_are_same_width = True
        self.line_height_size_mult = 1.0
        self.column_width_size_mult = 1.0
        self.large_line_indexs = []
        self.large_columns_names = []

        # Table total sizes
        self.table_height = 0
        self.table_width = 0

        # Table Height List
        self.cells_x_position_list = [self.xi]
        self.cells_y_position_list = []

        # Column Names Variables
        self.add_column_name_on_top = False
        self.add_column_name_on_bottom = False
        self.number_column_names_list_add = 0
        # For future use
        self.columns_names_list_to_add = []
        # --

        # Add lines
        self.add_lines = num_lines_add

        # df text atribs
        self.dxf_df_text_attribs = {}

    def set_column_names_variables(self, add_on_top=False, add_on_bottom=False, column_list_to_add=None):
        if add_on_top:
            self.add_column_name_on_top = True
            self.number_column_names_list_add += 1
        if add_on_bottom:
            self.add_column_name_on_bottom = True
            self.number_column_names_list_add += 1
        if column_list_to_add:
            self.columns_names_list_to_add = column_list_to_add

    def set_table_variables(self, cell_height, cell_width, lines_same_height=True, columns_same_width=True):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.lines_are_same_height = lines_same_height
        self.columns_are_same_width = columns_same_width

    def set_colums_and_lines_multiplier_sizes(self, mult_line_indexs=None, mult_columns_names=None,
                                              line_height_mult=1.0, column_width_mult=1.0):
        if isinstance(mult_line_indexs, list):
            self.line_height_size_mult = line_height_mult
            self.large_line_indexs = mult_line_indexs

            if line_height_mult == 1.0:
                raise ValueError('Line Height multiplier with same value as default(1.0)')

        if isinstance(mult_columns_names, list):
            self.column_width_size_mult = column_width_mult
            self.large_columns_names = mult_columns_names

            if line_height_mult == 1.0:
                raise ValueError('Column width multiplier with same value as default(1.0)')

        if (not mult_line_indexs) and (not mult_columns_names):
            raise ValueError('mult_line_indexs and mult_columns_names are empty')

    def set_axis_current_positions(self, x=None, y=None):
        if isinstance(x, int):
            self.x_position = x

        if isinstance(y, int):
            self.y_position = y

        if (not x) and (not y):
            raise ValueError('axis current position must be integers!')

    def calculate_table_sizes(self):
        if self.lines_are_same_height:
            self.table_height = self.cell_height * len(self.df) + self.cell_height * self.number_column_names_list_add
        else:
            self.table_height = (self.cell_height * (len(self.df) - len(self.large_line_indexs))) + \
                                (len(self.large_line_indexs) * self.cell_height * self.line_height_size_mult) +\
                                self.cell_height * self.number_column_names_list_add  # Precisa Modificar
            # Caso se precise altura de linhas diferentes para column_names

        if self.columns_are_same_width:
            self.table_width = self.cell_width * len(self.df.columns)
        else:
            self.table_width = (self.cell_width * (len(self.df.columns) - len(self.large_columns_names))) + \
                               (len(self.large_columns_names) * self.cell_width * self.column_width_size_mult)

    def update_x_and_y_current_positions(self, line_index=None, column_index=None, column_name=None):
        if line_index:
            if (line_index in self.large_line_indexs) and (not self.lines_are_same_height):
                self.y_position += (self.cell_height * self.line_height_size_mult)
                self.cells_y_position_list.append(self.y_position)
            else:
                self.y_position += self.cell_height
                self.cells_y_position_list.append(self.y_position)

        if column_index:
            if (column_name in self.large_columns_names) and (not self.columns_are_same_width):
                self.x_position += (self.cell_width * self.column_width_size_mult)
                self.cells_x_position_list.append(self.x_position)
            else:
                self.x_position += self.cell_width
                self.cells_x_position_list.append(self.x_position)

        if (not line_index) and (not column_index):
            raise ValueError('Need to set the "update_x_and_y_current_positions" method entries!')

    def draw_table_lines(self, layer='Table', text_layer='texto'):

        draw_on_dxf = DrawOnDxf(self.dxfdoc)
        for line_index in range(len(self.df) + 1 + self.number_column_names_list_add + self.add_lines):
            if line_index:
                self.update_x_and_y_current_positions(line_index=line_index)
            horizontal_line_coords = [(self.xi, self.y_position),
                                      (self.xi+self.table_width, self.y_position)]
            draw_on_dxf.draw_lines(horizontal_line_coords, layer)

        for col_index, column in enumerate(self.df.columns):
            vertical_line_coords = [(self.x_position, self.yi),
                                    (self.x_position, self.yi + self.table_height)]
            last_line_position = vertical_line_coords

            draw_on_dxf.draw_lines(vertical_line_coords, layer)

            self.update_x_and_y_current_positions(column_index=col_index + 1, column_name=column)
            next_line_position = [(self.x_position, self.yi),
                                  (self.x_position, self.yi + self.table_height)]

            # Math to center text.
            cell_x_start_position = last_line_position[0][0]
            cell_x_end_position = next_line_position[0][0]
            actual_cell_width = cell_x_end_position - cell_x_start_position

            if self.add_column_name_on_bottom:
                cell_y_start_position = self.yi
                cell_y_end_position = self.cells_y_position_list[0]
                actual_cell_height = cell_y_end_position - cell_y_start_position
                draw_on_dxf.write_text_in_center_of_cell(column, text_layer, cell_x_start_position,
                                                         cell_y_start_position, actual_cell_width, actual_cell_height)

            if self.add_column_name_on_top:
                cell_y_start_position = self.cells_y_position_list[-2]
                cell_y_end_position = self.yi + self.table_height
                actual_cell_height = cell_y_end_position - cell_y_start_position
                draw_on_dxf.write_text_in_center_of_cell(column, text_layer, cell_x_start_position,
                                                         cell_y_start_position, actual_cell_width, actual_cell_height)

            if col_index == len(self.df.columns)-1:
                vertical_line_coords = [(self.x_position, self.yi),
                                        (self.x_position, self.yi + self.table_height)]
                draw_on_dxf.draw_lines(vertical_line_coords, layer)

    def set_df_text_attribs(self, layer, height=12, color=7, lineweight=1.00):
        self.dxf_df_text_attribs = {'layer': layer, 'height': height,
                                    'color': color, 'lineweight': lineweight}

    def write_df_info(self):
        draw_on_dxf = DrawOnDxf(self.dxfdoc)
        new_cells_y_pos_list = 0
        if self.add_column_name_on_bottom and self.add_column_name_on_top:
            new_cells_y_pos_list = self.cells_y_position_list[1:-1]
        elif self.add_column_name_on_bottom:
            new_cells_y_pos_list = self.cells_y_position_list[1:]
        elif self.add_column_name_on_top:
            new_cells_y_pos_list = self.cells_y_position_list[:-1]

        for idy, y_initial_pos in enumerate(self.cells_y_position_list):
            # print(idy)
            if idy != len(new_cells_y_pos_list):
                y_final_pos = self.cells_y_position_list[idy + 1]
                actual_cell_height = y_final_pos - y_initial_pos
            else:
                break

            for idx, x_initial_pos in enumerate(self.cells_x_position_list[:-1]):
                if idx != (len(self.cells_x_position_list)):
                    x_final_pos = self.cells_x_position_list[idx + 1]
                    actual_cell_width = x_final_pos - x_initial_pos
                    texto = self.df.iloc[idy, idx]
                    if texto:
                        draw_on_dxf.write_text_in_center_of_cell(texto, "texto", x_initial_pos, y_initial_pos,
                                                                 actual_cell_width, actual_cell_height)
