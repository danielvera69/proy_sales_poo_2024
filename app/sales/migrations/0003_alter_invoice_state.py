# Generated by Django 4.2 on 2024-07-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_remove_invoicedetail_cost_alter_invoice_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='state',
            field=models.CharField(choices=[('F', 'Factura'), ('A', 'Anulada'), ('M', 'Modificada')], default='F', max_length=1, verbose_name='Estado'),
        ),
    ]
