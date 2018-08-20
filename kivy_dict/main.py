from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from translate import translate


def font_name():
    """
    苹果系统和微软系统需要不同的字体文件
    """
    from sys import platform
    if platform == "darwin":
        return 'Arial Unicode'
    elif platform == "win32":
        return 'SimHei'
    else:
        print('not support')


class TestApp(App):
    # 生成界面
    def build(self):
        self.config_window()
        root = self.setup_ui()
        return root

    def config_window(self):
        """
        禁止缩放, 宽度 400, 高度 600
        """
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 600)

    def setup_ui(self):
        """
        竖直排列, 单行文本框, 按回车触发
        """
        layout = BoxLayout(orientation='vertical')
        input = TextInput(multiline=False)
        input.bind(on_text_validate=self.check)
        layout.add_widget(input)
        
        result = TextInput()
        result.font_name = font_name()
        layout.add_widget(result)
        self.result = result
        
        return layout

    def check(self, input):
        self.result.text = translate(input.text)


def main():
    TestApp().run()


if __name__ == '__main__':
    main()
