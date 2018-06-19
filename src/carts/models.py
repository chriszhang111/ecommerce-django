from django.conf import settings
from django.db import models
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
from decimal import Decimal
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user == None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = self.new(user=request.user)
            request.session["cart_id"] = cart_obj.id
        return cart_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user

        return self.model.objects.create(user=user_obj)



class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=40,default=0.00)
    subtotal = models.DecimalField(decimal_places=2, max_digits=40, default=0.00)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action in ('post_add','post_remove','post_clear'):
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        instance.subtotal = total
        instance.save()

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = format(Decimal(instance.subtotal)*Decimal(1.05), '.2f')


m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)
pre_save.connect(pre_save_cart_receiver,sender=Cart)