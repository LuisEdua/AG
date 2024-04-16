from models.Presupuesto import Presupuesto
from models.Producto import Producto
import random
import numpy as np

class Generaciones:
    def __init__(self, monto: list[float], productos_dispensables: list[Producto], productos_indispensables: list[Producto], duracion: int, tamanio: int, prob_mutacion: float, prob_cruza: float, num_generaciones: int, pob_init):
        self.productos_dispensables = productos_dispensables
        self.productos_indispensables = productos_indispensables
        self.poblacion_inicial = pob_init
        self.tamano_poblacion = tamanio
        self.probabilidad_mutacion = prob_mutacion
        self.probabilidad_cruza = prob_cruza
        self.num_generaciones = num_generaciones
        self.monto_objetivo: float = sum(monto)
        self.duracion_presupuesto: int = duracion
        self.historial_mejores = []
        self.historial_promedios = []
        self.historial_peores = []

    def generar_individuo(self):
        individuo = []
        presupuesto_restante = self.monto_objetivo
        for producto in self.productos_indispensables:
            if presupuesto_restante - producto.precio >= 0:
                individuo.append(producto)
                presupuesto_restante -= producto.precio
        while presupuesto_restante > 0:
            producto = random.choice(self.productos_dispensables)
            if presupuesto_restante - producto.precio >= 0:
                individuo.append(producto)
                presupuesto_restante -= producto.precio
            else:
                break
        return Presupuesto(self.monto_objetivo - presupuesto_restante, individuo, self.duracion_presupuesto)
    
    def cruzar(self, padre1: Presupuesto, padre2: Presupuesto):
        if random.random() < self.probabilidad_cruza:
            punto_corte = random.randint(1, min(len(padre1.productos), len(padre2.productos)) - 1)
            hijo1 = Presupuesto(monto=padre1.monto, productos=padre1.productos[:punto_corte] + padre2.productos[punto_corte:] , duracion=self.duracion_presupuesto,  )
            hijo2 = Presupuesto(monto=padre2.monto, productos=padre2.productos[:punto_corte] + padre1.productos[punto_corte:], duracion=self.duracion_presupuesto )
            return hijo1, hijo2
        else:
            return padre1, padre2

    def mutar(self, individuo: Presupuesto):
        nuevo_individuo = individuo
        indice_mutacion = random.randint(0, len(individuo.productos) - 1)
        nuevo_producto = random.choice(self.productos_dispensables)
        nuevo_individuo.productos[indice_mutacion] = nuevo_producto

        if nuevo_individuo.calcular_total() > self.monto_objetivo:
            nuevo_individuo.productos.pop(indice_mutacion)
        
        nuevo_individuo.fitness = nuevo_individuo.calcular_fitness()

        
        return nuevo_individuo
    
    def poda(self, poblacion):
        for individuo in poblacion:
            if individuo.calcular_total() > self.monto_objetivo:
                poblacion.remove(individuo)
        if len(poblacion) > self.tamano_poblacion:
            poblacion = poblacion[:self.tamano_poblacion]

    def ejecutar_algoritmo_genetico(self):
        poblacion = [self.generar_individuo() for _ in range(self.poblacion_inicial)]

        for _ in range(self.num_generaciones):
            padres = random.choices(poblacion, k=self.tamano_poblacion)
            descendencia = [self.cruzar(padres[i], padres[i+1]) for i in range(0, self.tamano_poblacion, 2)]
            descendencia = [hijo for sublist in descendencia for hijo in sublist]
            for i in range(len(descendencia)):
                if random.random() < self.probabilidad_mutacion:
                    descendencia[i] = self.mutar(descendencia[i])
            poblacion.extend(descendencia)
            
            poblacion = sorted(poblacion, key=lambda x: x.fitness, reverse=True)
            mejor_individuo = poblacion[0]
            peor_individuo = poblacion[-1]
            promedio_fitness = np.mean([ind.fitness for ind in poblacion])
            self.historial_mejores.append(mejor_individuo)
            self.historial_promedios.append(promedio_fitness)
            self.historial_peores.append(peor_individuo)
            
            self.poda(poblacion)

        poblacion = [individuo for individuo in poblacion if individuo.calcular_total() <= self.monto_objetivo]
        mejor_individuo = max(poblacion, key=lambda x: x.fitness)

        producto_cantidad_precio = {}
        for producto in mejor_individuo.productos:
            if not producto.producto in producto_cantidad_precio:
                producto_cantidad_precio[producto.producto] = {"cantidad": producto.cantidad * len(producto.fechas_compra),
                                                               "cada_compra": producto.cantidad,
                                                               "precio_individual": producto.precio, 
                                                               "categoria": producto.categoria, 
                                                               "fechas_compra":producto.fechas_compra,
                                                               "stok": producto.stock,
                                                               "categoria": producto.categoria}
        
        
        return producto_cantidad_precio, mejor_individuo, self.historial_mejores, self.historial_promedios, self.historial_peores
