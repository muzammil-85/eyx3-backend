from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import DetectionSerializer
from .models import Detection, Doctor, User
from .stellar_utils import create_transaction

from rest_framework.views import APIView
from rest_framework import status
from .stellar_utils import reward_user_with_stellar

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    @action(detail=True, methods=['post'])
    def contact_doctor(self, request, pk=None):
        detection = self.get_object()
        detection.user_contacted_doctor = True
        detection.save()
        return Response({'status': 'Doctor contacted'})

    @action(detail=True, methods=['post'])
    def reward_user(self, request, pk=None):
        detection = self.get_object()
        user = User.objects.get(pk=request.data['user_id'])
        create_transaction(user.stellar_address, amount=10)  # Adjust the amount as needed
        detection.user_rewarded = True
        detection.save()
        return Response({'status': 'User rewarded'})

    @action(detail=True, methods=['post'])
    def reward_doctor(self, request, pk=None):
        detection = self.get_object()
        doctor = Doctor.objects.get(pk=request.data['doctor_id'])
        create_transaction(doctor.stellar_address, amount=10)  # Adjust the amount as needed
        detection.doctor_rewarded = True
        detection.save()
        return Response({'status': 'Doctor rewarded'})



class RewardUserView(APIView):
    def post(self, request, detection_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"detail": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            detection = Detection.objects.get(id=detection_id)
            user = User.objects.get(id=user_id)
        except Detection.DoesNotExist:
            return Response({"detail": "Detection not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Reward the user
        reward_amount = 1  # Assuming you have a reward_amount field in your Detection model    
        response = reward_user_with_stellar(user.stellar_address, reward_amount)
        
        if response is None:
            return Response({"detail": "Failed to send reward."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        detection.user_rewarded = True
        detection.save()

        return Response({"detail": "User rewarded successfully."}, status=status.HTTP_200_OK)