from django.contrib import admin

# Register your models here.
from app.models import AccountNumber, Transaction, Transfer

admin.site.register(AccountNumber)
admin.site.register(Transaction)
admin.site.register(Transfer)
