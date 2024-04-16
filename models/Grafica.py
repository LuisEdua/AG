import matplotlib.pyplot as plt

class Grafica:
    def __init__(self, datos: list[list[float]], path):
        self.datos: list[list[float]] = datos     
        self.path : str = path
        
        self.generar()

    def generar(self):
        
        for i, (x, y) in enumerate(self.datos):
            if((i+1) == 1):
                plt.plot(x, y, label=f'Mejores Individuos', color="#27A243")                
            if((i+1) == 2):
                plt.plot(x, y, label=f'Promedio Individuos', color="#FF8408")
            if((i+1) == 3):
                plt.plot(x, y, label=f'Peores Individuos', color="#FF0808")
                

        plt.xlabel("Generaciones")
        plt.ylabel("Fitnez")
        plt.title("Gráfico de Líneas")
        
        plt.legend()

        plt.savefig(self.path)

        plt.close()

