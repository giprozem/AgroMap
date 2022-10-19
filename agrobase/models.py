from django.db import models


class Material(models.Model):
    Category = [
        ('1', 'Болезни'),
        ('2', 'Насекомые'),
    ]
    category = models.CharField(max_length=125, choices=Category)


class MaterialImage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_images')
    image = models.ImageField(upload_to='material_images', blank=True, null=True)


class MaterialBlock(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_blogs')
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='material_block_images', blank=True, null=True)

