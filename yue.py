from pynput import keyboard
from playsound import playsound
import pygame
import os
import time
import tkinter
import random
import logging

NUM_MIXER_CHANNEL = 10
current_mixer_channel = 0
VOICE_BANK = None

mixer = pygame.mixer
mixer.init()
mixer.set_num_channels(NUM_MIXER_CHANNEL)
music = pygame.mixer.music


def on_press(key):
    global current_mixer_channel
    try:
        if key is None:
            print("unknown key")
        elif VOICE_BANK.startswith("yue"):
            yue_list = os.listdir(os.path.join("voice_bank", VOICE_BANK))
            path = os.path.join("voice_bank", VOICE_BANK, random.choice(yue_list))
        elif hasattr(key, "char"):
            keychar = key.char
            path = os.path.join("voice_bank", VOICE_BANK, keychar + ".mp3")
        else:
            keystring = str(key).split(".")[-1]
            path = os.path.join("voice_bank", VOICE_BANK, keystring + ".mp3")
        # logging.debug("play:", path)
        # music.load(path)
        # music.play()
        if not os.path.exists(path):
            path = path[:-4] + ".wav"
        print(path)
        mixer.Channel(current_mixer_channel).play(mixer.Sound(path))
        current_mixer_channel = (current_mixer_channel + 1) % NUM_MIXER_CHANNEL
        # time.sleep(5)
    except AttributeError:
        print('special key {0} pressed'.format(key))
        pass
    except Exception as e:
        print(e)
        pass

def on_release(key):
    # logging.debug('{0} released'.format(key))
    pass


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

def start_listener():
    global VOICE_BANK
    try:
        voice_bank_index = tk_list_voice_bank.curselection()[0]
        VOICE_BANK = voice_bank_list[voice_bank_index]
    except Exception as e:
        # logging.debug(e)
        pass

    global listener
    listener.stop()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

def stop_listener():
    listener.stop()

top = tkinter.Tk()

voice_bank_list = os.listdir("voice_bank")      # 获取voice_bank里都有哪些bank
tk_list_voice_bank = tkinter.Listbox(top)       # 创建列表组件
for bank in voice_bank_list:                    # 将bank列表插入列表组件里
    tk_list_voice_bank.insert(tkinter.END, bank)

tk_button_start = tkinter.Button(top, text="start", command=start_listener)
tk_button_stop = tkinter.Button(top, text="stop", command=stop_listener)

top.geometry("300x300")
top.eval('tk::PlaceWindow . center')

tk_list_voice_bank.pack()                       # 将组件放入主窗口
tk_button_start.pack()
tk_button_stop.pack()
top.mainloop()