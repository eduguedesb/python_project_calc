import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Compacta")
        self.setGeometry(100, 100, 250, 400)  # Ajustando para uma janela mais compacta
        self.initUI()

    def initUI(self):
        # Criação do widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Campo de resultado (visor)
        self.result_field = QLineEdit(self)
        self.result_field.setAlignment(Qt.AlignRight)
        self.result_field.setFixedHeight(40)  # Tamanho do visor
        self.result_field.setFont(QFont('Arial', 16, QFont.Bold))  # Estilo de texto maior e em negrito
        self.result_field.setReadOnly(True)
        self.result_field.setStyleSheet("background-color: #D3D3D3; color: black; border: 2px solid #A9A9A9; padding: 5px;")  # Visor cinza claro com texto preto
        
        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result_field)

        # Layout em grade para os botões
        grid_layout = QGridLayout()

        # Lista dos botões da calculadora
        buttons = [
            ('C', 0, 0), ('(', 0, 1), (')', 0, 2), ('⌫', 0, 3),
            ('√', 1, 0), ('x²', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('x', 2, 3),  # Botão exibe 'x'
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
        ]

        # Criação dos botões e adição ao layout em grade
        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(45, 45)  # Ajustando para botões menores e compactos
            button.setFont(QFont('Arial', 12, QFont.Bold))  # Texto em negrito nos botões
            
            # Definindo cores dos botões de operações, numéricos e de igualdade
            if btn_text in ['÷', 'x', '-', '+']:  # O botão de multiplicação exibe 'x'
                button.setStyleSheet("background-color: #8B0000; color: white; border: 2px solid #B22222;")  # Operações em vermelho escuro com texto branco
            elif btn_text == '=':
                button.setStyleSheet("background-color: #006400; color: white; border: 2px solid #228B22;")  # Botão de igualdade em verde escuro com texto branco
            elif btn_text in ['C', '√', 'x²', '%', '±', '(', ')', '⌫']:
                button.setStyleSheet("background-color: #1E90FF; color: white; border: 2px solid #4682B4;")  # Botões especiais em azul com texto branco
            else:
                button.setStyleSheet("background-color: #A9A9A9; color: black; border: 2px solid #696969;")  # Botões numéricos em cinza com texto preto

            button.clicked.connect(lambda checked, txt=btn_text: self.on_click(txt))
            grid_layout.addWidget(button, row, col)

        # Adicionando o layout de botões ao layout principal
        main_layout.addLayout(grid_layout)

        # Define o layout no widget central
        central_widget.setLayout(main_layout)

        # Estilo da janela principal (fundo preto)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
        """)

    def format_result(self, result):
        """Função para formatar o resultado, removendo o .0 se for um inteiro"""
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    def on_click(self, char):
        if char == 'C':
            self.result_field.clear()
        elif char == '⌫':
            current_text = self.result_field.text()
            self.result_field.setText(current_text[:-1])  # Apaga o último caractere
        elif char == '=':
            try:
                expression = self.result_field.text().replace('÷', '/').replace('x', '*')  # Substituindo 'x' por '*' na expressão
                result = eval(expression)
                self.result_field.setText(str(self.format_result(result)))
            except Exception:
                self.result_field.setText("Erro")
        elif char == '√':
            try:
                current_value = float(self.result_field.text())
                self.result_field.setText(str(self.format_result(math.sqrt(current_value))))
            except Exception:
                self.result_field.setText("Erro")
        elif char == 'x²':
            try:
                current_value = float(self.result_field.text())
                self.result_field.setText(str(self.format_result(current_value ** 2)))
            except Exception:
                self.result_field.setText("Erro")
        elif char == '%':
            try:
                current_value = float(self.result_field.text())
                self.result_field.setText(str(self.format_result(current_value / 100)))
            except Exception:
                self.result_field.setText("Erro")
        elif char == '±':
            current_text = self.result_field.text()
            # Verificar se o último número é negativo ou positivo
            if current_text and current_text[-1].isdigit():
                # Procurar o número mais recente para trocar o sinal
                tokens = list(current_text)
                i = len(tokens) - 1
                # Encontrar o início do número atual
                while i >= 0 and (tokens[i].isdigit() or tokens[i] == '.'):
                    i -= 1
                # Trocar o sinal
                if i >= 0 and tokens[i] == '-':
                    tokens.pop(i)  # Remover o sinal negativo
                else:
                    tokens.insert(i + 1, '-')  # Inserir o sinal negativo
                self.result_field.setText(''.join(tokens))
            else:
                self.result_field.setText(current_text + '-')  # Adicionar sinal negativo se o campo estiver vazio
        else:
            current_text = self.result_field.text()
            if char == 'x':  # Quando o botão 'x' for pressionado
                self.result_field.setText(current_text + '*')  # Mostra '*' no visor
            else:
                self.result_field.setText(current_text + char)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()
    sys.exit(app.exec_())
