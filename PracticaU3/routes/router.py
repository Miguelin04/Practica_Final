import time
from flask import Blueprint, jsonify, abort , request, render_template, redirect, Flask, flash, url_for
from controller.exception.linkedEmpty import LinkedEmpty
from controller.distancia import Distancia
from controller.casinoControl import CasinoControl
from controller.negocioGrafo import NegocioGrafo
from flask_cors import CORS
from controller.tda.recorrido.dijkstra import Dijkstra
from controller.tda.recorrido.floyd import Floyd

router = Blueprint('router', __name__)
#CORS(api)
cors = CORS(router, resource={
    r"/*":{
        "origins":"*"
    }
})

#GET: PARA PRESENTAR DATOS
#POST: GUARDA DATOS, MODIFICA DATOS Y EL INICIO DE SESION, EVIAR DATOS AL SERVIDOR

@router.route('/') #SON GETS
def home():
    return render_template('templateL.html')

@router.route('/grafo')
def grafo():
    return render_template("d3/grafo.html")

#------------------------------------NEGOCIOS-------------------------------------

#LISTA PERSONAS
@router.route('/casinos')
def lista_negocios():
    nc = CasinoControl()
    return render_template('casino/lista.html', lista=nc.to_dic())


@router.route('/casinos/agregar')
def ver_guardar_negocios():
    return render_template('casino/guardar.html')

@router.route('/casinos/editar/<pos>')
def ver_negocios(pos):
    pd = CasinoControl()
    nene = pd._get(int(pos))
    return render_template("casino/editar.html", data = nene )

@router.route('/casinos/guardar', methods=["POST"])
def guardar_negocios():
    nc = CasinoControl()
    data = request.form
    nc._casino._nombre = data["nombre"]
    nc._casino._direccion = data["direccion"]
    nc._casino._horario = data["horario"]
    nc._casino._longitud = data["longitud"]
    nc._casino._latitud = data["latitud"]
    nc.save   
    return redirect("/casinos", code=302)

@router.route('/casinos/modificar', methods=["POST"])
def modificar_negocios():
    ndc = CasinoControl()
    data = request.form
    pos = data["id"]
    nene = ndc._list().getNode(int(pos) -1)
    if not "nombre" in data.keys():
        abort(400)
    ndc._casino = nene
    ndc._casino._nombre = data["nombre"]
    ndc._casino._direccion = data["direccion"]
    ndc._casino._horario = data["horario"]
    ndc.merge(int(pos) -1)
    return redirect("/casinos", code=302)

@router.route('/casinos/eliminar', methods=["POST"])
def eliminar_negocio():
    ndc = CasinoControl()
    pos = request.form["id"]
    ndc._delete(int(pos) - 1)
    return redirect("/casinos", code=302)

@router.route('/casinos/grafo_negocio')
def grafo_negocio():
    ng = NegocioGrafo()
    ng.create_graph()
    return render_template("d3/grafo.html")

@router.route('/grafo_negocio/ver')
def ver_grafo_negocio():
    return render_template("d3/grafo.html")

@router.route('/casinos/reiniciar')
def reiniciar_grafo():
    ng = NegocioGrafo()
    ng.create_graph(None,None,True)
    return redirect("/casinos/grafo_ver_admin", code=302)

@router.route('/casinos/grafo_ver_admin')
def grafo_ver_admin():
    nc = CasinoControl()
    grafo = NegocioGrafo()._grafo
    arrayNegocios = nc.to_dic()
    distancia_calculador = Distancia()
    # Inicializar matriz de adyacencia
    matriz_ady = [["-----"] * len(arrayNegocios) for _ in range(len(arrayNegocios))]
    for i in range(len(arrayNegocios)):
        for j in range(len(arrayNegocios)):
            if grafo.exist_edge_E(arrayNegocios[i]["nombre"], arrayNegocios[j]["nombre"]):
                lat1, lon1 = float(arrayNegocios[i]["latitud"]), float(arrayNegocios[i]["longitud"])
                lat2, lon2 = float(arrayNegocios[j]["latitud"]), float(arrayNegocios[j]["longitud"])
                distancia = distancia_calculador.haversine(lat1, lon1, lat2, lon2)
                matriz_ady[i][j] = round(distancia, 2)    
    return render_template("casino/grafo.html", lista=nc.to_dic(), matris=matriz_ady)

#crear adyacencias
@router.route('/casinos/crear_ady', methods=["POST"])
def crear_ady():
    nc = CasinoControl()
    grafo = NegocioGrafo()._grafo
    data = request.form
    origen = data["origen"]
    destino = data["destino"]
    OrigenN = nc._list().binary_search_models(origen, "_nombre")
    DestinoN = nc._list().binary_search_models(destino, "_nombre")
    if OrigenN is None or DestinoN is None:
        flash('No se encontraron uno o ambos nodos especificados', 'error')
        return redirect("/casinos/grafo_ver_admin", code=302)
    origen_idx = OrigenN._id - 1
    destino_idx = DestinoN._id - 1
    if origen == destino:
        flash('Seleccione un origen y destino diferente', 'error')
        return redirect("/casinos/grafo_ver_admin", code=302)
    if grafo.exist_edges(origen_idx, destino_idx):
        flash('Ya existe una adyacencia entre estos casinos', 'error')
        return redirect("/casinos/grafo_ver_admin", code=302)
    NegocioGrafo().create_graph(OrigenN, DestinoN)
    return redirect("/casinos/grafo_ver_admin", code=302)

#buscar casinos
@router.route('/casinos/buscar', methods=['GET', 'POST'])
def buscar_negocios():
    if request.method == 'POST':
        ng = CasinoControl()
        data = request.form
        campo = data['select-campo']
        valor = data['input-campo']
        metodo = data['select-metodo']
        mensaje = ''
        negocios = []
        try:
            if metodo == 'binaria':
                negocio = ng._list().binary_search_models(valor, campo, type=1)
                if negocio is not None:
                    negocios.append(negocio)
                else:
                    mensaje = f'No se encontraron negocios para "{valor}" con el método binario'
            elif metodo == 'secuencial':
                negocios = ng._list().binary_models(valor, campo, type=1) 
                if not negocios:
                    mensaje = f'No se encontraron casinos para "{valor}" con el método secuencial'
            else:
                raise ValueError("Método de búsqueda no válido. Debe ser 'binaria' o 'secuencial'.")
        except LinkedEmpty:
            mensaje = f'No se encontraron negocios para "{valor}"'
        except ValueError as e:
            mensaje = str(e)
        return render_template("casino/buscar.html", lista=negocios, mensaje=mensaje)
    else:
        return render_template("casino/buscar.html")

#ordenar casinos
@router.route('/casinos/ordenar')
def ordenar_historial():
    campo_orden = request.args.get('campo', default='_nombre', type=str)
    direccion = request.args.get('direccion', default=1, type=int)
    algoritmo = request.args.get('algoritmo', default=1, type=int)
    ng = CasinoControl()
    lista_ordenada = ng.sort_models(campo_orden, direccion, algoritmo)
    return render_template('casino/ordenar.html', lista=lista_ordenada)

#------------------------------------RUTAS-------------------------------------
@router.route('/casinos/ruta', methods=["POST", "GET"])
def camino_minimo():
    nc = CasinoControl()
    if request.method == "POST":
        data = request.form
        metodo = data.get("metodo")
        origen, destino = data.get("origen"), data.get("destino")
        gf = NegocioGrafo()
        
        if metodo == "dijkstra":
            start = time.time()
            path, distance = gf._grafo.camino_dijkstra(origen, destino)
            metodo_nombre = 'Dijkstra'
            end = time.time()
            print(f"Tiempo de ejecución: {end-start}")
        elif metodo == "floyd":
            inicio = time.time()
            path, distance = gf._grafo.camino_floyd(origen, destino)
            metodo_nombre = 'Floyd-Warshall'
            fin = time.time()
            print(f"Tiempo de ejecución: {fin-inicio}")
        else:
            # Manejar caso en que el método no sea válido
            return "Método no válido", 400
        return render_template('casino/ruta.html', path=path, distance=distance, metodo=metodo_nombre, lista=nc.to_dic())
    else:
        return render_template('casino/ruta.html', lista=nc.to_dic())
 


