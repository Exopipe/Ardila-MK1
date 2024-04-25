import pyautogui


def is_img_onscreen(img):
    """
    Checks if the image is on screen

        Parameters:
                img (string): The image file name

        Returns:
                True if it's open, false otherwise
    """
    temp = pyautogui.locateOnScreen(img)
    if temp is None:
        return False
    return True


while True:
    if is_img_onscreen("ChatGPTCopyButton.png"):
        print("Lo veo")
    else:
        print("No lo veo")
