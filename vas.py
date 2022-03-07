#!/usr/bin/env conda run --name psychopy python

from psychopy import visual, core, logging
from psychopy.hardware import keyboard
import argparse

logging.console.setLevel(logging.CRITICAL)


class Style:
    bold = "\033[1m"
    red = "\033[91m"
    end = "\033[0m"


def get_args():
    parser = argparse.ArgumentParser(description="set screen number")
    parser.add_argument(
        "--screen", type=int, choices=[0, 1], default=0, help="local (0) or remote (1)"
    )
    return parser.parse_args()


def init_objects(x, y, screen):
    kb = keyboard.Keyboard()
    timer = core.CountdownTimer(10)
    fullscr = bool(screen)
    win = visual.Window(
        size=(x, y),
        pos=(0, 0),
        color="white",
        allowGUI=True,
        fullscr=fullscr,
        screen=screen,
    )
    title = visual.TextStim(win=win, text=None, color="black", pos=[0, 0.25])
    time = visual.TextStim(win=win, text="", color="red", pos=[0, -0.25])
    outline = visual.Rect(win=win, width=1, height=0.2)
    outline.lineColor = "black"
    outline.lineWidth = 2.3
    rect = visual.Rect(win=win, width=0.01, height=0.2)
    rect.fillColor = "red"
    pain0 = visual.TextStim(win=win, color="black", height=0.055, pos=[-0.7, 0])
    pain10 = visual.TextStim(win=win, color="black", height=0.055, pos=[0.75, 0])
    return kb, timer, win, title, time, outline, rect, pain0, pain10


def reset(title, time, rect, pain_type, pain0, pain10):
    title.text = pain_type
    time.text = ""
    rect.pos = [-0.5, 0]
    rect.width = 0.01
    rect.height = 0.2
    if pain_type == "PAIN INTENSITY":
        pain0.text = "NO PAIN\nSENSATION"
        pain10.text = "MOST INTENSE PAIN\nSENSATION IMAGINABLE"
    elif pain_type == "PAIN UNPLEASANTNESS":
        pain0.text = "NOT AT ALL\nUNPLEASANT"
        pain10.text = "MOST UNPLEASANT\nIMAGINABLE"


def update_win(win, title, time, outline, rect, pain0, pain10):
    rect.draw()
    outline.draw()
    title.draw()
    time.draw()
    pain0.draw()
    pain10.draw()
    win.flip()


def main():

    x = 720
    y = 450

    args = get_args()

    kb, timer, win, title, time, outline, rect, pain0, pain10 = init_objects(
        x, y, args.screen
    )

    for pain_type in ["PAIN INTENSITY", "PAIN UNPLEASANTNESS"]:

        reset(title, time, rect, pain_type, pain0, pain10)
        timer.reset()
        pain_rating = 0
        while timer.getTime() > 0:
            update_win(win, title, time, outline, rect, pain0, pain10)
            keys = kb.getKeys(["1", "2", "return"], waitRelease=False, clear=False)

            remaining = timer.getTime()
            if remaining < 3:
                time.text = f"{remaining:.1f}"

            if keys and not keys[-1].duration:  # key is being held down
                key = keys[-1].name
                if key == "1" and pain_rating > 0:
                    pain_rating -= 0.05
                    rect.width -= 0.005
                    rect.pos[0] -= 0.0025
                elif key == "2" and pain_rating < 10:
                    pain_rating += 0.05
                    rect.width += 0.005
                    rect.pos[0] += 0.0025
                del keys

        print(
            Style.bold + Style.red + f"{pain_type[5:8]}:\t{pain_rating:.2f}" + Style.end
        )
        win.flip()
        core.wait(1)


if __name__ == "__main__":
    main()
