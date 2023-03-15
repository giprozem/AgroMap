import os
import shutil

from PIL import Image
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ultralytics import YOLO

from container.forms import ImageBinForm, LastImageBinForm
from container.models import ImageBin


# ANYX.G3kjEDerD_ test


class PredictAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        model = YOLO("./bestlast.pt")
        if request.data:
            results = model.predict(source=Image.open(request.data['image']).convert('RGB'), save=True, conf=0.55)
            for result in results:
                path = result.path
                count = result.boxes.shape[0]
                probs = result.probs  # Class probabilities
                percent = result.boxes.conf.tolist()

                """array = np.zeros(result.orig_img.shape, dtype=np.uint8)
                img = Image.fromarray(array, mode='RGB')
                image_bin = ImageBin.objects.create()
                stream = BytesIO()
                img.save(stream, format='PNG')
                content = ContentFile(stream.getvalue())
                image_bin.image.save('filename.png', content)"""
                image_bin = ImageBin.objects.create()
                image_bin.image.save(os.listdir('runs/detect/predict/')[0],
                                     open(f"runs/detect/predict/{os.listdir('runs/detect/predict/')[0]}", 'rb'))
                shutil.rmtree('runs')
                return Response({"Quantity": count, "Percent": [round(i, 2) for i in percent], "Color": 'Unknown',
                                 "Capacity Type": "Unknown",
                                 "Container color": 'Unknown', "No wheel": "Unknown",
                                 "Capacity upside down": 'Unknown',
                                 "The integrity of the container is broken": "Unknown",
                                 "The presence of traces of damage to the container by fire": 'Unknown',
                                 "Hull damage": "Unknown",
                                 "Damage to structural elements for loading waste": 'Unknown', "Smoke": "Unknown",
                                 "Fire": 'Unknown', "Type of waste": "Unknown", "image_url": image_bin.image.url})

        else:
            return Response(data={"message": "parameter 'image' is required"}, status=400)


@csrf_exempt
def predicting(request):
    form = ImageBinForm()
    model = YOLO("./bestlast.pt")
    if request.POST:
        form = ImageBinForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            results = model.predict(source=Image.open(request.FILES['image']).convert('RGB'), save=True, conf=0.8)
            for result in results:
                path = result.path
                count = result.boxes.shape[0]
                probs = result.probs  # Class probabilities
                percent = result.boxes.conf.tolist()

                """array = np.zeros(result.orig_img.shape, dtype=np.uint8)
                img = Image.fromarray(array, mode='RGB')
                image_bin = ImageBin.objects.create()
                stream = BytesIO()
                img.save(stream, format='PNG')
                content = ContentFile(stream.getvalue())
                image_bin.image.save('filename.png', content)"""
                image_bin = ImageBin.objects.create(object_quantity=count, percent=[round(i, 2) for i in percent])
                image_bin.image.save(os.listdir('runs/detect/predict/')[0],
                                     open(f"runs/detect/predict/{os.listdir('runs/detect/predict/')[0]}", 'rb'))
                shutil.rmtree('runs')
            return redirect('last_predict')
    return render(request, 'my.html',  {'form': form})


@csrf_exempt
def last_predict(request):
    image = ImageBin.objects.all().last()
    return render(request, 'lat_object.html', {'image': image})
