"""
Voice processing module for STT and TTS.
"""

from .stt import whisper_transcribe
from .tts import whisper_tts

__all__ = ['whisper_transcribe', 'whisper_tts']