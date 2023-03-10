# Generated by Django 4.0 on 2023-01-31 17:29

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('particulars', models.CharField(max_length=150)),
                ('date', models.DateField(default=datetime.date.today)),
                ('received_by', models.CharField(max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovedPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('approved_package', models.DecimalField(decimal_places=2, max_digits=10)),
                ('approval_date', models.DateField(default=datetime.date.today)),
                ('proposed_fractions', models.IntegerField()),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('approved_package_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommonExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('particulars', models.CharField(default='MOULD', max_length=150)),
                ('date', models.DateField(default=datetime.date.today)),
                ('paid_by', models.CharField(max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('common_expenses_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CTScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt_number', models.CharField(default=None, max_length=15, validators=[django.core.validators.RegexValidator('(RT|rt|rT|Rt)\\/[0-9]{4}\\/[0-9]{2}\\/[0-9]{4}', 'Enter RT Number properly!')])),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(default=datetime.date.today)),
                ('conducted_by', models.CharField(default=None, max_length=4)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('ctscan_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Depositor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depositor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Discharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_discharge', models.DateField(default=datetime.date.today)),
                ('discharge_updated', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('discharge_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IpdReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approvedpackage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.approvedpackage')),
                ('ctscan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.ctscan')),
                ('discharge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.discharge')),
            ],
        ),
        migrations.CreateModel(
            name='Opd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.IntegerField(default=None)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('opd_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OtherExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('particulars', models.CharField(max_length=150)),
                ('date', models.DateField(default=datetime.date.today)),
                ('paid_by', models.CharField(max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OtherIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('particulars', models.CharField(max_length=150)),
                ('date', models.DateField(default=datetime.date.today)),
                ('received_by', models.CharField(max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=11)),
                ('gender', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=13, null=True)),
                ('alternate_phone_number', models.CharField(blank=True, default=None, max_length=13, null=True)),
                ('center', models.CharField(default='Dhule', max_length=7)),
                ('mr_uid', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='PatientType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_type', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('particulars', models.CharField(max_length=200, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_number', models.IntegerField(null=True)),
                ('voucher_number', models.IntegerField(null=True)),
                ('image', models.ImageField(blank=True, upload_to='Petty Cash/Images')),
                ('docs', models.FileField(blank=True, upload_to='Petty Cash/Docs')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('depositor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.depositor')),
            ],
        ),
        migrations.CreateModel(
            name='UnclaimedPendingCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipdreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.ipdreport')),
            ],
        ),
        migrations.CreateModel(
            name='RepudiatedClaims',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipdreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.ipdreport')),
            ],
        ),
        migrations.CreateModel(
            name='ReclaimedRepudiation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipdreport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.ipdreport')),
            ],
        ),
        migrations.CreateModel(
            name='Realization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.BooleanField(default=False)),
                ('amount_received', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('received_by', models.CharField(default=None, max_length=4)),
                ('billing_month', models.DateField(default=datetime.date.today)),
                ('deficit_or_surplus_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('deficit_percentage', models.FloatField(blank=True, default=0)),
                ('surplus_percentage', models.FloatField(blank=True, default=0)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('realization_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient')),
                ('patient_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype')),
            ],
        ),
        migrations.CreateModel(
            name='Radiations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('done_fractions', models.IntegerField(default=0)),
                ('base_value', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10)),
                ('expected_value', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('radiations_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient')),
                ('patient_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype')),
            ],
        ),
        migrations.CreateModel(
            name='PiggyBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('depositor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.depositor')),
            ],
        ),
        migrations.CreateModel(
            name='PettyCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('piggybank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.piggybank')),
                ('withdrawal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.withdrawal')),
            ],
        ),
        migrations.CreateModel(
            name='PaxMax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_fractions', models.IntegerField()),
                ('total_package', models.DecimalField(decimal_places=2, max_digits=10)),
                ('patient_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.treatment')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_admission', models.DateField(default=datetime.date.today)),
                ('max_fractions', models.IntegerField()),
                ('total_package', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remarks', models.TextField(blank=True, default=None, max_length=500)),
                ('package_date', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.diagnosis')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient')),
                ('patient_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.treatment')),
            ],
        ),
        migrations.CreateModel(
            name='OpdReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.opd')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient')),
            ],
        ),
        migrations.AddField(
            model_name='opd',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient'),
        ),
        migrations.AddField(
            model_name='opd',
            name='service_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dhule.servicename'),
        ),
        migrations.CreateModel(
            name='OngoingReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipdreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.ipdreport')),
            ],
        ),
        migrations.CreateModel(
            name='LockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lock', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.date.today)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patient')),
                ('patient_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype')),
            ],
        ),
        migrations.AddField(
            model_name='ipdreport',
            name='lockdata',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.lockdata'),
        ),
        migrations.AddField(
            model_name='ipdreport',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.package'),
        ),
        migrations.AddField(
            model_name='ipdreport',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient'),
        ),
        migrations.AddField(
            model_name='ipdreport',
            name='radiations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.radiations'),
        ),
        migrations.AddField(
            model_name='ipdreport',
            name='realization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhule.realization'),
        ),
        migrations.AddField(
            model_name='discharge',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient'),
        ),
        migrations.AddField(
            model_name='discharge',
            name='patient_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype'),
        ),
        migrations.AddField(
            model_name='ctscan',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient'),
        ),
        migrations.AddField(
            model_name='ctscan',
            name='patient_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype'),
        ),
        migrations.CreateModel(
            name='ClaimedPendingCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipdreport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.ipdreport')),
            ],
        ),
        migrations.AddField(
            model_name='approvedpackage',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhule.patient'),
        ),
        migrations.AddField(
            model_name='approvedpackage',
            name='patient_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dhule.patienttype'),
        ),
    ]
