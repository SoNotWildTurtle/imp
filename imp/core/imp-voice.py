import argparse
from pathlib import Path

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

ROOT = Path(__file__).resolve().parents[1]
VOICE_LOG = ROOT / "logs" / "imp-voice-log.txt"


def speak(text: str):
    if pyttsx3 is None:
        print("[!] pyttsx3 not installed")
        return
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():
    parser = argparse.ArgumentParser(description="IMP Voice Synthesizer")
    parser.add_argument("text", nargs="+", help="Text to speak")
    args = parser.parse_args()

    message = " ".join(args.text)
    speak(message)
    try:
        with open(VOICE_LOG, "a") as f:
            f.write(message + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
