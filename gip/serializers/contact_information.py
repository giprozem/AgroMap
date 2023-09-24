from rest_framework import serializers

from gip.models import Department, ContactInformation

# Serializer for the Department model
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  # Specify the model to serialize
        fields = '__all__'  # Serialize all fields of the model

# Serializer for the ContactInformation model
class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation  # Specify the model to serialize
        fields = '__all__'  # Serialize all fields of the model

    # Customize the representation of the serialized data
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Add a 'department' key with nested data for department information
        representation['department'] = {
            'id': instance.department.pk,
            'name': instance.department.name
        }
        
        # Add a 'district' key with nested data for district information
        representation['district'] = {
            'id': instance.district.pk,
            'name': instance.district.name,
            'region': {
                'id': instance.district.region.pk,
                'name': instance.district.region.name
            }
        }
        
        return representation
