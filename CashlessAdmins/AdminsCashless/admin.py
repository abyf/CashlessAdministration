from django.contrib import admin
from . models import CardHolder, Merchant, Administrator

class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','address','email','created_at', 'modified_at')

class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','card_id','qr_code','balance','created_at', 'modified_at')

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','email','reader_id','wallet_id', 'balance','created_at', 'modified_at')


admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(CardHolder,CardHolderAdmin)
admin.site.register(Merchant,MerchantAdmin)
