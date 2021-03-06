# Generated by Django 2.2.4 on 2020-02-23 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='details',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='places.PlaceDetails'),
        ),
        migrations.AddField(
            model_name='placephotos',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.Place'),
        ),
        migrations.AddField(
            model_name='placereviews',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='places.Place'),
        ),
    ]
