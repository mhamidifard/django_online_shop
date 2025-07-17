from rest_framework import serializers

from accounts.serilizers import UserProfileSerializer
from product_reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'created_at': {'read_only': True}}


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def validate(self, attrs):
        user = self.context['request'].user
        product_id = self.context['view'].kwargs['product_id']
        if Review.objects.filter(product_id=product_id, user=user).exists():
            raise serializers.ValidationError("You have already submitted a review for this product.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = self.context['view'].kwargs['product_id']
        return Review.objects.create(
            product_id=product_id,
            user=user,
            **validated_data
        )
