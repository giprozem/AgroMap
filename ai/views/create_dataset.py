from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.signals import post_save
from django.dispatch import receiver
from ai.models.create_dataset import Dataset, Process, CreateDescription
from notifications.signals import notify

from ai.serializers import CreateDescriptionSerializer
from ai.utils.predicted_contour import deleted_files


class CreateAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        process = Process.objects.get(id=1)
        if process.is_running:
            message = "Процесс сейчас идёт"
        else:
            user = request.user
            Process.objects.all().delete()
            Process.objects.create(is_running=True, type_of_process=2)
            @receiver(post_save, sender=Dataset)
            def my_handler(sender, instance, created, **kwargs):
                if created:
                    notify.send(instance, recipient=user, verb=f'Датасет №{instance.pk} создан')
                    deleted_files()
            message = "Процесс запущен"
        return Response({"message": message})


class CreateDescriptionAPIView(APIView):
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        responses={200: CreateDescriptionSerializer(many=True)},
        operation_summary='return instruction of creating dataset required adminuser'
    )
    def get(self, *args, **kwargs):
        query = CreateDescription.objects.all()
        serializer = CreateDescriptionSerializer(query, many=True)
        return Response(serializer.data, status=200)
