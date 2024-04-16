from datetime import datetime, timedelta

class Producto:
    def __init__(self, uuid: str, producto: str, precio: float, cantidad: int, categoria: str, duracion: int, esIndispensable: str, fecha: str):
        self.uuid : str = uuid
        self.producto: str = producto
        self.precio: float = precio
        self.cantidad: int = cantidad
        self.categoria: str = categoria
        self.duracion: int = duracion
        self.esIndispensable: str = esIndispensable
        self.fecha_inicial_compra: datetime = datetime.strptime(fecha[:10], "%Y-%m-%d")
        self.fechas_compra: list[datetime] = []
        self.stock = []

    def __str__(self):
        return f"{self.producto} ${self.precio} cantidad {self.cantidad}, categoría: {self.categoria}, Fecha Inicial de Compra: {self.fecha_inicial_compra.strftime('%Y-%m-%d')}"

    def calcular_proximas_compras(self, duracion_presupuesto: int):
        proximas_compras = []
        stock_local = []
        fecha_actual = self.fecha_inicial_compra
        
        while fecha_actual <= self.fecha_inicial_compra + timedelta(days=duracion_presupuesto):
            proximas_compras.append(fecha_actual.strftime("%d/%m/%Y"))
            stock_local.append({"fecha_inicial": fecha_actual.strftime("%d/%m/%Y"), "cantidad_inicial": self.cantidad, 
                                "fecha_final":(fecha_actual + timedelta(days=self.duracion)).strftime("%d/%m/%Y"), "cantidad_final":0})
            fecha_actual += timedelta(days=self.duracion)
               
        return proximas_compras, stock_local

