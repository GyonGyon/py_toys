
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

# 在 retina 屏幕上, 需要使用这个 dp 函数来转换像素坐标
from kivy.metrics import dp
import time
import datetime


def font_name():
    from sys import platform
    if platform == "darwin":
        return 'Arial Unicode'
    elif platform == "win32":
        return 'SimHei'
    else:
        print('not support')


class TestApp(App):
    def build(self):
        self.config_window()
        root = self.setup_ui()
        self.start = False
        self.pause = False
        return root

    def config_window(self):
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)

    def setup_ui(self):
        layout = FloatLayout(size=(400, 600))

        # 注意, 这里的像素值没有使用 dp, 在普通屏幕上没有差异, 在 retina 屏幕上自行观察
        button_config = dict(
            text='开始',
            font_size=20,
            pos=(20, 20),
            size=(200, 100),
            size_hint=(None, None),
            font_name=font_name(),
        )
        button = Button(**button_config)
        button.bind(on_press=self.button_press)
        layout.add_widget(button)
        self.button = button

        label_config = dict(
            text='00:00:00',
            font_size=50,
            # 横向居中显示
            halign='center',
        )
        label = Label(**label_config)
        layout.add_widget(label)
        self.label = label

        return layout

    # dt 意思是 delta-time, 间隔时间
    def timer(self, dt):
        tnow = time.time()
        t = tnow - self.starttime
        # https://stackoverflow.com/questions/775049/how-to-convert-seconds-to-hours-minutes-and-seconds
        s = time.strftime("%H:%M:%S", time.gmtime(t))
        print(s)
        self.label.text = s

    def button_press(self, button):
        if not self.start:
            Clock.schedule_interval(self.timer, 1)
            self.start = True
            self.starttime = time.time()
        # TODO: 增加暂停功能
        # elif self.pause:
        #     self.pause = False
        # elif not self.pause:
        #     self.pause = True

    def check(self, input):
        s = input.text + '\n' + 'done'


def main():
    TestApp().run()


if __name__ == '__main__':
    main()
