import curses
from pathlib import Path

try:
    import pyttsx3
except ImportError:  # pragma: no cover - if library missing, menu still loads
    pyttsx3 = None

ROOT = Path(__file__).resolve().parents[1]


def run_menu(initial_text: str = "Hello from IMP"):
    """Interactive curses menu to adjust voice settings and speak text."""
    text = [initial_text]
    rate = [150]
    volume = [0.8]
    voice_index = [0]

    def draw(stdscr):
        if pyttsx3 is None:
            stdscr.addstr(0, 0, "pyttsx3 not installed")
            stdscr.getch()
            return
        try:
            engine = pyttsx3.init()
        except Exception:
            stdscr.addstr(0, 0, "engine failed to init")
            stdscr.getch()
            return
        voices = engine.getProperty("voices")
        focus = 0  # 0 rate,1 volume,2 voice
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "IMP Voice Menu")
            stdscr.addstr(2, 0, f"Text: {text[0]}")
            stdscr.addstr(4, 0, f"Rate: {rate[0]} wpm")
            stdscr.addstr(5, 0, slider(rate[0], 50, 400, 30))
            stdscr.addstr(7, 0, f"Volume: {volume[0]:.1f}")
            stdscr.addstr(8, 0, slider(int(volume[0] * 100), 0, 100, 30))
            name = voices[voice_index[0]].name if voices else "none"
            stdscr.addstr(10, 0, f"Voice: {voice_index[0]} {name}")
            stdscr.addstr(12, 0, "TAB switch  a/d adjust  t text  ENTER speak  q quit")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord("q"), 27):
                break
            if ch in (curses.KEY_TAB, 9):
                focus = (focus + 1) % 3
            elif ch in (ord("a"), curses.KEY_LEFT):
                if focus == 0 and rate[0] > 50:
                    rate[0] -= 10
                elif focus == 1 and volume[0] > 0.0:
                    volume[0] = round(max(0.0, volume[0] - 0.1), 1)
                elif focus == 2 and voice_index[0] > 0:
                    voice_index[0] -= 1
            elif ch in (ord("d"), curses.KEY_RIGHT):
                if focus == 0 and rate[0] < 400:
                    rate[0] += 10
                elif focus == 1 and volume[0] < 1.0:
                    volume[0] = round(min(1.0, volume[0] + 0.1), 1)
                elif focus == 2 and voice_index[0] < len(voices) - 1:
                    voice_index[0] += 1
            elif ch in (10, 13):
                engine.setProperty("rate", rate[0])
                engine.setProperty("volume", volume[0])
                if voices:
                    engine.setProperty("voice", voices[voice_index[0]].id)
                engine.say(text[0])
                engine.runAndWait()
            elif ch == ord("t"):
                curses.echo()
                stdscr.addstr(14, 0, "New text: ")
                text[0] = stdscr.getstr(14, 10, 60).decode()
                curses.noecho()
        engine.stop()

    curses.wrapper(draw)


def slider(val, min_val, max_val, width):
    """Return a simple textual slider representation."""
    pos = int((val - min_val) / (max_val - min_val) * width)
    pos = max(0, min(width, pos))
    return "[" + "#" * pos + "-" * (width - pos) + "]"


def main():
    run_menu()


if __name__ == "__main__":  # pragma: no cover
    main()
