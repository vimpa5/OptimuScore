from django import forms
from django.db.models import fields
from django.forms import DateInput
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError

class PatientForm(ModelForm):
    GENDER_SELECT = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('o', 'Other'),
    )
    TITLE_SELECT = (
        ('0', 'Mr.'),
        ('1', 'Mrs.'),
        ('2', 'Ms.'),
        ('3', 'Mast.'),
    )
    title=forms.CharField(widget=forms.RadioSelect(choices=TITLE_SELECT, attrs={'class': 'form-check-inline'}))
    gender=forms.CharField(widget=forms.RadioSelect(choices=GENDER_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=Patient
        fields='__all__'
        labels={
            'phone_number':'Phone Number',
            'alternate_phone_number':'Alternate Phone Number',
            'mr_uid':'MR/UID',
        }
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your 10 digit number'}),
            'alternate_phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your 10 digit number'}),
            'center': forms.TextInput(attrs={'class':'form-control'}),
            'mr_uid': forms.NumberInput(attrs={'class':'form-control'}),

            }

class CommonExpensesForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    paid_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=CommonExpenses
        fields='__all__'
        labels={
            'particulars':'Description',
        }
        widgets={

            'particulars': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),

        }

class OpdForm(ModelForm):
    MODE_SELECT = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    mode=forms.CharField(widget=forms.RadioSelect(choices=MODE_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=Opd
        fields='__all__'
        labels={

            'bill_number':'Bill Number',
            'service_name':'Service Availed',
            'remarks':'Remarks (Optional)',
        }
        widgets={

           'patient': forms.Select(attrs={'class':'form-control'}),
           'bill_number': forms.NumberInput(attrs={'class':'form-control'}),
           'service_name': forms.Select(attrs={'class':'form-control'}),
           'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
           'amount': forms.NumberInput(attrs={'class':'form-control'}),
           'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pass
        else:
            if LockData.objects.filter(patient=self.instance.patient, date__gte=self.instance.date).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, date__gte=self.instance.date).order_by('id').first()
                print('LOCK DATA VALUE FOR OPD ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class OPDParticularsForm(ModelForm):
    class Meta:
        model=OPDParticulars
        fields='__all__'
        labels={
            'opd_particulars':'Description',
        }
        widgets={

           'opd_particulars': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),

        }

class DiagnosisForm(ModelForm):
    class Meta:
        model=Diagnosis
        fields='__all__'
        widgets={

           'diagnosis': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),

        }

class TreatmentForm(ModelForm):
    class Meta:
        model=Treatment
        fields='__all__'
        widgets={

           'treatment': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),

        }

class PatientTypeForm(ModelForm):
    class Meta:
        model=PatientType
        fields='__all__'
        labels={

            'patient_type':'Patient Category',
        }
        widgets={

           'patient_type': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),

        }

class PackageForm(ModelForm):
    class Meta:
        model=Package
        fields='__all__'
        labels={

            'patient_type':'Patient Category',
            'date_of_admission':'Admission Date',
            'max_fractions':'Fractions',
            'total_package':'Total Cost',
            'remarks':'Remarks (Optional)',
        }
        widgets={
           'patient': forms.Select(attrs={'class':'form-control'}),
           'diagnosis': forms.Select(attrs={'class':'form-control'}),
           'treatment': forms.Select(attrs={'class':'form-control'}),
           'patient_type': forms.Select(attrs={'class':'form-control'}),
           'date_of_admission': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
           'max_fractions': forms.NumberInput(attrs={'class':'form-control'}),
           'total_package': forms.NumberInput(attrs={'class':'form-control'}),
           'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pass
        else:
            if LockData.objects.filter(patient=self.instance.patient, date__gte=self.instance.date_of_admission).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, date__gte=self.instance.date_of_admission).order_by('id').first()
                print('LOCK DATA VALUE FOR PACKAGE ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class ApprovedPackageForm(ModelForm):
    class Meta:
        model=ApprovedPackage
        # exclude=['base_value', 'expected_value']
        fields='__all__'
        labels={
            
            'patient_type':'Patient Category',
            'approval_date':'Approval Date',
            'proposed_fractions':'Proposed Fractions',
            'approved_package':'Approved Package',
            'remarks':'Remarks (Optional)',
        }
        widgets={

           'patient': forms.Select(attrs={'class':'form-control'}),
           'patient_type': forms.Select(attrs={'class':'form-control'}),
           'discount': forms.NumberInput(attrs={'class':'form-control'}),
           'approved_package': forms.NumberInput(attrs={'class':'form-control'}),
           'approval_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
           'proposed_fractions': forms.NumberInput(attrs={'class':'form-control'}),
           'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(ApprovedPackageForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pt=self.cleaned_data['patient']
            ptt=self.cleaned_data['patient_type']
            tt=self.cleaned_data['treatment']
            print('patient type: ', ptt)
            print('treatment: ', tt)
            if Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt):
                dis1=Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                print('approved package form mein dis1 ka value: ', dis1)
                try:
                    pkg1=Package.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    dis2=dis1.order_by('-id').first()
                    pkg2=pkg1.filter(date_of_admission__gt=dis2.date_of_discharge)
                    if not pkg2:
                        raise ValidationError('There is no Package data for this patient - 1!')
                except Package.DoesNotExist:
                    raise ValidationError('No history of Package instance!')
            else:
                try:
                    Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    print(Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                except Package.DoesNotExist:
                    raise ValidationError('There is no Package value for this entry - 2!')
        else:
            print('self dot instance dot pk ka print approved package clean mein: ', self.instance.pk)
            print('self dot instance ka print approved package clean mein: ', self.instance)
            if LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.approval_date).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, date__gte=self.instance.approval_date).order_by('id').first()
                print('LOCK DATA VALUE FOR approved package ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class CTScanForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    conducted_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=CTScan
        fields='__all__'
        labels={
            'rt_number':'RT Number',
            'conducted_by':'Conducted By',
            'patient_type':'Patient Category',
            'remarks':'Remarks (Optional)',
        }
        widgets={

            'patient': forms.Select(attrs={'class':'form-control'}),
            'patient_type': forms.Select(attrs={'class':'form-control'}),
            'rt_number': forms.TextInput(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(CTScanForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pt=self.cleaned_data['patient']
            ptt=self.cleaned_data['patient_type']
            tt=self.cleaned_data['treatment']
            print('patient type: ', ptt)
            print('treatment: ', tt)
            if Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt):
                dis1=Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                print('ctscan form mein dis1 ka value: ', dis1)
                try:
                    pkg1=Package.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    dis2=dis1.order_by('-id').first()
                    pkg2=pkg1.get(date_of_admission__gt=dis2.date_of_discharge)
                    print('pkg2 ka value: ', pkg2)
                    if not pkg2:
                        raise ValidationError('There is no Package data for this patient - 1!')
                    else:
                        try:
                            ap1=ApprovedPackage.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                            ap2=ap1.filter(approval_date__gt=pkg2.date_of_admission)
                            if not ap2:
                                raise ValidationError('There is no ApprovedPackage data for this patient - 1!')
                        except ApprovedPackage.DoesNotExist:
                            raise ValidationError('No history of ApprovedPackage instance!')
                except Package.DoesNotExist:
                    raise ValidationError('No history of Package instance!')
            else:
                try:
                    Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    print(Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                    try:
                        ApprovedPackage.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                        print(ApprovedPackage.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                    except ApprovedPackage.DoesNotExist:
                        raise ValidationError('There is no ApprovedPackage data for this patient - 2!')
                except Package.DoesNotExist:
                    raise ValidationError('There is no Package data for this patient - 2!')
            if CTScan.objects.exclude(patient=pt):
                ct_exc=CTScan.objects.exclude(patient=pt)
                rt=self.request.POST.get('rt_number')
                for obj in ct_exc:
                    if rt==obj.rt_number:
                        raise ValidationError('This RT Number is already used!')
            else:
                pass
        else:
            print('self dot instance dot pk ka print CT Scan clean mein: ', self.instance.pk)
            print('self dot instance ka print CT Scan clean mein: ', self.instance)
            if LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date).order_by('id').first()
                print('LOCK DATA VALUE FOR CT Scan ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass
            if CTScan.objects.exclude(patient=self.instance.patient):
                ct_exc=CTScan.objects.exclude(patient=self.instance.patient)
                rt=self.instance.rt_number
                for obj in ct_exc:
                    if rt==obj.rt_number:
                        raise ValidationError('This RT Number is already used!')
            else:
                pass

class RadiationsForm(ModelForm):
    class Meta:
        model=Radiations
        fields='__all__'
        labels={
            'patient_type':'Patient Category',
            'done_fractions':'Fractions Done',
            'remarks':'Remarks (Optional)',
        }
        widgets={

            "base_value":forms.HiddenInput(),
            "expected_value":forms.HiddenInput(),
            'patient': forms.Select(attrs={'class':'form-control'}),
            'patient_type': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'done_fractions': forms.NumberInput(attrs={'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(RadiationsForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pt=self.cleaned_data['patient']
            ptt=self.cleaned_data['patient_type']
            tt=self.cleaned_data['treatment']
            print('patient type: ', ptt)
            print('treatment: ', tt)
            if Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt):
                dis1=Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                print('radiations form mein dis1 ka value: ', dis1)
                try:
                    pkg1=Package.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    dis2=dis1.order_by('-id').first()
                    pkg2=pkg1.get(date_of_admission__gt=dis2.date_of_discharge)
                    if not pkg2:
                        raise ValidationError('There is no Package data for this patient - 1!')
                    else:
                        try:
                            ap1=ApprovedPackage.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                            ap2=ap1.get(approval_date__gt=pkg2.date_of_admission)
                            if not ap2:
                                raise ValidationError('There is no Receivable data for this patient - 1!')
                            else:
                                try:
                                    ct1=CTScan.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt, date__gte=ap2.approval_date)
                                    if not ct1:
                                        raise ValidationError('There is no CT Scan data for this patient - 1!')
                                except CTScan.DoesNotExist:
                                    raise ValidationError('No history of CTScan instance!')
                        except ApprovedPackage.DoesNotExist:
                            raise ValidationError('No history of ApprovedPackage instance!')
                except Package.DoesNotExist:
                    raise ValidationError('No history of Package instance!')
            else:
                try:
                    Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    print(Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                    try:
                        ApprovedPackage.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                        print(ApprovedPackage.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                        try:
                            CTScan.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                            print(CTScan.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt))
                        except CTScan.DoesNotExist:
                            raise ValidationError('There is no CTScan data for this patient - 2!')
                    except ApprovedPackage.DoesNotExist:
                        raise ValidationError('There is no ApprovedPackage data for this patient - 2!')
                except Package.DoesNotExist:
                    raise ValidationError('There is no Package data for this patient - 2!')
        else:
            print('self dot instance dot pk ka print Radiations clean mein: ', self.instance.pk)
            print('self dot instance ka print Radiations clean mein: ', self.instance)
            if LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date).order_by('id').first()
                print('LOCK DATA VALUE FOR Radiations ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class DischargeForm(ModelForm):
    class Meta:
        model=Discharge
        fields='__all__'
        labels={
            'patient_type':'Patient Category',
            'date_of_discharge':'Discharge Date',
            'remarks':'Remarks (Optional)',
        }
        widgets={

            'patient': forms.Select(attrs={'class':'form-control'}),
            'patient_type': forms.Select(attrs={'class':'form-control'}),
            'date_of_discharge': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(DischargeForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pt=self.cleaned_data['patient']
            ptt=self.cleaned_data['patient_type']
            tt=self.cleaned_data['treatment']
            print('patient type: ', ptt)
            print('treatment: ', tt)
            print('Discharge clean mein pt ka value: ', pt)
            radiations=Radiations.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt).order_by('-id').first()
            if Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt, date_of_discharge__gt=radiations.date).exists():
                raise ValidationError('The patient has already been discharged!')
        else:
            print('self dot instance dot pk ka print dicharge clean mein: ', self.instance.pk)
            print('self dot instance ka print dicharge clean mein: ', self.instance)
            if LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date_of_discharge).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.date_of_discharge).order_by('id').first()
                print('LOCK DATA VALUE FOR DISCHARGE ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class RealizationForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    received_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}))
    cash=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    class Meta:
        model=Realization
        fields='__all__'
        labels={
            'patient_type':'Patient Category',
            'billing_month':'Date',
            'remarks':'Remarks (Optional)',
        }
        widgets={
            'deficit_or_surplus_amount': forms.HiddenInput(),
            'deficit_percentage': forms.HiddenInput(),
            'surplus_percentage': forms.HiddenInput(),
            'patient': forms.Select(attrs={'class':'form-control'}),
            'patient_type': forms.Select(attrs={'class':'form-control'}),
            'amount_received': forms.NumberInput(attrs={'class':'form-control'}),
            'billing_month': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request')
        super(RealizationForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.instance.pk:
            pt=self.cleaned_data['patient']
            ptt=self.cleaned_data['patient_type']
            tt=self.cleaned_data['treatment']
            print('patient type: ', ptt)
            print('treatment: ', tt)
            print(pt)
            if Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt):
                print('clean1')
                dis=Discharge.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt).order_by('-id').first()
                pkg=Package.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt).order_by('-id').first()
                rec=ApprovedPackage.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt).order_by('-id').first()
                if not dis.date_of_discharge<rec.approval_date:
                    print('bhai bhai')
                    if pkg.patient_type.patient_type!='CASH':
                        print('mera bhai')
                        if dis.discharge_updated==False:
                            raise ValidationError('This patient is yet to be claimed!')
                else:
                    if pkg.patient_type.patient_type!='CASH':
                        if self.request.POST.get('cash')==False:
                            raise ValidationError('The patient is not yet discharged!')
            else:
                try:
                    pkgpt=Package.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    if pkgpt.patient_type.patient_type!='CASH':
                        if self.request.POST.get('cash')==False:
                            raise ValidationError('The patient is not yet discharged!')
                    try:
                        ApprovedPackage.objects.get(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt)
                    except ApprovedPackage.DoesNotExist:
                        raise ValidationError('There is no ApprovedPackage value for this entry!')
                except Package.DoesNotExist:
                    raise ValidationError('There is no Package value for this entry - 2!')
            try:
                ap1=ApprovedPackage.objects.filter(patient=pt, patient_type__patient_type=ptt, treatment__treatment=tt).order_by('-id')[1]
                try:
                    RepudiatedClaims.objects.get(ipdreport__patient=pt, ipdreport__approvedpackage__approval_date=ap1.approval_date)
                    raise ValidationError('This patient is still in the Repudiated Claims Report. Please reclaim the repudiated claim first.')
                except RepudiatedClaims.DoesNotExist:
                    pass
                try:
                    ReclaimedRepudiation.objects.get(ipdreport__patient=pt, ipdreport__approvedpackage__approval_date=ap1.approval_date)
                    raise ValidationError('This patient is still in the Reclaimed Repudiation Report. Please click on "Claim Received" first.')
                except ReclaimedRepudiation.DoesNotExist:
                    pass
            except IndexError:
                pass
        else:
            print('self dot instance dot pk ka print realization clean mein: ', self.instance.pk)
            print('self dot instance ka print realization clean mein: ', self.instance)
            if LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.billing_month).order_by('id').first():
                lock=LockData.objects.filter(patient=self.instance.patient, patient_type__patient_type=self.instance.patient_type.patient_type, treatment__treatment=self.instance.treatment.treatment, date__gte=self.instance.billing_month).order_by('id').first()
                print('LOCK DATA VALUE FOR REALIZATION ', lock)
                if lock.lock==True:
                    raise ValidationError('This data is secured with a lock. To edit, please unlock it first.')
                else:
                    pass
            else:
                pass

class LockDataForm(ModelForm):
    class Meta:
        model=LockData
        fields='__all__'
        labels={
            'patient_type':'Patient Category',
        }
        widgets={

            'patient': forms.Select(attrs={'class':'form-control'}),
            'patient_type': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),

        }

class ServiceNameForm(ModelForm):
    class Meta:
        model=ServiceName
        fields='__all__'
        widgets={

           'service_name': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),

        }

class PiggyBankForm(ModelForm):
    class Meta:
        model=PiggyBank
        fields='__all__'
        widgets={

            'particulars': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),

        }

class WithdrawalForm(ModelForm):
    class Meta:
        model=Withdrawal
        # fields=('particulars', 'date', 'amount', 'bill_number', 'voucher_number', 'image', 'docs')
        exclude=['balance']
        labels={
            'particulars':'Description',
            'bill_number':'Bill Number',
            'voucher_number':'Voucher Number',
            'image':'Image File',
            'docs':'Document File'
        }
        widgets={

            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'particulars': forms.TextInput(attrs={'class':'form-control', 'autofocus':True}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
            'bill_number': forms.NumberInput(attrs={'class':'form-control'}),
            'voucher_number': forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'docs': forms.ClearableFileInput(attrs={'class':'form-control'}),

        }

class OPDCashSheetForm(ModelForm):
    MODE_SELECT = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    mode=forms.CharField(widget=forms.RadioSelect(choices=MODE_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=OPDCashSheet
        exclude=['patient', 'opd', 'cash_in', 'balance', 'bank_oopl']
        labels={
            'cash_out':'Cash-Out',
            'opd_particulars':'Description',
            'case_number':'Case Number',
            # 'bank_oopl':'To Bank',
        }
        widgets={

            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'opd_particulars': forms.Select(attrs={'class':'form-control'}),
            'source': forms.TextInput(attrs={'class':'form-control'}),
            'case_number': forms.NumberInput(attrs={'class':'form-control'}),
            'cash_out': forms.NumberInput(attrs={'class':'form-control'}),
            # 'bank_oopl': forms.NumberInput(attrs={'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

class UpdateOPDCashSheetForm(ModelForm):
    MODE_SELECT = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    mode=forms.CharField(widget=forms.RadioSelect(choices=MODE_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=OPDCashSheet
        labels={
            'cash_in':'Cash-in',
            'cash_out':'Cash-Out',
            'balance':'Cash Balance',
            'bank_oopl':'To Bank',
            'opd_particulars':'Description',
            'case_number':'Case Number',
        }
        fields='__all__'
        widgets={

            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'patient': forms.Select(attrs={'class':'form-control'}),
            'opd': forms.Select(attrs={'class':'form-control'}),
            'opd_particulars': forms.Select(attrs={'class':'form-control'}),
            'source': forms.TextInput(attrs={'class':'form-control'}),
            'case_number': forms.NumberInput(attrs={'class':'form-control'}),
            'cash_in': forms.NumberInput(attrs={'class':'form-control'}),
            'cash_out': forms.NumberInput(attrs={'class':'form-control'}),
            'balance': forms.NumberInput(attrs={'class':'form-control'}),
            'bank_oopl': forms.NumberInput(attrs={'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

class BankDepositsForm(ModelForm):
    MODE_SELECT = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
    )
    mode=forms.CharField(widget=forms.RadioSelect(choices=MODE_SELECT, attrs={'class': 'form-check-inline'}))
    class Meta:
        model=BankDeposits
        labels={

            'opdcashsheet':'OPD Cash',
            'bank_ac':'Bank A/c',
        }
        fields='__all__'
        widgets={

            'opdcashsheet': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
            'bank': forms.TextInput(attrs={'class':'form-control'}),
            'bank_ac': forms.TextInput(attrs={'class':'form-control'}),
            'branch': forms.TextInput(attrs={'class':'form-control'}),
            'remarks': forms.Textarea(attrs={'class':'form-control'}),

        }

class PaxMaxForm(ModelForm):
    class Meta:
        model=PaxMax
        labels={

            'patient_type':'Patient Category',
            'max_fractions':'Fractions',
            'total_package':'Total Cost',
        }
        fields='__all__'
        widgets={

           'treatment': forms.Select(attrs={'class':'form-control'}),
           'patient_type': forms.Select(attrs={'class':'form-control'}),
           'max_fractions': forms.NumberInput(attrs={'class':'form-control'}),
           'total_package': forms.NumberInput(attrs={'class':'form-control'}),

        }

class OtherIncomeForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    received_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}), label="Received By")
    class Meta:
        model=OtherIncome
        fields='__all__'
        labels={
            'particulars':'Description',
        }
        widgets={

            'particulars': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),

        }

class AdditionalIncomeForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    received_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}), label="Received By")
    class Meta:
        model=AdditionalIncome
        fields='__all__'
        labels={
            'particulars':'Description',
        }
        widgets={

            'particulars': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),

        }

class OtherExpensesForm(ModelForm):
    PARTY_SELECT = (
        ('s', 'SCC'),
        ('o', 'OOPL'),
    )
    paid_by=forms.CharField(widget=forms.RadioSelect(choices=PARTY_SELECT, attrs={'class': 'form-check-inline'}), label="Paid By")
    class Meta:
        model=OtherExpenses
        fields='__all__'
        labels={
            'particulars':'Description',
        }
        widgets={

            'particulars': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),

        }

class BillGateway(forms.Form):
    from_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), label='From ')
    to_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), label='To ')
    billing_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'from'}), label='Date of Billing ')

class AdditionalFields(forms.Form):
    change_rt_cash_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (SCC) Description', required=False)
    change_rt_cash_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (SCC) Amount", required=False)
    change_rt_cash_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (OOPL) Description', required=False)
    change_rt_cash_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (OOPL) Amount", required=False)
    change_partial_cash_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (SCC) Description', required=False)
    change_partial_cash_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (SCC) Amount", required=False)
    change_partial_cash_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (OOPL) Description', required=False)
    change_partial_cash_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (OOPL) Amount", required=False)
    change_mjpjay_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (SCC) Description', required=False)
    change_mjpjay_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (SCC) Amount", required=False)
    change_mjpjay_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (OOPL) Description', required=False)
    change_mjpjay_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (OOPL) Amount", required=False)
    change_pmjay_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (SCC) Description', required=False)
    change_pmjay_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (SCC) Amount", required=False)
    change_pmjay_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (OOPL) Description', required=False)
    change_pmjay_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (OOPL) Amount", required=False)
    change_police_file_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (SCC) Description', required=False)
    change_police_file_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (SCC) Amount", required=False)
    change_police_file_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (OOPL) Description', required=False)
    change_police_file_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (OOPL) Amount", required=False)
    change_insurance_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (SCC) Description', required=False)
    change_insurance_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (SCC) Amount", required=False)
    change_insurance_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (OOPL) Description', required=False)
    change_insurance_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (OOPL) Amount", required=False)
    change_other_income_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (SCC) Description', required=False)
    change_other_income_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (SCC) Amount", required=False)
    change_other_income_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (OOPL) Description', required=False)
    change_other_income_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (OOPL) Amount", required=False)
    change_ct_scc_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (SCC) Description', required=False)
    change_ct_scc_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (SCC) Amount", required=False)
    change_ct_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (OOPL) Description', required=False)
    change_ct_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (OOPL) Amount", required=False)
    change_mould_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (OOPL) Description', required=False)
    change_mould_oopl_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (OOPL) Amount", required=False)
    change_mould_scc_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (SCC) Description', required=False)
    change_mould_scc_amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (SCC) Amount", required=False)
    change_additional_income_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (SCC) Description', required=False)
    scc_share_add_in1=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_additional_income_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (OOPL) Description', required=False)
    scc_share_add_in2=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (SCC) Description', required=False)
    scc_share_other_expenses1=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_oopl_desc=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (OOPL) Description', required=False)
    scc_share_other_expenses2=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)

class QuarterlyBills(forms.Form):
    quarters=[
        ('q1', 'Quarter 1st'),
        ('q2', 'Quarter 2nd'),
        ('q3', 'Quarter 3rd'),
        ('q4', 'Quarter 4th'),
    ]
    financial_years=[
        ('2021-2022', '2021-22'),
        ('2022-2023', '2022-23'),
        ('2023-2024', '2023-24'),
        ('2024-2025', '2024-25'),
        ('2025-2026', '2025-26'),
        ('2026-2027', '2026-27'),
        ('2027-2028', '2027-28'),
        ('2028-2029', '2028-29'),
        ('2029-2030', '2029-30'),
    ]
    choose_quarter=forms.CharField(label='Choose Quarter', widget=forms.Select(choices=quarters, attrs={'class':'form-control'}))
    choose_financial_year=forms.CharField(label='Choose Financial Year', widget=forms.Select(choices=financial_years, attrs={'class':'form-control'}))
    billing_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id': 'to'}), label='Date of Billing ', label_suffix=' - ')

class AdditionalFieldsFirstMonth(forms.Form):
    change_amount_credited_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Edit Amount Credited')
    change_rt_cash_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (SCC) Description', required=False)
    change_rt_cash_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (SCC) Amount", required=False)
    change_rt_cash_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (OOPL) Description', required=False)
    change_rt_cash_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (OOPL) Amount", required=False)
    change_partial_cash_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (SCC) Description', required=False)
    change_partial_cash_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (SCC) Amount", required=False)
    change_partial_cash_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (OOPL) Description', required=False)
    change_partial_cash_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (OOPL) Amount", required=False)
    change_mjpjay_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (SCC) Description', required=False)
    change_mjpjay_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (SCC) Amount", required=False)
    change_mjpjay_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (OOPL) Description', required=False)
    change_mjpjay_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (OOPL) Amount", required=False)
    change_pmjay_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (SCC) Description', required=False)
    change_pmjay_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (SCC) Amount", required=False)
    change_pmjay_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (OOPL) Description', required=False)
    change_pmjay_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (OOPL) Amount", required=False)
    change_police_file_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (SCC) Description', required=False)
    change_police_file_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (SCC) Amount", required=False)
    change_police_file_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (OOPL) Description', required=False)
    change_police_file_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (OOPL) Amount", required=False)
    change_insurance_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (SCC) Description', required=False)
    change_insurance_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (SCC) Amount", required=False)
    change_insurance_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (OOPL) Description', required=False)
    change_insurance_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (OOPL) Amount", required=False)
    change_other_income_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (SCC) Description', required=False)
    change_other_income_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (SCC) Amount", required=False)
    change_other_income_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (OOPL) Description', required=False)
    change_other_income_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (OOPL) Amount", required=False)
    change_ct_scc_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (SCC) Description', required=False)
    change_ct_scc_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (SCC) Amount", required=False)
    change_ct_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (OOPL) Description', required=False)
    change_ct_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (OOPL) Amount", required=False)
    change_mould_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (OOPL) Description', required=False)
    change_mould_oopl_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (OOPL) Amount", required=False)
    change_mould_scc_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (SCC) Description', required=False)
    change_mould_scc_amount_first_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (SCC) Amount", required=False)
    change_additional_income_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (SCC) Description', required=False)
    scc_share_add_in1_first_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_additional_income_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (OOPL) Description', required=False)
    scc_share_add_in2_first_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (SCC) Description', required=False)
    scc_share_other_expenses1_first_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_oopl_desc_first_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (OOPL) Description', required=False)
    scc_share_other_expenses2_first_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)

class AdditionalFieldsSecondMonth(forms.Form):
    change_amount_credited_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label='Edit Amount Credited')
    change_rt_cash_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (SCC) Description', required=False)
    change_rt_cash_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (SCC) Amount", required=False)
    change_rt_cash_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (OOPL) Description', required=False)
    change_rt_cash_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (OOPL) Amount", required=False)
    change_partial_cash_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (SCC) Description', required=False)
    change_partial_cash_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (SCC) Amount", required=False)
    change_partial_cash_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (OOPL) Description', required=False)
    change_partial_cash_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (OOPL) Amount", required=False)
    change_mjpjay_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (SCC) Description', required=False)
    change_mjpjay_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (SCC) Amount", required=False)
    change_mjpjay_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (OOPL) Description', required=False)
    change_mjpjay_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (OOPL) Amount", required=False)
    change_pmjay_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (SCC) Description', required=False)
    change_pmjay_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (SCC) Amount", required=False)
    change_pmjay_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (OOPL) Description', required=False)
    change_pmjay_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (OOPL) Amount", required=False)
    change_police_file_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (SCC) Description', required=False)
    change_police_file_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (SCC) Amount", required=False)
    change_police_file_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (OOPL) Description', required=False)
    change_police_file_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (OOPL) Amount", required=False)
    change_insurance_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (SCC) Description', required=False)
    change_insurance_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (SCC) Amount", required=False)
    change_insurance_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (OOPL) Description', required=False)
    change_insurance_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (OOPL) Amount", required=False)
    change_other_income_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (SCC) Description', required=False)
    change_other_income_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (SCC) Amount", required=False)
    change_other_income_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (OOPL) Description', required=False)
    change_other_income_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (OOPL) Amount", required=False)
    change_ct_scc_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (SCC) Description', required=False)
    change_ct_scc_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (SCC) Amount", required=False)
    change_ct_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (OOPL) Description', required=False)
    change_ct_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (OOPL) Amount", required=False)
    change_mould_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (OOPL) Description', required=False)
    change_mould_oopl_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (OOPL) Amount", required=False)
    change_mould_scc_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (SCC) Description', required=False)
    change_mould_scc_amount_second_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (SCC) Amount", required=False)
    change_additional_income_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (SCC) Description', required=False)
    scc_share_add_in1_second_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_additional_income_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (OOPL) Description', required=False)
    scc_share_add_in2_second_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (SCC) Description', required=False)
    scc_share_other_expenses1_second_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_oopl_desc_second_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (OOPL) Description', required=False)
    scc_share_other_expenses2_second_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)

class AdditionalFieldsThirdMonth(forms.Form):
    change_rt_cash_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (SCC) Description', required=False)
    change_rt_cash_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (SCC) Amount", required=False)
    change_rt_cash_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit RT Cash (OOPL) Description', required=False)
    change_rt_cash_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit RT Cash (OOPL) Amount", required=False)
    change_partial_cash_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (SCC) Description', required=False)
    change_partial_cash_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (SCC) Amount", required=False)
    change_partial_cash_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Partial Cash (OOPL) Description', required=False)
    change_partial_cash_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Partial Cash (OOPL) Amount", required=False)
    change_mjpjay_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (SCC) Description', required=False)
    change_mjpjay_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (SCC) Amount", required=False)
    change_mjpjay_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit MJPJAY (OOPL) Description', required=False)
    change_mjpjay_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit MJPJAY (OOPL) Amount", required=False)
    change_pmjay_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (SCC) Description', required=False)
    change_pmjay_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (SCC) Amount", required=False)
    change_pmjay_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit PMJAY (OOPL) Description', required=False)
    change_pmjay_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit PMJAY (OOPL) Amount", required=False)
    change_police_file_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (SCC) Description', required=False)
    change_police_file_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (SCC) Amount", required=False)
    change_police_file_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Police File (OOPL) Description', required=False)
    change_police_file_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Police File (OOPL) Amount", required=False)
    change_insurance_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (SCC) Description', required=False)
    change_insurance_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (SCC) Amount", required=False)
    change_insurance_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Insurance (OOPL) Description', required=False)
    change_insurance_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Insurance (OOPL) Amount", required=False)
    change_other_income_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (SCC) Description', required=False)
    change_other_income_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (SCC) Amount", required=False)
    change_other_income_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Income (OOPL) Description', required=False)
    change_other_income_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Other Income (OOPL) Amount", required=False)
    change_ct_scc_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (SCC) Description', required=False)
    change_ct_scc_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (SCC) Amount", required=False)
    change_ct_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit CT (OOPL) Description', required=False)
    change_ct_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit CT (OOPL) Amount", required=False)
    change_mould_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (OOPL) Description', required=False)
    change_mould_oopl_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (OOPL) Amount", required=False)
    change_mould_scc_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Mould (SCC) Description', required=False)
    change_mould_scc_amount_third_month=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Edit Mould (SCC) Amount", required=False)
    change_additional_income_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (SCC) Description', required=False)
    scc_share_add_in1_third_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_additional_income_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Additional Income (OOPL) Description', required=False)
    scc_share_add_in2_third_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (SCC) Description', required=False)
    scc_share_other_expenses1_third_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)
    change_other_expenses_oopl_desc_third_month=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Edit Other Expenses (OOPL) Description', required=False)
    scc_share_other_expenses2_third_month=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="SCC's Share (%)", required=False)