from enum import Enum

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Count, Sum, IntegerField, OuterRef, Subquery
from django.core.exceptions import FieldError

from products.models import Product

"""
목적: 여러 제품의 정보를 전달하는 것

1. 가장 단순한 방법: 전체 가져와서 전달

조건
1. 필터링
- 카테고리
- 제품명

2. 정렬
- 신상품
- 오래된 상품
- 이름
- 이름 역순
- 가격 오름
- 가격 내림
- 후기 많은
- 판매량

3. 페이지네이션
- limit  : 1번 응답 당 데이터 수
- offset : 몇 번째 위치부터 

"""

class ProductOption(Enum):
    ONE = 1
    TEN = 2 

class ProductListView(View):
    def get(self, request):
        try:
            category = request.GET.get('category')
            search   = request.GET.get('search')
            sort     = request.GET.get('sort', 'name')
            offset   = int(request.GET.get('offset', 0))
            limit    = int(request.GET.get('limit', 6))

            q = Q()

            q &= Q(options__id=ProductOption.ONE.value)

            if category:
                q &= Q(category__name__contains=category)

            if search:
                q &= Q(name__contains=search)
            
            sort_set = {
                "new"    : "-created_at",
                "old"    : "created_at",
                "price"  : "options__price",
                "-price" : "-options__price",
                "review" : "-review_count",
                "sales"  : "-sales_sum",
            }

            sort = sort_set.get(sort, "name")

            review_count = Product.objects.annotate(review_count=Count('reviews')).filter(pk=OuterRef('pk'))
            sales_sum    = Product.objects.annotate(sales_sum=Sum('options__items__quantity')).filter(pk=OuterRef('pk'))
            products     = Product.objects\
                                  .filter(q)\
                                  .annotate(
                                      review_count = Subquery(review_count.values('review_count'),output_field = IntegerField()),
                                      sales_sum    = Subquery(sales_sum.values('sales_sum'), output_field=IntegerField())
                                    )\
                                  .order_by(sort).distinct()[offset:offset+limit]
            
            product_list = [{
                "product_id"      : product.id,
                "name"            : product.name,
                "description"     : product.description,
                "thumbnail_url"   : product.thumbnail_url,
                "review_count"    : product.reviews.count(),
                "price"           : product.options.first().price,
                "discount_rate"   : product.discount_rate,
                "discounted_price": product.options.first().price * (100 - product.discount_rate)/100
            } for product in products]

            return JsonResponse({"data": product_list}, status=200)