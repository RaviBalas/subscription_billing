from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subscription, SubscriptionStatus, Plans
from .serializers import SubscribeSerializer, UnSubscribeSerializer, PlanSerializer


class SubscribePlanView(APIView):

    def post(self, request):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        serializer = SubscribeSerializer(data=request.data | {"user": request.user.id})
        if serializer.is_valid():
            serializer.save()
            output["message"] = "Subscribed successfully."
        else:
            output.update({"type": "error", "data": serializer.errors})
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(output, status=status_code)


class UnSubscribePlanView(APIView):
    def post(self, request):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        serializer = UnSubscribeSerializer(data=request.data | {"user": request.user.id})
        if serializer.is_valid():
            request.user.my_subscriptions.filter(
                plan=serializer.data["plan"], is_active=True
            ).update(is_active=False, status=SubscriptionStatus.CANCELLED)
            output["message"] = "Unsubscribed successfully."
        else:
            output.update({"type": "error", "data": serializer.errors})
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(output, status=status_code)


class PlanView(generics.ListCreateAPIView):
    queryset = Plans.objects.all()
    serializer_class = PlanSerializer

    def get(self, request, *args, **kwargs):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        plans = self.get_queryset()
        output["data"] = self.get_serializer(plans, many=True).data
        return Response(output, status=status_code)
