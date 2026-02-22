from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0007_add_orden_tecnica_fecha_finalizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentecnica',
            name='plan_asociado',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ordenes_tecnicas',
                to='billing_app.clienteplan',
            ),
        ),
        migrations.AddField(
            model_name='ordentecnica',
            name='servicio_afectado',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ordenes_tecnicas',
                to='billing_app.servicio',
            ),
        ),
    ]
