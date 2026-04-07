from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastogeneral',
            name='tipo',
            field=models.CharField(
                choices=[('FIJO', 'Gasto Fijo'), ('VARIABLE', 'Gasto Variable'), ('COMPRA', 'Compra')],
                default='VARIABLE',
                max_length=10,
            ),
        ),
    ]
