from imports import *


class DrawOnDxf:

    def __init__(self, dxfdoc):
        self.dxfdoc = dxfdoc
        self.msp = dxfdoc.msp
        self.layer_list = dxfdoc.layers_list

    def draw_lines(self, polylines_coords_tuple_list, layer,
                   color=7, linetype='CONTINUOUS', lineweight=25, thickness=0):
        if layer not in self.layer_list:
            self.dxfdoc.layers_list.append(layer)
            self.layer_list.append(layer)

        self.msp.add_lwpolyline(
            polylines_coords_tuple_list,
            dxfattribs={
                'layer': layer,
                'color': color,  # white
                'linetype': linetype,
                'lineweight': lineweight,  # 25 mm
                'thickness': thickness  # depth of the line in 'Z' axis
            }
        )

    @staticmethod
    def set_rectangle_polyline_coords(xi, yi, width, height):
        rect_polyline = [(xi, yi), (xi+width, yi), (xi+width, yi+height),
                         (xi, yi+height), (xi, yi)]
        return rect_polyline

    def write_text_in_center_of_cell(self, texto, layer, cell_x_start, cell_y_start, cell_width, cell_height):
        # print(f'{texto}, {layer}, {cell_x_start}, {cell_y_start}, {cell_width}, {cell_height}')
        self.msp.add_text(texto, dxfattribs={'layer': layer, 'height': 12, 'color': 7, 'lineweight': 1.00}) \
            .set_placement((cell_x_start + cell_width / 2, cell_y_start + cell_height / 2),
                           align=TextEntityAlignment.MIDDLE_CENTER)
