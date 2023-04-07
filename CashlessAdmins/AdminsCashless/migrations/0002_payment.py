# Generated by Django 4.1.5 on 2023-04-06 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminsCashless', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(blank=True, max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('qr_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminsCashless.cardholder')),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminsCashless.merchant', to_field='wallet_id')),
            ],
        ),
    ]
