import hashlib

def generate_hash(url: str, timestamp: str):
    """Generate a hash from a URL and a timestamp."""
    result = hashlib.md5((url + timestamp).encode()).hexdigest()
    print(result)
    return result[:5]  # Truncate the result to the first 5 characters
