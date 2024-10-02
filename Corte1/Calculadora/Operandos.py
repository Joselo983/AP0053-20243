class Operandos:
    def __init__(self):
        self.num1 = 0
        self.num2 = 0

    def ingresar_operandos(self):
        try:
            self.num1 = float(input("Ingrese el primer número: "))
            self.num2 = float(input("Ingrese el segundo número: "))
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            self.ingresar_operandos()