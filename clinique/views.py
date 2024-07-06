from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import Patient, Docteur, PatientConsulté, PatientExaminé, Hospitalisation, Salle, Produit, Vente, Client
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate 
from django.contrib.auth.decorators import login_required



def accueil(request):
    return render (request, 'accueil.html')

def ajoutpatient(request):
    if request.method == "POST":
        data = request.POST
        toto = Patient.objects.create(
        prenom = data.get('prenom'),
        nom = data.get('nom'),
        datenaissance = data.get('datenaissance'),
        adresse = data.get('adresse'),
        telephone = data.get('telephone'),
        sexe = data.get('sexe')
        )
        print('Validé !')
        return redirect('affPat')
    return render(request, 'Patient/ajout_patient.html')

def affpatient(request):
    p = Patient.objects.all()
    return render(request, 'Patient/affichepatient.html', {'p':p})
   
    
def index(request):

    return render(request, 'index.html')


def infopatient(request):

    return render(request, 'Patient/infopatient.html')

def nav(request):

    return render(request, 'nav.html')


#------------------------------------------------------Fonctions des docteurs--------------------------------------------------------------------

def accueildocteur(request):

    return render (request, 'Docteur/accueil.html')

def ajoutdocteur(request):
    if request.method == "POST":
        data = request.POST
        toto = Docteur.objects.create(
        prenom = data.get('prenom'),
        nom = data.get('nom'),
        specialite = data.get('specialite'),
        telephone = data.get('telephone'),
        email = data.get('email'),
        )
        print('Validé !')
        return redirect('affDoc')
    return render (request, 'Docteur/ajout.html')

def affdocteur(request):
    d = Docteur.objects.all()
    return render(request, 'Docteur/affiche.html', {'d':d})


#----------------------------------------------------Fonctions des patients examinés-----------------------------------------------------------
def examiner_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        docteur_id = request.POST.get('docteur_id')
        date_examen = timezone.now()
        type_examen = request.POST.get('type_examen')
        resultats = request.POST.get('resultats')
        observations = request.POST.get('observations')
        suivi_necessaire = request.POST.get('suivi_necessaire')
        statut = request.POST.get('statut')
        notes = request.POST.get('notes')
        
        examen = PatientExaminé(
            patient_id=(patient_id),
            docteur_id=(docteur_id),
            date_examen=date_examen,
            type_examen=type_examen,
            resultats=resultats,
            observations=observations,
            suivi_necessaire=suivi_necessaire,
            statut=statut,
            notes=notes
        )
        examen.save()
        return redirect('index')

    patients = Patient.objects.all()
    docteur = Docteur.objects.all()
    return render(request, 'PatientExaminé/ajout_patient_examiné.html', {'patients': patients, 'docteur': docteur})


#----------------------------------------------------Fonctions des patients consultés----------------------------------------------------------
def consulter_patient(request):
    if request.method == 'POST':
        patient = request.POST.get('patient')
        docteur = request.POST.get('docteur')
        date_consultation = timezone.now()
        raison_consultation = request.POST.get('raison_consultation')
        antecedents_medicaux = request.POST.get('antecedents_medicaux')
        diagnostic = request.POST.get('diagnostic')
        prescriptions = request.POST.get('prescriptions')
        recommandations = request.POST.get('recommandations')
        notes = request.POST.get('notes')

        patient = get_object_or_404(Patient, id=patient)
        docteur = get_object_or_404(Docteur, id=docteur)
        consultation = PatientConsulté(
            patient=patient,
            docteur=docteur,
            date_consultation=date_consultation,
            raison_consultation=raison_consultation,
            antecedents_medicaux=antecedents_medicaux,
            diagnostic=diagnostic,
            prescriptions=prescriptions,
            recommandations=recommandations,
            notes=notes
        )
        consultation.save()
        return redirect('hospitaliser')

    patients = Patient.objects.all()
    docteur = Docteur.objects.all()
    return render(request, 'PatientConsulté/ajout_patient_consulté.html', {'patients': patients, 'docteur': docteur})

#---------------------------------------------------------Patients Hospitalisés-----------------------------------------------------
def hospitaliser_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        date_admission = request.POST.get('date_admission')
        motif_admission = request.POST.get('motif_admission')
        salle_id = request.POST.get('salle')

        salle = get_object_or_404(Salle, id=salle_id)
        patient = get_object_or_404(Patient, id=patient_id)

        nombre_patients = Hospitalisation.objects.filter(salle=salle).count()

        if nombre_patients >= salle.capacité_max:
            messages.error(request, "Cette salle est déjà pleine. Veuillez en choisir une autre.")
            return redirect("hospitaliser")

        hospitalisation = Hospitalisation(
            patient=patient,
            date_admission=date_admission,
            motif_admission=motif_admission,
            salle=salle
        )
        hospitalisation.save()
        return redirect('index')

    salles = Salle.objects.all()
    patientconsulé = PatientConsulté.objects.all()
    return render(request, 'PatientConsulté/patient_hospitalisé.html', {'patientconsulé': patientconsulé, 'salles':salles})

#-------------------------------------------------------------------Salle-----------------------------------------------------------------
def ajoutsalle(request):
    if request.method == "POST":
        data = request.POST
        toto = Salle.objects.create(
        nom = data.get('nom'),
        )
        print('Validé !')
    return render (request, 'PatientConsulté/salle.html')

def affsalle(request):
    
    return render(request, 'PatientConsulté/salle.html')




#-------------------------------------------------------Pharmacie-----------------------------------------------------------------------

def pharmacie(request):
    return render(request, 'Vente/accueil.html')


#-------------------------------------------------------Client---------------------------------------------------------------------------
def ajoutclient(request):
    if request.method == "POST":
        data = request.POST
        toto = Client.objects.create(
        prenom = data.get('prenom'),
        nom = data.get('nom'),
        adresse = data.get('adresse'),
        telephone = data.get('telephone'),
        )
        print('Validé !')
        return redirect('affClient')
    return render(request, 'Vente/ajoutclient.html')

def affclient(request):
    p = Client.objects.all()
    return render(request, 'Vente/afficheclient.html', {'p':p})


#----------------------------------------------------------Produit---------------------------------------------------------------------------
def ajoutproduit(request):
    if request.method == "POST":
        data = request.POST
        toto = Produit.objects.create(
        nom = data.get('nom'),
        description = data.get('description'),
        prix = data.get('prix'),
        quantite_stock = data.get('quantite_stock'),
        cout_achat = data.get('cout_achat'),
        )
        print('Validé !')
        return redirect('affProduit')
    return render(request, 'Vente/ajoutproduit.html')

def affproduit(request):
    p = Produit.objects.all()
    return render(request, 'Vente/afficheproduit.html', {'p':p})


#---------------------------------------------------------------Vente-----------------------------------------------------------------------
def vente(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        produit_id = request.POST.get('produit')
        quantite = int(request.POST.get('quantite'))
        montant = int(request.POST.get('montant'))
        date_vente = request.POST.get('date_vente')
        
        client = Client.objects.get(id=client_id)
        produit = Produit.objects.get(id=produit_id)
        
        if produit.quantite_stock >= quantite:
            Vente.objects.create(client=client, 
                                 produit=produit, 
                                 quantite=quantite,
                                 montant=montant, 
                                 date_vente= date_vente)
            messages.success(request, 'Super ! La vente a été effectuée avec succès.')
            return redirect('affProduit')
        else:
            messages.error(request, 'La quantité en stock est insuffisante pour effectuer cette vente.')
        
        return redirect('vente')
    
    clients = Client.objects.all()
    produits = Produit.objects.all()
    return render(request, 'Vente/vente.html', {'clients': clients, 'produits': produits})


#------------------------------------------------------Rapport mensuel----------------------------------------------------------------------
def rapport_mensuel(request):
    today = timezone.now()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    
    consultations = PatientConsulté.objects.filter(date_consultation__range=[start_of_month, end_of_month]).count()
    examens = PatientExaminé.objects.filter(date_examen__range=[start_of_month, end_of_month]).count()
    hospitalisations = Hospitalisation.objects.filter(date_admission__range=[start_of_month, end_of_month]).count()
    
    context = {
        'consultations': consultations,
        'examens': examens,
        'hospitalisations': hospitalisations,
        'mois': today.strftime('%B %Y')
    }
    
    return render(request, 'RapportMensuel/rapport_mensuel.html', context)


#----------------------------------------------------------Rapport-------------------------------------------------------------------

def rapport(request):
    return render(request, 'RapportMensuel/rapport.html')


#----------------------------------------------------------Rapport des ventes-------------------------------------------------------------------
def rapport_ventes(request):
    ventes = Vente.objects.all()
    
    montant_total = ventes.aggregate(
        total=Sum(ExpressionWrapper(F('quantite') * F('produit__prix'), output_field=DecimalField()))
    )['total'] or 0

    cout_total = ventes.aggregate(
        total=Sum(ExpressionWrapper(F('quantite') * F('produit__cout_achat'), output_field=DecimalField()))
    )['total'] or 0

    benefice_total = montant_total - cout_total

    return render(request, 'RapportMensuel/rapport_vente.html', {
        'ventes': ventes,
        'montant_total': montant_total,
        'benefice_total': benefice_total,
    })



#----------------------------------------------------------Authentification-------------------------------------------------------------------

#------------------------------------------------------------------Login-------------------------------------------------------------------
def connexion(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username = username, password = password )
        if user:
            login(request, user)
            print('Connexion réussie')
            return redirect('index')
        else:
            messages.error(request, 'Nom ou mot de passe incorrect')

    return render(request, 'Authentification/login.html')


#-------------------------------------------------------------Création compte-----------------------------------------------------------------
def compte(request):

    if request.method == 'POST':
        data = request.POST
        if data.get('password1') == data.get('password'):
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            #la méthode create_user permet de créer un utilisateur, ne pas utiliser la méthode save.
            isinstance = User.objects.create_user(
                username = username,
                email = email,
                password = password
            )
            print("Compte créé avec succès !!")
        else:
            print("Le compte n'a pas été créé")

    return render(request, 'Authentification/register.html')


#----------------------------------------------------------Réinitialiser son compte----------------------------------------------------------
def reset(request,pk):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        data = request.POST
        if data.get('password') == data.get('password1'):
            newpassword = data.get('password')
            user.set_password(newpassword)
            user.save()
            print("Mot de passe modifié avec succès")
            return redirect('urllogin')
        else :
            print("Désolé les deux mots de passe ne sont pas identiques")
            return redirect('urlreset')
    return render(request, 'Authentification/reset.html')



#-----------------------------------------------------------Email---------------------------------------------------------------------------
def email(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        user = User.objects.filter(email = email).last()
        if user :
            print("Email correct")
            return redirect('urlreset', user.id)
        else :
            print('Email incorrect')
            return redirect('urlemail')

    return render(request, 'Authentification/email.html')



#------------------------------------------------------------Déconnexion------------------------------------------------------------------
def deconnexion(request):
    logout(request)
    print('Déconnexion réussie')
    return redirect('accueil')