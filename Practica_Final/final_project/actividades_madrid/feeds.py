from django.contrib.syndication.views import Feed
from actividades_madrid.models import Usuario, Actividad
import datetime

class RssUsuarios(Feed):

    link = "/"

    def get_object(self, request, recurso):
        return recurso

    def title(self, obj):
        return "Actividades de " + obj

    def description(self, obj):
        return "Actividades seleccionadas por " + obj

    def item_title(self, item):
        return item.titulo

    def item_description(self):
        return 'Mas informacion en el link'

    def items(self, obj):
        usuario = Usuario.objects.get(nombre=obj)
        actividades_selecc = usuario.actividades.all()
        return actividades_selecc

class RssPrincipal(Feed):

    link = "/"

    def title(self, obj):
        return "Actividades mas proximas"

    def description(self, obj):
        return "Proximas 10 actividades"

    def item_title(self, item):
        return item.titulo

    def item_description(self):
        return 'Mas informacion en el link'

    def items(self, obj):
        fecha_actual = datetime.datetime.today()
        fecha_final = datetime.date(2020, 12, 31)
        hora_actual = datetime.datetime.now() + datetime.timedelta(hours=2)
        hora_final = datetime.time(23, 59, 00)
        actividades = Actividad.objects.filter(fecha__range=(fecha_actual, fecha_final))
        actividades = actividades.filter(hora__range=(hora_actual, hora_final)).order_by('fecha', 'hora')[0:10]
        return actividades
    
