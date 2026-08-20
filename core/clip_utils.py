import threading

_model = None
_model_lock = threading.Lock()


def get_model():
    """Carrega o modelo CLIP uma única vez por processo (fica em cache na memória)."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer
                _model = SentenceTransformer('clip-ViT-B-32')
    return _model


def compute_embedding(pil_image):
    """Recebe uma imagem PIL e devolve sua 'impressão digital' visual como lista de números."""
    model = get_model()
    embedding = model.encode(pil_image)
    return embedding.tolist()


def cosine_similarity(a, b):
    """Mede o quão parecidas duas impressões digitais são (1.0 = idênticas, 0 = nada a ver)."""
    import numpy as np
    a = np.array(a)
    b = np.array(b)
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)
