#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import Actividad, Usuario, UltimaFecha, EstiloCss
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from xmlparser import getNoticias
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
import urllib2


# Create your views here.

def login():
    salida = '<form action="" method="POST">'
    salida += 'Nombre de usuario<br><input type="text" name="Usuario"><br>'
    salida += 'Password<br><input type="password" name="Password">'
    salida += '<br><input type="submit" value="Entrar"> o '
    salida += '<a href="/registrarse">Registrate</a>'
    salida += '</form>'
    return salida

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def pie():
    salida = 'Copyright © 2015 Adrian Oter'
    return salida

def usuario_nuevo(request):
    log = '<form action="" method="POST">'
    log += 'Nombre de usuario<br><input type="text" name="Usuario"><br>'
    log += 'Password<br><input type="password" name="Password">'
    log += '<br><input type="submit" value="Registrarme">'
    log += '</form>'
    inicio = '<a href="/">Inicio</a>'
    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        lista = User.objects.all()
        for fila in lista:
            if fila.username == usuario:
                error = ""
                error += '<span>Error.</span><br>'
                error += 'El nombre de usuario ya esta usado. Pruebe otro.'
                plantilla = get_template('template2.html')
                c = Context({'loggin': log, 'inicio': inicio, 'error': error})
                renderizado = plantilla.render(c)
                return HttpResponse(renderizado)
        
        user = User.objects.create_user(usuario, usuario + '@ejemplo.com', password)
        user.save()
        user = Usuario(nombre=usuario)
        user.save()
        estilo_pagina = EstiloCss(usuario=usuario, banner='imagenes/alcala.png', login="", menu="red", pie="red")
        estilo_pagina.save()
        return HttpResponseRedirect('/')
    plantilla = get_template('template2.html')
    c = Context({'loggin': log, 'inicio': inicio,})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
        

def pagina_principal(request):

    cuerpo = ""
    log = ""
    titulo = u"Actividades más próximas"
    error = ""  
    personales = u"<br>Páginas personales"
    cuerpo_personales = ""
    rss = ""
    rss += '<a href="/principal/rss"><img id="destacado" src="/css/imagenes/rss.png"></img></a>'
    rss += '<a href="/principal/rss">Rss de la pagina principal</a>'

    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()

    fecha_actual = datetime.datetime.today()
    fecha_final = datetime.date(2020, 12, 31)
    hora_actual = datetime.datetime.now() + datetime.timedelta(hours=2)
    hora_final = datetime.time(23, 59, 00)
    actividades = Actividad.objects.filter(fecha__range=(fecha_actual, fecha_final))
    actividades = actividades.filter(hora__range=(hora_actual, hora_final)).order_by('fecha', 'hora')[0:10]
    for fila in actividades:
        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a><ul><li>' + 'Fecha: ' + str(fila.fecha) + ', Hora: ' + str(fila.hora) + '</li></ul></li></ul>'

    usuarios = Usuario.objects.all()
    for user in usuarios:
        if len(user.actividades.values()) == 0:
            pass
        else:
            titulo_user = user.titulo_personal
            if titulo_user == "":
                titulo_user = u'Página de ' + user.nombre
            cuerpo_personales += '<ul><li><a href="' + user.nombre + '">' + titulo_user 
            cuerpo_personales += '</a><ul><li>Usuario: ' + user.nombre + '</li></ul></li></ul>'

    #Logearse en la pagina principal
    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            error += '<span>Error.</span> Datos incorrectos<br>'
            plantilla = get_template('template.html')
            c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error,'personales': personales, 'cuerpo_personales': cuerpo_personales, 'pie': pie(), 'rss': rss})
            renderizado = plantilla.render(c)
            return HttpResponse(renderizado)

    plantilla = get_template('template.html')
    c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'personales': personales, 'cuerpo_personales': cuerpo_personales, 'pie': pie(), 'rss': rss})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)

def actividades_id(request, recurso):
    actividad = Actividad.objects.get(id=recurso)
    cuerpo = ""
    log = ""
    error = ""
    inicio = '<a href="/">Inicio</a>'
    titulo = actividad.titulo
    cuerpo += '<ul><li>Tipo de evento: ' + actividad.tipo + '<br></li>'
    cuerpo += '<li>Precio: ' + actividad.precio + '</li>'
    cuerpo += '<li>Fecha: ' + str(actividad.fecha) + ', Hora: ' + str(actividad.hora) + '</li>'
    cuerpo += u'<li>Evento de larga duración: ' + actividad.larga_duracion + '</li>'
    if actividad.url == 'No disponible':
         cuerpo += u'<li>Información adicional: No disponible</li></ul>'
    else:
        cuerpo += u'<li>Información adicional: <a href=http://www.madrid.es' + actividad.url + '>Pinche aqui</a></li></ul>'
    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()

     #Logearse en la pagina de alguna actividad
    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/actividades/" + str(recurso))
        else:
            error += '<span>Error.</span> Datos incorrectos<br>'
            plantilla = get_template('template.html')
            c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'pie': pie()})
            renderizado = plantilla.render(c)
            return HttpResponse(renderizado)

    plantilla = get_template('template.html')
    c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'inicio': inicio, 'pie': pie()})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)

def todas(request):
    titulo = "Todas las actividades disponibles"
    cuerpo = ""
    log = ""
    error = ""
    actualizar = ""
    inicio = '<a href="/">Inicio</a>'
    busqueda = ""
    busqueda += '<label><strong>Busqueda</strong></label> <br/>'
    busqueda += '<form action="" method="POST">'
    busqueda += '<select name="buscar"><option value="" selected="selected">- selecciona -</option>'
    busqueda += '<option value="fecha">Por fecha</option>'
    busqueda += u'<option value="titulo">Por título</option>'
    busqueda += '<option value="precio">Por precio</option></select>'
    busqueda += '<br><input type="submit" value="Buscar">'
    busqueda += '</form>'
    actividades = Actividad.objects.all()

    if request.user.is_authenticated():
        actualizar += '<label><strong>Actualizar Actividades</strong></label>'
        actualizar += '<form action="" method="POST" >'
        actualizar += '<input type="submit" name="update" value="Actualizar">'
        actualizar += '</form>'
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'
        fecha = UltimaFecha.objects.all()[0]
        cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
        cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
        for fila in actividades:
            cuerpo += '<form action="" method="POST" >'
            cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
            cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
            cuerpo += '</li></ul>' 
        cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
    else:
        log += login()
        for fila in actividades:
            cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'
 
    if request.method == 'POST':
        cuerpo = ""
        datos = request.body
        name = datos.split('=')[0]

        if name == 'seleccion':
            #Solo seleccionamos 1
            if datos.find('&') == -1:
                num = datos.split('=')[1]
                fecha_actual = datetime.datetime.now() + datetime.timedelta(hours=2) 
                actividad = Actividad.objects.get(id=num)
                actividad.fecha_seleccion = fecha_actual
                actividad.save()
                usuario = Usuario.objects.get(nombre=request.user.username)
                usuario.actividades.add(actividad)
                cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                for fila in actividades:
                    cuerpo += '<form action="" method="POST" >'
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                    cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                    cuerpo += '</li></ul>' 
                cuerpo  += '<center><input type="submit" value="Elegir"></center></form>'
            #Seleccionamos varias actividades
            else:
                datos = datos.split('&')
                aux = 0
                while (aux < len(datos)):
                    datos[aux] = datos[aux].split('=')[1]
                    aux = aux + 1
                aux = 0
                while (aux < len(datos)):
                    fecha_actual = datetime.datetime.now() + datetime.timedelta(hours=2)
                    actividad = Actividad.objects.get(id=datos[aux])
                    actividad.fecha_seleccion = fecha_actual
                    actividad.save()
                    usuario = Usuario.objects.get(nombre=request.user.username)
                    usuario.actividades.add(actividad)
                    aux = aux + 1

                cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                for fila in actividades:
                    cuerpo += '<form action="" method="POST" >'
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                    cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                    cuerpo += '</li></ul>' 
                cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
            
                
        elif name == "buscar":
            if request.POST['buscar'] == 'fecha':
                actividades = actividades.order_by('fecha')
                if request.user.is_authenticated():
                    fecha = UltimaFecha.objects.all()[0]
                    cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                    cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '<ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul>'
                        cuerpo += '</li></ul>' 
                    cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">'
                        cuerpo += fila.titulo + '</a><ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul></li></ul>'

                    
            elif request.POST['buscar'] == 'precio':
                actividades = actividades.order_by('precio')
                if request.user.is_authenticated():
                    fecha = UltimaFecha.objects.all()[0]
                    cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                    cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '<ul><li>' + 'Precio: ' + fila.precio + '</li></ul>'
                        cuerpo += '</li></ul>' 
                    cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' 
                        cuerpo += fila.titulo + '</a><ul><li>' + 'Precio: ' + fila.precio + '</li></ul></li></ul>'


            elif request.POST['buscar'] == 'titulo':
                actividades = actividades.order_by('titulo')
                if request.user.is_authenticated():
                    fecha = UltimaFecha.objects.all()[0]
                    cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                    cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '</li></ul>' 
                    cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">'
                        cuerpo += fila.titulo + '</a></li></ul>'
            elif request.POST['buscar'] == "":
                 for fila in actividades:
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'


        elif name == 'update':
            if request.POST['update'] == 'Actualizar':
                actializacion = getNoticias()
                ultima_fecha = UltimaFecha.objects.all()
                ultima_fecha.delete()
                fecha_actualizacion = datetime.datetime.now() + datetime.timedelta(hours=2)
                ultima_fecha = UltimaFecha(fecha=fecha_actualizacion)
                ultima_fecha.save()
                actividades = Actividad.objects.all()
                if request.user.is_authenticated():
                    fecha = UltimaFecha.objects.all()[0]
                    cuerpo += str(actividades.count()) + ' actividades disponibles<br>'
                    cuerpo += u'Última fecha de actualización: ' + str(fecha.fecha).split('.')[0]
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '</li></ul>' 
                    cuerpo  += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'
        #Si se logea
        else:
            for fila in actividades:
                cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'
            usuario = request.POST['Usuario']
            password = request.POST['Password']
            user = auth.authenticate(username=usuario, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/todas")
            else:
                error += '<span>Error.</span> Datos incorrectos<br>'
                plantilla = get_template('template.html')
                c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'actualizar': actualizar, 'error': error, 'pie': pie()})
                renderizado = plantilla.render(c)
                return HttpResponse(renderizado)

        plantilla = get_template('template.html')
        c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'actualizar': actualizar, 'pie': pie()})
        renderizado = plantilla.render(c)
        return HttpResponse(renderizado)
    
    plantilla = get_template('template.html')
    c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'actualizar':actualizar, 'pie': pie()})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)


def pagina_usuario(request, recurso):
    cuerpo = ""
    usuario = Usuario.objects.get(nombre=recurso)
    titulo = usuario.titulo_personal
    log = ""
    error = ""
    cambio_titulo = ""
    cambio_estilo = ""
    rss = ""
    inicio = '<a href="/">Inicio</a>'
    rss += '<a href="/' + recurso + '/rss"><img id="destacado" src="/css/imagenes/rss.png"></img></a>'
    rss += '<a href="/' + recurso + '/rss">Rss del usuario</a>'

    if titulo == "":
        titulo = u'Página de ' + usuario.nombre
    try:
        actividades_selecc = usuario.actividades.all()
        actividades_selecc = actividades_selecc.values()
        aux = 0
        while (aux < len(actividades_selecc)):
            num = actividades_selecc[aux]['id']
            titulo_actividad = actividades_selecc[aux]['titulo']
            fecha = actividades_selecc[aux]['fecha']
            hora = actividades_selecc[aux]['hora']
            cuerpo += '<ul><li><a href="/actividades/' + str(num) + '">' + titulo_actividad
            cuerpo += '</a><ul><li>' + 'Fecha: ' + str(fecha) + ', Hora: ' + str(hora) + '</li></ul></li></ul>'
            aux = aux + 1
    except ObjectDoesNotExist:
        return HttpResponse('No')

    if request.user.is_authenticated():
        pagina_estilo = EstiloCss.objects.get(usuario=recurso)
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'


        if recurso == request.user.username:
            cambio_titulo += '<form action="" method="POST">'
            cambio_titulo += u'<strong>Cambiar título</strong><br><input type="text" name="Titulo">'
            cambio_titulo += '<input type="submit" value="Cambiar">'
            cambio_titulo += '</form>' 

            cambio_estilo += '<strong>Cambiar estilo</strong>:'
            cambio_estilo += '<form action="" method="POST">'
            cambio_estilo += '<label>Banner  </label>'
            cambio_estilo += '<select name="banner"><option value="" selected="selected">- selecciona -</option>'
            cambio_estilo += '<option value="defecto">Alcala</option>'
            cambio_estilo += '<option value="real">Real Madrid</option>'
            cambio_estilo += '<option value="retiro">El Retiro</option></select>'
            cambio_estilo += '<br><label>Menu  </label>'
            cambio_estilo += '<select name="menu"><option value="" selected="selected">- selecciona -</option>'
            cambio_estilo += '<option value="defecto">Rojo</option>'
            cambio_estilo += '<option value="verde">Verde</option>'
            cambio_estilo += '<option value="azul">Azul</option></select>'
            cambio_estilo += '<br><label>Login  </label>'
            cambio_estilo += '<select name="login"><option value="" selected="selected">- selecciona -</option>'
            cambio_estilo += '<option value="defecto">Sin color</option>'
            cambio_estilo += '<option value="verde">Verde</option>'
            cambio_estilo += '<option value="azul">Azul</option></select>'
            cambio_estilo += '<br><label>Pie  </label>'  
            cambio_estilo += '<select name="pie"><option value="" selected="selected">- selecciona -</option>'
            cambio_estilo += '<option value="defecto">Rojo</option>'      
            cambio_estilo += '<option value="azul">Azul</option>'
            cambio_estilo += '<option value="verde">Verde</option></select>'
            cambio_estilo += '<br><center><input type="submit" value="Aplicar"></center>'
            cambio_estilo += '</form>'

            if request.method == 'POST':

                #Cambiar estilo

                if request.body.find('banner') == 0:
                    name = ["", "", "", ""]
                    valor = ["", "", "", ""]
                    datos = request.body.split('&')
                    aux = 0
                    while (aux < len(datos)):
                        name[aux] = datos[aux].split('=')[0]
                        aux = aux + 1
                    aux = 0
                    while (aux < len(datos)):
                        valor[aux] = datos[aux].split('=')[1]
                        aux = aux + 1  
                    aux = 0
                    while aux < len(name):
                        trozo = name[aux]
                        estilo = valor[aux]
                        if trozo == 'banner':
                            if estilo == 'defecto':
                                pagina_estilo.banner = 'imagenes/alcala.png'
                                pagina_estilo.save()
                            elif estilo == 'real':
                                pagina_estilo.banner = 'imagenes/realmadrid.png'
                                pagina_estilo.save()
                            elif estilo == 'retiro':
                                pagina_estilo.banner = 'imagenes/retiro.png'
                                pagina_estilo.save()
                            elif estilo == '':
                                pass
                            aux = aux + 1

                        elif trozo == 'menu':
                            if estilo == 'defecto':
                                pagina_estilo.menu = 'red'
                                pagina_estilo.save()
                            elif estilo == 'verde':
                                pagina_estilo.menu = 'green'
                                pagina_estilo.save()
                            elif estilo == 'azul':
                                pagina_estilo.menu = 'blue'
                                pagina_estilo.save()
                            elif estilo == '':
                                pass
                            aux = aux + 1

                        elif trozo == 'login':
                            if estilo == 'defecto':
                                pagina_estilo.login = ''
                                pagina_estilo.save()
                            elif estilo == 'verde':
                                pagina_estilo.login = 'green'
                                pagina_estilo.save()
                            elif estilo == 'azul':
                                pagina_estilo.login = 'blue'
                                pagina_estilo.save()
                            elif estilo == '':
                                pass
                            aux = aux + 1

                        elif trozo == 'pie':
                            if estilo == 'defecto':
                                pagina_estilo.pie = 'red'
                                pagina_estilo.save()
                            elif estilo == 'verde':
                                pagina_estilo.pie = 'green'
                                pagina_estilo.save()
                            elif estilo == 'azul':
                                pagina_estilo.pie = 'blue'
                                pagina_estilo.save()
                            elif estilo == '':
                                pass
                            aux = aux + 1

                else:
                    #Cambiarlo que no hace falta !!
                    if recurso == request.user.username:
                        usuario = Usuario.objects.get(nombre=recurso)
                        usuario.titulo_personal = request.POST['Titulo']
                        usuario.save()
                        titulo = usuario.titulo_personal
                    else:
                        cambio_titulo += '<span>Error. </span>'
                        cambio_titulo += u'No eres el usuario de esta página'
            
        
    else:
        #Logearse en cualquier pagina de usuario
        log += login()
        if request.method == 'POST':
            usuario = request.POST['Usuario']
            password = request.POST['Password']
            user = auth.authenticate(username=usuario, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/" + recurso)
            else:
                error += '<span>Error.</span> Datos incorrectos<br>'
                plantilla = get_template('template.html')
                c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'inicio': inicio, 'pie': pie()})
                renderizado = plantilla.render(c)
                return HttpResponse(renderizado)

    plantilla = get_template('template.html')
    c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'inicio': inicio, 'actualizar': cambio_titulo, 'busqueda': cambio_estilo, 'pie': pie(), 'rss': rss})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)

def ayuda(request):
    cuerpo = ""
    log = ""
    titulo = u"Ayuda. Funcionamiento de la página"
    inicio = '<a href="/">Inicio</a>'
    error = ''
    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()
    

    cuerpo += u'<span>Interfaz pública:</span>'
    cuerpo += '<br><ul style="list-style-type: square">'
    cuerpo += u'<li>Página principal: muestra las 10 actividades mas proximas y posteriormente un listado con las paginas personales.</li>'
    cuerpo += u'<li>Pagina personal de usuario: muestra las actividades seleccionadas por el usuario.</li>'
    cuerpo += '<li>Todas: muestra todas las actividades disponibles. Permite filtrarlas por varios campos.</li>'
    cuerpo += u'<li>Cada actividad tiene su página con información de la misma.</li></ul>'
    cuerpo += '<span>Interfaz privada: </span>'
    cuerpo += u'además de todas las funcionalidades de la interfaz publica, permite:'
    cuerpo += '<ul style="list-style-type: square">'
    cuerpo += u'<li>Seleccionar actividades en la pagina "todas" para su página personal.</li>'
    cuerpo += u'<li>Permite modificar varios aspectos de la página web, como el estilo o el título de su página personal.</li></ul>'
    
    #Logearse en ayuda
    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/ayuda")
        else:
            error += '<span>Error.</span> Datos incorrectos<br>'
            plantilla = get_template('template.html')
            c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'pie': pie()})
            renderizado = plantilla.render(c)
            return HttpResponse(renderizado)

    plantilla = get_template('template.html')
    c = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'inicio': inicio, 'pie': pie()})
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
    

def plantillaCss(request, recurso):
    if request.user.is_authenticated():
        hoja_Estilo = EstiloCss.objects.get(usuario=request.user.username)
        login = hoja_Estilo.login
        menu = hoja_Estilo.menu
        banner = hoja_Estilo.banner
        pie = hoja_Estilo.pie
    else:
        login = ""
        menu = 'red'
        banner = 'imagenes/alcala.png'
        pie = 'red'
    plantilla_css = get_template(recurso)
    c = Context({'login':login, 'menu': menu, 'banner': banner, 'pie': pie})
    css = plantilla_css.render(c)
    return HttpResponse(css, content_type='text/css')

