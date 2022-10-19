from rest_framework import serializers

from agrobase.models import Material, MaterialImage, MaterialBlock


class InlineMaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialImage
        exclude = ('material', )


class InlineMaterialBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBlock
        exclude = ('material', )


class MaterialSerializer(serializers.ModelSerializer):
    images = InlineMaterialImageSerializer(many=True, read_only=True)
    blogs = InlineMaterialBlockSerializer(many=True, read_only=True)

    class Meta:
        model = Material
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {'id': instance.category, 'title': instance.get_category_display()}
        representation['images'] = InlineMaterialImageSerializer(instance.material_images.all(), many=True, context=self.context).data
        representation['blocks'] = InlineMaterialBlockSerializer(instance.material_blocks.all(), many=True, context=self.context).data
        return representation


class MaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialImage
        fields = '__all__'


class MaterialBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBlock
        fields = '__all__'