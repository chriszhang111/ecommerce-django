from django.forms import ModelForm

from .models import Address

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'address_line1',
            'address_line2',
            'city',
            'country',
            'state',
            'post_code'
        ]




