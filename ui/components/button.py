class HoverButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="TButton", **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event):
        self.config(style="Hover.TButton")
        
    def _on_leave(self, event):
        self.config(style="TButton")