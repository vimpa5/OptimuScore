from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.http import request
from .models import *
from django.http.request import QueryDict
from .forms import RadiationsForm, RealizationForm, RadiationsForm

@receiver(post_save, sender=Realization)
def new_approved_package_save(sender, instance, created, **kwargs):
    pkg=Package.objects.filter(patient=instance.patient, patient_type=instance.patient_type).order_by('-id').first()
    rad=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, date__gte=pkg.date_of_admission).order_by('-id').first()
    if created:
        print('Naya hai Yah')
        if pkg.patient_type.patient_type!='CASH' and instance.cash==False:
            if instance.deficit_or_surplus_amount<=0:
                Radiations(patient=rad.patient, patient_type=rad.patient_type, date=rad.date, done_fractions=rad.done_fractions, base_value=rad.base_value, expected_value=instance.deficit_or_surplus_amount, remarks=rad.remarks).save()
    else:
        print('Not a new instance.')
        print(pkg.patient_type)
        print(instance.patient_type)
        print(instance.patient)
        print(instance.realization_date)
        print(instance.cash)
        print(instance.deficit_or_surplus_amount)
        if pkg.patient_type.patient_type!='CASH' and instance.cash==False:
            print('Yahaan tak aa gaya ab')
            if instance.deficit_or_surplus_amount<=0:
                rad1=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, radiations_date__gte=instance.realization_date).order_by('id').first()
                print('rad1 ka value signal mein: ', rad1)
                print('rad1 ka expected value signal mein: ', rad1.expected_value)
                my_dict={'patient':rad1.patient.id, 'patient_type':rad1.patient_type, 'date':rad1.date, 'done_fractions':rad1.done_fractions, 'base_value':rad1.base_value, 'expected_value':instance.deficit_or_surplus_amount, 'remarks':rad1.remarks}
                data_to_update=QueryDict('', mutable=True)
                data_to_update.update(my_dict)
                print('querydict ka value apna waala: ', data_to_update)
                form=RadiationsForm(data_to_update, instance=rad1, request=request)
                if form.is_valid():
                    rad2=form.save()
                    print('rad 2 ka value: ', rad2)
                    print('rad 2 ka expected value: ', rad2.expected_value)
                    rad3=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, radiations_date__lt=instance.realization_date).order_by('-id').first()
                    print('rad3 ka value: ', rad3)
                    print('rad3 mein expected ka value: ', rad3.expected_value)
                    all_real=Realization.objects.filter(patient=instance.patient, patient_type=instance.patient_type, realization_date__gt=instance.realization_date).order_by('id')
                    print('all real ka value: ', all_real)
                    for realized in all_real:
                        new_deficit_value=realized.amount_received-(rad2.expected_value*-1)
                        print('new deficit value: ', new_deficit_value)
                        new_surplus_percentage=0
                        new_deficit_percentage=0
                        if rad3.expected_value<0:
                            if realized.amount_received>(rad2.expected_value*-1):
                                new_surplus_percentage=new_deficit_value/(rad2.expected_value*-1)*100
                            elif realized.amount_received<(rad2.expected_value*-1):
                                new_deficit_percentage=new_deficit_value/(rad2.expected_value*-1)*100
                            elif realized.amount_received==(rad2.expected_value*-1):
                                new_deficit_percentage=0
                        else:
                            if realized.amount_received>(rad2.expected_value):
                                new_surplus_percentage=new_deficit_value/(rad2.expected_value)*100
                            elif realized.amount_received<(rad2.expected_value):
                                new_deficit_percentage=new_deficit_value/(rad2.expected_value)*100
                            elif realized.amount_received==(rad2.expected_value):
                                new_deficit_percentage=0
                        print('new surplus percent: ', new_surplus_percentage)
                        print('new deficit percent: ', new_deficit_percentage)
                        my_real_dict={'patient':realized.patient.id, 'patient_type':realized.patient_type, 'cash':realized.cash, 'amount_received':realized.amount_received, 'received_by':realized.received_by, 'billing_month':realized.billing_month, 'deficit_or_surplus_amount':new_deficit_value, 'deficit_percentage':new_deficit_percentage, 'surplus_percentage':new_surplus_percentage, 'remarks':realized.remarks}
                        real_data_to_update=QueryDict('', mutable=True)
                        real_data_to_update.update(my_real_dict)
                        print('realization ke querydict ka value apna waala: ', real_data_to_update)
                        form_real=RealizationForm(real_data_to_update, instance=realized, request=request)
                        # print('Hello 27', form_real)
                        if form_real.is_valid():
                            print('Hello 46')
                            real2=form_real.save()
                            print('real2 ka value signal mein: ', real2)

@receiver(post_save, sender=PiggyBank)
def balance_update(sender, instance, created, **kwargs):
    wd=Withdrawal.objects.all().order_by('-id').first()
    print('wd ka value: ', wd)
    if created:
        if wd is not None:
            Withdrawal(depositor=instance.depositor, date=instance.date, particulars=None, amount=None, balance=wd.balance+instance.amount, voucher_number=None).save()
            print('The End adding balance')
        else:
            Withdrawal(depositor=instance.depositor, date=instance.date, particulars=None, amount=None, balance=instance.amount, voucher_number=None).save()
            print('The End adding balance')