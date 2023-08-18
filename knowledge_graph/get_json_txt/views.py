from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # store to db
            # JsonData.objects.create(data=data)
            print(data)
            return JsonResponse({"message": "Success"})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Failed"}, status=400)
    else:
        return JsonResponse({'message': 'Only accpet POST reqiest'}, status=405)

