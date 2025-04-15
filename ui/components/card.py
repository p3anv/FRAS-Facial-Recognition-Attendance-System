class Card(ttk.Frame):
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        self.config(padding=15)
        
        if title:
            ttk.Label(
                self, 
                text=title, 
                style="CardTitle.TLabel"
            ).pack(anchor="w", pady=(0,10))
        
        self.content = ttk.Frame(self)
        self.content.pack(fill="both", expand=True)