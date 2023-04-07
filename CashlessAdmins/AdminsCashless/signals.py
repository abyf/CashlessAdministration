import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .webhook import WebhookSerializer
from .models import CarHolder, Merchant,Payment, Transaction


@receiver(post_save,sender=CardHolder)
@receiver(post_save,sender=Merchant)
@receiver(post_save,sender=Transaction)
@receiver(post_save,sender=Payment)
def notify_update(sender,instance,created,**kwargs):
    if created:
        # Check if user is a cardholder or merchant
        if instance.groups.filter(name__in=['cardholders','merchant']).exists():
            #Send signal for new cardholder or merchant
            payload = WebhookSerializer(instance).data
            headers = {'content-type':'application/json'}
            url = ''
            response = requests.post(ur,json=payload,headers=headers)
            if response.status_code != 200:
                #handle error here
                pass
        elif isinstance(instance,payment):
        else:
            ###instance  is a transaction
