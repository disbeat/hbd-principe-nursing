from django.contrib import admin
from django.contrib.admin import register
from .models import Patient, Visit, Diagnosys, Treatment, Department, PatientType, MedicineType, Medicine, MedicineStockChange

class MedicineStockChangeInline(admin.TabularInline):
    model = MedicineStockChange

class VisitInline(admin.StackedInline):
    model = Visit

@register(Visit)
class VisitAdmin(admin.ModelAdmin):
    date_hierarchy = 'when'
    list_display = ('patient', 'department', 'when')
    filter_horizontal = ('diagnosys','treatments', 'medicines', )
    inlines = [MedicineStockChangeInline, ]


@register(Patient)
class PatientAdmin(admin.ModelAdmin):
    date_hierarchy = 'when'
    list_display = ('name', 'birthdate', 'patient_type')
    inlines = [VisitInline,]

@register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    date_hierarchy = 'expiration'
    list_display = ('code', 'name', 'quantity', 'expiration')



admin.site.register(Diagnosys)
admin.site.register(Treatment)
admin.site.register(Department)
admin.site.register(PatientType)
admin.site.register(MedicineType)
admin.site.register(MedicineStockChange)