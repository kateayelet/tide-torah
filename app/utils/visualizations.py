import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from typing import Dict, Any
from math import sin, cos, pi
import json

class MoonVisualization:
    def __init__(self):
        self.phase_colors = {
            "New Moon": "#1a1a1a",
            "Waxing Crescent": "#4d4d4d",
            "First Quarter": "#808080",
            "Waxing Gibbous": "#b3b3b3",
            "Full Moon": "#ffffff",
            "Waning Gibbous": "#b3b3b3",
            "Last Quarter": "#808080",
            "Waning Crescent": "#4d4d4d"
        }

    def create_moon_visual(self, phase: float, phase_name: str) -> Dict[str, Any]:
        """
        Create a visual representation of the moon phase
        """
        # Create moon shape
        theta = np.linspace(0, 2*pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        
        # Calculate illuminated portion
        illuminated = phase / 100
        theta_ill = np.linspace(0, 2*pi*illuminated, 50)
        x_ill = np.cos(theta_ill)
        y_ill = np.sin(theta_ill)
        
        # Create figure
        fig = go.Figure()
        
        # Add moon outline
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='black', width=2),
            name='Moon'
        ))
        
        # Add illuminated portion
        fig.add_trace(go.Scatter(
            x=x_ill, y=y_ill,
            mode='lines',
            line=dict(color=self.phase_colors[phase_name], width=2),
            fill='toself',
            fillcolor=self.phase_colors[phase_name],
            name='Illuminated'
        ))
        
        # Update layout
        fig.update_layout(
            width=300,
            height=300,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=0, r=0, t=0, b=0),
            annotations=[
                dict(
                    text=f"{phase_name}<br>{phase:.1f}%",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=14)
                )
            ]
        )
        
        return fig.to_dict()

class TideVisualization:
    def __init__(self):
        self.tide_colors = {
            "high": "#0066cc",
            "low": "#00cc99",
            "current": "#ff0000"
        }

    def create_tide_visual(self, tide_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a visualization of tide patterns
        """
        # Generate x-axis (time)
        x = np.linspace(0, 24, 100)
        
        # Generate y-axis (tide height)
        y = 1.5 * np.sin(2*pi*x/12) + 1.5 * np.sin(2*pi*x/24)  # Combines diurnal and semidiurnal tides
        
        # Create figure
        fig = go.Figure()
        
        # Add tide line
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='#0066cc', width=2),
            name='Tide Level'
        ))
        
        # Add high and low tide markers
        high_tide = max(y)
        low_tide = min(y)
        
        fig.add_trace(go.Scatter(
            x=[0, 24],
            y=[high_tide, high_tide],
            mode='lines',
            line=dict(color=self.tide_colors["high"], dash='dash'),
            name='High Tide'
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, 24],
            y=[low_tide, low_tide],
            mode='lines',
            line=dict(color=self.tide_colors["low"], dash='dash'),
            name='Low Tide'
        ))
        
        # Add current time marker
        current_time = datetime.now().hour
        current_tide = 1.5 * np.sin(2*pi*current_time/12) + 1.5 * np.sin(2*pi*current_time/24)
        
        fig.add_trace(go.Scatter(
            x=[current_time],
            y=[current_tide],
            mode='markers',
            marker=dict(color=self.tide_colors["current"], size=10),
            name='Current Time'
        ))
        
        # Update layout
        fig.update_layout(
            title='Tide Pattern (24-hour cycle)',
            xaxis_title='Hours',
            yaxis_title='Tide Level (m)',
            width=600,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            hovermode='x unified'
        )
        
        return fig.to_dict()

class SefirotVisualization:
    def __init__(self):
        self.sefirot_positions = {
            "Keter": (0, 10),
            "Chochmah": (-5, 8),
            "Binah": (5, 8),
            "Chesed": (-10, 6),
            "Gevurah": (10, 6),
            "Tiferet": (0, 4),
            "Netzach": (-5, 2),
            "Hod": (5, 2),
            "Yesod": (0, 0),
            "Malchut": (0, -2)
        }
        
        self.sefirot_colors = {
            "Keter": "#ff0000",
            "Chochmah": "#ff8000",
            "Binah": "#ffff00",
            "Chesed": "#00ff00",
            "Gevurah": "#00ffff",
            "Tiferet": "#0000ff",
            "Netzach": "#ff00ff",
            "Hod": "#800080",
            "Yesod": "#808080",
            "Malchut": "#ffffff"
        }

    def create_sefirot_tree(self, highlighted_sefirot: list = None) -> Dict[str, Any]:
        """
        Create a visualization of the Tree of Life with highlighted sefirot
        """
        fig = go.Figure()
        
        # Add connections
        connections = [
            ("Keter", "Chochmah"), ("Keter", "Binah"),
            ("Chochmah", "Binah"),
            ("Chochmah", "Chesed"), ("Binah", "Gevurah"),
            ("Chesed", "Gevurah"),
            ("Chesed", "Tiferet"), ("Gevurah", "Tiferet"),
            ("Tiferet", "Netzach"), ("Tiferet", "Hod"),
            ("Netzach", "Hod"),
            ("Netzach", "Yesod"), ("Hod", "Yesod"),
            ("Yesod", "Malchut")
        ]
        
        for start, end in connections:
            x0, y0 = self.sefirot_positions[start]
            x1, y1 = self.sefirot_positions[end]
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines',
                line=dict(color='black', width=1),
                showlegend=False
            ))
        
        # Add sefirot
        for sefira in self.sefirot_positions:
            x, y = self.sefirot_positions[sefira]
            color = self.sefirot_colors[sefira]
            
            # Highlight if needed
            if highlighted_sefirot and sefira in highlighted_sefirot:
                color = '#ff0000'
                size = 15
            else:
                size = 10
            
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(color=color, size=size),
                text=[sefira],
                textposition='middle right',
                textfont=dict(color='black', size=12),
                showlegend=False
            ))
        
        # Update layout
        fig.update_layout(
            width=800,
            height=600,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=50, r=50, t=50, b=50),
            title='Tree of Life (Etz Chaim)'
        )
        
        return fig.to_dict()

# Create singleton instances
moon_visualizer = MoonVisualization()
tide_visualizer = TideVisualization()
sefirot_visualizer = SefirotVisualization()
