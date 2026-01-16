"""Text cleaning, tokenization and stopword removal."""
import re
from typing import List
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords




def clean_tweet(text: str) -> str:
if not isinstance(text, str):
return ""
text = text.lower()
text = re.sub(r"http\S+", "", text) # remove URLs
text = re.sub(r"@\w+", "", text) # remove mentions
text = re.sub(r"[^a-z\s]", "", text) # keep only letters
text = re.sub(r"\s+", " ", text).strip()
return text




def tokenize(text: str) -> List[str]:
if not text:
return []
return word_tokenize(text)




_stopwords_cache = None


def get_stopwords() -> set:
global _stopwords_cache
if _stopwords_cache is None:
_stopwords_cache = set(stopwords.words("english"))
return _stopwords_cache




def remove_stopwords(tokens: List[str]) -> List[str]:
sw = get_stopwords()
return [t for t in tokens if t not in sw]