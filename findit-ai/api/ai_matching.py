# File: api/ai_matching.py

import os
from huggingface_hub import InferenceClient

def find_most_similar_item(source_item, items_to_compare):
    """
    Finds the most semantically similar item from a list using a sentence-transformer model.
    """
    hf_api_token = os.environ.get('HF_API_TOKEN')
    if not hf_api_token:
        print("Hugging Face API token not found in environment variables!")
        return None, 0.0

    client = InferenceClient(token=hf_api_token)

    # Combine item name and description for better semantic context
    source_sentence = f"{source_item.item_name} {source_item.description}"
    sentences_to_compare = [f"{item.item_name} {item.description}" for item in items_to_compare]

    if not sentences_to_compare:
        return None, 0.0

    try:
        # Call the sentence similarity API endpoint
        scores = client.sentence_similarity(
            sentence=source_sentence,
            other_sentences=sentences_to_compare,
            model="sentence-transformers/all-MiniLM-L6-v2",
        )
        
        highest_score = max(scores)
        best_match_index = scores.index(highest_score)
        best_match_item = items_to_compare[best_match_index]
        
        return best_match_item, highest_score
        
    except Exception as e:
        print(f"Hugging Face API request failed: {e}")
        return None, 0.0