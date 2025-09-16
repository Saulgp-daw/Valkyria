# tooltip.py
import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay  # en milisegundos
        self.tooltip_window = None
        self.after_id = None

        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.cancel_tooltip)
        widget.bind("<Motion>", self.move_tooltip)

    def schedule_tooltip(self, event=None):
        # Programa el tooltip con retardo
        self.after_id = self.widget.after(700, lambda: self.show_tooltip(event))

    def cancel_tooltip(self, event=None):
        # Cancela tooltip si estaba pendiente o ya visible
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide_tooltip()

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.attributes("-alpha", 0.85)

        label = tk.Label(
            tw,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", 9)
        )
        label.pack(ipadx=1)

        self.move_tooltip(event)

    def move_tooltip(self, event):
        if not self.tooltip_window:
            return

        x = event.x_root + 10
        y = event.y_root - 30
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
