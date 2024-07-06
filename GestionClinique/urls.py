from django.contrib import admin
from django.urls import path
from clinique import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Page accueil
    path('accueil', views.accueil, name="accueil"),

    #Pour gérer les patients
    path('ajout', views.ajoutpatient),
    path('index', views.index, name="index"),
    path('infopatient', views.infopatient),
    path('affPat', views.affpatient, name='affPat'),

    #Pour gérer les docteurs
    path('accueilDoc', views.accueildocteur, name='accueilDoc'),
    path('ajoutDoc', views.ajoutdocteur, name='ajoutDoc'),
    path('affDoc', views.affdocteur, name='affDoc'),

    #Pour les patients examinés
    path('patientexaminé', views.examiner_patient, name="patientexaminé"),

    #Pour les patients consultés
    path('patientconsulté', views.consulter_patient, name="patientconsulté"),

    #Pour les patients hospitalisés
    path('hospitaliser', views.hospitaliser_patient, name="hospitaliser"),

    #Pour la salle
    path('affsalle', views.affsalle, name="affsalle"),
    path('ajoutsalle', views.ajoutsalle, name="ajoutsalle"),


    #Pour la pharmacie
    path('pharma', views.pharmacie, name="pharmacie"),

    #Pour les clients
    path('ajoutclient', views.ajoutclient, name="ajoutclient"),
    path('affClient', views.affclient, name='affClient'),

    #Pour les produits
    path('ajoutproduit', views.ajoutproduit, name="ajoutproduit"),
    path('affProduit', views.affproduit, name='affProduit'),

    #Pour la vente
    path('vente', views.vente, name='vente'),

    #Rapport
    path('rapport', views.rapport, name="rapport"),
    path('rapport_mensuel', views.rapport_mensuel, name='rapport_mensuel'),
    path('rapport_vente', views.rapport_ventes, name='rapport_vente'),



    #Authentification
    path('login', views.connexion, name="urllogin"),
    path('logout', views.deconnexion, name="urldeconnexion"),
    path('register', views.compte, name="urlregister"),
    path('email', views.email, name="urlemail"),
    path('reset/<int:id>/', views.reset, name="urlreset"),
    
]
