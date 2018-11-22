from django.contrib import admin
from .models import Account, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display= ('name', 'getUser', 'balance')
    list_filter = ('name', 'user__username')
    search_fields = ('name', 'user__username')

    def getUser(self, obj):
        return obj.user.username
    getUser.short_description = 'User'
    getUser.admin_order_field = 'user__username'

class TransactionAdmin(admin.ModelAdmin):
    list_display= ('getAccount', 'getUser', 'amount', 'transaction_date', 'active')
    list_display_links = ('amount', 'transaction_date')
    list_filter = ('account__user__username', 'account__name', 'transaction_date', 'active')
    search_fields = ('account__user__username', 'account__name', 'transaction_date')

    def getAccount(self, obj):
        return obj.account.name
    getAccount.short_description = 'Account'
    getAccount.admin_order_field = 'account__name'

    def getUser(self, obj):
        return obj.account.user.username
    getUser.short_description = 'User'
    getUser.admin_order_field = 'account__user__username'


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
