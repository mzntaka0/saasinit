from django.db import models

from accounts.models import TenantRelatedModel
from next import consts


# TODO: Is these models related with subscription needed?
class Plan(models.Model):
    name = models.CharField(max_length=20)
    basic_usage_fee = models.FloatField()
    pay_per_use_fee = models.FloatField()


class Subscription(TenantRelatedModel):
    PLAN_TYPE = consts.PLAN_TYPE

    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    stripe_subscription_id = models.CharField(max_length=255)
    stripe_plan_id = models.CharField(max_length=255)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True)
    billing_period_ends_at = models.DateTimeField(null=True)


class Payment(TenantRelatedModel):
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


#class Refund(models.Model):
#    order = models.ForeignKey(Order, on_delete=models.CASCADE)
#    reason = models.TextField()
#    accepted = models.BooleanField(default=False)
#    email = models.EmailField()
#
#    def __str__(self):
#        return f"{self.pk}"
