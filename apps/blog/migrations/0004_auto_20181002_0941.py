# Generated by Django 2.0.3 on 2018-10-02 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20181001_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerapply',
            name='age',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customerapply',
            name='comment',
            field=models.CharField(default='未发送', max_length=50),
        ),
        migrations.AlterField(
            model_name='customerapply',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customerapply',
            name='phone',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customerapply',
            name='verify',
            field=models.CharField(default='noresponse', max_length=50),
        ),
    ]