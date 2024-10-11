#point_size_to_color
from django.shortcuts import render, redirect, get_object_or_404

from typing import Any
from django.core.management.base import BaseCommand
from product.models import Color, SIZE, ColorSizePointer, ProductColor, ProductSize

class Command(BaseCommand):
    help = 'Populate ProductColorSize with existing ProductColor and ProductSize data'
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        pc = ProductColor.objects.all()
        ps = ProductSize.objects.all()
        ColorSizePointer.objects.all().delete()
        for color in pc:
            for size in ps:
                if color.product == size.product:
                    if color.quantity == size.quantity:
                        the_color = get_object_or_404(Color,name=color.color.name)
                        the_size = get_object_or_404(SIZE,size_value=size.size.size_value)
                        pointer = ColorSizePointer.objects.create(
                            color=the_color,
                            product_color=color,
                            
                        )
                        pointer.sizes.add(the_size)
                        pointer.quantities.append(color.quantity)
                        pointer.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated ColorSizePointer table.'))