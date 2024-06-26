
from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'balance')
    search_fields = ('user__username', 'address')
    readonly_fields = ('private_key',)
    fieldsets = (
        (None, {
            'fields': ('user', 'address', 'balance')
        }),
        ('Security', {
            'fields': ('private_key',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'amount', 'timestamp', 'transaction_hash', 'status')
    search_fields = ('sender__address', 'recipient', 'transaction_hash')
    list_filter = ('status', 'timestamp')
    readonly_fields = ('transaction_hash', 'timestamp')
    fieldsets = (
        (None, {
            'fields': ('sender', 'recipient', 'amount', 'status')
        }),
        ('Advanced options', {
            'fields': ('transaction_hash', 'block_number', 'fee'),
            'classes': ('collapse',),
        }),
    )
