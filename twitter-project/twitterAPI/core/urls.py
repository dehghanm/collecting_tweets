from django.urls import path

from core.views import GetCSVFile, GetAllAccounts, AccountsManagement

app_name = 'core'

urlpatterns = [
    path('get-csv-file/', GetCSVFile.as_view(), name='get_csv_file'),
    path('get-all-accounts/', GetAllAccounts.as_view(), name='get_all_accounts'),
    path('accounts-management/', AccountsManagement.as_view(), name='accounts_management'),
]
