from django.db import models
from django.core.validators import RegexValidator
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
import datetime

class Patient(models.Model):
    title=models.CharField(max_length=11)
    gender=models.CharField(max_length=11)
    name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=13, default=None, blank=True, null=True)
    alternate_phone_number=models.CharField(max_length=13, default=None, blank=True, null=True)
    center=models.CharField(max_length=7, default='Dhule')
    mr_uid=models.IntegerField(default=None)

    @property
    def patient_number(self):
        if self.pk:
            return "{}{:d}".format('PN/D/', self.pk)
        else:
            return ""

    def __str__(self):
        return "{}{}{}".format(self.name,' - ', self.patient_number)

class ServiceName(models.Model):
    service_name=models.CharField(max_length=150)

    def __str__(self):
        return self.service_name

class Opd(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    bill_number=models.IntegerField(default=None)
    date=models.DateField(default=datetime.date.today)
    service_name=models.ForeignKey(ServiceName, on_delete=SET_NULL, null=True)
    amount=models.DecimalField(max_digits=7, decimal_places=2)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    opd_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class Diagnosis(models.Model):
    diagnosis=models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.diagnosis

class Treatment(models.Model):
    treatment=models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.treatment

class PatientType(models.Model):
    patient_type=models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.patient_type

class PaxMax(models.Model):
    treatment=models.ForeignKey(Treatment, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE)
    max_fractions=models.IntegerField()
    total_package=models.DecimalField(max_digits=10, decimal_places=2)

class Package(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    diagnosis=models.ForeignKey(Diagnosis, on_delete=CASCADE)
    treatment=models.ForeignKey(Treatment, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE)
    date_of_admission=models.DateField(default=datetime.date.today)
    max_fractions=models.IntegerField()
    total_package=models.DecimalField(max_digits=10, decimal_places=2)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    package_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class ApprovedPackage(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None)
    discount=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    approved_package=models.DecimalField(max_digits=10, decimal_places=2)
    approval_date=models.DateField(default=datetime.date.today)
    proposed_fractions=models.IntegerField()
    remarks=models.TextField(max_length=500, blank=True, default=None)
    approved_package_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

    """date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)"""

class CTScan(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None)
    pattern = RegexValidator(r'(RT|rt|rT|Rt)\/[0-9]{4}\/[0-9]{2}\/[0-9]{4}', 'Enter RT Number properly!')
    rt_number=models.CharField(max_length=15, validators=[pattern], default=None)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date=models.DateField(default=datetime.date.today)
    conducted_by=models.CharField(max_length=4, default=None)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    ctscan_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class Radiations(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None)
    date=models.DateField(default=datetime.date.today)
    done_fractions=models.IntegerField(default=0)
    base_value=models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=None)
    expected_value=models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=None)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    radiations_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

    @property
    def package(self):
        try:
            return Package.objects.filter(patient=self.patient, patient_type=self.patient_type).order_by('-id').first()
        except Package.DoesNotExist:
            return None
    
    @property
    def approved(self):
        try:
            return ApprovedPackage.objects.filter(patient=self.patient, patient_type=self.patient_type, approval_date__gte=self.package.date_of_admission).order_by('-id').first()
        except ApprovedPackage.DoesNotExist:
            return None

    def calculate_base_value(self):
        if (self.package):
            process_charge=self.package.total_package*15/100
            net_total_package=self.package.total_package - process_charge
            amount_per_fraction=net_total_package/self.package.max_fractions
            net_cost=amount_per_fraction*self.done_fractions
            gross_cost=net_cost+process_charge
            self.base_value=gross_cost
        else:
            self.base_value=self.approved_package

    def calculate_expected_value(self):
        if self.approved:
            if self.expected_value:
                if not self.expected_value <= 0:
                    if self.base_value<self.approved.approved_package:
                        self.expected_value=self.base_value
                    else:
                        self.expected_value=self.approved.approved_package
                else:
                    print('Expected ka value: ', self.expected_value*-1)
                    return self.expected_value
            else:
                if self.base_value<self.approved.approved_package:
                    self.expected_value=self.base_value
                else:
                    self.expected_value=self.approved.approved_package

    def save(self, *args, **kwargs):
        self.calculate_base_value()
        self.calculate_expected_value()
        print('Radiations model mein save method ke andar se expected value: ', self.calculate_expected_value())
        super(Radiations, self).save(*args, **kwargs)

class Discharge(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None)
    date_of_discharge=models.DateField(default=datetime.date.today)
    discharge_updated=models.BooleanField(default=False)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    discharge_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class Realization(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None)
    cash=models.BooleanField(default=False)
    amount_received=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received_by=models.CharField(max_length=4, default=None)
    billing_month=models.DateField(default=datetime.date.today)
    deficit_or_surplus_amount=models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    deficit_percentage=models.FloatField(blank=True, default=0)
    surplus_percentage=models.FloatField(blank=True, default=0)
    remarks=models.TextField(max_length=500, blank=True, default=None)
    realization_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

    @property
    def radiations(self):
        try:
            return Radiations.objects.filter(patient=self.patient, patient_type=self.patient_type).order_by('-id').first()
        except Radiations.DoesNotExist:
            return None
    
    @property
    def radiations_old(self):
        try:
            return Radiations.objects.filter(patient=self.patient, patient_type=self.patient_type, radiations_date__lte=self.realization_date).order_by('-id').first()
        except Radiations.DoesNotExist:
            return None

    @property
    def discharge(self):
        try:
            return Discharge.objects.filter(patient=self.patient, patient_type=self.patient_type).order_by('-id').first()
        except Discharge.DoesNotExist:
            return None

    @property
    def package(self):
        try:
            return Package.objects.filter(patient=self.patient, patient_type=self.patient_type).order_by('-id').first()
        except Package.DoesNotExist:
            return None

    def calculate_deficit_surplus_amount(self):
        if not self.id:
            if (self.radiations):
                if self.radiations.expected_value<0:
                    print('1. calculate_deficit_surplus_amount wala instance: ', self.radiations)
                    self.deficit_or_surplus_amount=self.amount_received-(self.radiations.expected_value*-1)
                else:
                    self.deficit_or_surplus_amount=self.amount_received-self.radiations.expected_value
            else:
                self.deficit_or_surplus_amount=0
        else:
            print('Hello 23')
            if (self.radiations_old):
                print('Hello 24')
                if self.radiations_old.expected_value<0:
                    print('Hello 25')
                    self.deficit_or_surplus_amount=self.amount_received-(self.radiations_old.expected_value*-1)
                else:
                    print('Hello 26')
                    self.deficit_or_surplus_amount=self.amount_received-self.radiations_old.expected_value
            else:
                print('Hello 27')
                self.deficit_or_surplus_amount=0

    def calculate_deficit_or_surplus_percentage(self):
        if not self.id:
            if (self.radiations):
                if self.radiations.expected_value<0:
                    if self.amount_received>(self.radiations.expected_value*-1):
                        self.surplus_percentage=self.deficit_or_surplus_amount/(self.radiations.expected_value*-1)*100
                    elif self.amount_received<(self.radiations.expected_value*-1):
                        self.deficit_percentage=self.deficit_or_surplus_amount/(self.radiations.expected_value*-1)*100
                    elif self.amount_received==(self.radiations.expected_value*-1):
                        self.deficit_percentage=0
                else:
                    if self.amount_received>self.radiations.expected_value:
                        self.surplus_percentage=self.deficit_or_surplus_amount/self.radiations.expected_value*100
                    elif self.amount_received<self.radiations.expected_value:
                        self.deficit_percentage=self.deficit_or_surplus_amount/self.radiations.expected_value*100
                    elif self.amount_received==self.radiations.expected_value:
                        self.deficit_percentage=0
            else:
                self.surplus_percentage=0
        else:
            print('Hello 28')
            if (self.radiations_old):
                print('Hello 29')
                if self.radiations_old.expected_value<0:
                    print('Hello 30')
                    if self.amount_received>(self.radiations_old.expected_value*-1):
                        print('Hello 31')
                        self.surplus_percentage=self.deficit_or_surplus_amount/(self.radiations_old.expected_value*-1)*100
                        if self.surplus_percentage !=0:
                            print('Hello 32')
                            self.deficit_percentage=0
                    elif self.amount_received<(self.radiations_old.expected_value*-1):
                        print('Hello 33')
                        self.deficit_percentage=self.deficit_or_surplus_amount/(self.radiations_old.expected_value*-1)*100
                        if self.deficit_percentage!=0:
                            print('Hello 34')
                            self.surplus_percentage=0
                    elif self.amount_received==(self.radiations_old.expected_value*-1):
                        print('Hello 35')
                        self.deficit_percentage=0
                else:
                    print('Hello 36')
                    if self.amount_received>self.radiations_old.expected_value:
                        print('Hello 37')
                        self.surplus_percentage=self.deficit_or_surplus_amount/self.radiations_old.expected_value*100
                        if self.surplus_percentage !=0:
                            print('Hello 38')
                            self.deficit_percentage=0
                    elif self.amount_received<self.radiations_old.expected_value:
                        print('Hello 39')
                        self.deficit_percentage=self.deficit_or_surplus_amount/self.radiations_old.expected_value*100
                        if self.deficit_percentage!=0:
                            print('Hello 40')
                            self.surplus_percentage=0
                    elif self.amount_received==self.radiations_old.expected_value:
                        print('Hello 41')
                        self.deficit_percentage=0
            else:
                print('Hello 42')
                self.surplus_percentage=0

    def save(self, *args, **kwargs):
        print('Hello 43')
        self.calculate_deficit_surplus_amount()
        print('Hello 44')
        self.calculate_deficit_or_surplus_percentage()
        print('Hello 45')
        super(Realization, self).save(*args, **kwargs) # call save in ancestror

class LockData(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE, default=None)
    patient_type=models.ForeignKey(PatientType, on_delete=CASCADE, default=None, blank=True, null=True)
    lock=models.BooleanField(default=False)
    date=models.DateField(default=datetime.date.today)
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class CommonExpenses(models.Model):
    particulars=models.CharField(max_length=150, default='MOULD')
    date=models.DateField(default=datetime.date.today)
    paid_by=models.CharField(max_length=11)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    common_expenses_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class OtherIncome(models.Model):
    particulars=models.CharField(max_length=150)
    date=models.DateField(default=datetime.date.today)
    received_by=models.CharField(max_length=11)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class AdditionalIncome(models.Model):
    particulars=models.CharField(max_length=150)
    date=models.DateField(default=datetime.date.today)
    received_by=models.CharField(max_length=11)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class OtherExpenses(models.Model):
    particulars=models.CharField(max_length=150)
    date=models.DateField(default=datetime.date.today)
    paid_by=models.CharField(max_length=11)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class IpdReport(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    package=models.ForeignKey(Package, on_delete=CASCADE, blank=True, null=True)
    approvedpackage=models.ForeignKey(ApprovedPackage, on_delete=CASCADE, blank=True, null=True)
    ctscan=models.ForeignKey(CTScan, on_delete=CASCADE, blank=True, null=True)
    radiations=models.ForeignKey(Radiations, on_delete=CASCADE, blank=True, null=True)
    discharge=models.ForeignKey(Discharge, on_delete=CASCADE, blank=True, null=True)
    realization=models.ForeignKey(Realization, on_delete=CASCADE, blank=True, null=True)
    lockdata=models.ForeignKey(LockData, on_delete=CASCADE, blank=True, null=True)

    @property
    def track_id(self):
        if self.pk:
            return "{}{:d}".format('OOPL/D/', self.pk)
        else:
            return ""
    @property
    def previous(self):
        # print('self ka value: ', self)
        print()
        ipd=IpdReport.objects.filter(patient=self.patient).order_by('id')
        for obj in ipd:
            # print('obj ka value: ', obj)
            if self.id==obj.id:
                newer=IpdReport.objects.filter(id__lt=obj.id, patient=obj.patient).order_by('id').last()
                print('newer ka value ', newer.package.patient_type)
                print('self ka value ', self.package.patient_type)
        return newer

class OpdReport(models.Model):
    patient=models.ForeignKey(Patient, on_delete=CASCADE)
    opd=models.ForeignKey(Opd, on_delete=CASCADE)

    @property
    def track_id(self):
        if self.pk:
            return "{}{:d}".format('OPD/D/', self.pk)
        else:
            return ""

class OngoingReport(models.Model):
    ipdreport=models.ForeignKey(IpdReport, on_delete=CASCADE)

class RepudiatedClaims(models.Model):
    ipdreport=models.ForeignKey(IpdReport, on_delete=CASCADE)

class ClaimedPendingCases(models.Model):
    ipdreport=models.ForeignKey(IpdReport, on_delete=CASCADE)

class UnclaimedPendingCases(models.Model):
    ipdreport=models.ForeignKey(IpdReport, on_delete=CASCADE)

class ReclaimedRepudiation(models.Model):
    ipdreport=models.ForeignKey(IpdReport, on_delete=CASCADE, blank=True, null=True)

class Depositor(models.Model):
    depositor=models.CharField(max_length=100)

    def __str__(self):
        return self.depositor

class PiggyBank(models.Model):
    depositor=models.ForeignKey(Depositor, on_delete=CASCADE)
    date=models.DateField(default=datetime.date.today)
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

class Withdrawal(models.Model):
    depositor=models.ForeignKey(Depositor, on_delete=CASCADE, default=None)
    date=models.DateField(default=datetime.date.today)
    particulars=models.CharField(max_length=200, null=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_number=models.IntegerField(null=True)
    voucher_number=models.IntegerField(null=True)
    image=models.ImageField(upload_to='Petty Cash/Images', blank=True)
    docs=models.FileField(upload_to='Petty Cash/Docs', blank=True)
    upload_date=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)

    def recalculate_balance(self):
        if self.amount is not None:
            wd=Withdrawal.objects.all().order_by('-id').first()
            self.balance=wd.balance-self.amount

    def save(self, *args, **kwargs):
        self.recalculate_balance()
        super(Withdrawal, self).save(*args, **kwargs)

class PettyCash(models.Model):
    piggybank=models.ForeignKey(PiggyBank, on_delete=CASCADE, blank=True, null=True)
    withdrawal=models.ForeignKey(Withdrawal, on_delete=CASCADE, blank=True, null=True)