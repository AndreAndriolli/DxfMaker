from imports import *


class XlsxInfoExtraction:

    def __init__(self, path_xlsx):
        self.workbook = load_workbook(path_xlsx, data_only=False)
        self.df = pd.DataFrame()
        self.sheet = self.workbook.active  # load the last sheet that had someone working on

    def load_the_desire_sheet(self, sheet):
        self.sheet = self.workbook[sheet]

    def df_from_sheet_in_xlsx(self, sheet='', index_columns_indexs=0):
        if not sheet:
            sheet = self.sheet
        try:
            self.load_the_desire_sheet(sheet)
            df = pd.DataFrame(self.sheet.values)
            new_header = df.iloc[index_columns_indexs]  # Pegando a segunda linha para os nomes das colunas
            df = df[(index_columns_indexs+1):]  # Excluindo a primeira linha
            df.columns = new_header  # Definindo os novos nomes das colunas
            df = df.reset_index(drop=True)
            df = df.rename_axis('index', axis=1)
            self.df = df
            return df
        except KeyError as e:
            print(f"Sheet '{sheet}' not found in the workbook. Error: {e}")

    def get_row_format_and_text(self, row_number: int, sheet='', is_current_sheet=False):
        # Result format:
        # [(dict_cell_format, cell_text, Merged_cells, values_with_border), ...]
        if not is_current_sheet:
            self.load_the_desire_sheet(sheet)

        result = []
        row = self.sheet[row_number]

        for cell in row:
            cell_text = str(cell.value)
            cell_style = self._get_cell_style(cell)
            cell_merge = self._get_cell_merge_info(cell)
            cell_border = self._get_cell_border(cell)
            result.append((cell_style, cell_text, cell_merge, cell_border))
        return result

    def _get_cell_style(self, cell) -> Dict[str, str]:
        style_info = {}

        # Verificar se a célula tem um estilo nomeado que não seja 'Normal'
        if cell.style and cell.style != 'Normal':
            named_style = self.workbook.named_styles[cell.style] if cell.style in self.workbook.named_styles else None
            if named_style:
                style_info['NamedStyle'] = named_style.name

        # Verificar se há formatação direta na célula
        if cell.has_style:
            if cell.font:
                style_info['Font'] = str(cell.font)
            if cell.fill:
                style_info['Fill'] = str(cell.fill)
            if cell.border:
                style_info['Border'] = str(cell.border)
            if cell.alignment:
                style_info['Alignment'] = str(cell.alignment)
            if cell.protection:
                style_info['Protection'] = str(cell.protection)
            if cell.number_format:
                style_info['NumberFormat'] = str(cell.number_format)

        if not style_info:
            style_info['Style'] = 'Normal'

        return style_info

    def _get_cell_merge_info(self, cell) -> str:
        for merged_range in self.sheet.merged_cells.ranges:
            if cell.coordinate in merged_range:
                return str(merged_range)
        return 'None'

    @staticmethod
    def _get_cell_border(cell) -> List:
        border_sides = []
        if cell.border.left.style:
            border_sides.append('left')
        if cell.border.right.style:
            border_sides.append('right')
        if cell.border.top.style:
            border_sides.append('top')
        if cell.border.bottom.style:
            border_sides.append('bottom')
        return border_sides
