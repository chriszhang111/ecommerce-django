from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    type = models.CharField(max_length=30, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120, null=True,blank=True)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30, default='US')
    state = models.CharField(max_length=30)
    post_code = models.CharField(max_length=30)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
            line1=self.address_line1,
            line2=self.address_line2 or "",
            city=self.city,
            state=self.state,
            postal=self.post_code,
            country=self.country
        )


