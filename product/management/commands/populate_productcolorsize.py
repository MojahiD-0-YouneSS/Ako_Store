from django.core.management.base import BaseCommand
from product.models import ProductColor, ProductSize, ProductColorSize

class Command(BaseCommand):
    help = 'Populate ProductColorSize with existing ProductColor and ProductSize data'

    def handle(self, *args, **kwargs):
        product_colors = ProductColor.objects.all()
        product_sizes = ProductSize.objects.all()
        for product_color in product_colors:
            for product_size in product_sizes:
                if product_color.product == product_size.product:
                    ProductColorSize.objects.create(
                        product_color=product_color,
                        product_size=product_size,
                        quantity=min(product_color.quantity, product_size.quantity)  # Set initial quantity
                    )
        self.stdout.write(self.style.SUCCESS('Successfully populated ProductColorSize table.'))
    
'''    
so logically (mathimatically) let's say ProductColor is Pcq with (c = color and q = quantity) and ProductSize is Psq with (c = color and q = quantity)
relationships:
pcq.is_related_to(Color, ProductModel) and psq.is_related_to(SIZE, ProductModel)
so logically :
if there is a Product A then there is Ac (A in pcq) and As (A in psq) then:

if length(As.objects.s) == 1 (only one size) and length(Ac.objects.c) == 1 (only one color):
   Ac.objects.q (quantity) == As.objects.q (quantity) it means that c is related to s (this color is the color of that size Ac.objects.c = As.objects.s)

if length(As.objects.s) > 1 (more than one size) and length(Ac.objects.c) = 1 (only one color):
  c = Ac.objects.c
for s in As.objects.s:
   if c.q (quantity) == s.q (quantity):
    it means that c is related to s (this color is the color of that size)

if length(As.objects.s) = 1 (only one size) and length(Ac.objects.c) > 1 (more than one color):
  s = Ac.objects.s
for c in As.objects.c:
   if c.q (quantity) == s.q (quantity):
    it means that c is related to s (this color is the color of that size)
********* my issue ****:
example if there is: 3 sizes for 3 color (each color get's a size) with same quantity then this aproach of using quantity is
failling cuzz will give us each color 3 sizes. 
if length(As.objects.s) > 1 (more than one size) and length(Ac.objects.c) > 1 (more one color) and length(both).are_equal():
  c = Ac.objects.c
for s in As.objects.s:
    for s in As.objects.s:
        if c.q (quantity) == s.q (quantity):
            it means that c is related to s (this color is the color of that size)

if u understood this try to apply this consept in the handle function by fixing it:
class Command(BaseCommand):
    help = 'Populate ProductColorSize with existing ProductColor and ProductSize data'

    def handle(self, *args, **kwargs):
        product_colors = ProductColor.objects.all()
        product_sizes = ProductSize.objects.all()
        for product_color in product_colors:
            for product_size in product_sizes:
                if product_color.product == product_size.product:
                    ProductColorSize.objects.create(
                        product_color=product_color,
                        product_size=product_size,
                        quantity=min(product_color.quantity, product_size.quantity)  # Set initial quantity
                    )
        self.stdout.write(self.style.SUCCESS('Successfully populated ProductColorSize table.'))

'''