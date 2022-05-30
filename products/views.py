from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Count, Sum, IntegerField, OuterRef, Subquery

from products.models import Product

class ProductListView(View):
    def get(self, request):
        category = request.GET.get('category', None)
        search   = request.GET.get('search', None)
        sort     = request.GET.get('sort', 'created_at')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 8))

        q = Q()

        q &= Q(options__name="1개입")

        if category:
            q &= Q(category__name__contains=category)

        if search:
            q &= Q(name__contains=search)
        
        sort_dict = {
            "new"   : "created_at",
            "old"   : "-created_at",
            "name"  : "name",
            "-name" : "-name",
            "price" : "options__price",
            "-price": "-options__price",
            "review": "-review_count",
            "sales" : "-sales_sum",
        }

        if sort in sort_dict:
            sort = sort_dict[sort]

        review_count = Product.objects.annotate(review_count=Count('reviews')).filter(pk=OuterRef('pk'))
        sales_sum    = Product.objects.annotate(sales_sum=Sum('options__items__quantity')).filter(pk=OuterRef('pk'))

        products     = Product.objects.filter(q).annotate(review_count=Subquery(review_count.values('review_count'), 
        output_field=IntegerField()),sales_sum=Subquery(sales_sum.values('sales_sum'), output_field=IntegerField()))\
        .order_by(sort).distinct()[offset:offset+limit]
        
        product_list = [{
            "product_id"      : product.id,
            "name"            : product.name,
            "description"     : product.description,
            "thumbnail_url"   : product.thumbnail_url,
            "discount_rate"   : product.discount_rate,
            "review_count"    : product.reviews.count(),
            "price"           : product.options.first().price,
            "discounted_price": product.options.first().price * (100 - product.discount_rate)/100
        } for product in products]

        return JsonResponse({"data": product_list}, status=200)