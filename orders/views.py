import json

from django.http  import JsonResponse
from django.views import View

from orders.models   import Cart
from products.models import ProductOption
from users.utils     import login_decorator

class CartView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        cart = Cart.objects.select_related('product_option').filter(user=user)

        if not cart.exists():
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=404)

        result = [{
            'cart_id'            : item.id,
            'product_name'       : item.product_option.product.name,
            'product_option_id'  : item.product_option_id,
            'product_option_name': item.product_option.name,
            'thumbnail_url'      : item.product_option.product.thumbnail_url,
            'price'              : item.product_option.price,
            'discounted_price'   : item.product_option.price * \
                (100 - item.product_option.product.discount_rate)/100,
            'quantity'           : item.quantity,
            'item_total'         : item.product_option.price * \
                (100 - item.product_option.product.discount_rate)/100 * item.quantity,
            } for item in cart ]

        total_bill    = int(sum(item['item_total'] for item in result))
        shipping_cost = 0 if total_bill >= 30000 else 3000

        return JsonResponse({
            "data"         : result, 
            "total_bill"   : total_bill + shipping_cost,
            "shipping_cost": shipping_cost,
            "shipping_info": "유료배송, 3000원" if shipping_cost else "무료배송"}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data              = json.loads(request.body)
            user              = request.user
            product_option_id = data["product_option_id"]
            quantity          = data["quantity"]

            if not ProductOption.objects.filter(id=product_option_id).exists():
                return JsonResponse({"message": "PRODUCT_OPTION_NOT_EXIST"}, status=404)

            if Cart.objects.filter(user=user, product_option_id=product_option_id).exists():
                cart           = Cart.objects.filter(user=user).get(product_option_id=product_option_id)
                cart.quantity += quantity
                cart.save()
                return JsonResponse({"message": "PRODUCT_QUANTITY_UPDATED"}, status=201)

            Cart.objects.create(
                user              = user,
                product_option_id = product_option_id,
                quantity          = quantity,
            )
            return JsonResponse({"message": "CART_CREATED"}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)
    
    @login_decorator
    def patch(self, request):
        try:
            data                  = json.loads(request.body)
            user                  = request.user
            product_option_id     = data['product_option_id']
            quantity              = data['quantity']
            
            if not Cart.objects.filter(user=user, product_option_id=product_option_id).exists():
                return JsonResponse({"message": "CART_NOT_EXIST"}, status=404)
            
            cart          = Cart.objects.get(user=user, product_option_id=product_option_id)
            cart.quantity = quantity
            cart.save()

            if cart.quantity <= 0:
                return JsonResponse({"message": "PRODUCT_QUANTITY_ERROR"}, status=400)

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "CART_NOT_EXIST"}, status=404)  

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

    @login_decorator
    def delete(self, request):
        cart_remove_list = request.GET.getlist('cart_id', None)
        cart             = Cart.objects.filter(id__in=cart_remove_list, user=request.user)

        if not cart.exists():
            return JsonResponse({"message": "CART_NOT_EXIST"}, status=404)
        
        cart.delete()
        return JsonResponse({"message": "CART_DELETED"}, status=204)