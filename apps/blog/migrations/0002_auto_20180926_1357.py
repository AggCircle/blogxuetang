# Generated by Django 2.0.3 on 2018-09-26 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerapply',
            options={'ordering': ['name'], 'verbose_name': '报名信息', 'verbose_name_plural': '报名信息'},
        ),
        migrations.AlterModelTable(
            name='customerapply',
            table='customerapply',
        ),
    ]
