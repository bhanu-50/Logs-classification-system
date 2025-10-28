import os
import warnings

warnings.filterwarnings("ignore")

_model_emdedding = None
_model_classification = None

def _load_embedding():
    """Load and return a SentenceTransformer model or None."""
    
    global _model_emdedding
    if _model_emdedding is not None:
        return _model_emdedding
    try:
        from sentence_transformers import SentenceTransformer
        _model_emdedding = SentenceTransformer('all-MiniLM-L6-v2')
    
    except Exception:
        _model_emdedding = None
    
    return _model_emdedding

def _load_classifier():
    """Load and return the joblib classifier or None. Looks in two likely locations."""
    
    global _model_classification
    if _model_classification is not None:
        return _model_classification
    
    try:
        from joblib import load
    except Exception as ex:
        warnings.warn(f"joblib not available: {ex}")
        _model_classification = None
        return _model_classification

    # Try several likely candidate locations/names for the joblib file.
    base_dir = os.path.dirname(__file__)
    fname = "log_classifier.joblib"
    candidates = [
        os.path.join(base_dir, "Models", fname),
        os.path.join(base_dir, "Models", "classifier.joblib"),
        os.path.join(base_dir, "models", fname),
        os.path.join(os.path.dirname(base_dir), "Models", fname),
        os.path.join(os.path.dirname(base_dir), "models", fname),
    ]

    model_path = None
    for p in candidates:
        if os.path.isfile(p):
            model_path = p
            break

    if model_path is None:
        # not found — set to None and return
        warnings.warn(f"No joblib classifier found. Tried: {candidates}")
        _model_classification = None
        return _model_classification

    try:
        _model_classification = load(model_path)
    except Exception as ex:
        # preserve None but warn to help debugging
        warnings.warn(f"Failed to load classifier at {model_path}: {ex}")
        _model_classification = None

    return _model_classification

def _load_models():
    """Convenience wrapper that returns (embedding, classifier)."""
    return _load_embedding(), _load_classifier()

def classify_with_bert(log_message: str) -> str:
    embedding_model, classifier = _load_models()
    # If models aren't available, don't crash at import/runtime — return fallback
    if embedding_model is None or classifier is None:
        return "Unclassified"
    
    try:
        embeddings = embedding_model.encode([log_message])
        # classifier may expect 2D array; embeddings is already suitable
        if hasattr(classifier, "predict_proba"):
            probabilities = classifier.predict_proba(embeddings)[0]
            if max(probabilities) < 0.5:
                return "Unclassified"

        predicted_label = classifier.predict(embeddings)[0]
        return predicted_label
    except Exception as ex:
        warnings.warn(f"Failed to classify log message: {ex}")
        return "Unclassified"
    
        
        
    


        
        
    
