from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
# 用于播放声音
from kivy.core.audio import SoundLoader
import time


log = print


def font_name():
    from sys import platform
    if platform == "darwin":
        return 'Arial Unicode'
    elif platform == "win32":
        return 'SimHei'
    else:
        print('not support')


def formated_sec(second):
    s = time.strftime("%H:%M:%S", time.gmtime(second))
    return s


class TestApp(App):
    def build(self):
        self.config_window()
        root = self.setup_ui()
        self.start = False
        self.pause_time = 0
        return root

    def config_window(self):
        g = 'graphics'
        Config.set(g, 'resizable', False)
        Config.set(g, 'width', 400)
        Config.set(g, 'height', 600)

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')
        self.audio = SoundLoader.load('SPYAIR - I Wanna Be.mp3')

        self.audio_max = formated_sec(self.audio.length)
        audio_now = formated_sec(0)
        self.progress_label = Label(
            text='{}/{}'.format(audio_now, self.audio_max),
        )
        layout.add_widget(self.progress_label)

        control_layout = BoxLayout(orientation='vertical')
        layout.add_widget(control_layout)
        self.play_buttion = Button(
            text='Play',
        )
        self.play_buttion.bind(on_press=self.play_music)
        self.stop_buttion = Button(
            text='Stop',
        )
        self.stop_buttion.bind(on_press=self.stop_music)
        control_layout.add_widget(self.play_buttion)
        control_layout.add_widget(self.stop_buttion)
        return layout

    def try_cancel_play_interval(self):
        try:
            self.play_interval.cancel()
        except:
            pass


    def stop_music(self, button):
        self.try_cancel_play_interval()
        self.play_buttion.text = 'Play'
        self.start = False
        self.audio.stop()
        self.pause_time = 0
        self.update_progress(0)

    def play_music(self, button):
        if self.start:
            self.try_cancel_play_interval()
            self.play_buttion.text = 'Play'
            self.pause_time = self.audio.get_pos()
            self.audio.stop()
            self.start = False
            # self.update_progress(0)
        else:
            self.try_cancel_play_interval()
            self.play_interval = Clock.schedule_interval(
                self.update_progress, 1)
            self.start = True
            self.audio.play()
            self.audio.seek(self.pause_time)
            self.play_buttion.text = 'Pause'
            # self.update_progress(0)

    def update_progress(self, dt):
        audio_now = formated_sec(self.audio.get_pos())
        audio_max = self.audio_max
        self.progress_label.text = '{}/{}'.format(audio_now, audio_max)


def main():
    TestApp().run()


if __name__ == '__main__':
    main()
