from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key="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"
)

result = client.sentence_similarity(
    "That is a happy person",   # source sentence
    [                           # other sentences
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day",
    ],
    model="sentence-transformers/all-MiniLM-L6-v2",
)

print(result)

