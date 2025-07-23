from textual.app import App
from textual.widgets import Button, Header, Label
from textual.events import Key
from textual.containers import Horizontal, Vertical

import asyncio

from  as file

class MyApp(App):
    CSS = """
    #nav {
        height: 3;
        align: center top;
    }
    #main-content {
        height: 100%;
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
        """调度异步保存操作"""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        self._save_task = asyncio.create_task(self.save_settings())

    def compose(self):
        yield Horizontal(
            Button("首页", id="home", variant="primary"),
            Button("设置页", id="settings", variant="success"),
            Button("帮助页", id="help", variant="success"),
            id="nav"
        )

        # 页面主体
        self.content_area = Vertical(id="main-content")
        yield self.content_area

    def on_mount(self) -> None:
        self.update_page("home")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "home_change_init":
            self.inited = not self.inited
            self.update_page("help")  # 保持在当前页面
            return
        elif event.button.id == "home_navigate_to_init":
            self.update_page("home")
            return
            
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
                button.variant = "primary" if button.id == page else "success"

    def _build_home_page(self) -> Vertical:
        status = "已初始化" if self.inited else "未初始化"
        return Vertical(
            Label(f"首页 - 初始化状态: {status}"),
            Button("切换初始化状态", id="home_change_init", variant="success"),
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

    async def on_unmount(self) -> None:
        # 确保所有保存任务完成
        if self._save_task and not self._save_task.done():
            await self._save_task

    async def save_settings(self):
        """异步保存设置"""
        await asyncio.to_thread(file.save_settings, self.settings)