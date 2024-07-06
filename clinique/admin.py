from django.contrib import admin

# Register your models here.
from .models import Patient, Docteur, PatientExaminé, PatientConsulté, Hospitalisation, Salle, Client, Produit, Vente

admin.site.register(Patient)
admin.site.register(Docteur)
admin.site.register(PatientExaminé)
admin.site.register(PatientConsulté)
admin.site.register(Hospitalisation)
admin.site.register(Salle)
admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Vente)
