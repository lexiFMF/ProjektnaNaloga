# Generated by Django 5.1 on 2024-08-23 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0002_alter_uporabnik_območje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uporabnik',
            name='kategorija',
            field=models.CharField(choices=[('4', 'A'), ('2', 'A1'), ('3', 'A2'), ('1', 'AM'), ('6', 'B'), ('5', 'B1'), ('7', 'BE'), ('10', 'C'), ('8', 'C1'), ('9', 'C1E'), ('11', 'CE'), ('14', 'D'), ('12', 'D1'), ('15', 'DE'), ('13', 'D1E'), ('16', 'F'), ('17', 'G')], max_length=3),
        ),
        migrations.AlterField(
            model_name='uporabnik',
            name='območje',
            field=models.CharField(choices=[('17', 'Območje 1'), ('18', 'Območje 2'), ('19', 'Območje 3'), ('20', 'Območje 4'), ('21', 'Območje 5')], max_length=9),
        ),
    ]
