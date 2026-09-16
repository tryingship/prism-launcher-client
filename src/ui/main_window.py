"""Main Window UI for Prism Launcher Client"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path

from core.prism_manager import PrismManager
from core.instance_manager import InstanceManager
from core.launcher import MinecraftLauncher
from ui.create_instance import CreateInstanceDialog
from ui.styles import COLORS, FONTS, SPACING
from utils.config import Config

logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window."""
    
    def __init__(self, config: Config):
        """Initialize the main window."""
        self.config = config
        self.prism_manager = PrismManager(config)
        self.instance_manager = InstanceManager(config)
        self.launcher = MinecraftLauncher(config)
        
        # Create root window
        self.root = tk.Tk()
        self.root.title("Prism Launcher Client")
        self.root.geometry("900x700")
        self.root.minsize(600, 400)
        
        # Configure style
        self.root.configure(bg=COLORS['background'])
        
        # Setup UI
        self._setup_ui()
        self._load_instances()
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup the user interface."""
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Prism Launcher",
            font=FONTS['title'],
            fg='white',
            bg=COLORS['primary']
        )
        title.pack(side=tk.LEFT, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Header buttons
        button_frame = tk.Frame(header, bg=COLORS['primary'])
        button_frame.pack(side=tk.RIGHT, padx=SPACING['lg'], pady=SPACING['lg'])
        
        new_btn = tk.Button(
            button_frame,
            text="+ New Instance",
            command=self._create_instance,
            bg=COLORS['success'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        new_btn.pack(side=tk.LEFT, padx=SPACING['sm'])
        
        settings_btn = tk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self._open_settings,
            bg=COLORS['secondary'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        settings_btn.pack(side=tk.LEFT, padx=SPACING['sm'])
        
        # Content area
        content = tk.Frame(self.root, bg=COLORS['background'])
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=SPACING['lg'])
        
        # Instances label
        label = tk.Label(
            content,
            text="Your Instances",
            font=FONTS['subheading'],
            fg=COLORS['text_primary'],
            bg=COLORS['background']
        )
        label.pack(anchor=tk.W, pady=(0, SPACING['md']))
        
        # Instances list with scrollbar
        list_frame = tk.Frame(content, bg=COLORS['surface'], relief=tk.SUNKEN, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.instances_listbox = tk.Listbox(
            list_frame,
            font=FONTS['body'],
            bg=COLORS['surface'],
            fg=COLORS['text_primary'],
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.instances_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=self.instances_listbox.yview)
        
        # Bind right-click context menu
        self.instances_listbox.bind('<Button-3>', self._show_context_menu)
        self.instances_listbox.bind('<Button-1>', lambda e: self._on_instance_selected())
        
        # Action buttons
        button_area = tk.Frame(content, bg=COLORS['background'])
        button_area.pack(fill=tk.X, pady=(SPACING['lg'], 0))
        
        launch_btn = tk.Button(
            button_area,
            text="🚀 Launch Selected",
            command=self._launch_instance,
            bg=COLORS['success'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        launch_btn.pack(side=tk.LEFT, padx=(0, SPACING['sm']))
        
        delete_btn = tk.Button(
            button_area,
            text="🗑️ Delete Selected",
            command=self._delete_instance,
            bg=COLORS['danger'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=(0, SPACING['sm']))
        
        refresh_btn = tk.Button(
            button_area,
            text="🔄 Refresh",
            command=self._load_instances,
            bg=COLORS['text_secondary'],
            fg='white',
            font=FONTS['body'],
            padx=SPACING['md'],
            pady=SPACING['sm'],
            border=0,
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=FONTS['small'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background'],
            anchor=tk.W,
            padx=SPACING['lg'],
            pady=SPACING['sm']
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _load_instances(self):
        """Load instances from Prism Launcher."""
        self.instances_listbox.delete(0, tk.END)
        self._set_status("Loading instances...")
        
        try:
            instances = self.instance_manager.get_instances()
            for instance in instances:
                self.instances_listbox.insert(tk.END, instance['name'])
            
            self._set_status(f"Loaded {len(instances)} instance(s)")
            logger.info(f"Loaded {len(instances)} instances")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load instances: {e}")
            self._set_status("Error loading instances")
            logger.error(f"Failed to load instances: {e}")
    
    def _on_instance_selected(self):
        """Handle instance selection."""
        selection = self.instances_listbox.curselection()
        if selection:
            instance_name = self.instances_listbox.get(selection[0])
            self._set_status(f"Selected: {instance_name}")
    
    def _launch_instance(self):
        """Launch the selected instance."""
        selection = self.instances_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an instance to launch")
            return
        
        instance_name = self.instances_listbox.get(selection[0])
        self._set_status(f"Launching {instance_name}...")
        
        try:
            self.launcher.launch(instance_name)
            messagebox.showinfo("Success", f"Launched {instance_name}")
            logger.info(f"Launched instance: {instance_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch instance: {e}")
            self._set_status("Launch failed")
            logger.error(f"Failed to launch instance: {e}")
    
    def _create_instance(self):
        """Open create instance dialog."""
        dialog = CreateInstanceDialog(self.root, self.config)
        self.root.wait_window(dialog.window)
        
        if dialog.result:
            self._load_instances()
            self._set_status(f"Created instance: {dialog.result['name']}")
    
    def _delete_instance(self):
        """Delete the selected instance."""
        selection = self.instances_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an instance to delete")
            return
        
        instance_name = self.instances_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirm", f"Delete '{instance_name}'? This cannot be undone."):
            try:
                self.instance_manager.delete_instance(instance_name)
                self._load_instances()
                messagebox.showinfo("Success", f"Deleted {instance_name}")
                logger.info(f"Deleted instance: {instance_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete instance: {e}")
                logger.error(f"Failed to delete instance: {e}")
    
    def _open_settings(self):
        """Open settings dialog."""
        messagebox.showinfo("Settings", "Settings feature coming soon!")
    
    def _show_context_menu(self, event):
        """Show context menu on right-click."""
        selection = self.instances_listbox.nearest(event.y)
        if selection >= 0:
            self.instances_listbox.selection_clear(0, tk.END)
            self.instances_listbox.selection_set(selection)
            self.instances_listbox.activate(selection)
            
            menu = tk.Menu(self.root, tearoff=False)
            menu.add_command(label="Launch", command=self._launch_instance)
            menu.add_command(label="Delete", command=self._delete_instance)
            menu.add_separator()
            menu.add_command(label="View Details", command=lambda: messagebox.showinfo("Details", "Coming soon!"))
            
            menu.tk_popup(event.x_root, event.y_root)
    
    def _set_status(self, message: str):
        """Update the status bar."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()
