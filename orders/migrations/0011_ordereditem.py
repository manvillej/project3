# Generated by Django 2.0.7 on 2018-08-01 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='orders.Cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Item')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Size')),
            ],
        ),
    ]
