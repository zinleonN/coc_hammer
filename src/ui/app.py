from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label, Markdown, Checkbox, Footer
from textual.events import Key
from textual.containers import Horizontal, Vertical
from textual.screen import Screen


import asyncio

import core.common.file as file

from core.process.initial import initial

class MyApp(App):
    CSS = """
    #nav {
        height: 3;
        align: left top;
    }
    """

    def __init__(self):
        super().__init__()
        self.settings = file.load_settings()
        self._save_task = None  # 跟踪保存任务

    @property
    def count(self):
        return self.settings.get("count", 0)

    @count.setter
    def count(self, value):
        self.settings["count"] = value
        self._schedule_save()  # 统一使用异步保存

    @property
    def inited(self):
        return self.settings.get("inited", False)
    
    @inited.setter
    def inited(self, value):
        self.settings["inited"] = value
        self._schedule_save()  # 统一使用异步保存

    def _schedule_save(self):
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        self._save_task = asyncio.create_task(self._save_settings())

    def compose(self):
        yield Horizontal(
            Button("首页", id="home", variant="primary"),
            Button("配置", id="settings", variant="default"),
            Button("日志", id="help", variant="default"),
            id="nav"
        )

        self.content_area = Vertical(id="main-content")
        yield self.content_area

    def on_mount(self) -> None:
        self.update_page("home")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        
        if event.button.id == "home_change_init":
            self.push_screen(self._build_init_screen())
            return
        elif event.button.id == "home_navigate_to_init":
            self.update_page("home")
            return
        elif event.button.id == "init_back":
            self.pop_screen()
        elif event.button.id == "init_success":
            self.inited = True
            initial()
            self.pop_screen()
            self.update_page("home")
            
        page_id = event.button.id
        if page_id in {"home", "settings", "help"}:
            self.update_page(page_id)

    def update_page(self, page: str) -> None:
        self.current_page = page
        self.content_area.remove_children()
        
        if page == "home":
            content = self._build_home_page()
        elif page == "settings":
            content = self._build_settings_page()
        elif page == "help":
            content = self._build_help_page()  # 重命名函数
            
        self.content_area.mount(content)
        
        # 更新导航按钮状态
        for button in self.query(Button):
            if button.id in {"home", "settings", "help"}:
                button.variant = "primary" if button.id == page else "default"

    def _build_home_page(self) -> Vertical:
        status = "已初始化" if self.inited else "未初始化"
        return Vertical(
            Label(f"首页 - 初始化状态: {status}"),
            Button("切换初始化状态", id="home_change_init", variant="default"),
        )
    
    def _build_settings_page(self) -> Vertical:
        return Vertical(
            Label("设置页面"),
            Label(f"计数: {self.count}")
        )
    
    def _build_help_page(self) -> Vertical:
        status = "已初始化" if self.inited else "未初始化"
        return Vertical(
            Label(f"帮助页面 - 当前状态: {status}"),
            Button("跳转到帮助页", id="home_navigate_to_init", variant="default"),
        )
    
    def _build_init_screen(self) -> Screen:
        screen = Screen()
        def compose() -> ComposeResult:
            # yield Markdown("""- 设置屏幕游戏内分辨率与屏幕分辨率相同""")
            # yield Markdown("""- 将每条边至少放上两个任意类型的采集器""")
            # # yield Label(file.ascii_pic)
            # yield Markdown("""- 将游戏和运行的终端通过alt tab切换，返回终端""")
            yield Markdown("""
- 设置屏幕游戏内分辨率与屏幕分辨率相同
- 将每条边至少放上两个任意类型的采集器
```
                                       █  █                                                                      
                                    ██      █                                                                
                                  ██████     ██                                                              
                                █    █     ██████                                                            
                             █                     █                                                         
                           █████                     █                                                       
                         █ █████                       █                                                     
                      █                                   █                                                   
                    █                                  ██████                                                
                  █                                      █    █                                              
                █                                               █                                            
              █                                                   █                                          
                █ █████                                        █                                             
                  ███                                        █                                               
                     █   ██                                █                                                 
                       ██████                       ███  █                                                   
                         █                          ███                                                      
                            █                       █                                                        
                              █                   █                                                          
                                █          ████ █                                                            
                                   █         ███                                                               
                                     █     █                                                                 
                                       █ █        
```                


""")
            yield Horizontal(
                Button("返回", id="init_back", variant="default"),
                Button("完成", id="init_success", variant="primary"),
                classes="expand"
            )
            yield Footer()
            
        screen.compose = compose
        return screen

    async def on_unmount(self) -> None:
        # 确保所有保存任务完成
        if self._save_task and not self._save_task.done():
            await self._save_task

    async def _save_settings(self):
        """异步保存设置"""
        await asyncio.to_thread(file.save_settings, self.settings)


