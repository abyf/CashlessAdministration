from django.db import models
import uuid,random,string
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

class Manager(models.Model):
    username = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    email = models.EmailField(max_length=120,null=True, blank=True)
    cardholder_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    merchant_commission = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrators')
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
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
    phone = models.CharField(max_length=120)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    card_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True,null=True, blank=True)
    qr_code = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=3)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Administrator, add them to the Administrator Group
            group = Group.objects.get(name='cardholders')
            self.group = group
        if not self.alias:
            while True:
                new_alias = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not CardHolder.objects.filter(alias=new_alias).exists():
                    break
            self.alias = new_alias
        super().save(*args, **kwargs)

class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='merchants')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,default=2)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    address = models.CharField(max_length=250,null=True, blank=True)
    email = models.EmailField(max_length=120,null=True, blank=True)
    reader_id = models.CharField(max_length=50,null=True, blank=True, unique=True)
    wallet_id = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)
    alias = models.CharField(max_length=8,unique=True,editable=False)
    balance = models.DecimalField(max_digits=250,decimal_places=2,default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name}:{phone}".format(name=self.name,phone=self.phone)

    def save(self,*args,**kwargs):
        if not self.pk:
            #If this is a new Merchant, add them to the merchant Group
            group = Group.objects.get(name='merchant')
            self.user.groups.add(group)
        if not self.alias:
            while True:
                new_alias = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not Merchant.objects.filter(alias=new_alias).exists():
                    break
            self.alias = new_alias
        super().save(*args, **kwargs)


class Transaction(models.Model):
    TRANSACTION_TYPES = [('load','Load'),('withdraw','Withdraw')]
    cardholder_alias = models.CharField(max_length=8,null=True,blank=True)
    merchant_alias = models.CharField(max_length=8,null=True,blank=True)
    card_id = models.UUIDField(unique=True,null=True, blank=True)
    qr_code = models.UUIDField(unique=True,null=True, blank=True)
    amount = models.DecimalField(max_digits=250,decimal_places=2,null=True, blank=True)
    message = models.CharField(max_length=1000, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES,max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.cardholder_alias or self.card_id or self.qr_code:
            return "Cardholder {cardholder_alias} credited ${amount} at {date}".format(cardholder_alias=self.cardholder_alias,amount=self.amount,date=self.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        elif self.merchant_alias:
            return "Merchant {merchant_alias} withdrew ${amount} at {date}".format(merchant_alias=self.merchant_alias,amount=self.amount,date=self.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return "Unknown transaction"

    def clean(self):
        if not any([self.cardholder_alias,self.card_id,self.qr_code]):
            raise ValidationError("At least one of the fields 'cardholder_alias', 'card_id', or 'qr_code' must be provided.")
        if self.cardholder_alias and not CardHolder.objects.filter(alias=self.cardholder_alias).exists():
            raise ValidationError("Cardholder with alias {} does not exist.".format(self.cardholder_alias))
        if self.merchant_alias and not Merchant.objects.filter(alias=self.merchant_alias).exists():
            raise ValidationError("Merchant with alias {} does not exist.".format(self.merchant_alias))
        if self.card_id and not CardHolder.objects.filter(card_id=self.card_id).exists():
            raise ValidationError("Cardholder with Card ID {} does not exist.".format(self.card_id))
        if self.qr_code and not CardHolder.objects.filter(qr_code=self.qr_code).exists():
            raise ValidationError("Cardholder with QR code {} does not exist.".format(self.qr_code))

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)
