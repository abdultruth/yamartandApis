from account_API import serializer
from rest_framework import viewsets, generics



from account_API.serializer import UserSerializer


from account.models import CustomUser


class UserDetailApiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    


# ViewSets define the view behavior.
class UserApiViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

