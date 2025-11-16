from rest_framework import serializers
from .models import LostItem, FoundItem, Claim, CustomUser, Testimonial, ChatMessage

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class LostItemNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostItem
        fields = ['id', 'item_name', 'image', 'description', 'location', 'date_lost', 'category']

class FoundItemNestedSerializer(serializers.ModelSerializer):
    finder = UserNestedSerializer(read_only=True)
    class Meta:
        model = FoundItem
        fields = ['id', 'item_name', 'image', 'description', 'location_found', 'date_found', 'category', 'finder']

class ClaimNestedSerializer(serializers.ModelSerializer):
    claimant = UserNestedSerializer(read_only=True)
    class Meta:
        model = Claim
        fields = ['id', 'status', 'claimant']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserNestedSerializer(read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'timestamp']

class FoundItemSerializer(serializers.ModelSerializer):
    finder_username = serializers.ReadOnlyField(source='finder.username')
    has_user_claimed = serializers.SerializerMethodField()
    claims = ClaimNestedSerializer(many=True, read_only=True)
    class Meta:
        model = FoundItem
        fields = ['id','item_name','category','date_found','location_found','description','image','created_at','status','finder','finder_username','has_user_claimed','claims']
        read_only_fields = ('finder', 'status',)
    def get_has_user_claimed(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return Claim.objects.filter(found_item=obj, claimant=user).exists()
        return False

class LostItemSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    claims = ClaimNestedSerializer(many=True, read_only=True)
    class Meta:
        model = LostItem
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {'image': {'required': False}}

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'
        read_only_fields = ['claimant', 'status', 'chat_id', 'exchange_token']

class ClaimDetailSerializer(serializers.ModelSerializer):
    found_item = FoundItemNestedSerializer(read_only=True)
    lost_item = LostItemNestedSerializer(read_only=True)
    has_testimonial = serializers.SerializerMethodField()
    claimant = UserNestedSerializer(read_only=True)
    
    # --- 1. ADD THIS NEW FIELD FOR THE QR CODE TOKEN ---
    exchange_token = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = [
            'id', 'found_item', 'lost_item', 'claimant', 'status', 
            'created_at', 'chat_id', 'has_testimonial', 
            'exchange_token' # <-- 2. Added to fields
        ]

    def get_has_testimonial(self, obj):
        return hasattr(obj, 'testimonial')
        
    # --- 3. ADD THIS METHOD TO SECURELY PROVIDE THE TOKEN ---
    def get_exchange_token(self, obj):
        """
        Only show the exchange token to the finder of the item.
        The claimant should not be able to see this token.
        """
        request = self.context.get('request')
        # Check if a user is making the request and if that user is the finder
        if request and hasattr(request, "user") and request.user == obj.found_item.finder:
            return obj.exchange_token
        # Return None for everyone else (including the claimant)
        return None

class TestimonialSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    class Meta:
        model = Testimonial
        fields = ['id', 'user', 'claim', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']
