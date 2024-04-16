import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import io

class GraficaStock:
    def __init__(self, productos_por_categoria):
        self.productos_por_categoria = productos_por_categoria

    def generar_grafica_por_categoria(self, categoria):
        plt.figure(figsize=(10, 5))
        for producto in self.productos_por_categoria[categoria]:
            fechas = []
            cantidades = []
            for stock in producto['stok']:
                fecha_inicial = datetime.strptime(stock['fecha_inicial'], "%d/%m/%Y")
                fecha_final = datetime.strptime(stock['fecha_final'], "%d/%m/%Y")
                fechas.extend([fecha_inicial, fecha_final])
                cantidades.extend([stock['cantidad_inicial'], 0])
            plt.plot(fechas, cantidades, marker='o', label=producto['nombre'])

        plt.title(f"Stock de {categoria}")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad en Stock")
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf


