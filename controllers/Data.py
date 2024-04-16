from models.Generaciones import Generaciones
from models.Producto import Producto
from models.Presupuesto import Presupuesto
from models.Grafica import Grafica
from models.GraficaStock import GraficaStock
import base64


def organize_products_by_category(productos):
    categorias = {}
    for nombre, detalles in productos.items():
        categoria = detalles['categoria']
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append({
            'nombre': nombre,
            **detalles
        })
    return categorias

def init(req : object):
    
    productos_dispensables = [Producto(**producto) for producto in req['productos_dispensables']]
    productos_indispensables = [Producto(**producto) for producto in req['productos_indispensables']]
    duracion = int(req['duracion'])
    monto = float(req['monto'])
    intervalo = int(req['Intervalo'])
    categorias = req['categorias']
    pob_init = int(req['poblacion_inicial'])
    tamanio = int(req['size'])
    prob_m = float(req['prob_mutacion'])
    prob_c = float(req['prob_cruza'])
    num_generaciones = int(req['num_generaciones'])
    
    veces = int(duracion/intervalo)
    montos: list[float]= [monto for _ in range(veces)]
    
    generaciones = Generaciones(montos, productos_dispensables, productos_indispensables, duracion, tamanio, prob_m, prob_c, num_generaciones, pob_init)
    producto_cantidad_precio, mejor_individuo, historial_mejores, historial_promedios, historial_peores= generaciones.ejecutar_algoritmo_genetico()
    
    response = {'mejor presupuesto': producto_cantidad_precio, 'total': mejor_individuo.calcular_total(), 
                'presupuesto': sum(montos), 'ahorro': sum(montos) - mejor_individuo.calcular_total(), 
                "categorias": categorias}
    
    x_mejor = [individuo.fitness for individuo in historial_mejores]
        
    x_peor = [individuo.fitness if individuo.fitness != 0 else 0 for individuo in historial_peores]
    
    x_promedio = [fitness for fitness in historial_promedios]
    
        
    datos = [
        ([i + 1 for i in range(len(x_mejor))], sorted(x_mejor)),
        ([i + 1 for i in range(len(x_promedio))], sorted(x_promedio)),
        ([i + 1 for i in range(len(x_peor))], sorted(x_peor))
    ]
    path = "assets/grafica.png"
    Grafica(datos, path)
    productos_por_categoria = organize_products_by_category(response['mejor presupuesto'])
    graficador = GraficaStock(productos_por_categoria)
    graficas = {}
    for categoria in productos_por_categoria:
        graficas[categoria] = graficador.generar_grafica_por_categoria(categoria)
        
    response['graficas'] = {cat: f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}" for cat, buf in graficas.items()}

    
    return response
    