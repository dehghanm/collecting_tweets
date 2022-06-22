from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.models import TwitterAccount
from core.serilizers import GetAllAccountsSerializer, AccountsManagementSerializer
from core.tools import check_file_if_exist, remove_csv_file


class GetCSVFile(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            if check_file_if_exist():
                with open('all_tweets.csv') as my_file:
                    response = HttpResponse(my_file, content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=all_tweets.csv'
                    return response
            else:
                response_message = {"message": "file is downloaded before."}
                return Response(response_message, status=status.HTTP_200_OK)
        finally:
            remove_csv_file()


class GetAllAccounts(APIView):

    def get(self, request):
        all_accounts = TwitterAccount.objects.all()
        data = GetAllAccountsSerializer(all_accounts, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class AccountsManagement(APIView):

    def post(self, request):
        serializer = AccountsManagementSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.do_action()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
