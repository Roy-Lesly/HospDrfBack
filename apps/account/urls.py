from django.urls import path
from rest_framework.routers import DefaultRouter
# from .views import CreateAccount
from .views import (AccountNameView, MeView, 
    LoginView, UpdatePasswordView, AccountViewSet)

app_name = 'apps.account'

# router = DefaultRouter()
router = DefaultRouter(trailing_slash=False)
router.register('login', LoginView, basename='login',)
router.register('account', AccountViewSet, 'account',)
router.register('update-account-password', UpdatePasswordView, 'update_account_password',)
router.register('me', MeView, basename='me',)
router.register('accountname', AccountNameView, basename='account_name')

urlpatterns = router.urls

# urlpatterns = [
#     path('createaccount/', CreateAccountView.as_view(), name="createaccount"),
#     path('listaccount/', CreateAccountView.as_view(), name="createaccount"),
#     path('retrieveaccount/', CreateAccountView.as_view(), name="createaccount"),
#     path('veaccount/', CreateAccountView.as_view(), name="createaccount"),
# ]