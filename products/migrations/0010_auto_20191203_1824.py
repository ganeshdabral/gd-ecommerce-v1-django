# Generated by Django 2.2.6 on 2019-12-03 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20191203_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('men', 'men'), ('women', 'women'), ('kids', 'kids')], max_length=12, null=True),
        ),
    ]