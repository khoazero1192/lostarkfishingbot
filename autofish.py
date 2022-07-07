import pyautogui
import time
import os
import cv2
import glob
from datetime import datetime
import schedule

import pathlib
SCREENSHOTS_DIR = pathlib.Path(os.path.expanduser("~"), 'lostarkscreenshots')
TEMPLATE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(TEMPLATE_DIR, 'template.PNG')

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
           cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]


if not os.path.exists(SCREENSHOTS_DIR):
    os.mkdir(SCREENSHOTS_DIR)


def screen_shot():
    im1 = pyautogui.screenshot(region=(1200, 450, 100, 200))
    im1.save(SCREENSHOTS_DIR / "screenshot.png")
    screenshot = cv2.imread(str(SCREENSHOTS_DIR / "screenshot.png"), 0)
    return screenshot


def start_timer():
    schedule.every(6).seconds.do(run)
    while True:
        schedule.run_pending()


def run():
    template = cv2.imread(TEMPLATE_FILE, 0)
    h, w = template.shape
    print("Casting a new line")
    time.sleep(2)
    pyautogui.press("E")
    counter = 0
    while counter < 16:
        # Take screenshots
        sc = screen_shot()
        copy = sc.copy()
        result = cv2.matchTemplate(copy, template, methods[0])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(min_val, max_val, min_loc, max_loc)
        # Wait for the yellow indicator to appear

        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        cv2.rectangle(copy, max_loc, bottom_right, 255, 5)
        if 36 < max_loc[0] < 43 and 25 < max_loc[1] < 35:
            print("Indicator detected, reeling in")
            pyautogui.press("E")
            break
        time.sleep(0.2)
        counter += 0.2
        print(f"counter {counter}")


def take_images():
    time.sleep(5)
    while True:
        im1 = pyautogui.screenshot(region=(1200, 450, 100, 200))
        im1.save(SCREENSHOTS_DIR / f"screenshot{datetime.now().timestamp()}.png")
        time.sleep(0.2)


def compare_images():
    images = glob.glob(os.path.join(SCREENSHOTS_DIR, "*png"))
    template = cv2.imread(TEMPLATE_FILE, 0)
    h, w = template.shape
    index = 0
    for image in images:
        print(f"processing image {image} index {index}")
        index += 1
        image = cv2.imread(image, 0)
        copy = image.copy()
        result = cv2.matchTemplate(copy, template, methods[0])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(min_val, max_val, min_loc, max_loc)
        # Wait for the yellow indicator to appear

        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        cv2.rectangle(copy, max_loc, bottom_right, 255, 5)
        if 38 < max_loc[0] < 40 and 29 < max_loc[1] < 31:
            print("Indicator detected")
            break


if __name__ == '__main__':
    start_timer()
