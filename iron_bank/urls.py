
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app.views import SignUpView, AccountNumberList, AccountCreateView, AccountDetailView, TransCreateView, TransListView, TransferCreateView, TransDetailView, OverDraftView, \
    TransferListView, homepage, TransferDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', homepage),
    url(r'^signup/$', SignUpView.as_view(), name="signup_view"),
    url(r'^login/$', auth_views.login, name="login_view"),
    url(r'^logout/$', auth_views.logout_then_login, name="logout_view"),
    url(r'^transactionlist/(?P<pk>\d+)/$', TransListView.as_view(), name="trans_list_view"),
    url(r'^accountlist/$', AccountNumberList.as_view(), name="account_list_view"),
    url(r'^accountcreate/$', AccountCreateView.as_view(), name="create_account_view"),
    url(r'^accountdetail/(?P<pk>\d+)/$', AccountDetailView.as_view(), name="account_detail_view"),
    url(r'^createtransaction/(?P<pk>\d+)/$', TransCreateView.as_view(), name="trans_create_view"),
    url(r'^transdetail/(?P<pk>\d+)/$', TransDetailView.as_view(), name="trans_detail_view"),
    url(r'^transfer/(?P<pk>\d+)/$', TransferCreateView.as_view(), name="transfer_create_view"),
    url(r'^overdraft/', OverDraftView.as_view(), name="over_view"),
    url(r'^transferlist/$', TransferListView.as_view(), name="transfer_list_view"),
    url(r'^transferdetails/(?P<pk>\d+)', TransferDetailView.as_view(), name="transfer_detail_view")
]
