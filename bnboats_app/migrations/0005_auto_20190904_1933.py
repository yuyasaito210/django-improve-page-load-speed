# Generated by Django 2.1.7 on 2019-09-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bnboats_app', '0004_auto_20190903_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='manufacturer',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='boat',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='captainextraactivities',
            name='activity',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='captainlanguages',
            name='language',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='captainprofile',
            name='experience',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_additional',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_street',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bank_account',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bank_branch',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bank_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bank_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
