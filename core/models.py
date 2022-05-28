from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Machine(models.Model):
    machine_name = models.CharField(max_length=200)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=200)
    manufacture_order = models.CharField(max_length=200)
    order_number = models.CharField(max_length=200)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=200)
    product_description = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    product_diameter = models.DecimalField(max_digits=10, decimal_places=2)
    product_height = models.DecimalField(max_digits=10, decimal_places=2)
    product_weight_gross = models.DecimalField(max_digits=10, decimal_places=2)
    product_weight_color = models.DecimalField(max_digits=10, decimal_places=2)
    is_enable = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DecorationInspection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_decoration_inspection')
    decoration_type = models.CharField(max_length=200, choices=(
        ('ser_aspect', 'ser_aspect'), ('ser_printq', 'ser_printq'), ('ser_color', 'ser_color'),
        ('ver_aspect', 'ver_aspect'), ('ver_shine', 'ver_shine'), ('ver_break', 'ver_break'),
        ('dec_aspect', 'dec_aspect'),
        ('dec_color', 'dec_color'), ('dec_debut', 'dec_debut'), ('dec_humadity', 'dec_humadity')))
    value = models.IntegerField(blank=True)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def image_url(self):
        return self.image.url


class PackagingInspection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_packaging_inspection')
    packaging_type = models.CharField(max_length=200, choices=(
        ('lab_address', 'lab_address'), ('lab_printing', 'lab_printing'), ('lab_dirty', 'lab_dirty'),
        ('lab_position', 'lab_position'), ('fol_correct', 'fol_correct'), ('fol_rugged', 'fol_rugged'),
        ('fol_solder', 'fol_solder'), ('fol_holes', 'fol_holes'), ('pac_aspect', 'pac_aspect'), ('pac_ean', 'pac_ean'),
        ('pac_batch', 'pac_batch'), ('pac_printing', 'pac_printing'), ('pac_dirty', 'pac_dirty'),
        ('pal_aspect', 'pal_aspect'), ('pal_label', 'pal_label'), ('pal_cinta', 'pal_cinta'),
        ('pal_film', 'pal_film'), ('pal_position', 'pal_position'), ('pal_perpack', 'pal_perpack')))
    value = models.IntegerField(blank=True)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def image_url(self):
        return self.image.url


class CandleInspection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_candle_inspection')
    candle_type = models.CharField(max_length=200, choices=(
        ('mat_rawmaterial', 'mat_rawmaterial'), ('mat_lotmaterial', 'mat_lotmaterial'), ('mat_mix', 'mat_mix'),
        ('mat_lotmix', 'mat_lotmix'), ('mat_powdercolor', 'mat_powdercolor'), ('mat_lotpowder', 'mat_lotpowder'),
        ('mat_tankcolor', 'mat_tankcolor'), ('sur_gaspect', 'sur_gaspect'), ('sur_surface', 'sur_surface'),
        ('sur_extelem', 'sur_extelem'), ('sur_dirty', 'sur_dirty'), ('sur_contract', 'sur_contract'),
        ('sur_breaksur', 'sur_breaksur'), ('sur_color', 'sur_color'), ('wir_freleng', 'wir_freleng'),
        ('wir_position', 'wir_position'), ('wir_extend', 'wir_extend'), ('wir_basedist', 'wir_basedist'),
        ('wir_burn', 'wir_burn'), ('com_fireheig', 'com_fireheig'), ('com_shape', 'com_shape'),
        ('com_position', 'com_position'), ('com_ash', 'com_ash'), ('com_runoff', 'com_runoff'),
        ('com_collapse', 'com_collapse'), ('com_fog', 'com_fog')))
    value = models.IntegerField(blank=True)
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def image_url(self):
        return self.image.url
