from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    date = models.DateField()

class Patient(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    datenaissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    sexe = models.CharField(max_length=9)

    def __str__(self):
        
        return f'{self.prenom} {self.nom} {self.datenaissance}, {self.adresse}, {self.telephone}, de sexe {self.sexe},'


class Docteur(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, default='isaac@gmail.com')
  
    def __str__(self):
        return f'Docteur {self.prenom} {self.nom}, du service {self.specialite}, {self.telephone}, {self.email}'
    

#--------------------------------------------------------Salle-------------------------------------------------------------------------------
class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacité_max = models.IntegerField(default=5)
    
    def __str__(self):
        return f'Salle {self.nom}'

#-----------------------------------------------------Hospitalisation--------------------------------------------------------------------------
class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_admission = models.DateTimeField()
    motif_admission = models.TextField()
    salle = models.ForeignKey(Salle, related_name='patients',on_delete=models.CASCADE)

    def __str__(self):
        return f"Hospitalisation de {self.patient} le {self.date_admission} dans la salle {self.salle}"

@receiver(pre_save, sender=Hospitalisation)
def capacite_salle(sender, instance, **kwargs):
    salle=instance.salle
    if salle.patients.count()>=salle.capacité_max:
        raise ValidationError("la salle est pleine, impossible d'ajouter un nouveau patient")

#----------------------------------------------------Patient Consulté-------------------------------------------------------------------------
class PatientConsulté(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    docteur = models.ForeignKey(Docteur, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField()
    raison_consultation = models.TextField()
    antecedents_medicaux = models.TextField(blank=True, null=True)
    diagnostic = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank=True, null=True)
    recommandations = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation de {self.patient} par le docteur {self.docteur} le {self.date_consultation}"

#----------------------------------------------------Patient Examiné-----------------------------------------------------------------------
class PatientExaminé(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    docteur = models.ForeignKey(Docteur, on_delete=models.CASCADE)
    date_examen = models.DateTimeField()
    type_examen = models.CharField(max_length=100)
    resultats = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    suivi_necessaire = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Examen de {self.patient} par le docteur {self.docteur} le {self.date_examen}"






#------------------------------------------------------------Client-------------------------------------------------------------------
class Client(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f'Le client {self.prenom} {self.nom}, numéro : {self.telephone}'


#----------------------------------------------------------Produit--------------------------------------------------------------------
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    cout_achat = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField()

    def __str__(self):
        return f'Le produit {self.nom} coûte {self.prix}'


#------------------------------------------------------------Vente------------------------------------------------------------------
class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_vente = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Vérifier si la quantité en stock est suffisante pour la vente
        if self.quantite > self.produit.quantite_stock:
            raise ValidationError(f"La quantité en stock de {self.produit.nom} est insuffisante pour cette vente.")

    def save(self, *args, **kwargs):
        # Appeler la méthode clean pour valider les données
        self.clean()
        # Mettre à jour la quantité en stock du produit
        self.montant = self.quantite * self.produit.prix
        self.produit.quantite_stock -= self.quantite
        self.produit.save()
        # Sauvegarder la vente
        super().save(*args, **kwargs)

    def benefice(self):
        return self.montant - (self.quantite * self.produit.cout_achat)