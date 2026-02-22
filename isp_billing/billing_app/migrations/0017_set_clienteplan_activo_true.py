from django.db import migrations


def set_clienteplan_activo_true(apps, schema_editor):
    ClientePlan = apps.get_model('billing_app', 'ClientePlan')
    ClientePlan.objects.filter(activo=False).update(activo=True)


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('billing_app', '0016_ordentecnica_fecha_asistencia'),
    ]

    operations = [
        migrations.RunPython(set_clienteplan_activo_true, reverse_noop),
    ]
