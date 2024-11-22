Paulina Velásquez y Helen Sanabria
Generador de Árboles Sintácticos
Este proyecto implementa un generador de árboles sintácticos utilizando una gramática definida en BNF (Backus-Naur Form) para una expresión aritmética. El programa permite realizar derivaciones de la expresión por izquierda o derecha (ascendente o descendente), generando tanto el árbol de derivación como el Árbol Sintáctico Abstracto (AST).




import nltk
nltk.download('punkt')
Descripción del Código
1. Definición de la Gramática
La gramática utilizada sigue la estructura básica de una expresión aritmética con operaciones +, -, *, y /. Se definen tres tipos de reglas:

E (Expresión): La expresión puede ser una combinación de términos conectados por + o -.
T (Término): Los términos pueden estar conectados por multiplicación (*) o división (/).
F (Factor): Los factores son números o expresiones entre paréntesis.
2. Derivación de la Expresión
Se implementan derivaciones por izquierda y por derecha:

Derivación por izquierda: Expande el primer no terminal de izquierda a derecha en la expresión.
Derivación por derecha: Expande el último no terminal de derecha a izquierda en la expresión.
3. Árbol Sintáctico y AST
El árbol de derivación se genera de acuerdo con la gramática y muestra cómo la expresión es transformada.
El Árbol Sintáctico Abstracto (AST) simplifica el árbol de derivación eliminando los nodos intermedios como E, T, y F para mostrar una representación más concisa.
4. Interfaz Gráfica (PyQt5)
La interfaz gráfica proporciona una forma interactiva para que el usuario ingrese la gramática y la expresión, elija la dirección de derivación y vea los resultados en una ventana gráfica. Utiliza la librería PyQt5 para crear la interfaz.

El usuario puede ingresar la expresión y elegir la derivación (izquierda o derecha).
El programa muestra tanto el árbol de derivación como el AST en dos ventanas gráficas separadas.
Ejemplo de Uso
Entrada de la expresión: El usuario ingresa una expresión como 5 * (3 + 2).
Selección de la dirección de derivación: El usuario elige si la derivación debe ser izquierda o derecha.
Resultado:
El Árbol de Derivación se genera y muestra gráficamente.
El Árbol Sintáctico Abstracto (AST) también se genera y muestra en una ventana gráfica separada.
Ejemplo de Entrada/Salida
Entrada:
Ingrese la expresión a derivar: 5 * (3 + 2)
Seleccione la derivación (i para izquierda, d para derecha): i

