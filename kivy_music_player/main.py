from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.metrics import dp
# 用于播放声音
from kivy.core.audio import SoundLoader
import time
import enum
import sys


log = print


class PathTable(str, enum.Enum):
    d = sys.path[0]
    audios = '{}/audios'.format(d)


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
        self.start = False
        self.pause_time = 0
        self.audio_max = 0
        self.config_window()
        root = self.setup_ui()
        return root

    def config_window(self):
        g = 'graphics'
        Config.set(g, 'resizable', False)
        Config.set(g, 'width', 400)
        Config.set(g, 'height', 600)

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical')
        
        self.setup_progress_label(layout)
        self.setup_progress_layout(layout)
        self.setup_control_layout(layout)
        self.setup_listview(layout)

        self.update_progress(0)
        self.init_progress()
        return layout

    def setup_progress_label(self, layout):
        audio_now = formated_sec(0)
        self.progress_label = Label(
            text='{}/{}'.format(audio_now, self.audio_max),
        )
        layout.add_widget(self.progress_label)

    def setup_progress_layout(self, layout):
        progress_layout = BoxLayout(
            orientation='horizontal',
            height=10,
            size_hint_y=None,
        )
        layout.add_widget(progress_layout)
        
        self.progress_played = Button(background_color=(1, 0, 0, 1))
        progress_layout.add_widget(self.progress_played)
        
        self.progress_unplayed = Button(background_color=(0, 0, 1, 1))
        progress_layout.add_widget(self.progress_unplayed)

    def setup_control_layout(self, layout):
        control_layout = BoxLayout(orientation='horizontal')
        layout.add_widget(control_layout)
        self.setup_button_player(control_layout)
        self.setup_button_stop(control_layout)

    def setup_button_player(self, layout):
        self.play_buttion = Button(
            text='Play',
        )
        self.play_buttion.bind(on_press=self.play_music)
        layout.add_widget(self.play_buttion)

    def setup_button_stop(self, layout):
        self.stop_buttion = Button(
            text='Stop',
        )
        self.stop_buttion.bind(on_press=self.stop_music)
        layout.add_widget(self.stop_buttion)

    def setup_listview_inner(self, layout):
        listview = GridLayout(
            cols=1,
            spacing=dp(2),
            size_hint_y=None,
        )
        listview.bind(minimum_height=listview.setter('height'))
        # 测试: 往 listview 中添加 30 个 Button
        l = ['SPYAIR - I Wanna Be.mp3']
        for i, name in enumerate(l):
            file_p = '{}/{}'.format(PathTable.audios, name)
            text = '{} - {}'.format(str(i), name)
            btn = Button(text=text, size_hint_y=None, height=40)
            btn.bind(on_press=self.play_music_selected(file_p))
            listview.add_widget(btn)

        self.audio = SoundLoader.load('SPYAIR - I Wanna Be.mp3')
        self.audio_max = formated_sec(self.audio.length)
        layout.add_widget(listview)

    def setup_listview(self, layout):
        scroll = ScrollView(
            # pos=(dp(100), dp(100)),
            size=(dp(200), dp(300)),
            size_hint_y=(None),
            bar_width=dp(10),
        )
        self.setup_listview_inner(scroll)
        layout.add_widget(scroll)

    def try_cancel_play_interval(self):
        try:
            self.play_interval.cancel()
        except:
            pass

    def init_progress(self):
        self.progress_played.size_hint_x = 0
        self.progress_played.width = 0
        self.progress_unplayed.size_hint_x = 1

    def stop_music(self, button):
        self.try_cancel_play_interval()
        self.play_buttion.text = 'Play'
        self.start = False
        self.audio.stop()
        self.pause_time = 0
        self.update_progress(0)
        self.init_progress()

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
                self.update_progress, 1/60)
            self.start = True
            self.audio.play()
            self.audio.seek(self.pause_time)
            self.play_buttion.text = 'Pause'
            # self.update_progress(0)

    def play_music_selected(self, path):
        def func(button):
            print(path)
            self.audio = SoundLoader.load(path)
            self.audio_max = formated_sec(self.audio.length)
            self.play_music(button)
        return func

    def update_progress(self, dt):
        now = self.audio.get_pos()
        audio_now = formated_sec(now)
        audio_max = self.audio_max
        played = now / self.audio.length
        unplayed = 1 - played
        self.progress_played.size_hint_x = played
        self.progress_unplayed.size_hint_x = unplayed
        self.progress_label.text = '{}/{}'.format(audio_now, audio_max)


def main():
    TestApp().run()


if __name__ == '__main__':
    main()
