# Generated by Django 5.0.6 on 2024-06-28 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0004_delete_rendezvous'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='produit',
            name='cout_achat',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vente',
            name='montant',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
