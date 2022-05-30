from django.http     import JsonResponse
from django.views    import View

from products.models import Product, ProductImage, ProductOption

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            
            product = Product.objects.get(id = product_id) 
            data = {
                'id'              : product.id,
                'name'            : product.name,
                'thumbnail_url'   : product.thumbnail_url,
                'product_image'   : [image.url for image in product.image_url.all()],
                'description'     : product.description,
                'discount_rate'   : product.discount_rate,
                'price'           : [option.price for option in product.options.all()],
                'discounted_price': [int(option.price)* (100 - product.discount_rate)/100 for option in product.options.all()],
                'product_option'  : [option.name for option in product.options.all()]
            }
            
            return JsonResponse({'result' : data}, status=200)

        except KeyError:
                return JsonResponse({'message' : 'Key Error'}, status=400)

        except Product.DoesNotExist:
                return JsonResponse({'message' : 'NOT_FOUND'}, status=401)