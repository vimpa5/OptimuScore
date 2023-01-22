from django.contrib import admin
# Register your models here.
from .models import *

@admin.register(ServiceName)
class ServiceNameAdmin(admin.ModelAdmin):
    list_display=('service_name',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('title', 'name', 'gender', 'phone_number', 'alternate_phone_number', 'center', 'mr_uid')

@admin.register(PaxMax)
class PaxMaxAdmin(admin.ModelAdmin):
    list_display=('treatment', 'patient_type', 'max_fractions', 'total_package')

@admin.register(CommonExpenses)
class CommonExpensesAdmin(admin.ModelAdmin):
    list_display=('particulars', 'date', 'paid_by', 'amount', 'common_expenses_date', 'modified_on')

@admin.register(OtherIncome)
class OtherIncomeAdmin(admin.ModelAdmin):
    list_display=('particulars', 'date', 'received_by', 'amount', 'created_on', 'modified_on')

@admin.register(AdditionalIncome)
class AdditionalIncomeAdmin(admin.ModelAdmin):
    list_display=('particulars', 'date', 'received_by', 'amount', 'created_on', 'modified_on')

@admin.register(OtherExpenses)
class OtherExpensesAdmin(admin.ModelAdmin):
    list_display=('particulars', 'date', 'paid_by', 'amount', 'created_on', 'modified_on')

@admin.register(Opd)
class OpdAdmin(admin.ModelAdmin):
    list_display=('patient', 'bill_number', 'date', 'service_name', 'mode', 'amount', 'remarks', 'opd_date', 'modified_on')

@admin.register(OPDCashSheet)
class OPDCashSheetAdmin(admin.ModelAdmin):
    list_display=('date', 'patient', 'opd', 'opd_particulars', 'source', 'case_number', 'mode', 'cash_in', 'cash_out', 'balance', 'bank_oopl', 'remarks', 'created_on', 'modified_on')

@admin.register(OPDParticulars)
class OPDParticularsAdmin(admin.ModelAdmin):
    list_display=('opd_particulars',)

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display=('diagnosis',)

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display=('treatment',)

@admin.register(PatientType)
class PatientTypeAdmin(admin.ModelAdmin):
    list_display=('patient_type',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display=('patient', 'diagnosis', 'date_of_admission', 'treatment', 'patient_type', 'max_fractions', 'total_package', 'remarks', 'package_date', 'modified_on')

@admin.register(ApprovedPackage)
class ApprovedPackageAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'discount', 'approved_package', 'approval_date', 'proposed_fractions', 'remarks', 'approved_package_date', 'modified_on')

@admin.register(CTScan)
class CTScanAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'rt_number', 'amount', 'date', 'conducted_by', 'remarks', 'ctscan_date', 'modified_on')

@admin.register(Radiations)
class RadiationsAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'date', 'done_fractions', 'base_value', 'expected_value', 'remarks', 'radiations_date', 'modified_on')

@admin.register(Realization)
class RealizationAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'cash', 'amount_received', 'received_by', 'billing_month', 'surplus_percentage', 'deficit_or_surplus_amount', 'deficit_percentage', 'remarks', 'realization_date', 'modified_on')

@admin.register(LockData)
class LockDataAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'lock', 'date', 'created_on', 'modified_on')

@admin.register(Discharge)
class DischargeAdmin(admin.ModelAdmin):
    list_display=('patient', 'patient_type', 'treatment', 'date_of_discharge', 'discharge_updated', 'remarks', 'discharge_date', 'modified_on')

@admin.register(PiggyBank)
class PiggyBankAdmin(admin.ModelAdmin):
    list_display=('date', 'particulars', 'amount', 'created_on', 'modified_on')

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display=('date', 'particulars', 'amount', 'balance', 'voucher_number', 'image', 'docs', 'upload_date', 'modified_on')