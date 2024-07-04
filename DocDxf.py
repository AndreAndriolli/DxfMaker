from imports import *


class MakeDocDxf:

    def __init__(self):
        # Criação de um novo documento DXF
        self.doc = ezdxf.new('R2010')  # Set Dxf version
        self.msp = self.doc.modelspace()

        # Mapeia layers criados
        self.layers_list = []

    def set_layers_for_use(self, lista_layers):
        self.layers_list = lista_layers

    def add_layer_to_current_layers_list(self, layer):
        self.layers_list.append(layer)

    def save_dxf(self, path_saida='Output Dxf'):
        self.doc.saveas(path_saida)  # Salving Dxf File
        print(f'Doc: "{path_saida}" saved!')
