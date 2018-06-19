from django.db import models
from carts.models import Cart
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_id_generator
import math
from billing.models import BillingProfile
from address.models import Address
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        qs = self.get_queryset().filter(cart=cart_obj, billing_profile=billing_profile, active=True, status='created')
        if qs.count() == 1:
            order_obj = qs.first()
        else:
            order_obj = self.model.objects.create(cart=cart_obj,
                                             billing_profile=billing_profile)
        return order_obj



class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    active = models.BooleanField(default=True)
    order_id = models.CharField(max_length=120, blank=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name="billing_address", blank=True, null=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(decimal_places=2, max_digits=40,default=6.99)
    total = models.DecimalField(decimal_places=2, max_digits=40,default=0.00)
    objects = OrderManager()

    def __str__(self):
        return self.order_id


    def update_total(self):
        #print("update_total")
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        total = format(math.fsum([cart_total,shipping_total]),'.2f')
        self.total = total
        self.save()
        return total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total

        if billing_profile and shipping_address and billing_address and total>0:

            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status





def pre_save_create_order_id(sender, instance, *args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart = instance
        cart_total = cart.total
        cart_id = cart.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists() and qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        instance.update_total()
        print("update")

post_save.connect(post_save_order, sender=Order)






