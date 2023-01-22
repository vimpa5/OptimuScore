from datetime import date
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.http import request
from .models import *
from django.http.request import QueryDict
from .forms import RadiationsForm, RealizationForm, BankDepositsForm, UpdateOPDCashSheetForm

@receiver(post_save, sender=Realization)
def new_approved_package_save(sender, instance, created, **kwargs):
    pkg=Package.objects.filter(patient=instance.patient, patient_type=instance.patient_type, treatment=instance.treatment).order_by('-id').first()
    rad=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, treatment=instance.treatment, date__gte=pkg.date_of_admission).order_by('-id').first()
    if created:
        print('Naya hai Yah')
        if pkg.patient_type.patient_type!='CASH' and instance.cash==False:
            if instance.deficit_or_surplus_amount<=0:
                Radiations(patient=rad.patient, patient_type=rad.patient_type, treatment=rad.treatment, date=rad.date, done_fractions=rad.done_fractions, base_value=rad.base_value, expected_value=instance.deficit_or_surplus_amount, remarks=rad.remarks).save()
    else:
        print('Not a new instance.')
        print(pkg.patient_type)
        print(instance.patient_type)
        print(instance.treatment)
        print(instance.patient)
        print(instance.realization_date)
        print(instance.cash)
        print(instance.deficit_or_surplus_amount)
        if pkg.patient_type.patient_type!='CASH' and instance.cash==False:
            print('Yahaan tak aa gaya ab')
            if instance.deficit_or_surplus_amount<=0:
                rad1=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, treatment=instance.treatment, radiations_date__gte=instance.realization_date).order_by('id').first()
                print('rad1 ka value signal mein: ', rad1)
                print('rad1 ka expected value signal mein: ', rad1.expected_value)
                my_dict={'patient':rad1.patient.id, 'patient_type':rad1.patient_type, 'treatment':rad1.treatment, 'date':rad1.date, 'done_fractions':rad1.done_fractions, 'base_value':rad1.base_value, 'expected_value':instance.deficit_or_surplus_amount, 'remarks':rad1.remarks}
                data_to_update=QueryDict('', mutable=True)
                data_to_update.update(my_dict)
                print('querydict ka value apna waala: ', data_to_update)
                form=RadiationsForm(data_to_update, instance=rad1, request=request)
                if form.is_valid():
                    rad2=form.save()
                    print('rad 2 ka value: ', rad2)
                    print('rad 2 ka expected value: ', rad2.expected_value)
                    rad3=Radiations.objects.filter(patient=instance.patient, patient_type=instance.patient_type, treatment=instance.treatment, radiations_date__lt=instance.realization_date).order_by('-id').first()
                    print('rad3 ka value: ', rad3)
                    print('rad3 mein expected ka value: ', rad3.expected_value)
                    all_real=Realization.objects.filter(patient=instance.patient, patient_type=instance.patient_type, treatment=instance.treatment, realization_date__gt=instance.realization_date).order_by('id')
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
                        my_real_dict={'patient':realized.patient.id, 'patient_type':realized.patient_type, 'treatment':realized.treatment, 'cash':realized.cash, 'amount_received':realized.amount_received, 'received_by':realized.received_by, 'billing_month':realized.billing_month, 'deficit_or_surplus_amount':new_deficit_value, 'deficit_percentage':new_deficit_percentage, 'surplus_percentage':new_surplus_percentage, 'remarks':realized.remarks}
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
            Withdrawal(date=instance.date, particulars=None, amount=None, balance=wd.balance+instance.amount, voucher_number=None).save()
            print('The End adding balance')
        else:
            Withdrawal(date=instance.date, particulars=None, amount=None, balance=instance.amount, voucher_number=None).save()
            print('The End adding balance')

@receiver(pre_save, sender=Opd)
def opd_pre_save(sender, instance, **kwargs):
    try:
        _pre_save_instance = Opd.objects.get(pk=instance.pk)
        instance._pre_save_amount=_pre_save_instance.amount
        instance._pre_save_mode=_pre_save_instance.mode
    except Opd.DoesNotExist:
        instance._pre_save_amount = instance.amount
        instance._pre_save_mode = instance.mode


@receiver(signal=post_save, sender=Opd)
def opd_post_save(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        _pre_save_amount = instance._pre_save_amount
        post_save_amount = instance.amount
        _pre_save_mode = instance._pre_save_mode
        post_save_mode = instance.mode
        print()
        print('instance type: ', type(instance))
        print()
        print('instance: ', instance)
        print()
        print('_pre_save_amount ', _pre_save_amount)
        print('post_save_amount ', post_save_amount)
        if _pre_save_amount!=post_save_amount:
            if post_save_mode=='cash' and _pre_save_mode=='cash':
                try:
                    opd1=OPDCashSheet.objects.get(opd=instance.id, date=instance.date, patient=instance.patient)
                    # opd_prev=OPDCashSheet.objects.filter(id__lt=opd1.id)|OPDCashSheet.objects.filter(date__lt=instance.date)
                    opd_prev=OPDCashSheet.objects.order_by('date').first()
                    if opd1!=opd_prev:
                        diff=_pre_save_amount-post_save_amount
                        new_bal=opd1.balance-diff
                        opd_dict={'date':opd1.date, 'patient':opd1.patient.id, 'opd':opd1.opd.id, 'source':opd1.source, 'case_number':opd1.case_number, 'mode':opd1.mode, 'cash_in':instance.amount, 'cash_out':opd1.cash_out, 'balance':new_bal, 'bank_oopl':opd1.bank_oopl, 'remarks':opd1.remarks}
                        opd_data_to_update=QueryDict('', mutable=True)
                        opd_data_to_update.update(opd_dict)
                        form_opd=UpdateOPDCashSheetForm(opd_data_to_update, instance=opd1)
                        # print('Hello 025', form_opd)
                        print('Hello 025')
                        if form_opd.is_valid():
                            print('hello 026')
                            opd2=form_opd.save()
                            try:
                                opd3=OPDCashSheet.objects.filter(id__gt=opd2.id, date__gte=opd2.date, created_on__gt=opd2.created_on).order_by('date')
                                for opd in opd3:
                                    new_bal1=opd.balance-diff
                                    opd_dict_1={'date':opd.date, 'patient':opd.patient.id, 'opd':opd.opd.id, 'source':opd.source, 'case_number':opd.case_number, 'mode':opd.mode, 'cash_in':opd.cash_in, 'cash_out':opd.cash_out, 'balance':new_bal1, 'bank_oopl':opd.bank_oopl, 'remarks':opd.remarks}
                                    opd_data_to_update_1=QueryDict('', mutable=True)
                                    opd_data_to_update_1.update(opd_dict_1)
                                    form_opd_1=UpdateOPDCashSheetForm(opd_data_to_update_1, instance=opd)
                                    # print('Hello 033', form_opd_1)
                                    print('Hello 033')
                                    if form_opd_1.is_valid():
                                        print('hello 034')
                                        form_opd_1.save()
                            except OPDCashSheet.DoesNotExist:
                                pass
                    else:
                        opd_dict={'date':opd1.date, 'patient':opd1.patient.id, 'opd':opd1.opd.id, 'source':opd1.source, 'case_number':opd1.case_number, 'mode':opd1.mode, 'cash_in':instance.amount, 'cash_out':opd1.cash_out, 'balance':instance.amount, 'bank_oopl':opd1.bank_oopl, 'remarks':opd1.remarks}
                        opd_data_to_update=QueryDict('', mutable=True)
                        opd_data_to_update.update(opd_dict)
                        form_opd=UpdateOPDCashSheetForm(opd_data_to_update, instance=opd1)
                        # print('Hello 037', form_opd)
                        print('Hello 037')
                        if form_opd.is_valid():
                            print('hello 038')
                            opd2=form_opd.save()
                            try:
                                diff=_pre_save_amount-post_save_amount
                                opd3=OPDCashSheet.objects.filter(id__gt=opd2.id, date__gte=opd2.date, created_on__gt=opd2.created_on).order_by('date')
                                for opd in opd3:
                                    new_bal=opd.balance-diff
                                    opd_dict_1={'date':opd.date, 'patient':opd.patient.id, 'opd':opd.opd.id, 'source':opd.source, 'case_number':opd.case_number, 'mode':opd.mode, 'cash_in':opd.cash_in, 'cash_out':opd.cash_out, 'balance':new_bal, 'bank_oopl':opd.bank_oopl, 'remarks':opd.remarks}
                                    opd_data_to_update_1=QueryDict('', mutable=True)
                                    opd_data_to_update_1.update(opd_dict_1)
                                    form_opd_1=UpdateOPDCashSheetForm(opd_data_to_update_1, instance=opd)
                                    # print('Hello 039', form_opd_1)
                                    print('Hello 039')
                                    if form_opd_1.is_valid():
                                        print('hello 040')
                                        form_opd_1.save()
                            except OPDCashSheet.DoesNotExist:
                                pass
                except OPDCashSheet.DoesNotExist:
                    pass
            elif post_save_mode=='bank' and _pre_save_mode=='bank':
                try:
                    opd1=OPDCashSheet.objects.get(opd=instance.id, date=instance.date, patient=instance.patient)
                    opd_dict={'date':opd1.date, 'patient':opd1.patient.id, 'opd':opd1.opd.id, 'source':opd1.source, 'case_number':opd1.case_number, 'mode':opd1.mode, 'cash_in':opd1.cash_in, 'cash_out':opd1.cash_out, 'balance':opd1.balance, 'bank_oopl':instance.amount, 'remarks':opd1.remarks}
                    opd_data_to_update=QueryDict('', mutable=True)
                    opd_data_to_update.update(opd_dict)
                    form_opd=UpdateOPDCashSheetForm(opd_data_to_update, instance=opd1)
                    # print('Hello 027', form_opd)
                    print('Hello 027')
                    if form_opd.is_valid():
                        print('hello 028')
                        form_opd.save()
                        try:
                            bd=BankDeposits.objects.get(opdcashsheet=opd1.id, date=instance.date)
                            bd_dict={'opdcashsheet':opd1.id, 'date':bd.date, 'amount':instance.amount, 'bank':bd.bank, 'mode':bd.mode, 'bank_ac':bd.bank_ac, 'branch':bd.branch, 'remarks':bd.remarks}
                            bd_data_to_update=QueryDict('', mutable=True)
                            bd_data_to_update.update(bd_dict)
                            form_bd=BankDepositsForm(bd_data_to_update, instance=bd)
                            # print('Hello 029', form_bd)
                            print('Hello 029')
                            if form_bd.is_valid():
                                print('hello 030')
                                form_bd.save()
                        except BankDeposits.DoesNotExist:
                            pass
                except OPDCashSheet.DoesNotExist:
                    pass

@receiver(pre_save, sender=OPDCashSheet)
def opdcashsheet_pre_save(sender, instance, **kwargs):
    if instance.opd_particulars:
        if instance.opd_particulars.opd_particulars=='Cash Deposited To Bank':
            try:
                _pre_save_instance = OPDCashSheet.objects.get(pk=instance.pk)
                instance._pre_save_cash_out=_pre_save_instance.cash_out
                instance._pre_save_balance=_pre_save_instance.balance
                instance._pre_save_mode=_pre_save_instance.mode
                instance._pre_save_particulars=_pre_save_instance.opd_particulars.opd_particulars
            except OPDCashSheet.DoesNotExist:
                instance._pre_save_cash_out = instance.cash_out
                instance._pre_save_balance = instance.balance
                instance._pre_save_mode = instance.mode
                instance._pre_save_particulars=instance.opd_particulars.opd_particulars

@receiver(signal=post_save, sender=OPDCashSheet)
def opdcashsheet_post_save(sender, instance, created, **kwargs):
    if instance.opd_particulars:
        if instance.opd_particulars.opd_particulars=='Cash Deposited To Bank':
            if instance.mode=='bank':
                if created:
                    pass
                else:
                    _pre_save_cash_out = instance._pre_save_cash_out
                    post_save_cash_out = instance.cash_out
                    _pre_save_balance = instance._pre_save_balance
                    post_save_balance = instance.balance
                    _pre_save_particulars= instance._pre_save_particulars
                    post_save_particulars=instance.opd_particulars.opd_particulars
                    _pre_save_mode = instance._pre_save_mode
                    post_save_mode = instance.mode
                    if _pre_save_particulars=='Cash Deposited To Bank' and post_save_particulars=='Cash Deposited To Bank':
                        if _pre_save_mode==post_save_mode:
                            if _pre_save_cash_out!=post_save_cash_out:
                                try:
                                    bd=BankDeposits.objects.get(opdcashsheet=instance.id, date=instance.date)
                                    bd_dict={'opdcashsheet':instance.id, 'date':bd.date, 'amount':instance.cash_out, 'bank':bd.bank, 'mode':bd.mode, 'bank_ac':bd.bank_ac, 'branch':bd.branch, 'remarks':bd.remarks}
                                    bd_data_to_update=QueryDict('', mutable=True)
                                    bd_data_to_update.update(bd_dict)
                                    form_bd=BankDepositsForm(bd_data_to_update, instance=bd)
                                    # print('Hello 031', form_bd)
                                    print('Hello 031')
                                    if form_bd.is_valid():
                                        print('hello 032')
                                        form_bd.save()
                                except BankDeposits.DoesNotExist:
                                    pass
                            if _pre_save_balance!=post_save_balance:
                                diff=_pre_save_balance-post_save_balance
                                try:
                                    opd1=OPDCashSheet.objects.filter(id__gt=instance.id, date__gte=instance.date, created_on__gt=instance.created_on).order_by('date')
                                    for opd in opd1:
                                        new_bal=opd.balance+diff
                                        # if opd.opd:
                                        opd_dict={'date':opd.date, 'patient':opd.patient.id, 'opd':opd.opd.id, 'opd_particulars':opd.opd_particulars.id, 'source':opd.source, 'case_number':opd.case_number, 'mode':opd.mode, 'cash_in':opd.cash_in, 'cash_out':opd.cash_out, 'balance':new_bal, 'bank_oopl':opd.bank_oopl, 'remarks':opd.remarks}
                                        opd_data_to_update=QueryDict('', mutable=True)
                                        opd_data_to_update.update(opd_dict)
                                        form_opd=UpdateOPDCashSheetForm(opd_data_to_update, instance=opd)
                                        # print('Hello 035', form_opd)
                                        print('Hello 035')
                                        if form_opd.is_valid():
                                            print('hello 036')
                                            form_opd.save()
                                        # else:
                                        #     opd_dict={'date':opd.date, 'opd_particulars':opd.opd_particulars.id, 'source':opd.source, 'case_number':opd.case_number, 'mode':opd.mode, 'cash_in':opd.cash_in, 'cash_out':opd.cash_out, 'balance':new_bal, 'bank_oopl':opd.bank_oopl, 'remarks':opd.remarks}
                                        #     opd_data_to_update=QueryDict('', mutable=True)
                                        #     opd_data_to_update.update(opd_dict)
                                        #     form_opd=UpdateOPDCashSheetForm(opd_data_to_update, instance=opd)
                                        #     # print('Hello 041', form_opd)
                                        #     print('Hello 041')
                                        #     if form_opd.is_valid():
                                        #         print('hello 042')
                                        #         form_opd.save()
                                except OPDCashSheet.DoesNotExist:
                                    pass