import argparse
from pathlib import Path

try:
    import speech_recognition as sr
except ImportError:
    sr = None

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "logs" / "imp-speech-log.txt"

def transcribe(audio_file=None, duration=None):
    if sr is None:
        print("[!] speech_recognition not installed")
        return ""
    r = sr.Recognizer()
    if audio_file:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
    else:
        with sr.Microphone() as source:
            if duration:
                audio = r.record(source, duration=duration)
            else:
                audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
    except Exception:
        text = ""
    if text:
        try:
            with open(LOG_FILE, "a") as f:
                f.write(text + "\n")
        except Exception:
            pass
        print(text)
    return text

def main():
    parser = argparse.ArgumentParser(description="IMP Speech-to-Text")
    parser.add_argument("--file", help="Audio file to transcribe")
    parser.add_argument("--duration", type=int, help="Record time in seconds")
    parser.add_argument("--check", action="store_true", help="Check library availability only")
    args = parser.parse_args()
    if args.check:
        if sr is None:
            print("[!] speech_recognition not installed")
        else:
            print("speech_recognition ready")
        return
    transcribe(args.file, args.duration)

if __name__ == "__main__":
    main()
