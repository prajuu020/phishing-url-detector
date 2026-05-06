import re

def extract_features(url):

    url_length = len(url)

    has_https = 1 if url.startswith("https") else 0

    has_at_symbol = 1 if "@" in url else 0

    num_dots = url.count(".")

    suspicious_words = ['login', 'verify', 'bank', 'update', 'free']
    has_suspicious_word = 1 if any(word in url.lower() for word in suspicious_words) else 0

    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    num_hyphens = url.count('-')

    long_url = 1 if len(url) > 75 else 0

    return [
        url_length,
        has_https,
        has_at_symbol,
        num_dots,
        has_suspicious_word,
        has_ip,
        num_hyphens,
        long_url
    ]