from django.contrib import admin

# Register your models here.

from models import Usuario, Actividad, UltimaFecha, EstiloCss

admin.site.register(Usuario)
admin.site.register(Actividad)
admin.site.register(UltimaFecha)
admin.site.register(EstiloCss)
