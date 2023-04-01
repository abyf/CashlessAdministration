from django.db import models
import uuid
from django.contrib.auth.models import User, Group

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrators')
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Administrator, add them to the Administrator Group
            group = Group.objects.get(name='administrators')
            self.user.groups.add(group)
        #if the user has been used, disable it before saving
        if Administrator.objects.filter(user=self.user).exclude(pk=self.pk).exists():
            self.user.is_active = False
            self.user.save()
        super().save(*args, **kwargs)

class CardHolder(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    card_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True,null=True, blank=True)
    qr_code = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=3)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Administrator, add them to the Administrator Group
            group = Group.objects.get(name='cardholders')
            self.user.groups.add(group)
        super().save(*args, **kwargs)

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='merchants')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=2)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    reader_id = models.CharField(max_length=50,null=True, blank=True, unique=True)
    wallet_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Merchant, add them to the merchant Group
            group = Group.objects.get(name='merchant')
            self.user.groups.add(group)
        super().save(*args, **kwargs)


class Transaction(models.Model):
    cardholder = models.ForeignKey(CardHolder, on_delete=models.CASCADE,null=True,blank=True, related_name='transactions')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE,null=True,blank=True, related_name='transactions')
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL, null=True,related_name='transactions')
    amount = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    message = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{administrator} credited {amount} to {cardholder} card'.format(administrator=self.administrator,cardholder=self.cardholder,amount=self.amount)
