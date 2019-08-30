from django.db import models
from billing.models import BillingProfile
# Create your models here.
ADDRESS_TYPE=(('billing','Billing'),('shipping','Shipping'))
class Address(models.Model):
    billing_profile=models.ForeignKey(BillingProfile)
    address_type=models.CharField(max_length=1120,choices=ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=120)
    address_line_2=models.CharField(max_length=120,null=True,blank=True)
    city=models.CharField(max_length=120)
    country=  models.CharField(max_length=120,default="United State Of America")                                                              
    state=models.CharField(max_length=120)
    postal=models.CharField(max_length=120)


    def __str__(self):
        return str(self.billing_profile)
     
    def get_address(self):
        return "{line1}\n{line2}\n{city}\n{state},\n{postal}\n{country}".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            state=self.state,
            postal=self.postal,
            country=self.country



        )
