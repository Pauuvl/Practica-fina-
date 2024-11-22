import sys
import nltk
from nltk import CFG, ChartParser
from nltk.tree import Tree
from nltk.grammar import Nonterminal
from collections import deque
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

# Definición de la gramática
gramatica = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")

# Función de derivación recursiva
def derivar(gramatica, expresion, modo='izquierda'):
    procesados = set()

    def expandir(gramatica, simbolo):
        """Expande un símbolo no terminal de acuerdo con la gramática."""
        for regla in gramatica.productions(lhs=simbolo):
            return [regla]
        return []

    def derivacion_recursiva(gramatica, simbolo, derivacion=[]):
        """Realiza la derivación recursiva, ya sea por izquierda o por derecha."""
        if isinstance(simbolo, str):
            return derivacion + [simbolo]

        if simbolo in procesados:
            return derivacion

        procesados.add(simbolo)

        producciones = expandir(gramatica, simbolo)
        for produccion in producciones:
            derivacion_parcial = derivacion + [str(produccion.lhs())]
            expresion_parcial = " ⇒ ".join([str(elemento) for elemento in derivacion_parcial])
            print(f"Derivación parcial: {expresion_parcial}")

            for parte in produccion.rhs():
                derivacion_parcial = derivacion_recursiva(gramatica, parte, derivacion_parcial)
            return derivacion_parcial
        return derivacion

    derivacion_final = derivacion_recursiva(gramatica, gramatica.start())
    return [str(p) if isinstance(p, Nonterminal) else p for p in derivacion_final]

# Función para generar el árbol AST simplificado
def tree_to_AST_visual(tree):
    def bfs_tree(tree):
        """Recorre un árbol y devuelve una lista de nodos por nivel."""
        result = []
        queue = deque([tree])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                # Filtra nodos no terminales (E, T, F) y paréntesis
                if isinstance(node, nltk.Tree):
                    queue.extend(node)  # Agrega los hijos del nodo
                    if node.label() not in {'E', 'T', 'F'}:
                        level.append(node)
                elif node not in {'(', ')'}:  # Filtra los paréntesis
                    level.append(node)
            if level:  # Agregar solo niveles no vacíos
                result.append(level)
        return result

    levels = bfs_tree(tree)
    for level in levels:
        for terminal in level:
            if terminal is not None:
                print(terminal)

# Función para imprimir el árbol de derivación de forma estructurada
def print_derivation_tree(tree):
    """
    Imprime el árbol de derivación de manera visual similar a la estructura solicitada.
    """
    def print_tree_structure(tree, indent=""):
        if isinstance(tree, nltk.Tree):
            # Imprimir el nodo actual con su etiqueta
            print(f"{indent}{tree.label()}")
            indent += "  "
            for child in tree:
                print_tree_structure(child, indent)
        else:
            # Imprimir los terminales directamente
            print(f"{indent}{tree}")

    print_tree_structure(tree)

# Clase principal de la interfaz PyQt5
class GrammarParserApp(QWidget):
    def _init_(self):
        super()._init_()

        self.initUI()

    def initUI(self):
        # Establecer el título y el tamaño inicial de la ventana
        self.setWindowTitle('Generador de Árboles Sintácticos')
        self.setGeometry(100, 100, 650, 400)

        # Estilo de la interfaz con botones morados
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 5px;
            }
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #9b59b6;  /* Morado */
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #8e44ad;  /* Morado más oscuro */
            }
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #9b59b6;
                margin-top: 20px;
                padding: 15px;
                border: 2px solid #9b59b6;
                border-radius: 10px;
            }
            QVBoxLayout {
                margin: 20px;
            }
            QHBoxLayout {
                spacing: 20px;
                margin-top: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #9b59b6;
            }
            QLabel#resultLabel {
                font-size: 16px;
                font-weight: normal;
                color: #555;
                padding-top: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta y campo de entrada para la expresión
        self.label = QLabel('Ingrese una expresión:')
        layout.addWidget(self.label)

        self.expression_input = QLineEdit(self)
        layout.addWidget(self.expression_input)

        # Grupo de opciones para derivación
        derivacion_group = QGroupBox('Seleccione dirección de derivación:')
        derivacion_layout = QHBoxLayout()

        self.modo_button_izquierda = QPushButton('Izquierda', self)
        self.modo_button_izquierda.clicked.connect(self.derivar_izquierda)
        derivacion_layout.addWidget(self.modo_button_izquierda)

        self.modo_button_derecha = QPushButton('Derecha', self)
        self.modo_button_derecha.clicked.connect(self.derivar_derecha)
        derivacion_layout.addWidget(self.modo_button_derecha)

        derivacion_group.setLayout(derivacion_layout)
        layout.addWidget(derivacion_group)

        # Etiqueta para mostrar el resultado
        self.result_label = QLabel('Resultado:')
        self.result_label.setObjectName("resultLabel")
        layout.addWidget(self.result_label)

        # Establecer el layout en la ventana
        self.setLayout(layout)

    def derivar_izquierda(self):
        self.derivar('izquierda')

    def derivar_derecha(self):
        self.derivar('derecha')

    def derivar(self, modo):
        # Obtener la expresión ingresada por el usuario
        expresion = self.expression_input.text().split()

        # Derivar la expresión
        derivacion = derivar(gramatica, expresion, modo)
        derivacion_final = " ⇒ ".join(derivacion)

        # Mostrar la derivación en la interfaz
        self.result_label.setText(f"Derivación final: {derivacion_final}")

        # Generar el árbol sintáctico
        parser = ChartParser(gramatica)
        trees = list(parser.parse(expresion))

        if trees:
            print("\nÁrbol de derivación generado:")
            for tree in trees:
                print(tree.pretty_print())  # Mostrar árbol sintáctico
                tree.draw()  # Mostrar el árbol de forma visual

            # Ahora generar el árbol AST
            print("\nÁrbol de sintaxis abstracta (AST):")
            for tree in trees:
                tree_to_AST_visual(tree)

        else:
            print("No se pudo generar un árbol con la gramática proporcionada.")

import sys
import nltk
from nltk import CFG, ChartParser
from nltk.tree import Tree
from nltk.grammar import Nonterminal
from collections import deque
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

# Definición de la gramática
gramatica = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")

# Mostrar las reglas de la gramática
def mostrar_gramatica():
    print("Gramática definida:")
    print(gramatica)

# Función de derivación recursiva
def derivar(gramatica, expresion, modo='izquierda'):
    procesados = set()

    def expandir(gramatica, simbolo):
        """Expande un símbolo no terminal de acuerdo con la gramática."""
        for regla in gramatica.productions(lhs=simbolo):
            return [regla]
        return []

    def derivacion_recursiva(gramatica, simbolo, derivacion=[]):
        """Realiza la derivación recursiva, ya sea por izquierda o por derecha."""
        if isinstance(simbolo, str):
            return derivacion + [simbolo]

        if simbolo in procesados:
            return derivacion

        procesados.add(simbolo)

        producciones = expandir(gramatica, simbolo)
        for produccion in producciones:
            derivacion_parcial = derivacion + [str(produccion.lhs())]

            # No se imprime la derivación parcial en consola
            # Expresión parcial para la derivación (no se muestra en este caso)
            for parte in produccion.rhs():
                derivacion_parcial = derivacion_recursiva(gramatica, parte, derivacion_parcial)
            return derivacion_parcial
        return derivacion

    # Obtener la derivación final y devolverla
    derivacion_final = derivacion_recursiva(gramatica, gramatica.start())
    return [str(p) if isinstance(p, Nonterminal) else p for p in derivacion_final]

# Función para generar el árbol AST simplificado
def tree_to_AST_visual(tree):
    def bfs_tree(tree):
        """Recorre un árbol y devuelve una lista de nodos por nivel."""
        result = []
        queue = deque([tree])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                # Filtra nodos no terminales (E, T, F) y paréntesis
                if isinstance(node, nltk.Tree):
                    queue.extend(node)  # Agrega los hijos del nodo
                    if node.label() not in {'E', 'T', 'F'}:
                        level.append(node)
                elif node not in {'(', ')'}:  # Filtra los paréntesis
                    level.append(node)
            if level:  # Agregar solo niveles no vacíos
                result.append(level)
        return result

    levels = bfs_tree(tree)
    for level in levels:
        for terminal in level:
            if terminal is not None:
                print(terminal)

# Clase principal de la interfaz PyQt5
class GrammarParserApp(QWidget):
    def _init_(self):
        super()._init_()

        self.initUI()

    def initUI(self):
        # Establecer el título y el tamaño inicial de la ventana
        self.setWindowTitle('Generador de Árboles Sintácticos')
        self.setGeometry(100, 100, 650, 400)

        # Estilo de la interfaz con botones morados
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 5px;
            }
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QPushButton {
                font-size: 16px;
                padding: 12px;
                background-color: #9b59b6;  /* Morado */
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #8e44ad;  /* Morado más oscuro */
            }
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #9b59b6;
                margin-top: 20px;
                padding: 15px;
                border: 2px solid #9b59b6;
                border-radius: 10px;
            }
            QVBoxLayout {
                margin: 20px;
            }
            QHBoxLayout {
                spacing: 20px;
                margin-top: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #9b59b6;
            }
            QLabel#resultLabel {
                font-size: 16px;
                font-weight: normal;
                color: #555;
                padding-top: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta y campo de entrada para la expresión
        self.label = QLabel('Ingrese una expresión:')
        layout.addWidget(self.label)

        self.expression_input = QLineEdit(self)
        layout.addWidget(self.expression_input)

        # Grupo de opciones para derivación
        derivacion_group = QGroupBox('Seleccione dirección de derivación:')
        derivacion_layout = QHBoxLayout()

        self.modo_button_izquierda = QPushButton('Izquierda', self)
        self.modo_button_izquierda.clicked.connect(self.derivar_izquierda)
        derivacion_layout.addWidget(self.modo_button_izquierda)

        self.modo_button_derecha = QPushButton('Derecha', self)
        self.modo_button_derecha.clicked.connect(self.derivar_derecha)
        derivacion_layout.addWidget(self.modo_button_derecha)

        derivacion_group.setLayout(derivacion_layout)
        layout.addWidget(derivacion_group)

        # Etiqueta para mostrar el resultado
        self.result_label = QLabel('Resultado:')
        self.result_label.setObjectName("resultLabel")
        layout.addWidget(self.result_label)

        # Establecer el layout en la ventana
        self.setLayout(layout)

    def derivar_izquierda(self):
        self.derivar('izquierda')

    def derivar_derecha(self):
        self.derivar('derecha')

    def derivar(self, modo):
        # Obtener la expresión ingresada por el usuario
        expresion = self.expression_input.text().split()

        # Derivar la expresión
        derivacion = derivar(gramatica, expresion, modo)
        derivacion_final = " ".join(derivacion)

        # Mostrar la derivación en la interfaz
        self.result_label.setText(f"Derivación final: {derivacion_final}")

        # Imprimir la derivación final en consola (igual a la expresión ingresada por el usuario)
        print(f"Derivación final: {' '.join(expresion)}")

        # Generar el árbol sintáctico
        parser = ChartParser(gramatica)
        trees = list(parser.parse(expresion))

        if trees:
            print("\nÁrbol de derivación generado:")
            for tree in trees:
                tree.pretty_print()  # Mostrar árbol sintáctico
                tree.draw()  # Mostrar el árbol de forma visual

            # Ahora generar el árbol AST
            print("\nÁrbol de sintaxis abstracta (AST):")
            for tree in trees:
                tree_to_AST_visual(tree)

        else:
            print("No se pudo generar un árbol con la gramática proporcionada.")


# Función principal
def main():
    app = QApplication(sys.argv)
    ex = GrammarParserApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()