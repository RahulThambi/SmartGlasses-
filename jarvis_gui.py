import tkinter as tk
from tkinter import ttk
import queue
import threading
import time
from datetime import datetime
import customtkinter as ctk
import math

class ModernJarvisGUI:
    def __init__(self):
        # Set up the main window with a dark theme
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S. Interface")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        
        # Configure the window for a sleek, borderless look
        self.root.attributes("-fullscreen", True)
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Message queue for inter-thread communication
        self.message_queue = queue.Queue()
        
        # Initialize animation variables
        self.animation_frame = 0
        self.startup_progress = 0
        
        # Create main container with a dark background
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color='#0A1929',
            corner_radius=20
        )
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create startup animation canvas
        self.startup_canvas = tk.Canvas(
            self.main_container,
            background='#0A1929',
            highlightthickness=0,
            width=window_width,
            height=window_height
        )
        self.startup_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Start the startup sequence
        self.run_startup_sequence()
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.fullscreen = True
        
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        return "break"
    def run_startup_sequence(self):
        def animate_startup():
            if self.startup_progress < 100:
                self.startup_progress += 2
                self.draw_startup_animation()
                self.root.after(50, animate_startup)
            else:
                self.startup_canvas.destroy()
                self.create_main_interface()
                self.fade_in_window()
        
        self.draw_startup_animation()
        self.root.after(50, animate_startup)
        
    def draw_startup_animation(self):
        self.startup_canvas.delete("all")
        
        # Draw circular progress
        center_x = self.startup_canvas.winfo_width() // 2
        center_y = self.startup_canvas.winfo_height() // 2
        radius = 100
        
        # Draw multiple rotating circles
        for i in range(3):
            angle = (self.startup_progress * 3.6) + (i * 120)
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            
            # Create glowing circles with proper color values
            for j in range(20, 0, -5):
                intensity = int(j * 12.75)
                color = f'#{intensity:02x}BFFF'
                self.startup_canvas.create_oval(
                    x-10-j, y-10-j, x+10+j, y+10+j,
                    fill='',
                    outline=color,
                    width=2
                )
        
        # Draw progress text
        self.startup_canvas.create_text(
            center_x, center_y + 150,
            text=f"Initializing JARVIS... {self.startup_progress}%",
            fill='#00BFFF',
            font=('Roboto', 16)
        )
        
    def fade_in_window(self):
        def fade_in():
            alpha = self.root.attributes('-alpha')
            if alpha < 1.0:
                self.root.attributes('-alpha', alpha + 0.1)
                self.root.after(50, fade_in)
                
        self.root.after(0, fade_in)
        
    def create_main_interface(self):
        # Configure grid
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=3)
        
        # Create left panel for status and modules
        self.create_left_panel()
        
        # Create right panel for output
        self.create_right_panel()
        
        # Start animations
        self.animate_interface()
        
    def create_left_panel(self):
        left_panel = ctk.CTkFrame(
            self.main_container,
            fg_color='#0D2137',
            corner_radius=15
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Status Section
        self.create_status_section(left_panel)
        
        # Module Section
        self.create_module_section(left_panel)
        
    def create_status_section(self, parent):
        status_frame = ctk.CTkFrame(
            parent,
            fg_color='#102C44',
            corner_radius=10
        )
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create circular status indicator
        self.status_canvas = tk.Canvas(
            status_frame,
            width=100,
            height=100,
            bg='#102C44',
            highlightthickness=0
        )
        self.status_canvas.pack(pady=10)
        
        # Status text
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="STANDBY",
            font=("Roboto", 18, "bold"),
            text_color='#00BFFF'
        )
        self.status_label.pack(pady=5)
        
    def create_module_section(self, parent):
        module_frame = ctk.CTkFrame(
            parent,
            fg_color='#102C44',
            corner_radius=10
        )
        module_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Module header
        module_header = ctk.CTkLabel(
            module_frame,
            text="Active Modules",
            font=("Roboto", 16, "bold"),
            text_color='#00BFFF'
        )
        module_header.pack(pady=10)
        
        # Module indicators with animations
        self.module_indicators = {}
        modules = [
            "Object Detection",
            "Face Recognition",
            "Text Capture",
            "Speech Recording",
            "Gesture Control",
            "Navigation",
            "QR Scanner",
            "Music Player",
            "Environment Descriptor"
        ]
        
        for module in modules:
            module_container = ctk.CTkFrame(
                module_frame,
                fg_color='#153450',
                corner_radius=5
            )
            module_container.pack(fill=tk.X, padx=10, pady=5)
            
            # Create animated indicator canvas
            indicator_canvas = tk.Canvas(
                module_container,
                width=30,
                height=30,
                bg='#153450',
                highlightthickness=0
            )
            indicator_canvas.pack(side=tk.LEFT, padx=5)
            
            # Create circles for glow effect
            circles = []
            for i in range(3):
                circle = indicator_canvas.create_oval(
                    10-i*2, 10-i*2, 20+i*2, 20+i*2,
                    outline='#FF0000',
                    width=1
                )
                circles.append(circle)
            
            label = ctk.CTkLabel(
                module_container,
                text=module,
                font=("Roboto", 12),
                text_color='#FFFFFF'
            )
            label.pack(side=tk.LEFT, padx=10)
            
            self.module_indicators[module.lower().replace(" ", "")] = {
                'canvas': indicator_canvas,
                'circles': circles,
                'active': False
            }
            
    def create_right_panel(self):
        right_panel = ctk.CTkFrame(
            self.main_container,
            fg_color='#0D2137',
            corner_radius=15
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Output header
        header_frame = ctk.CTkFrame(
            right_panel,
            fg_color='#102C44',
            corner_radius=10
        )
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="System Output",
            font=("Roboto", 16, "bold"),
            text_color='#00BFFF'
        )
        header_label.pack(pady=10)
        
        # Create output text area
        self.output_text = ctk.CTkTextbox(
            right_panel,
            wrap=tk.WORD,
            font=("Roboto", 12),
            fg_color='#102C44',
            text_color='#FFFFFF',
            corner_radius=10
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags
        self.output_text.tag_config('user', foreground='#00ff00')    # Green
        self.output_text.tag_config('jarvis', foreground='#00bfff')  # Light blue
        self.output_text.tag_config('system', foreground='#ffa500')  # Orange
        self.output_text.tag_config('timestamp', foreground='#808080')  # Gray
        
    def animate_interface(self):
        # Animate status indicator
        self.animate_status()
        
        # Animate module indicators
        self.animate_modules()
        
        # Schedule next animation frame
        self.root.after(50, self.animate_interface)
        
    def animate_status(self):
        self.status_canvas.delete("all")
        
        # Draw rotating circles
        center_x = 50
        center_y = 50
        
        for i in range(3):
            angle = self.animation_frame + (i * 120)
            x = center_x + 30 * math.cos(math.radians(angle))
            y = center_y + 30 * math.sin(math.radians(angle))
            
            # Create glowing effect with proper color values
            for j in range(15, 0, -5):
                intensity = int(j * 12.75)
                color = f'#{intensity:02x}BFFF'
                self.status_canvas.create_oval(
                    x-5-j, y-5-j, x+5+j, y+5+j,
                    fill='',
                    outline=color,
                    width=2
                )
                
    def animate_modules(self):
        for module_data in self.module_indicators.values():
            if module_data['active']:
                canvas = module_data['canvas']
                circles = module_data['circles']
                
                # Animate each circle with different phases
                for i, circle in enumerate(circles):
                    phase = (self.animation_frame + i * 120) % 360
                    radius = 5 + math.sin(math.radians(phase)) * 2
                    
                    canvas.coords(
                        circle,
                        15-radius, 15-radius,
                        15+radius, 15+radius
                    )
                    
                    # Update color with pulsing effect
                    intensity = int(128 + 127 * math.sin(math.radians(phase)))
                    color = f'#00{intensity:02x}FF'
                    canvas.itemconfig(circle, outline=color)
                    
        # Increment animation frame
        self.animation_frame = (self.animation_frame + 1) % 360
        
    def update_status(self, status):
        self.status_label.configure(text=status)
        
    def update_module_status(self, module, active):
        if module.lower() in self.module_indicators:
            self.module_indicators[module.lower()]['active'] = active
            
            # Get the canvas for the module
            indicator_canvas = self.module_indicators[module.lower()]['canvas']
            
            if active:
                # If the module is active, set to blue
                for circle in self.module_indicators[module.lower()]['circles']:
                    indicator_canvas.itemconfig(circle, outline='#00BFFF')  # Active color
            else:
                # If the module is inactive, set to red (default color)
                for circle in self.module_indicators[module.lower()]['circles']:
                    indicator_canvas.itemconfig(circle, outline='#FF0000')  # Inactive color

            
    def add_message(self, message, message_type="info"):
        self.output_text.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add message with proper formatting
        self.output_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.output_text.insert(tk.END, f"{message}\n", message_type)
        
        # Auto-scroll to the bottom
        self.output_text.see(tk.END)
        self.output_text.configure(state='disabled')
        
    def process_messages(self):
        try:
            while not self.message_queue.empty():
                message = self.message_queue.get_nowait()
                
                if message['type'] == 'status':
                    self.update_status(message['value'])
                elif message['type'] == 'module':
                    self.update_module_status(message['module'], message['active'])
                elif message['type'] == 'message':
                    self.add_message(message['content'], message['source'])
                    
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_messages)
            
    def start(self):
        self.process_messages()
        self.root.mainloop()

def create_jarvis_gui():
    gui = ModernJarvisGUI()
    return gui.message_queue, gui.start

if __name__ == "__main__":
    queue, start_gui = create_jarvis_gui()
    start_gui()


