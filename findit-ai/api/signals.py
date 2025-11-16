from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import LostItem, FoundItem, Claim, ChatMessage # <-- Make sure ChatMessage is imported
from .ai_matching import find_most_similar_item

# --- SIGNAL 1: AI Matching on Item Creation ---

# This threshold determines how similar two items must be to be considered a match.
SIMILARITY_THRESHOLD = 0.6 

@receiver(post_save, sender=LostItem)
@receiver(post_save, sender=FoundItem)
def find_match_on_save(sender, instance, created, **kwargs):
    """
    Signal receiver that runs after a LostItem or FoundItem is saved.
    If the item is newly created, it searches for a potential match.
    """
    if created:
        print(f"✅ New item created: '{instance.item_name}'. Searching for matches...")
        
        # Determine which list of items to search against
        if sender is LostItem:
            items_to_search = list(FoundItem.objects.all())
        else: # sender is FoundItem
            items_to_search = list(LostItem.objects.all())

        if not items_to_search:
            print("No items in the opposite category to compare against.")
            return

        # Find the best matching item using the AI service
        best_match, highest_score = find_most_similar_item(instance, items_to_search)

        if best_match and highest_score >= SIMILARITY_THRESHOLD:
            print("\n---!!! ✨ MATCH FOUND !!! ---✨")
            print(f"New Item: '{instance.item_name}'")
            print(f"Best Match: '{best_match.item_name}' (Score: {highest_score:.2f})")
            
            # Assign lost and found items based on which one triggered the signal
            if sender is LostItem:
                lost_item = instance
                found_item = best_match
            else: # sender is FoundItem
                lost_item = best_match
                found_item = instance
            
            # Create a new Claim object to record the match
            Claim.objects.create(
                found_item=found_item,
                lost_item=lost_item,
                claimant=lost_item.user, # The user who lost the item is the claimant
                status='match_found'      # A status to indicate it was an AI-generated match
            )
            print("Match has been saved to the database as a new Claim.\n")
            
        else:
            print(f"No strong match found. Highest score was {highest_score:.2f}")

# --- SIGNAL 2: Email Notification on New Chat Message ---

@receiver(post_save, sender=ChatMessage)
def send_email_on_new_message(sender, instance, created, **kwargs):
    """
    Sends an email notification when a new ChatMessage is created.
    """
    # 'created' is True only when a new record is made
    if created:
        message = instance
        claim = message.claim

        # Determine who the recipient is
        if message.sender == claim.claimant:
            # If the sender is the claimant, the recipient is the finder
            recipient = claim.found_item.finder
        else:
            # Otherwise, the recipient is the claimant
            recipient = claim.claimant

        # --- Email Details ---
        subject = f"You have a new message about '{claim.found_item.item_name}'"
        email_message = f"""
        Hi {recipient.username},

        You've received a new message from {message.sender.username} regarding the item '{claim.found_item.item_name}'.

        Message: "{message.content}"

        You can reply by visiting the chat page: http://localhost:5173/chat/{claim.id}

        Thanks,
        The FindIt AI Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_email = recipient.email

        # Send the email
        send_mail(subject, email_message, from_email, [recipient_email])
        print(f"✅ Email notification sent to {recipient_email} for new chat message.")
