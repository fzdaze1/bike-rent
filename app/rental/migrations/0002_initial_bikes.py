from django.db import migrations


def create_initial_bikes(apps, schema_editor):
    Bike = apps.get_model('rental', 'Bike')
    bikes = []
    for i in range(1, 11):
        bikes.append(Bike(name=f'Bike {i}'))
    Bike.objects.bulk_create(
        bikes
    )


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_bikes),
    ]
