from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from app.models import AccountNumber, Transaction, Transfer
how_many_days = 30


class LimitedAccessMixin:

    def get_queryset(self):
        return AccountNumber.objects.filter(user=self.request.user)


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("login_view")


def homepage(request):
    return HttpResponseRedirect(reverse('login_view'))


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
        form_object = form.save(commit=False)
        acct_num = AccountNumber.objects.get(pk=self.kwargs['pk'])
        form_object.account = acct_num
        if form_object.account > 0:
            if form_object.trans_type == 'd':
                new_balance = acct_num.balance + form_object.amount
                AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
            elif form_object.trans_type == 'w':
                if form_object.amount > acct_num.balance:
                    return HttpResponseRedirect('/overdraft')
                else:
                    new_balance = acct_num.balance - form_object.amount
                    AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
            form_object.save()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('/overdraft')

    def get_success_url(self):
        return reverse("trans_list_view")


class TransListView(ListView):
    model = Transaction
    model.objects.filter(time_created=datetime.now()-timedelta(days=how_many_days))


class TransDetailView(DetailView):
    model = Transaction


class TransferCreateView(CreateView):
    model = Transfer
    fields = ('account', 'amount')

    def form_valid(self, form):
        form_object = form.save(commit=False)
        acct_num_from = AccountNumber.objects.get(pk=self.kwargs['pk'])
        if acct_num_from == AccountNumber:
            new_balance_from = acct_num_from.balance - form_object.amount
            new_balance_to = form_object.balance + form_object.amount
            if new_balance_from < 0:
                return HttpResponseRedirect('/overdraft')
            elif new_balance_to < 0:
                return HttpResponseRedirect('/overdraft')
            else:
                AccountNumber.objects.filter(pk=form_object.account.id).update(balance=new_balance_to)
                AccountNumber.objects.filter(pk=self.kwargs['pk']).update(balance=new_balance_from)
                form_object.save()
                return super().form_valid(form)
        else:
            return HttpResponseRedirect('/overdraft')

    def get_success_url(self):
        return reverse("account_list_view")


class OverDraftView(TemplateView):
    template_name = 'overdraft.html'


class TransferListView(ListView):
    model = Transfer

    def get_queryset(self):
        return Transfer.objects.filter(account__user=self.request.user)


class TransferDetailView(DetailView):
    model = Transfer
