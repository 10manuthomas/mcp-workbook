import time
import threading
import tkinter as tk
import winsound  # Standard Windows sound library
from tkinter import simpledialog
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont


class BlinkingTaskbarTimer:
    def __init__(self):
        self.work_mins = 25
        self.break_mins = 5
        self.current_mode = "Work"
        self.remaining_seconds = self.work_mins * 60
        self.running = False
        self.visible = True
        self.alarm_active = False  # Controls the repeated sound

        self.icon = Icon("Pomodoro", icon=self.create_icon(self.work_mins))
        self.icon.menu = self.create_menu()

    def play_alarm(self):
        """Plays a repeated system beep while alarm_active is True."""
        while self.alarm_active:
            # Frequency 800Hz, Duration 500ms
            winsound.Beep(800, 500)
            time.sleep(0.5)

    def create_icon(self, number, is_visible=True):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        if not is_visible:
            return img

        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arialbd.ttf", 55)
        except:
            font = ImageFont.load_default()

        color = "#66ff66" if self.current_mode == "Break" else "#ff3333"
        d.text((32, 32), str(number), font=font, fill=color, anchor="mm")
        return img

    def set_custom_time(self, is_work=True):
        def ask_user():
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            current = self.work_mins if is_work else self.break_mins
            title = "Set Work Time" if is_work else "Set Break Time"

            new_val = simpledialog.askinteger(title, "Enter minutes (1-99):",
                                              initialvalue=current, minvalue=1, maxvalue=99)
            if new_val:
                if is_work:
                    self.work_mins = new_val
                else:
                    self.break_mins = new_val
                self.reset()
            root.destroy()

        threading.Thread(target=ask_user, daemon=True).start()

    def create_menu(self):
        return Menu(
            MenuItem(lambda item: "⏸ Pause" if self.running else "▶ Start", self.toggle),
            MenuItem("🔄 Reset / Stop Alarm", self.reset),
            Menu.SEPARATOR,
            MenuItem("💻 Work Mode", lambda: self.switch_mode("Work")),
            MenuItem("☕ Break Mode", lambda: self.switch_mode("Break")),
            Menu.SEPARATOR,
            MenuItem("⚙ Set Work Time", lambda: self.set_custom_time(True)),
            MenuItem("⚙ Set Break Time", lambda: self.set_custom_time(False)),
            Menu.SEPARATOR,
            MenuItem("❌ Quit", lambda icon: icon.stop())
        )

    def toggle(self):
        self.alarm_active = False  # Stop alarm if user starts/pauses
        self.running = not self.running

    def switch_mode(self, mode):
        self.alarm_active = False
        self.current_mode = mode
        self.remaining_seconds = (self.work_mins if mode == "Work" else self.break_mins) * 60
        self.update_ui()

    def reset(self):
        self.alarm_active = False
        self.remaining_seconds = (self.work_mins if self.current_mode == "Work" else self.break_mins) * 60
        self.running = False
        self.visible = True
        self.update_ui()

    def update_ui(self):
        display_mins = (self.remaining_seconds + 59) // 60
        if self.remaining_seconds <= 0:
            display_mins = 0
        self.icon.icon = self.create_icon(max(0, display_mins), self.visible)

    def timer_thread(self):
        last_tick = time.time()

        while True:
            now = time.time()

            if self.running and self.remaining_seconds > 0:
                if now - last_tick >= 1.0:
                    self.remaining_seconds -= 1
                    last_tick = now

                    if self.remaining_seconds <= 0:
                        self.running = False
                        self.visible = True
                        self.update_ui()

                        # Trigger Notification and Alarm
                        msg = f"{self.current_mode} session is complete!"
                        self.icon.notify(msg, "Pomodoro Timer")

                        self.alarm_active = True
                        threading.Thread(target=self.play_alarm, daemon=True).start()
                        continue

                if self.current_mode == "Work":
                    self.visible = int(now * 2) % 2 == 0
                else:
                    self.visible = True

                self.update_ui()

            time.sleep(0.1)

    def run(self):
        threading.Thread(target=self.timer_thread, daemon=True).start()
        self.icon.run()


if __name__ == "__main__":
    app = BlinkingTaskbarTimer()
    app.run()
