from rest_framework import serializers

from agrobase.models import Material, MaterialImage, MaterialBlock


class InlineMaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialImage
        exclude = ('material', )


class InlineMaterialBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBlock
        exclude = ('material', )


class MaterialSerializer(serializers.ModelSerializer):
    images = InlineMaterialImageSerializer(many=True, read_only=True)
    blogs = InlineMaterialBlogSerializer(many=True, read_only=True)

    class Meta:
        model = Material
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {'id': instance.category, 'title': instance.get_category_display()}
        representation['images'] = InlineMaterialImageSerializer(instance.material_images.all(), many=True, context=self.context).data
        representation['blocks'] = InlineMaterialBlogSerializer(instance.material_blocks.all(), many=True, context=self.context).data
        return representation
