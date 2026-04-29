from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart': cart}
        except Cart.DoesNotExist:
            return {'cart': None}
    return {'cart': None}
