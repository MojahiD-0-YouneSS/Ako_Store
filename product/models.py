from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
import os
from django.core.exceptions import ValidationError
from django.db.models import Sum
# Create your models here.
class ProductCategoryParent(models.Model):
    CATEGORY_CHOICES = [
        ('Top', 'Top'),
        ('Down', 'Down'),
        ('Feet', 'Feet'),
    ]

    ProductCategoryP = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        unique=True, 
    )

    def __str__(self):
        return self.ProductCategoryP
    
class ProductCategoryChild(models.Model):
    ProductCategoryC = models.CharField(max_length=100)
    
    def __str__(self):
        return self.ProductCategoryC
    
class Tags(models.Model):
    New = models.BooleanField(default=True)
    Limited = models.BooleanField(default=True)
    Ondemand = models.BooleanField(default=True)
    Viral = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Tag - New: {self.New}, Limited: {self.Limited}, Ondemand: {self.Ondemand}, Viral: {self.Viral}"
    
class ProductTags(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)
    product_tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    def __str__(self):
        return f"Tag - New: {self.product_tags.New}, Limited: {self.product_tags.Limited}, Ondemand: {self.product_tags.Ondemand}, Viral: {self.product_tags.Viral}"
        
class SIZE(models.Model):
    size_value = models.TextField(max_length=50, unique=True)

    def __str__(self):
        return self.size_value

class ProductColorSize(models.Model):
    product_color = models.ForeignKey('ProductColor', on_delete=models.CASCADE)
    product_size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    def clean(self):
        super().clean()
        if self.quantity > self.product_color.quantity or self.quantity > self.product_size.quantity:
            
            raise ValidationError(
                f"The quantity for color '{self.product_color.color.name}' ({self.product_color.quantity}) or "
                f"size '{self.product_size.size.size_value}' ({self.product_size.quantity}) is exceeded."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class ProductSize(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)
    size = models.ForeignKey(SIZE, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.size.size_value}"

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=7, unique=True)
    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.color.name}"

class ColorSizePointer(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(SIZE)
    quantities = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.color.name} - Sizes: {', '.join([str(size) for size in self.sizes.all()])}"

class ProductCategory(models.Model):
    sub_category = models.ForeignKey(ProductCategoryChild, on_delete=models.CASCADE, null=True, blank=True)
    main_category = models.ForeignKey(ProductCategoryParent, on_delete=models.CASCADE,  null=True, blank=True)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE,)
    
    def __str__(self):
        return f"{self.main_category} - {self.sub_category} - {self.product.ProductName}"

class SearchLabel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ProductSearchLabel(models.Model):
    search_label = models.ForeignKey(SearchLabel, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.search_label.name

class BrandModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand_Image = models.ImageField(upload_to='brand/', null=True,  blank=True)
    
    class Meta:
        verbose_name = _("BrandModel")
        verbose_name_plural = _("BrandModels")

    def __str__(self):
        return self.name

class ProductBrand(models.Model):
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, null=True, blank=True)

class FabricModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = _("FabricModel")
        verbose_name_plural = _("FabricModels")

    def __str__(self):
        return self.name

class ProductFabric(models.Model):
    pure = models.BooleanField(default=True)
    fabric = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        
        if self.pure:
            if not FabricModel.objects.filter(name=self.fabric).exists():
                raise ValidationError(f"The fabric '{self.fabric}' is not found in FabricModel.")
        else:
            fabric_names = []
            L1_fabric_comb = self.fabric.split('\n')
            for x in L1_fabric_comb:
                try:
                    name = x.split(' ', 1)[1].strip()  
                    fabric_names.append(name)
                except IndexError:
                    raise ValidationError("Invalid fabric format. Ensure each line follows the format '<percentage> <fabricName>'.")

            missing_fabrics = [name for name in fabric_names if not FabricModel.objects.filter(name=name).exists()]
            if missing_fabrics:
                raise ValidationError(f"The fabric(s) '{', '.join(missing_fabrics)}' are not found in FabricModel.")
        
    def __str__(self):
        return self.fabric
    
class ProductModel(models.Model):
    reference_number = models.CharField(max_length=20, unique=True, null=True)
    ProductName = models.CharField(max_length=255)
    ProductPrice = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ProductSKU = models.CharField(max_length=50)
    ProductImages = models.ManyToManyField('ProductImage', related_name='images')    
    ProductCategoriesParent = models.ManyToManyField(ProductCategoryParent, through='ProductCategory', related_name='parent_category')
    ProductCategoriesChild = models.ManyToManyField(ProductCategoryChild, through='ProductCategory', related_name='child_category')
    related_products = models.ManyToManyField('self', symmetrical=False, related_name='related_to', blank=True)
    ProductDescription = models.TextField(blank=True) #delete
    size = models.ManyToManyField(SIZE, through='ProductSize', related_name='product_size')
    available_from = models.DateField()
    available_until = models.DateField()
    quantity = models.IntegerField()
    headding = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    original = models.BooleanField(default=False)
    gifted = models.BooleanField(default=False)
    ProductTagsList = models.ManyToManyField(Tags, through='ProductTags', related_name='products')  
    colors = models.ManyToManyField(Color, through='ProductColor', related_name='products')
    search_labls =  models.ManyToManyField(SearchLabel, through='ProductSearchLabel', related_name='product_label')
    mark = models.ManyToManyField(BrandModel, through='ProductBrand', related_name='product_mark')
    def __str__(self):
        return self.ProductName  
    
def get_image_filename(instance, filename):
    product_name = instance.Product.ProductName
    slug = slugify(product_name)
    return "productPhotos/%s-%s" % (slug, filename) 
    
class ProductImage(models.Model):
    Product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
    Product_Image = models.ImageField(_('Image'), upload_to=get_image_filename, null=True,  blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    order = models.PositiveIntegerField(default=0, help_text=_('The order in which the images will be displayed'))

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.Product.ProductName}"
