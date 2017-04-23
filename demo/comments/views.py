from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Comment, IPLockout
from .serializers import CommentSerializer

import datetime

class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoints that allow comments to be posted or viewed.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def list(self, request):
        url = request.GET.get('url', '')
        queryset = Comment.objects.filter(url=url)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        # Validate data and check if the user is locked out from a previous submission
        if serializer.is_valid(raise_exception=True) and not self._locked_out(serializer.validated_data.get('posting_ip', None)):
            Comment.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Comment could not be saved: user is locked out.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def _locked_out(self, ip_address):
        return True if not ip_address else IPLockout.objects.filter(ip_address=ip_address, locked_until__gt=datetime.datetime.now()).exists()