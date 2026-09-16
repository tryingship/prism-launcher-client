"""UI Styling for Prism Launcher Client"""

# Color scheme
COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'success': '#06A77D',      # Green
    'danger': '#D62828',       # Red
    'warning': '#F77F00',      # Orange
    'background': '#F5F5F5',   # Light gray
    'surface': '#FFFFFF',      # White
    'text_primary': '#1A1A1A', # Dark gray
    'text_secondary': '#666666', # Medium gray
    'border': '#E0E0E0',       # Light border
}

# Typography
FONTS = {
    'title': ('Helvetica Neue', 24, 'bold'),
    'heading': ('Helvetica Neue', 18, 'bold'),
    'subheading': ('Helvetica Neue', 14, 'bold'),
    'body': ('Helvetica Neue', 12, 'normal'),
    'small': ('Helvetica Neue', 10, 'normal'),
    'mono': ('Courier New', 11, 'normal'),
}

# Spacing
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 24,
    'xxl': 32,
}

# Button styling
BUTTON_STYLE = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': 'white',
        'padding_y': 8,
        'padding_x': 16,
    },
    'secondary': {
        'bg': COLORS['secondary'],
        'fg': 'white',
        'padding_y': 8,
        'padding_x': 16,
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': 'white',
        'padding_y': 8,
        'padding_x': 16,
    },
}
