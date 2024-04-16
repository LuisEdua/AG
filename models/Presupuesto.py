from models.Producto import Producto

class Presupuesto:
    def __init__(self, monto: float, productos: list[Producto], duracion: int):
        self.monto: float = monto
        self.productos: list[Producto] = productos
        self.duracion: int = duracion
        self.fitness = self.calcular_fitness()
        self.calcular_fechas_compra_productos()

    def calcular_total(self):
        return sum(producto.precio for producto in self.productos)

    def calcular_fechas_compra_productos(self):
        for producto in self.productos:
            producto.fechas_compra, producto.stock = producto.calcular_proximas_compras(self.duracion)
            
    def calcular_fitness(self):
        total = self.calcular_total()
        if total > self.monto:
            return 0
        return len(self.productos) / total       
            