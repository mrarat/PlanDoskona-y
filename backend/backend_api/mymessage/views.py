from django.http import JsonResponse
from rest_framework.views import APIView

class MyMessageView(APIView):
    def get(self, request):
        msg = request.GET.get('msg')
        if msg:
            response_data = {'message': f'{msg} brrr!'}
            return JsonResponse(response_data)
        else:
            response_data = {'error': 'No message parameter provided'}
            return JsonResponse(response_data, status=400)