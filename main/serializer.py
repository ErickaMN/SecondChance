from rest_framework import serializers
from .models import Category, Post, PostImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        created_post = Post.objects.create(**validated_data)
        images_objects = [PostImage(post=created_post, image=image) for image in images_data.getlist('images')]
        PostImage.objects.bulk_create(images_objects)
        return created_post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation (self, instance):
        representation = super().to_representation(instance)
        representation ['image'] = self._get_image_url(instance)
        return representation

