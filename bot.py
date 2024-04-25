from pynput.keyboard import Key, Controller as KC
from pynput.mouse import Button, Controller as MC
from time import sleep
from random import Random
import pyautogui
import cexceptions
import pyperclip


class Bot(object):

    def slow_type(self, texto):
        """function that types text in a human-like manner"""
        kontroller = KC()
        r = Random()
        for c in texto:
            kontroller.press(c)
            kontroller.release(c)
            if (c == ' '):
                sleep(r.random())
            else:
                sleep(r.uniform(0.0, 0.2))

    def find_and_click(self, desc, path, p=0, con=1.0, g=False):
        """"
        Finds an element and clicks it

            Parameters:
                    desc (string): A description of the element to be clicked
                    path (string): A Path to the reference image of the element
                    p (int): Distance in pixels from the top and left borders of the element to be clicked, if 0 then the function will click the center of the element (default 0)
                    con (float): Minimun percentage of match required to carry on execution (default 1.0)
                    g (boolean): Use grayscale matching (default False)
            Returns:
                    1 if success, 0 if failure
        """
        mc = MC()
        t_loc = None

        try:
            tuple(location=pyautogui.locateOnScreen(
                image=path, confidence=con, grayscale=g))
        except pyautogui.ImageNotFoundException:
            print(f"No pude encontrar esto: '{desc}'")
            return 0
        if p == 0:
            t_loc = pyautogui.center(location)
        else:
            t_loc = (location[0]+p, location[1]+p)
        mc.position = t_loc
        mc.click(Button.left, 1)
        return 1

    def is_img_onscreen(self, img):
        """
        Checks if the image is on screen

            Parameters:
                    img (string): The image file name

            Returns:
                    True if it's on the screen, false otherwise
        """
        temp = pyautogui.locateOnScreen(img)
        if temp is None:
            return False
        return True

    def go_to_chatgpt(self):
        """
        Opens the browser; searches for an open ChatGPT tab, if it doesn't find one, it creates a new one; searches for 'Alex, Assitant' chat; searches and clicks the message box

            Raises: ImageNotFoundException if it doesn't find an element
        """
        kc = KC()

        if not Bot.is_img_onscreen(self, "OperaSideBar.png"):
            if Bot.find_and_click(self, "Opera", "OpenOpera.png", 0.8, True) != 1:
                raise pyautogui.ImageNotFoundException
        kc.press(Key.ctrl)
        sleep(0.1)
        kc.press(Key.space)
        sleep(0.1)
        kc.release(Key.ctrl)
        kc.release(Key.space)
        sleep(0.3)
        kc.type("chat.openai.com")
        sleep(2)
        if Bot.find_and_click(self, "Open Tabs", "OpenTabs.png", 0.9) == 1:
            kc.tap(Key.enter)
        else:
            sleep(1)
            kc.tap(Key.esc)
            sleep(0.1)
            kc.press(Key.ctrl)
            sleep(0.1)
            kc.press('t')
            sleep(0.1)
            kc.release(Key.ctrl)
            kc.release('t')
            sleep(0.5)
            kc.type("chat.openai.com")
            sleep(0.5)
            kc.tap(Key.enter)
        f = False
        for i in range(0, 9):
            if Bot.find_and_click(self, "Alex's Chat",
                                  "AlexAssistant.png", 0.8, True) == 1:
                f = True
                break
            sleep(0.3)
        if not f:
            raise pyautogui.ImageNotFoundException
        f = False
        for j in range(0, 19):
            if Bot.find_and_click(self, "ChatGPT's Message Box",
                                  "MessageChatGPT.png", 0.9) == 1:
                f = True
                break
            sleep(0.3)
        if not f:
            raise pyautogui.ImageNotFoundException

    def ask_chatgpt(self, pr):
        """"
        Asks ChatGPT

            Parameters:
                    pr (string): Prompt that will be asked to ChatGPT

            Returns:
                    res (string): ChatGPT's response
        """
        kc = KC()
        res = "Error: Un elemento no pudo ser encontrado"
        try:
            Bot.go_to_chatgpt(self)
        except pyautogui.ImageNotFoundException:
            pyautogui.alert(
                text='Un elemento no pudo ser encontrado', title='Error', button='OK')
            return res
        sleep(1)
        pyautogui.write(pr)
        kc.tap(Key.enter)
        sleep(1)
        done = False
        while not done:
            if Bot.check_chatgpt_status(self) < 2:
                done = True
        res = Bot.get_chatgpt_response(self)
        sleep(0.3)
        return res

    def check_chatgpt_status(self):
        """
        Checks ChatGPT's status

            Returns:
                    0 if available, 1 if available and the message box is not empty, 2 if busy, 3 if error
        """
        if Bot.is_img_onscreen(self, "ChatGPTStopButton.png"):
            print("Veo que ChatGPT está ocupado")
            return 2
        if Bot.is_img_onscreen(self, "ChatGPTSendButton.png"):
            print("Veo que ChatGPT está desocupado")
            return 0
        if Bot.is_img_onscreen(self, "ChatGPTSendButton2.png"):
            print(
                "Veo que ChatGPT está desocupado, pero, hay algo en el cuadro de dialogo")
            return 1
        print("No puedo determinar el estado de ChatGPT")
        return 3

    def get_chatgpt_response(self):
        """
        Gets the latest ChatGPT's response

            Returns:
                    A string containing the latest response

        """
        temp = 0
        l = None
        try:
            responses = pyautogui.locateAllOnScreen("ChatGPTResponse.png")
        except pyautogui.ImageNotFoundException as exc:
            raise cexceptions.NoResponseFromAIException from exc
        for r in responses:
            x, y, w, h = r
            if y > temp:
                l = (x, y)
        pyautogui.moveTo(l)
        sleep(0.2)
        if Bot.find_and_click(self, "ChatGPT's Copy button",
                              "ChatGPTCopyButton.png", 0.9) != 1:
            raise pyautogui.ImageNotFoundException
        sleep(0.1)
        return pyperclip.paste()

    def ask_user(self, t):
        """
        Displays a dialog box in the screen of the computer with an input field

            Parameters:
                    t (string): The latest message from Alex to the user

            Returns:
                    A string containing the user's response

        """
        Bot.ask_chatgpt(self, pyautogui.prompt(
            text=t, title='Alex', default=''))


clau = Bot()
kc = KC()

sleep(3)
while True:
    try:
        clau.go_to_chatgpt()
        clau.get_chatgpt_response()
        clau.find_and_click("Say Button", "ChatGPTReadButton.png", 0.9)
        clau.ask_user(pyperclip.paste())
    except pyautogui.ImageNotFoundException:
        pyautogui.alert(
            text='Un elemento no pudo ser encontrado', title='Error', button='OK')
