embedding = data_point["embedding"]

# Fix: Ensure vector has exactly 3072 elements
if len(embedding) < 3072:
    # Pad with 0.0
    embedding += [0.0] * (3072 - len(embedding))
elif len(embedding) > 3072:
    # Trim extra elements
    embedding = embedding[:3072]