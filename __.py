import random
from models.Producto import Producto
from models.Presupuesto import Presupuesto

class Generaciones:
    def __init__(self, monto: float, productos_disponibles: list[Producto], productos_indispensables: list[Producto]):
        self.productos_disponibles = productos_disponibles
        self.productos_indispensables = productos_indispensables
        self.tamano_poblacion = 100
        self.probabilidad_mutacion = 0.1
        self.probabilidad_cruza = 0.5
        self.num_generaciones = 50
        self.monto_objetivo: float = monto

    def generar_individuo(self):
        individuo = []
        presupuesto_restante = self.monto_objetivo
        # Incluir productos indispensables
        for producto in self.productos_indispensables:
            if presupuesto_restante - producto.precio >= 0:
                individuo.append(producto)
                presupuesto_restante -= producto.precio
        # Generar otros productos aleatorios
        while presupuesto_restante > 0:
            producto = random.choice(self.productos_disponibles)
            if presupuesto_restante - producto.precio >= 0:
                individuo.append(producto)
                presupuesto_restante -= producto.precio
            else:
                break
        return Presupuesto(self.monto_objetivo - presupuesto_restante, individuo)

    def evaluar_aptitud(self, individuo: Presupuesto):
        monto_total = individuo.calcular_total()
        if monto_total > self.monto_objetivo:
            return 0
        cantidad_productos = len(individuo.productos)
        diferencia_monto = abs(monto_total - self.monto_objetivo)
        # Ajustar la evaluación para reflejar la prioridad de los productos indispensables
        peso_productos_indispensables = sum(producto.precio for producto in self.productos_indispensables)
        for producto in individuo.productos:
            if producto in self.productos_indispensables:
                diferencia_monto -= producto.precio
        return cantidad_productos + 1 / (diferencia_monto + peso_productos_indispensables + 1)
    

    def cruzar(self, padre1: Presupuesto, padre2: Presupuesto):
        if random.random() < self.probabilidad_cruza:
            punto_corte = random.randint(1, min(len(padre1.productos), len(padre2.productos)) - 1)
            hijo1 = Presupuesto(monto=padre1.monto, productos=padre1.productos[:punto_corte] + padre2.productos[punto_corte:])
            hijo2 = Presupuesto(monto=padre2.monto, productos=padre2.productos[:punto_corte] + padre1.productos[punto_corte:])
            return hijo1, hijo2
        else:
            return padre1, padre2

    def mutar(self, individuo: Presupuesto):
        nuevo_individuo = individuo
        indice_mutacion = random.randint(0, len(individuo.productos) - 1)
        nuevo_producto = random.choice(self.productos_disponibles)
        nuevo_individuo.productos[indice_mutacion] = nuevo_producto

        if nuevo_individuo.calcular_total() > self.monto_objetivo:
            nuevo_individuo.productos.pop(indice_mutacion)
        
        return nuevo_individuo

    def ejecutar_algoritmo_genetico(self):
        poblacion = [self.generar_individuo() for _ in range(self.tamano_poblacion)]

        for _ in range(self.num_generaciones):
            padres = random.choices(poblacion, k=self.tamano_poblacion)
            descendencia = [self.cruzar(padres[i], padres[i+1]) for i in range(0, self.tamano_poblacion, 2)]
            descendencia = [hijo for sublist in descendencia for hijo in sublist]
            for i in range(len(descendencia)):
                if random.random() < self.probabilidad_mutacion:
                    descendencia[i] = self.mutar(descendencia[i])
            poblacion = descendencia

        poblacion = [individuo for individuo in poblacion if individuo.calcular_total() <= self.monto_objetivo]
        mejor_individuo = max(poblacion, key=self.evaluar_aptitud)

        producto_cantidad_precio = {}
        for producto in mejor_individuo.productos:
            if producto.producto in producto_cantidad_precio:
                producto_cantidad_precio[producto.producto]["cantidad"] += producto.cantidad
            else:
                producto_cantidad_precio[producto.producto] = {"cantidad": producto.cantidad, "precio_individual": producto.precio, "categoria": producto.categoria}

        return producto_cantidad_precio, mejor_individuo

productos_disponibles = [
    Producto("leche", 20, 1, "lacteos", "2024-04-11"),
    Producto("pan", 10, 1, "panaderia", "2024-04-11"),
    Producto("1/2 Cono de Huevo", 30, 1, "huevos", "2024-04-11"),
    Producto("1/2 Tortilla", 11, 1, "tortillas", "2024-04-11"),
    Producto("Garrafón de agua", 35, 1, "bebidas", "2024-04-11"),
]

productos_indispensables = [
    Producto("leche", 20, 1, "lacteos", "2024-04-11"),
    Producto("pan", 10, 1, "panaderia", "2024-04-11")
]

monto = 750
generador = Generaciones(monto, productos_disponibles, productos_indispensables)
producto_cantidad_precio, mejor_individuo = generador.ejecutar_algoritmo_genetico()

print("Mejor presupuesto para la semana:")
total_productos = 0
for producto, info in producto_cantidad_precio.items():
    precio_total = info["cantidad"] * info["precio_individual"]
    print(f"{producto} ({info['categoria']}): ${precio_total} (precio individual: ${info['precio_individual']}, cantidad: {info['cantidad']})")
    total_productos += info["cantidad"]

print("Total de productos comprados:", total_productos)
total_gastos = mejor_individuo.calcular_total()
print("Total gastado:", total_gastos)
print("Monto inical", monto)
print("Usted ahorro", monto - total_gastos)
