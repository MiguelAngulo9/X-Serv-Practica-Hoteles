from django.shortcuts import render
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from models import Hotel, Imagen, Comentario, Hotel_Identificado, Estilo_CSS
from datetime import *
from django.template.loader import get_template
from django.contrib.auth import login, authenticate, logout
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
import urllib2
import sys
import os.path
# Create your views here.
var_global = 10

def parse(idioma):
    analizador = make_parser()
    manejador = myContentHandler()
    analizador.setContentHandler(manejador)
    if idioma =='es':
        fichero_xml = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_es.xml")
    if idioma =='en':
        fichero_xml = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_en.xml")
    if idioma =='fr':
        fichero_xml = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_fr.xml")
    analizador.parse(fichero_xml)
    todos_hoteles = manejador.lista_hoteles()
    return todos_hoteles


def usuario_esta_logueado(request):
    if  request.user.is_authenticated():
        try:
            usuario_logueado = Estilo_CSS.objects.get(usuario = request.user.username)
        except Estilo_CSS.DoesNotExist:
            usuario_logueado = Estilo_CSS(usuario =request.user.username, titulo = "Pagina de " + request.user.username, fuente=12, color_fondo = "#655A46 url(img/bg.gif);")
            usuario_logueado.save()

def pagina_inicio(request):
    global var_global
    var_global = 10
    hoteles = Hotel.objects.all()
    if(len(hoteles) == 0):
        hoteles_lista = {}
        hoteles_lista = parse('es')
        for elemento in hoteles_lista:
            try:
                elemento["subcat"]
            except Exception as e:
                elemento["subcat"] = "Undefined"

            hotel_clase = Hotel(nombre = elemento["name"],direccion = elemento['address'],numero_tlf = elemento['phone'],contenido = elemento['body'],URL = elemento['web'],categoria = elemento['cat'],subcategoria = elemento["subcat"],numero_coment = 0)
            hotel_clase.save()

            hotel_id = hotel_clase.id
            for url in elemento["url"]:
                imagen_clase = Imagen(id_hotel=hotel_id,URL=url)
                imagen_clase.save()

def cambiar_CSS(request):
    if request.user.is_authenticated():
        try:
            pagina = Estilo_CSS.objects.get(usuario = request.user.username)
        except Exception as e:
            return ""

        fondo = pagina.color_fondo
        letra = pagina.fuente
        resultado = "body{background:" + fondo + "}"
        resultado += "*{font-size:" + str(letra) + "px}"
        return resultado
    else:
        return ""

def pagina_about(request):
    global var_global
    var_global = 10
    template = get_template("About.html")
    Context = ({"css":cambiar_CSS(request)})
    Plantilla = template.render(Context)
    return HttpResponse(Plantilla)

@csrf_exempt
def entrar(request):
    global var_global
    var_global = 10
    if request.method == "POST":
        usuario_id = request.POST['Username']
        contrasena = request.POST['Password']
        acceso = authenticate(username = usuario_id, password = contrasena)
        if acceso is not None:
            if acceso.is_active:
                login(request,acceso)
                usuario_esta_logueado(request)
                return HttpResponseRedirect('/' + usuario_id)
            else:
                return HttpResponseNotFound ("ESTE USUARIO NO ESTA ACTIVO")
        else:
            return HttpResponseNotFound ("ESTE USUARIO NO ES VALIDO")

def salir(request):
    global var_global
    var_global = 10
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def formulario_registro(request):
    if not request.user.is_authenticated():
        return '<form method="post" action="/login"><table><td> USERNAME <input type="text"name="Username" Username=""</td>'+\
                     '</tr><td> PASSWORD <input type="password"name="Password" Password=""</td></tr></table><input type="submit" value="Enviar" /></form></br>'
    else:
        return 'Usted se ha registrado como: <a href="/'+ request.user.username +'">' + request.user.username + '</a><br>Para salir pulse aqui: <a href="/logout">logout</a></br>'


def pagina_usuario_xml(request,usuario):
    global var_global
    var_global = 10
    hoteles = Hotel_Identificado.objects.all()
    hoteles = hoteles.filter(usuario = usuario)
    xml = "<?xml version='1.0' encoding='UTF-8' ?>"
    xml += "<data><usuario name='" + usuario +"'>"
    for alojamiento in hoteles:
        hotel = Hotel.objects.get(id = alojamiento.id_hotel)
        xml += "<hotel>"
        xml += "<nombre>" + hotel.nombre + "</nombre>"
        xml += "<address>" + hotel.direccion + "</address>"
        xml += "<phone>" + hotel.numero_tlf + "</phone>"
        xml += "<web>" + hotel.URL + "</web>"
        xml += "<cat>" + hotel.categoria + "</cat>"
        xml += "<subcat>" + hotel.subcategoria + "</subcat></hotel>"

    xml += "</usuario></data>"
    return HttpResponse(xml, content_type="text/xml")

@csrf_exempt
def filtrado_alojamientos():
    return( '<form method="post">FILTRAR POR CATEGORIA O SUBCATEGORIA:  <select name="Filtro">' +
        '<option value="Categoria">CATEGORIA</option> ' +
        '<option value="SubCategoria">SUBCATEGORIA</option> ' +
        '</select><br>INTRODUCIR BUSQUEDA: <input type="text"name="valor" value="" /><button type="submit"> Enviar</button></br></br> </form>')

def pagina_personal_usuarios(request):
    usuarios = Estilo_CSS.objects.all()
    resultado = '<b><u>PAGINAS PERSONALES</u></b></br></br>'
    for usuario in usuarios:
        resultado += '- ' + '<a href="/'+ usuario.usuario +'">' + usuario.usuario + '</a>'
        resultado += ': ' + usuario.titulo + "</br>"
    return resultado

@csrf_exempt
def pagina_todos_alojamientos(request):
    global var_global
    var_global = 10
    hoteles = Hotel.objects.all()

    if request.method == "POST":
        nombre_filtro = request.POST['Filtro']
        valor_filtro =  request.POST['valor']
        if(nombre_filtro == "Categoria"):
            hoteles = hoteles.filter(categoria = valor_filtro)
        else:
            hoteles = hoteles.filter(subcategoria = valor_filtro)

    html = "<p>Se han encontrado " + str(len(hoteles)) + " resultados</p<ul>"

    for alojamiento in hoteles:
        html += "<li><a href='alojamientos/" + str(alojamiento.id) + "'>" + alojamiento.nombre + "</a></li>"
    html += "</ul>"
    template = get_template("Alojamientos_totales.html")
    Context = ({"css":cambiar_CSS(request),"form":filtrado_alojamientos(),"hoteles":html,"form_reg":formulario_registro(request),"datos_usuarios":pagina_personal_usuarios(request)})
    Plantilla = template.render(Context)
    return HttpResponse(Plantilla)

def comentario_hotel(id):
    comentarios = Comentario.objects.all()
    comentarios = comentarios.filter(id_hotel = id)
    resultado = ""
    if(len(comentarios) != 0):
        for comentario in comentarios:
            resultado += "<b>" + comentario.usuario_comentador + ": </b>"
            resultado +=  "  " + comentario.contenido
            resultado +=  "<p>" + str(comentario.fecha) + "</p>"

    else:
        return ("<p> ESTE HOTEL NO TIENE NINGUN COMENTARIO </p>")
    return resultado

@csrf_exempt
def seleccion_idioma(request,id):
    if request.user.is_authenticated():
        valor = '<form method="POST" action=/alojamientos/' + str(id) + '><button type="submit" value="EN" name="EN">Ingles</button>'
        valor += '<button type="submit" value="FR" name="FR">Frances</button>'
        valor += '<button type="submit" value="ADD" name="ADD">Incorporar a mis hoteles destacados</button></form>'
        return valor
    else:
        return ""

@csrf_exempt
def formulario_comentario(request,identificador):

    if request.user.is_authenticated():
         return ('<form  method="post" action="/poner_comentario/' + str(identificador) + '">Poner un comentario: <input type="text"name="coment" coment=""/><input type="submit" value="Enviar" /></form>')
    else:
        return ""

@csrf_exempt
def poner_comentario(request,id):
    global var_global
    var_global = 10
    YaComentado = 0
    alojamiento = Hotel.objects.get(id = id)
    if (request.method == "POST"):
        comentarios = Comentario.objects.all()
        comentarios = comentarios.filter(usuario_comentador = request.user.username, id_hotel = alojamiento.id)
        for comentario in comentarios:
            YaComentado = 1
        if YaComentado == 0:
            comentario_subido = request.POST['coment']
            if len(request.POST['coment']) != 0:
                comentario_clase = Comentario(usuario_comentador=request.user.username, contenido=comentario_subido, id_hotel=alojamiento.id, fecha=datetime.now())
                comentario_clase.save()
                alojamiento.numero_coment = alojamiento.numero_coment + 1
                alojamiento.save()

        return HttpResponseRedirect('/alojamientos/' + str(alojamiento.id))

@csrf_exempt
def pagina_alojamiento_id(request,id):
    global var_global
    var_global = 10
    resultado = ""
    alojamiento = Hotel.objects.get(id = id)
    encontrado = 0
    if (request.method == "POST"):
        try:
            request.POST["ADD"]
        except Exception as e:
            try:
                request.POST["EN"]
            except Exception as e:
                hoteles_lista = parse("fr")

            try:
                request.POST["FR"]
            except Exception as e:
                hoteles_lista = parse("en")

            for elemento in hoteles_lista:
                if(elemento["name"] == alojamiento.nombre):
                    resultado += "<h3>" + elemento["name"] + "</h3>"
                    resultado += "<ul><li>" + elemento["address"] + elemento["phone"] + "</li>"
                    resultado += "<li>" + elemento["cat"] + elemento["subcat"] + "</li>"
                    resultado += "<li>" + elemento["web"] + "</li>"
                    if len(elemento["body"]) != 0:
                        resultado += "<li>" + elemento["body"] + "</li></ul>"
                    encontrado = 1
                    break
        else:
            encontrado = 1
            hotel = Hotel_Identificado(id_hotel = alojamiento.id, usuario = request.user.username, fecha = datetime.now())
            hotel.save()

        if encontrado == 0:
            resultado += "<h3> EL HOTEL NO ESTA DISPONIBLE PARA EL IDIOMA SELECCIONADO </h3></br></br>"

    resultado += "<h3>" + alojamiento.nombre + "</h3>"
    resultado += "<ul><li>" + alojamiento.direccion + alojamiento.numero_tlf + "</li>"
    resultado += "<li>" + alojamiento.categoria + alojamiento.subcategoria + "</li>"
    resultado += "<li>" + alojamiento.URL + "</li>"

    if len(alojamiento.contenido) != 0:
        resultado += "<li>" + alojamiento.contenido + "</li></ul>"

    imagen = Imagen.objects.all()
    imagen = imagen.filter(id_hotel=alojamiento.id)
    for foto in imagen:
        resultado += "<img class='imagenes' src='" + foto.URL + "'>"

    template = get_template("Alojamientos_id.html")
    Context = ({"css":cambiar_CSS(request),"idiomas":seleccion_idioma(request,alojamiento.id),"form":formulario_comentario(request,alojamiento.id),"form_reg":formulario_registro(request),"hoteles":resultado,"datos_usuarios":pagina_personal_usuarios(request),"nombre":alojamiento.nombre,"comentarios":comentario_hotel(alojamiento.id)})
    Plantilla = template.render(Context)
    return HttpResponse(Plantilla)

@csrf_exempt
def hoteles_seleccionados(request, usuario):
    global var_global
    if request.method == "POST":
        var_global += 10

    hoteles = Hotel_Identificado.objects.all()
    resultado = "<ul>"
    contador = 0
    hoteles = hoteles.filter(usuario = usuario)
    if(len(hoteles) == 0):
        return ("<p>El usuario no ha agregado ningun hotel</p>")

    for hotel in hoteles:
        imagen = Imagen.objects.all()
        imagen = imagen.filter(id_hotel=hotel.id_hotel)
        alojamiento = Hotel.objects.get(id=hotel.id_hotel)
        resultado += "<li><b>" +  alojamiento.nombre + " </b>Direccion: " + alojamiento.direccion
        if (len(imagen) != 0):
            resultado += "<img class='imagenes' src='" + imagen[0].URL + "'></br>"
        resultado +=  "Fecha de seleccion: " + str(hotel.fecha) + "<a href='alojamientos/" + str(alojamiento.id) + "'> Mas informacion...</br></br></br></a></li>"

        contador += 1
        if(contador == var_global):
            resultado += "</ul>"
            break

    if(len(hoteles) > var_global):
        resultado += '<form method="post"  action=/' + usuario + '>' + '<button type="submit" > Siguiente</button></form>'

    return resultado

@csrf_exempt
def datos_usuario(request):
    global var_global
    var_global = 10
    nombre_usuario = request.user.username
    usuario = Estilo_CSS.objects.get(usuario = nombre_usuario)

    if len(request.POST['titulo']) != 0:
        usuario.titulo = request.POST['titulo']
    if len(request.POST['fondo']) != 0:
        usuario.color_fondo = request.POST['fondo']
    if len(request.POST['letra']) != 0:
        usuario.fuente = request.POST['letra']
    usuario.save()
    return HttpResponseRedirect('/' + nombre_usuario)

@csrf_exempt
def pagina_usuario(request,usuario):
    if request.method == "GET":
        global var_global
        var_global = 10

    formulario1 = ""
    formulario2 = ""
    if(request.user.is_authenticated() and usuario == request.user.username):
        formulario1 = ' <form method="post" action="/datos_usuario"><table>'
        formulario1 += 'Titulo de la pagina:<input type="text"name="titulo" titulo=""'
        formulario2 = ' <form method="post" action="/formulario2"><table>Color de fondo:'
        formulario2 += '<input type="text"name="fondo" fondo=""></br>'
        formulario2 += 'Tamano de la letra:<input type="text"name="letra" letra=""></br><input type="submit" value="Enviar"/></form></br></br></br>'


    contenido = Estilo_CSS.objects.get(usuario=usuario)
    template = get_template("Usuario_id.html")
    Context = ({"css":cambiar_CSS(request),"form":formulario1,"formcss":formulario2,"titulo":contenido.titulo,"hoteles":hoteles_seleccionados(request,usuario),"form_reg":formulario_registro(request),"datos_usuarios":pagina_personal_usuarios(request)})
    Plantilla = template.render(Context)
    return HttpResponse(Plantilla)

def  hoteles_mas_comentados():
    resultado = "<ul>"
    contador = 0

    hoteles = Hotel.objects.all()
    hoteles = hoteles.order_by("-numero_coment")

    for alojamiento in hoteles:
        if(alojamiento.numero_coment > 0):
            imagen = Imagen.objects.all()
            imagen = imagen.filter(id_hotel=alojamiento.id)
            resultado += "<li><a href='" + alojamiento.URL + "'>" + alojamiento.nombre + "</a> + Direccion: " + alojamiento.direccion
            if (len(imagen) > 0):
                resultado += "<img class='imagenes' src='" + imagen[0].URL + "'>"
            resultado += "<a href='alojamientos/" + str(alojamiento.id) + "'> Mas informacion...</br></br></br></a></li>"
            contador += 1
            if(contador == 10):
                resultado += "</ul>"
                return resultado
        else:
            continue
    return resultado

def pagina_principal(request):
    global var_global
    var_global = 10
    pagina_inicio(request)
    template = get_template("Index.html")
    Context = ({"css":cambiar_CSS(request),"form_reg":formulario_registro(request),"hotelesHome":hoteles_mas_comentados(),"datos_usuarios":pagina_personal_usuarios(request)})
    Plantilla = template.render(Context)
    return HttpResponse(Plantilla)
