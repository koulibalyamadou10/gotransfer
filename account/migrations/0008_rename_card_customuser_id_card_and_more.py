# Generated by Django 5.2 on 2025-04-23 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_customuser_beneficiaries'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='card',
            new_name='id_card',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='card_exp_date',
            new_name='id_card_exp_date',
        ),
        migrations.AddField(
            model_name='customuser',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shBilling',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shCarrier',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shOTher',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='commission',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('customer', 'Client'), ('admin', 'Administrateur'), ('agent', 'Agent')], default='customer', max_length=20),
        ),
    ]
