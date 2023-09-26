from django.db import models
from django.db.models import CharField, EmailField, ManyToManyField, ForeignKey, CASCADE, DateField, FloatField, \
    TextField, BooleanField, DateTimeField
from django.forms import DecimalField
from django.utils import timezone

TYPE_COMPTE = (
    ('P','Particulier'),
    ('I','Intermédiaire'),
    ('E','Entreprise'),
)


DEGRE_PRIORITE = (
    ('N','Normal'),
    ('P','Prioritaire'),
    ('H','Haute Priorité'),
)


class Avantage(models.Model):
    designation = CharField(max_length=255, verbose_name='désignation')
    valeur = CharField(max_length=255, verbose_name='valeur')

    def __str__(self):
        return f'{self.designation} : {self.valeur}' if self is not None else ''


class PlanAbonnement(models.Model):
    designation = CharField(max_length=255, verbose_name='désignation')
    avantages = ManyToManyField(Avantage)

    def __str__(self):
        return f'{self.designation}' if self is not None else ''


class Facture(models.Model):
    compte = ForeignKey('Compte', on_delete=CASCADE, verbose_name='compte')
    num = CharField(max_length=1000, verbose_name='n°')
    date_facture = DateField(default=timezone.now, verbose_name='date')
    montant = DecimalField(default=0, decimal_places=2, verbose_name='montant')

    def __str__(self):
        return f'Montant de la facture n°{self.num} s\'élève à : {self.montant} DZD' if self is not None else ''


class Contact(models.Model):
    compte = ForeignKey('Compte', on_delete=CASCADE, verbose_name='compte')
    nom = CharField(max_length=1000, verbose_name='nom')
    adresse = CharField(max_length=1000, verbose_name='adresse')
    email = EmailField(max_length=255, verbose_name='courrier éléctronique')
    tel = CharField(max_length=255, verbose_name='téléphone')

    def __str__(self):
        return f'{self.nom} ({self.tel})' if self is not None else ''


class TemplateSMS(models.Model):
    compte = ForeignKey('Compte', on_delete=CASCADE, verbose_name='compte')
    designation = CharField(max_length=1000, verbose_name='désignation')
    texte = TextField(max_length=1000, verbose_name='texte')
    tag = CharField(max_length=255, verbose_name='tag')

    def __str__(self):
        return f'{self.designation} ({self.tag})' if self is not None else ''


class SMS(models.Model):
    compte = ForeignKey('Compte', on_delete=CASCADE, verbose_name='compte')
    destinataire = CharField(max_length=1000, verbose_name='destinataire')
    priorite = CharField(max_length=1, choices=DEGRE_PRIORITE, default='N',verbose_name='priorité')
    texte = TextField(max_length=1000, verbose_name='texte')
    tag = CharField(max_length=255, verbose_name='tag')
    date_envoi = DateTimeField(default=timezone.now, verbose_name='date et heure d\'envoi')
    envoye = BooleanField(default=False, verbose_name='envoyé?')
    accuse = BooleanField(default=False, verbose_name='accusé?')

    def __str__(self):
        return f'{self.designation} ({self.tag})' if self is not None else ''


class SMSEnAttenteManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = SMS.objects.get_queryset().filter(envoye=False)
        return qs


class SMSEnAttente(SMS):
    objects= SMSEnAttenteManager()

    class Meta:
        proxy = True


class Compte(models.Model):
    nom = CharField(max_length=255, verbose_name='nom')
    prenom = CharField(max_length=255, verbose_name='prénom')
    email = EmailField(max_length=255, verbose_name='courrier éléctronique')
    mdp = CharField(max_length=1000, verbose_name='mot de passe')
    date_creation = DateField(default=timezone.now, verbose_name='date de création')
    type = CharField(max_length=1, choices=TYPE_COMPTE, default='P')
    plan_abonnement = ForeignKey(PlanAbonnement, on_delete=CASCADE, verbose_name='plan d\'abonnement')

    def __str__(self):
        return f'{self.email}' if self is not None else '-'




