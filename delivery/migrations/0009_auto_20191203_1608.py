# Generated by Django 2.2.7 on 2019-12-03 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_auto_20191203_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qntItensTotal', models.IntegerField(blank=True, null=True)),
                ('status_pagamento', models.CharField(blank=True, choices=[('1', 'Pagamento Pendente'), ('2', 'Pagamento Realizado')], max_length=50, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produto', models.IntegerField()),
                ('id_pedido', models.IntegerField()),
                ('quantidade_itens', models.IntegerField(blank=True, null=True, verbose_name='Quantidade')),
            ],
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': 'Delivery', 'verbose_name_plural': "Delivery's"},
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='quantidade_itens',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='status_pagamento',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='valor_total',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='pedido',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='qnt',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone1',
            field=models.CharField(help_text='EX.:(99)99999-9999', max_length=14),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone2',
            field=models.CharField(blank=True, help_text='EX.:(87)3333-3333', max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='getCliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='telefone1',
            field=models.CharField(help_text='EX.:(99)99999-9999', max_length=14),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='telefone2',
            field=models.CharField(blank=True, help_text='EX.:(87)3333-3333', max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='getDelivery', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='getCliente', to='delivery.Cliente'),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='entregador',
        ),
        migrations.AddField(
            model_name='pedido',
            name='entregador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='delivery.Entregador'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='restaurante',
            field=models.ManyToManyField(related_name='getDeliverys', to='delivery.Delivery'),
        ),
        migrations.AddField(
            model_name='produto',
            name='id_produto_pedido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='getPedido', to='delivery.ProdutoPedido'),
        ),
    ]
