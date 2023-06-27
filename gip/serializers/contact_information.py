from rest_framework import serializers

from gip.models import Department, ContactInformation


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = {'id': instance.department.pk, 'name': instance.department.name}
        representation['district'] = {'id': instance.district.pk, 'name': instance.district.name,
                                      'region': {'id': instance.district.region.pk,
                                                 'name': instance.district.region.name}}
        return representation
