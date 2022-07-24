import re
import gi
gi.require_version('Gtk', '4.0')

import logging
logger = logging.getLogger('apostrophe')


class FixTable():

    def __init__(self, TextBuffer):
        self.TextBuffer = TextBuffer

    @staticmethod
    def create_seperator(widths, char):
        """
            Generate a line of + and - as sepeartor

            Example:
            >>> create_separarator([2, 4], '-')
            '+----+------+'
        """
        line = []

        for w in widths:
            line.append("+" + char * (w + 2))

        line.append("+")
        return ''.join(line)

    @staticmethod
    def create_line(columns, widths):
        """
            Crea una fila de la tabla separando los campos con un '|'.

            El argumento `columns` es una lista con las celdas que se
            quieren imprimir y el argumento `widths` tiene el ancho
            de cada columna. Si la columna es mas ancha que el texto
            a imprimir se agregan espacios vacíos.

            Example
                >>> create_line(['nombre', 'apellido'], [7, 10])
                '| nombre  | apellido   |'
        """

        line = zip(columns, widths)
        result = []

        for text, width in line:
            spaces = " " * (width - len(text))
            text = "| " + text + spaces + " "
            result.append(text)

        result.append("|")
        return ''.join(result)

    @staticmethod
    def create_table(content):
        """Imprime una tabla en formato restructuredText.

        El argumento `content` tiene que ser una lista
        de celdas.

        Example:

            >>> print create_table([['software', 'vesion'], ['python', '3.2'],
                ['vim', '7.3']])
+----------+--------+
| software | vesion |
+==========+========+
| python   | 3.2    |
+----------+--------+
| vim      | 7.3    |
+----------+--------+
        """

        # obtiene las columnas de toda la tabla.
        columns = zip(*content)
        # calcula el tamano maximo que debe tener cada columna.
        # replace with len()
        widths = [max([len(x) for x in i]) for i in columns]

        result = []

        result.append(FixTable.create_seperator(widths, '-'))
        print(content, widths)
        result.append(FixTable.create_line(content[0], widths))
        result.append(FixTable.create_seperator(widths, '='))

        for line in content[1:]:
            result.append(FixTable.create_line(line, widths))
            result.append(FixTable.create_seperator(widths, '-'))

        return '\n'.join(result)

    @staticmethod
    def are_in_a_table(current_line):
        "Line in a table?"
        return "|" in current_line or "+" in current_line

    @staticmethod
    def are_in_a_paragraph(current_line):
        "Line in a paragraph?"
        return len(current_line.strip()) >= 1

    def get_table_bounds(self, are_in_callback):
        """
            Gets the row number where the table begins and ends.
            are_in_callback argument must be a function
                    indicating whether a particular line belongs or not
                        to the table to be measured (or create).
                        Returns two values ​​as a tuple
        """
        top = 0

        buf = self.TextBuffer
        start_iter = buf.get_start_iter()
        end_iter = buf.get_end_iter()

        text = self.TextBuffer.get_text(
            start_iter, end_iter, False).split('\n')
        logger.debug(text)
        length = len(text)
        bottom = length - 1

        insert_mark = self.TextBuffer.get_insert()
        insert_iter = self.TextBuffer.get_iter_at_mark(insert_mark)
        current_row_index = insert_iter.get_line()

        for a in range(current_row_index, top, -1):
            if not are_in_callback(text[a]):
                top = a + 1
                break

        for b in range(current_row_index, length):
            if not are_in_callback(text[b]):
                bottom = b - 1
                break

        return top, bottom

    @staticmethod
    def remove_spaces(string):
        """Remove unnecessary spaces"""
        return re.sub("\\s\\s+", " ", string)

    @staticmethod
    def create_separators_removing_spaces(string):
        return re.sub("\\s\\s+", "|", string)

    @staticmethod
    def extract_cells_as_list(string):
        "Extrae el texto de una fila de tabla y lo retorna como una lista."
        string = FixTable.remove_spaces(string)
        return [item.strip() for item in string.split('|') if item]

    @staticmethod
    def extract_table(text, top, bottom):
        full_table_text = text[top:bottom]
        # selecciona solamente las lineas que tienen celdas con texto.
        only_text_lines = [x for x in full_table_text if '|' in x]
        # extrae las celdas y descarta los separadores innecesarios.
        return [FixTable.extract_cells_as_list(x) for x in only_text_lines]

    @staticmethod
    def extract_words_as_lists(text, top, bottom):
        "Genera una lista de palabras para crear una lista."

        lines = text[top:bottom + 1]
        return [FixTable.create_separators_removing_spaces(
            line).split('|') for line in lines]

    def fix_table(self):
        """
            Fix Table, so all columns have the same width (again)

            `initial_row` is a int idicationg the current row index
        """

        cursor_mark = self.TextBuffer.get_insert()
        cursor_iter = self.TextBuffer.get_iter_at_mark(cursor_mark)
        cursor_iter.set_line(cursor_iter.get_line())

        end_line = cursor_iter.copy()
        end_line.forward_to_line_end()

        line_text = self.TextBuffer.get_text(cursor_iter, end_line, False)
        if FixTable.are_in_a_table(line_text):

            # obtiene el indice donde comienza y termina la tabla.
            r1, r2 = self.get_table_bounds(FixTable.are_in_a_table)

            logger.debug('asdasd ')

            # extrae de la tabla solo las celdas de texto
            buf = self.TextBuffer
            start_iter = buf.get_start_iter()
            end_iter = buf.get_end_iter()

            text = self.TextBuffer.get_text(
                start_iter, end_iter, False).split('\n')

            table_as_list = FixTable.extract_table(text, r1, r2)
            logger.debug(table_as_list)
            # genera una nueva tabla tipo restructured text y la dibuja en el
            # buffer.
            table_content = FixTable.create_table(table_as_list)
            logger.debug(table_content)
            # Insert table back into Buffer ...
            self.TextBuffer.insert(start_iter, table_content, -1)
        else:
            logger.debug("Not in a table")
            print("Not in table")
