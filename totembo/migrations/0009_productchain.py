# Generated by Django 5.1.6 on 2025-05-02 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('totembo', '0008_vendor_delete_product2'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=200)),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
        ),
    ]
