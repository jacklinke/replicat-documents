# Generated by Django 3.2.5 on 2021-07-22 04:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('replicat_documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentissuerchoice',
            options={'verbose_name': 'Document Issuer', 'verbose_name_plural': 'Document Issuers'},
        ),
        migrations.AlterModelOptions(
            name='replicatdocument',
            options={'verbose_name': 'Replicat Document', 'verbose_name_plural': 'Replicat Document'},
        ),
        migrations.AlterField(
            model_name='replicatdocument',
            name='document_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Generated document identifier', unique=True, verbose_name='Document ID'),
        ),
    ]