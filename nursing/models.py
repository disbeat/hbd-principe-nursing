from __future__ import unicode_literals
from datetime import datetime

from django.db import models

CHARFIELDS_LEN = 1024

class PatientType(models.Model):
    ''' Patient type: expat, tourist, local, etc '''
    
    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.name

class Patient(models.Model):
    ''' Patient information, mostly immutable '''

    name            = models.CharField(max_length=CHARFIELDS_LEN)
    birthdate       = models.DateField(verbose_name='Birth Date', null=True, blank=True)
    patient_type    = models.ForeignKey(PatientType, related_name='patients', null=True)
    address         = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    contact         = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    pmh             = models.TextField(null=True, blank=True, verbose_name='Personal Medical History')
    alergies        = models.TextField(null=True, blank=True)
    when            = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name='Registration Datetime')
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')

    def __unicode__(self):
		return str(self.id) + ': ' + self.name

class Diagnosys(models.Model):
    ''' Diagnosis list '''

    code            = models.CharField(max_length=CHARFIELDS_LEN)
    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    group           = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.code + ' - ' + self.name

class Treatment(models.Model):
    ''' Treatments list '''

    code            = models.CharField(max_length=CHARFIELDS_LEN)
    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    group           = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.code + ' - ' + self.name

class Department(models.Model):
    ''' Department list '''

    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.name



class MedicineType(models.Model):
    ''' Medicine type: oral, topic, wound, etc '''
    
    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.name

class Medicine(models.Model):
    ''' List of medicine available '''

    code            = models.CharField(max_length=CHARFIELDS_LEN)
    name            = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    group           = models.CharField(null=True, blank=True, max_length=CHARFIELDS_LEN)
    medicine_type   = models.ForeignKey(MedicineType, related_name='medicines', null=True)
    expiration      = models.DateField(null=True, blank=True)
    quantity        = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')
    
    def __unicode__(self):
		return self.code + ' - ' + self.name



class Visit(models.Model):
    ''' Visit data, each time a patient goes to the clinic '''

    filter_horizontal = ('diagnosys',)

    patient         = models.ForeignKey(Patient, related_name='visits')
    when            = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name='Visit Datetime')
    department      = models.ForeignKey(Department, related_name='visits', null=True)
    symptoms        = models.TextField(null=True, blank=True, verbose_name="Signs and Symptoms")
    diagnosys       = models.ManyToManyField(to=Diagnosys, blank=True)
    treatments      = models.ManyToManyField(to=Treatment, blank=True)
    medicines           = models.ManyToManyField(Medicine, through='MedicineStockChange')
    info            = models.TextField(null=True, blank=True, verbose_name='Additional Information')

    def __unicode__(self):
		return str(self.id) + ': ' + self.patient.name + ' @ '+ str(self.when)



class MedicineStockChange(models.Model):
    ''' Refill or consumption of a medicine '''
    medicine        = models.ForeignKey(Medicine, related_name='consumptions')
    quantity        = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    visit           = models.ForeignKey(Visit, related_name='consumptions', null=True, blank=True)
    when            = models.DateTimeField(default=datetime.now)

    def save(self):
        super(MedicineStockChange, self).save()
        self.medicine.quantity += self.quantity
        self.medicine.save()

    def __unicode__(self):
		return str(self.medicine) + ' | ' + str(self.quantity)
