"""Create Instance Dialog for Prism Launcher Client"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from core.instance_manager import InstanceManager
from ui.styles import COLORS, FONTS, SPACING
from utils.config import Config

logger = logging.getLogger(__name__)


class CreateInstanceDialog:
    """Dialog for creating a new Minecraft instance."""
    
    MINECRAFT_VERSIONS = [
        "1.20.1",
        "1.20",
        "1.19.2",
        "1.19.1",
        "1.19",
        "1.18.2",
        "1.18.1",
        "1.18",
        "1.17.1",
        "1.17",
        "1.16.5",
        "1.16.4",
        "1.16.3",
        "1.16.2",
        "1.16.1",
        "1.16",
        "1.15.2",
    ]
    
    def __init__(self, parent, config: Config):
        """Initialize the create instance dialog."""
        self.config = config
        self.instance_manager = InstanceManager(config)
        self.result = None
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Create New Instance")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.configure(bg=COLORS['background'])
        
        # Make modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Setup UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the dialog UI."""
        # Header
        header = tk.Frame(self.window, bg=COLORS['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Create New Instance",
            font=FONTS['heading'],
            fg='white',
            bg=COLORS['primary']
        )
        title.pack(padx=SPACING['lg'], pady=SPACING['lg'], anchor=tk.W)
        
        # Content
        content = tk.Frame(self.window, bg=COLORS['background'])
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Instance Name
        name_label = tk.Label(
            content,
            text="Instance Name",
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        name_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))
        
        self.name_entry = tk.Entry(
            content,
            font=FONTS['body'],
            width=40,
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            relief=tk.SUNKEN,
            bd=1
        )
        self.name_entry.pack(anchor=tk.W, pady=(0, SPACING['lg']))
        self.name_entry.focus()
        
        # Game Version
        version_label = tk.Label(
            content,
            text="Game Version",
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        version_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))
        
        self.version_var = tk.StringVar(value=self.MINECRAFT_VERSIONS[0])
        version_combo = ttk.Combobox(
            content,
            textvariable=self.version_var,
            values=self.MINECRAFT_VERSIONS,
            state='readonly',
            font=FONTS['body'],
            width=37
        )
        version_combo.pack(anchor=tk.W, pady=(0, SPACING['lg']))
        
        # Memory Settings Frame
        memory_frame = tk.LabelFrame(
            content,
            text="Memory Settings",
            font=FONTS['subheading'],
            fg=COLORS['text_primary'],
            bg=COLORS['background'],
            padx=SPACING['md'],
            pady=SPACING['md']
        )
        memory_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, SPACING['lg']))
        
        # Min Memory
        min_label = tk.Label(
            memory_frame,
            text="Minimum Memory (MB)",
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        min_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))
        
        self.min_mem_entry = tk.Entry(
            memory_frame,
            font=FONTS['body'],
            width=40,
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            relief=tk.SUNKEN,
            bd=1
        )
        self.min_mem_entry.insert(0, "512")
        self.min_mem_entry.pack(anchor=tk.W, pady=(0, SPACING['lg']))
        
        # Max Memory
        max_label = tk.Label(
            memory_frame,
            text="Maximum Memory (MB)",
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        max_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))
        
        self.max_mem_entry = tk.Entry(
            memory_frame,
            font=FONTS['body'],
            width=40,
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            relief=tk.SUNKEN,
            bd=1
        )
        self.max_mem_entry.insert(0, "2048")
        self.max_mem_entry.pack(anchor=tk.W)
        
        # Java Settings Frame
        java_frame = tk.LabelFrame(
            content,
            text="Java Settings",
            font=FONTS['subheading'],
            fg=COLORS['text_primary'],
            bg=COLORS['background'],
            padx=SPACING['md'],
            pady=SPACING['md']
        )
        java_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, SPACING['lg']))
        
        # Java Path
        java_label = tk.Label(
            java_frame,
            text="Java Path",
            font=FONTS['body'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        java_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))
        
        self.java_entry = tk.Entry(
            java_frame,
            font=FONTS['mono'],
            width=40,
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            relief=tk.SUNKEN,
            bd=1
        )
        self.java_entry.insert(0, "/usr/libexec/java_home")
        self.java_entry.pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(self.window, bg=COLORS['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['lg'], pady=SPACING['lg'])
        
        create_btn = tk.Button(
            button_frame,
            text="✓ Create",
            command=self._create_instance,
            bg=COLORS['success'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        create_btn.pack(side=tk.LEFT, padx=(0, SPACING['sm']))
        
        cancel_btn = tk.Button(
            button_frame,
            text="✕ Cancel",
            command=self.window.destroy,
            bg=COLORS['text_secondary'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def _create_instance(self):
        """Create the instance."""
        # Validate inputs
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an instance name")
            return
        
        if len(name) > 100:
            messagebox.showerror("Error", "Instance name is too long (max 100 characters)")
            return
        
        try:
            min_mem = int(self.min_mem_entry.get())
            max_mem = int(self.max_mem_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Memory values must be valid integers")
            return
        
        if min_mem <= 0 or max_mem <= 0:
            messagebox.showerror("Error", "Memory values must be greater than 0")
            return
        
        if min_mem > max_mem:
            messagebox.showerror("Error", "Minimum memory cannot be greater than maximum")
            return
        
        java_path = self.java_entry.get().strip()
        if not java_path:
            messagebox.showerror("Error", "Please enter a Java path")
            return
        
        # Create instance
        try:
            instance_data = {
                'name': name,
                'version': self.version_var.get(),
                'min_memory': str(min_mem),
                'max_memory': str(max_mem),
                'java_path': java_path
            }
            
            self.instance_manager.create_instance(instance_data)
            self.result = instance_data
            messagebox.showinfo("Success", f"Created instance '{name}'")
            logger.info(f"Created instance: {name}")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create instance: {e}")
            logger.error(f"Failed to create instance: {e}")
