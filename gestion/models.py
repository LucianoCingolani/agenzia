from django.utils import timezone
from django.db import models

# Create your models here.

class Operacion(models.Model):
    TIPO_CHOICES = [('VENTA', 'Venta'), ('GASTO', 'Gasto')]
    
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    # El monto total que realmente ocurrió
    monto_total_real = models.DecimalField(max_digits=12, decimal_places=2)
    
    # La parte que tiene papel legal
    monto_facturado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    archivo_factura = models.FileField(upload_to='facturas/', null=True, blank=True)
    
    es_fiscal = models.BooleanField(default=False) # Si se declara o no

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} (${self.monto_total_real})"
    

class GastoGeneral(models.Model):
    CATEGORIAS = [
        ('SERVICIOS', 'Servicios (Luz, Gas, Agua)'),
        ('MANTENIMIENTO', 'Mantenimiento / Limpieza'),
        ('SUELDOS', 'Sueldos / Adelantos'),
        ('MERCADERIA', 'Compra Mercadería'),
        ('VARIOS', 'Gastos Varios'),
    ]
    TIPOS = [
            ('FIJO', 'Gasto Fijo'),
            ('VARIABLE', 'Gasto Variable'),
            ('COMPRA', 'Compra'),
    ]
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('MERCADO_PAGO', 'Mercado Pago'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('OTRO', 'Otro'),
    ]
    
    fecha = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    tipo = models.CharField(max_length=10, choices=TIPOS, default='VARIABLE')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='EFECTIVO')
    
    monto = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock_actual = models.IntegerField(default=0)
    umbral_minimo = models.IntegerField(default=5, help_text="Avisar cuando el stock sea menor a este número")
    
    @property
    def necesita_reposicion_urgente(self):
        return self.stock_actual <= self.umbral_minimo
    
    def necesita_reposicion(self):
        return self.stock_actual <= self.umbral_minimo * 1.5

    def __str__(self):
        return f"{self.nombre} ({self.stock_actual})"