from django import forms
import django_filters
from .models import *

class IpdFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    ctscan__rt_number=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='RT Number')
    package__patient_type__patient_type=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Type of Patient')
    realization__amount_received__gt=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}), field_name='realization__amount_received', lookup_expr='gt', label='Min. Amount Received')
    realization__amount_received__lt=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}), field_name='realization__amount_received', lookup_expr='lt', label='Max. Amount Received')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from_doa', 'class':'form-control'}), field_name='package__date_of_admission', label='From - Date of Admission ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to_doa', 'class':'form-control'}), field_name='package__date_of_admission', label='To - Date of Admission ', lookup_expr='lte')
    from_date_bill=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from_bd', 'class':'form-control'}), field_name='realization__billing_month', label='From - Date of Billing ', lookup_expr='gte')
    to_date_bill=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to_bd', 'class':'form-control'}), field_name='realization__billing_month', label='To - Date of Billing ', lookup_expr='lte')
    
    class Meta:
        model=IpdReport
        fields={
            'realization__cash':['exact']
        }

class CTScanFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    rt_number=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='RT Number')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')
    conducted_by=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Conducted By ')

class RadiationsFilters(django_filters.FilterSet):
    patient=django_filters.ModelMultipleChoiceFilter(widget=forms.TextInput(attrs={'class':'form-control'}), label='Name', queryset=Patient.objects.all())
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')

class CommonExpensesFilters(django_filters.FilterSet):
    particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Particulars')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')
    amount=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))
    paid_by=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Paid By ')

class OtherIncomeFilters(django_filters.FilterSet):
    particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Particulars')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')
    amount=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))
    received_by=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Received By ')

class AdditionalIncomeFilters(django_filters.FilterSet):
    particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Particulars')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')
    amount=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))
    received_by=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Received By ')

class OtherExpensesFilters(django_filters.FilterSet):
    particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Particulars')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='date', label='To - Date ', lookup_expr='lte')
    amount=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))
    paid_by=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Paid By ')

class LockDataFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class OpdFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='opd__date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='opd__date', label='To - Date ', lookup_expr='lte')

class OngoingFilters(django_filters.FilterSet):
    ipdreport__patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    ipdreport__package__patient_type__patient_type=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Type of Patient')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), field_name='ipdreport__package__date_of_admission', label='From - Date of Admission ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), field_name='ipdreport__package__date_of_admission', label='To - Date of Admission ', lookup_expr='lte')

class UnclaimedFilters(django_filters.FilterSet):
    ipdreport__patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class ClaimedFilters(django_filters.FilterSet):
    ipdreport__patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class PatientFilters(django_filters.FilterSet):
    name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains')

class PackageFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class ApprovedPackageFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class DischargeFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class RealizationFilters(django_filters.FilterSet):
    patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')

class RepudiatedFilters(django_filters.FilterSet):
    ipdreport__patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), field_name='ipdreport__realization__billing_month', label='From - Date of Admission ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), field_name='ipdreport__realization__billing_month', label='To - Date of Admission ', lookup_expr='lte')

class ReclaimedRepudiationFilters(django_filters.FilterSet):
    ipdreport__patient__name=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label='Name')
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), field_name='ipdreport__realization__billing_month', label='From - Date of Admission ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), field_name='ipdreport__realization__billing_month', label='To - Date of Admission ', lookup_expr='lte')

class PiggyBankFilters(django_filters.FilterSet):
    depositor=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label="Depositor's Name")
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), field_name='date', label='To - Date ', lookup_expr='lte')

class WithdrawalFilters(django_filters.FilterSet):
    particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label="Particulars")
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), field_name='date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), field_name='date', label='To - Date ', lookup_expr='lte')
    amount=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))
    voucher_number=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}))

class PettyCashFilters(django_filters.FilterSet):
    withdrawal__voucher_number=django_filters.NumberFilter(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Voucher Number')
    withdrawal__particulars=django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}), lookup_expr='icontains', label="Particulars")
    from_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'from', 'class':'form-control'}), field_name='withdrawal__date', label='From - Date ', lookup_expr='gte')
    to_date=django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date', 'id': 'to', 'class':'form-control'}), field_name='withdrawal__date', label='To - Date ', lookup_expr='lte')