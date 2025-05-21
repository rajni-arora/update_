# custom_recognizers.py
from presidio_analyzer import PatternRecognizer, Pattern

class CustomSensitiveTermsRecognizer(PatternRecognizer):
    def __init__(self):
        # Define your custom redaction patterns here
        patterns = [
            Pattern(name="Custom Sensitive Term", regex=r"\bUK\b", score=1.0),
            Pattern(name="Custom Sensitive Term", regex=r"\bMax LTM\b", score=1.0),
        ]
        super().__init__(
            supported_entity="CUSTOM_SENSITIVE_TERM",
            name="CustomSensitiveTermsRecognizer",
            patterns=patterns
        )
        
        
        
        
        
from custom_recognizers import CustomSensitiveTermsRecognizer

def get_contexts_thresholds():
    contexts = {
        ...
        "custom_sensitive_terms": CustomSensitiveTermsRecognizer.CONTEXT,
    }

    thresholds = {
        ...
        "custom_sensitive_terms": 1.0,
    }

    return contexts, thresholds, []