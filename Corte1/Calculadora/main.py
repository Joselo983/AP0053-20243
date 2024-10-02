from Menu import Menu
from Operandos import Operandos
from Suma import Suma
from Resta import Resta
from Multiplicacion import Multiplicacion
from Division import Division


class Main:
    def __init__(self):
        #
        print("Inicializando la calculadora...")
        self.operacion = None
        self.operandos = Operandos()  
        self.menu = Menu()           
        print("Inicialización completada")

    def ejecutar(self):
        while True:
            self.menu.mostrar()
            opcion = input("Seleccione una opción (1-5): ")

            if opcion == '1':
                self.operacion = Suma()
            elif opcion == '2':
                self.operacion = Resta()
            elif opcion == '3':
                self.operacion = Multiplicacion()
            elif opcion == '4':
                self.operacion = Division()
            elif opcion == '5':
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida, intente de nuevo.")
                continue

            self.operandos.ingresar_operandos()
            resultado = self.operacion.operar(self.operandos.num1, self.operandos.num2)
            print(f"El resultado es: {resultado}")


if __name__ == "__main__":
    calculadora = Main()
    calculadora.ejecutar()
