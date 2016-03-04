from django.contrib.auth.models import User
from django.db import models

# Create your models here.
TYPE_CHOICES = [('w', 'withdrawal'), ('d', 'deposit')]


class AccountNumber(models.Model):
    nickname = models.CharField(max_length=20)
    balance = models.IntegerField()
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.user)


class Transaction(models.Model):
    account = models.ForeignKey(AccountNumber)
    trans_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    description = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_created"]


class Transfer(models.Model):
    account = models.ForeignKey(AccountNumber)
    amount = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
