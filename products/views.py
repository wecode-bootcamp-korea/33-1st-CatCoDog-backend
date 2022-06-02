from enum import Enum

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count, Sum, OuterRef

from products.models import Product

class ProductOption(Enum):
    ONE = "1개입"
    TEN = "10개입"

class ProductListView(View):
    def get(self, request):
        category = request.GET.get('category', None)
        search   = request.GET.get('search', None)
        sort     = request.GET.get('sort', 'name')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 6))

        q = Q()

        q &= Q(options__name=ProductOption.ONE.value)

        if category:
            q &= Q(category__name__contains=category)

        if search:
            q &= Q(name__contains=search)

        sort_set = {
            "name"  : "name",
            "-name" : "-name",
            "old"   : "created_at",
            "new"   : "-created_at",
            "price" : "options__price",
            "-price": "-options__price",
            "review": "-review_count",
            "sales" : "-sales_sum",            
        }
        sort = sort_set.get(sort)

        review_count = Product.objects.annotate(review_count=Count('reviews')).filter(pk=OuterRef('pk'))
        sales_sum    = Product.objects.annotate(sales_sum=Sum('options__items__quantity')).filter(pk=OuterRef('pk'))

        products = Product.objects.filter(q).prefetch_related('options', 'reviews').annotate\
                (review_count=review_count.values('review_count'), sales_sum=sales_sum.values('sales_sum'))\
                .order_by(sort).distinct()[offset:offset+limit]

        product_list = [{
            "product_id"      : product.id,
            "name"            : product.name,
            "description"     : product.description,
            "thumbnail_url"   : product.thumbnail_url,
            "review_count"    : product.reviews.count(),
            "price"           : format(int(product.options.all()[0].price), ',d'),
            "discount_rate"   : product.discount_rate,
            "discounted_price": format(int(product.options.all()[0].price * (100 - product.discount_rate)/100), ',d'),
        } for product in products]

        return JsonResponse({"data": product_list}, status=200)

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
                'product_option'  : [{
                    "option_name"     : option.name,
                    "optios_price"    : option.price,
                    "discounted_price": int(option.price) * (100 - product.discount_rate)/100
                    } for option in product.options.all()]
            }
            return JsonResponse({'result' : data}, status=200)

        except KeyError:
                return JsonResponse({'message' : 'Key Error'}, status=400)

        except Product.DoesNotExist:
                return JsonResponse({'message' : 'NOT_FOUND'}, status=404)