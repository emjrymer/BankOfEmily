from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
#from datetime import datetime, timedelta, aMonthAgo
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DetailView, ListView

from app.models import AccountNumber, Transaction, Transfer


class LimitedAccessMixin:

    def get_queryset(self):
        return AccountNumber.objects.filter(user=self.request.user)


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("login_view")


class AccountNumberList(LimitedAccessMixin, ListView):
    model = AccountNumber


class AccountCreateView(CreateView):
    model = AccountNumber
    fields = ('nickname', 'balance')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account_list_view")


class AccountDetailView(LimitedAccessMixin, DetailView):
    model = AccountNumber


class TransCreateView(CreateView):
    model = Transaction
    fields = ('trans_type', 'amount', 'description')

    def form_valid(self, form):
        object = form.save(commit=False)
        acct_num = AccountNumber.objects.get(user=self.request.user)
        object.account = acct_num
        if object.trans_type == 'd':
            new_balance = acct_num.balance + object.amount
            AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
        elif object.trans_type == 'w':
            if object.amount > acct_num.balance:
                return "Insufficient Funds"
            else:
                new_balance = acct_num.balance - object.amount
                AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("trans_list_view")


class TransListView(ListView):
    model = Transaction
    #items = model.objects.filter(created_date__gte=aMonthAgo)


class TransDetailView(DetailView):
    model = Transaction


class TransferCreateView(CreateView):
    model = Transfer
    fields = ('account', 'amount')

    def get_queryset(self):
        return AccountNumber.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("account_list_view")
