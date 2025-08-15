import argparse
from pathlib import Path

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

ROOT = Path(__file__).resolve().parents[1]
VOICE_LOG = ROOT / "logs" / "imp-voice-log.txt"


def get_default_female_voice(engine):
    """Return index of the first female voice if available."""
    voices = engine.getProperty("voices")
    for i, v in enumerate(voices):
        name = getattr(v, "name", "").lower()
        if "female" in name:
            return i
    return None


def find_voice_by_name(engine, name_substr):
    """Return index of voice containing given substring."""
    voices = engine.getProperty("voices")
    name_substr = name_substr.lower()
    for i, v in enumerate(voices):
        if name_substr in getattr(v, "name", "").lower():
            return i
    return None


def speak(text: str, voice_index=None, voice_name=None, rate=None, volume=None):
    if pyttsx3 is None:
        print("[!] pyttsx3 not installed")
        return
    try:
        engine = pyttsx3.init()
    except Exception:
        print("[!] pyttsx3 engine failed to initialize")
        return
    voices = engine.getProperty("voices")
    if voice_index is None and voice_name:
        voice_index = find_voice_by_name(engine, voice_name)
    if voice_index is None:
        voice_index = get_default_female_voice(engine)
    if voice_index is not None and 0 <= voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)
    if rate is not None:
        engine.setProperty("rate", rate)
    if volume is not None:
        engine.setProperty("volume", volume)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("[!] speech synthesis failed")


def list_voices():
    if pyttsx3 is None:
        print("[!] pyttsx3 not installed")
        return
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for i, v in enumerate(voices):
        print(f"{i}: {getattr(v, 'name', 'unknown')}")


def main():
    parser = argparse.ArgumentParser(description="IMP Voice Synthesizer")
    parser.add_argument("text", nargs="*", help="Text to speak")
    parser.add_argument("--list", action="store_true", help="List available voices")
    parser.add_argument("--voice", type=int, help="Voice index to use")
    parser.add_argument("--voice-name", help="Select voice by matching name")
    parser.add_argument("--rate", type=int, help="Speech rate in words per minute")
    parser.add_argument("--volume", type=float, help="Volume between 0.0 and 1.0")
    args = parser.parse_args()

    if args.list:
        list_voices()
        return

    message = " ".join(args.text) if args.text else ""
    if message:
        speak(message, args.voice, args.voice_name, args.rate, args.volume)
        try:
            with open(VOICE_LOG, "a") as f:
                f.write(message + "\n")
        except Exception:
            pass
    else:
        print("[!] No text provided")


if __name__ == "__main__":
    main()
