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