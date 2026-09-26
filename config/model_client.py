import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import CreateResult
from config.constant import MODEL

load_dotenv()

def _load_keys() -> list[str]:
    """Load all GEMINI_API_KEY, GEMINI_API_KEY_1, GEMINI_API_KEY_2, ... from .env"""
    keys = []
    # Support both GEMINI_API_KEY and GEMINI_API_KEY_1, _2, _3 ...
    base_key = os.getenv("GEMINI_API_KEY")
    if base_key:
        keys.append(base_key)
    i = 1
    while True:
        k = os.getenv(f"GEMINI_API_KEY_{i}")
        if not k:
            break
        keys.append(k)
        i += 1
    if not keys:
        raise ValueError("No GEMINI_API_KEY found in .env")
    return list(dict.fromkeys(keys))  # deduplicate while preserving order


class RotatingModelClient:
    """
    Wraps multiple OpenAIChatCompletionClient instances (one per API key).
    On a rate-limit / quota error (429 or ResourceExhausted), automatically
    rotates to the next available key and retries — no restart needed.
    """

    def __init__(self, keys: list[str], model: str):
        self._clients = [
            OpenAIChatCompletionClient(model=model, api_key=k) for k in keys
        ]
        self._index = 0
        print(f"RotatingModelClient: loaded {len(self._clients)} API key(s).")

    @property
    def _current(self) -> OpenAIChatCompletionClient:
        return self._clients[self._index]

    def _rotate(self) -> bool:
        """Rotate to the next key. Returns False if all keys are exhausted."""
        next_index = (self._index + 1) % len(self._clients)
        if next_index == self._index:
            return False  # Only one key, nothing to rotate to
        self._index = next_index
        msg = f"API key exhausted — switched to key #{self._index + 1}. Continuing from where it stopped..."
        print(f"RotatingModelClient: {msg}")
        # Show toast in Streamlit UI if running in a script context
        try:
            import streamlit as st
            st.toast(f"⚡ {msg}", icon="🔄")
        except Exception:
            pass
        return True

    def _is_quota_error(self, e: Exception) -> bool:
        msg = str(e).lower()
        return any(kw in msg for kw in ["429", "quota", "resource_exhausted", "rate limit", "resourceexhausted"])

    async def create(self, messages, *, cancellation_token=None, **kwargs) -> CreateResult:
        tried = set()
        while self._index not in tried:
            try:
                return await self._current.create(messages, cancellation_token=cancellation_token, **kwargs)
            except Exception as e:
                if self._is_quota_error(e):
                    print(f"RotatingModelClient: quota hit on key #{self._index + 1} — {e}")
                    tried.add(self._index)
                    if not self._rotate() or self._index in tried:
                        raise RuntimeError("All Gemini API keys have hit their quota.") from e
                else:
                    raise

    async def create_stream(self, messages, **kwargs):
        tried = set()
        while self._index not in tried:
            try:
                async for chunk in self._current.create_stream(messages, **kwargs):
                    yield chunk
                return
            except Exception as e:
                if self._is_quota_error(e):
                    print(f"RotatingModelClient: quota hit on key #{self._index + 1} (stream) — {e}")
                    tried.add(self._index)
                    if not self._rotate() or self._index in tried:
                        raise RuntimeError("All Gemini API keys have hit their quota.") from e
                else:
                    raise

    # Delegate everything else to the current underlying client
    def __getattr__(self, name: str):
        return getattr(self._current, name)


def get_model_client() -> RotatingModelClient:
    keys = _load_keys()
    return RotatingModelClient(keys=keys, model=MODEL)