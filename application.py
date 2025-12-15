# application.py
#--- Importing Libraries

import dash #for the website
from dash import html, dcc, Input, Output, callback_context, State, ALL, MATCH, dash_table #for the sliders, drop-down, etc
import dash_bootstrap_components as dbc #for pre-styled buttons
import plotly.graph_objects as go #for plot
import numpy as np #for math
import requests #for arduino
#--- Import From Previous
from bioreactor_generalized import gravity, rpm_to_w, gravity_to_rpm_n_tilt, rotation_matrix
from particle_properties import particle_concentration_time, particle_fraction, fluid_viscosity_time, sedimentation_velocity, reynolds_number, flow_type, ang_linear_v_and_shear, particles_property
from particle_bioreactor import particle_rotating
from rectangle_heatmap import circular_heatmap
from docs import full_text  # Import math content from docs.py

#--- Initialize Application
app= dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions= True) #making the code connected to "app" and the app looks "darkly / space-like"
app.title= "Rotating Wall Vessel Bioreactor" #seen at the top

# Custom CSS for space theme
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

* {
    font-family: 'Rajdhani', sans-serif;
}

body {
    background: linear-gradient(135deg, #0c0c2e 0%, #1a1a4a 25%, #2d1b4e 50%, #1a1a4a 75%, #0c0c2e 100%);
    background-attachment: fixed;
    overflow-x: hidden;
}

/* Animated stars background */
.stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}

.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle 3s infinite;
}

@keyframes twinkle {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}

/* Glassmorphism effect */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    padding: 30px;
    margin: 20px auto;
    transition: all 0.3s ease;
    /* FIX 3: Positioning Context for Dropdown Layering */
    position: relative; /* Creates stacking context */
    z-index: 1; /* Low z-index - dropdowns (z-index: 9999) will appear above */
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(147, 112, 219, 0.3);
}

/* Title styling */
.cosmic-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 3.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #764ba2 75%, #667eea 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 5s ease infinite;
    text-shadow: 0 0 30px rgba(118, 75, 162, 0.5);
    letter-spacing: 3px;
    margin: 30px 0;
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    color: #a78bfa;
    text-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
    margin: 25px 0;
    letter-spacing: 2px;
}

/* Modern input styling */
.custom-input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px solid rgba(167, 139, 250, 0.3) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 15px 20px !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin: 10px 0 !important;
}

.custom-input:focus {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid #a78bfa !important;
    box-shadow: 0 0 20px rgba(167, 139, 250, 0.4) !important;
    outline: none !important;
}

.custom-input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Modern button styling */
.cosmic-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 15px 40px !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: white !important;
    box-shadow: 0 8px 25px rgba(118, 75, 162, 0.4) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.cosmic-button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 12px 35px rgba(118, 75, 162, 0.6) !important;
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
}

/* Tab styling */
.custom-tabs .tab {
    background: rgba(255, 255, 255, 0.05) !important;
    border: none !important;
    border-radius: 15px 15px 0 0 !important;
    padding: 15px 30px !important;
    color: rgba(255, 255, 255, 0.6) !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    margin: 0 5px !important;
}

.custom-tabs .tab--selected {
    background: rgba(167, 139, 250, 0.2) !important;
    color: #a78bfa !important;
    border-bottom: 3px solid #a78bfa !important;
}

.custom-tabs .tab:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
}

/* =====================================================
   DROPDOWN STYLING - COMPREHENSIVE FIX
   =====================================================
   Fixes:
   1. Dark background with white text for good contrast
   2. Proper z-index management to prevent overlap
   3. Correct positioning context for dropdown layering
   ===================================================== */

/* Dropdown Wrapper Container
   - Creates positioning context for absolute-positioned menu
   - Sets base z-index (low when closed, higher when open)
   - Ensures full width for proper dropdown display */
.custom-dropdown {
    width: 100% !important;
    min-width: 100% !important;
    position: relative !important; /* CRITICAL: Creates stacking context for menu positioning */
    z-index: 10 !important; /* Base z-index when dropdown is closed */
}

/* Select Component Base Styling
   - Default state: low z-index to stay in normal flow
   - Prevents dropdown from overlapping other content when closed */
.custom-dropdown .Select {
    position: relative !important;
    z-index: 10 !important; /* Same as wrapper - stays in normal document flow */
}

/* Select Component When Open
   - Increases z-index significantly to ensure menu appears above all content
   - High enough to overlay other cards/inputs but not excessively high */
.custom-dropdown .Select.is-open {
    z-index: 9999 !important; /* HIGH z-index when open - ensures menu is on top */
}

/* Select Control (the clickable dropdown button/box)
   - When open, control stays visible but doesn't block the menu
   - Proper z-index ensures menu appears above control */
.custom-dropdown .Select.is-open > .Select-control {
    z-index: 9998 !important; /* Slightly lower than menu so menu appears on top */
}

/* Universal selectors for react-select within custom-dropdown */
.custom-dropdown .Select,
.custom-dropdown .Select > div,
.custom-dropdown .Select div,
.custom-dropdown .Select input,
.custom-dropdown .Select span {
    color: white !important;
}

/* Control (main dropdown box) */
.custom-dropdown .Select-control,
.custom-dropdown .Select.is-open > .Select-control,
.custom-dropdown .Select.is-focused > .Select-control,
.custom-dropdown .Select.is-focused:not(.is-open) > .Select-control {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(167, 139, 250, 0.5) !important;
    border-radius: 12px !important;
    min-height: 50px !important;
    height: auto !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

.custom-dropdown .Select-control:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 2px solid #a78bfa !important;
    box-shadow: 0 0 20px rgba(167, 139, 250, 0.5) !important;
}

/* Value (selected text) - critical for visibility */
.custom-dropdown .Select-value {
    position: relative !important;
    top: auto !important;
    left: 0 !important;
    transform: none !important;
    line-height: 1.5 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

.custom-dropdown .Select-value-label {
    color: #ffffff !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    line-height: 1.5 !important;
    word-wrap: break-word !important;
}

/* Input area */
.custom-dropdown .Select-input {
    height: auto !important;
    line-height: 1.5 !important;
    padding: 0 !important;
}

.custom-dropdown .Select-input > input {
    color: white !important;
    font-size: 1.15rem !important;
    font-weight: 500 !important;
    padding: 0 !important;
}

.custom-dropdown .Select-placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 1.15rem !important;
    font-weight: 500 !important;
}

/* Arrow */
.custom-dropdown .Select-arrow-zone {
    padding: 0 10px !important;
    width: auto !important;
}

.custom-dropdown .Select-arrow {
    color: #a78bfa !important;
    border-color: #a78bfa transparent transparent !important;
    border-width: 6px 5px 0 5px !important;
}

/* =====================================================
   DROPDOWN MENU (Options List) - CONTRAST & Z-INDEX FIX
   ===================================================== */

/* Menu Outer Container
   - SOLID dark background (#1a1a4a) ensures white text is visible
   - Highest z-index (9999) ensures menu appears above ALL other content
   - Absolute positioning relative to .custom-dropdown wrapper
   - Positioned directly below the control button */
.custom-dropdown .Select-menu-outer {
    /* FIX 1: Dark Background for Contrast */
    background: #1a1a4a !important; /* Solid dark blue-purple - NOT transparent */
    background-color: #1a1a4a !important; /* Redundant but ensures override of any inherited styles */
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    
    /* Visual Styling */
    border: 2px solid rgba(167, 139, 250, 0.6) !important; /* Purple border matches theme */
    border-radius: 12px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8) !important; /* Strong shadow for depth */
    
    /* FIX 2: Z-Index Management */
    z-index: 9999 !important; /* HIGHEST z-index - ensures menu overlays everything */
    position: absolute !important; /* Positioned relative to .custom-dropdown wrapper */
    
    /* Positioning */
    top: 100% !important; /* Appears directly below the control */
    left: 0 !important; /* Aligned with left edge of wrapper */
    right: 0 !important; /* Aligned with right edge of wrapper */
    margin-top: 8px !important; /* Small gap between control and menu */
    width: 100% !important; /* Full width of wrapper */
    
    /* Scrolling */
    max-height: 350px !important; /* Limit height to prevent off-screen overflow */
    overflow-y: auto !important; /* Enable vertical scrolling if needed */
}

/* Menu Inner Container
   - Inherits dark background from outer container
   - Ensures all menu content has dark background */
.custom-dropdown .Select-menu {
    max-height: 350px !important;
    overflow-y: auto !important;
    /* FIX 1: Dark Background Inheritance */
    background: #1a1a4a !important; /* Same dark color as outer */
    background-color: #1a1a4a !important; /* Ensures solid background */
}

/* Dropdown Options (Individual Menu Items)
   - FIX 1: Solid dark background ensures white text visibility
   - FIX 1: White text color (#ffffff) for maximum contrast
   - Proper padding and spacing for readability */
.custom-dropdown .Select-option {
    /* FIX 1: Dark Background - NO transparency */
    background: #1a1a4a !important; /* Solid dark background */
    background-color: #1a1a4a !important; /* Ensures solid color, not transparent */
    
    /* FIX 1: White Text for Contrast */
    color: #ffffff !important; /* Pure white text - excellent contrast on dark background */
    
    /* Typography & Spacing */
    padding: 14px 18px !important; /* Comfortable padding for clickability */
    font-size: 1.1rem !important; /* Readable font size */
    font-weight: 500 !important; /* Medium weight for normal options */
    line-height: 1.6 !important; /* Good line spacing for readability */
    
    /* Text Handling */
    white-space: normal !important; /* Allow text wrapping if needed */
    word-wrap: break-word !important; /* Break long words if necessary */
    overflow: visible !important; /* Show full text, no truncation */
    text-overflow: clip !important; /* Don't truncate with ellipsis */
    
    /* Layout */
    width: 100% !important; /* Full width of menu */
    display: block !important; /* Block display for proper spacing */
    min-height: auto !important; /* Auto height based on content */
    height: auto !important;
    cursor: pointer !important; /* Pointer cursor indicates clickability */
    
    /* Visual Separator */
    border-bottom: 1px solid rgba(167, 139, 250, 0.2) !important; /* Subtle purple divider */
}

/* Remove border from last option */
.custom-dropdown .Select-option:last-child {
    border-bottom: none !important;
}

/* Option Hover & Focus States
   - FIX 1: Purple background maintains contrast (still dark enough for white text)
   - White text remains visible on purple background */
.custom-dropdown .Select-option:hover,
.custom-dropdown .Select-option.is-focused {
    /* FIX 1: Dark Purple Background - maintains contrast */
    background: rgba(167, 139, 250, 0.5) !important; /* Dark purple - still readable */
    background-color: rgba(167, 139, 250, 0.5) !important;
    color: #ffffff !important; /* White text still visible */
    font-weight: 700 !important; /* Bold on hover for emphasis */
}

/* Selected Option State
   - FIX 1: Darker purple for selected state, white text still visible
   - Provides clear visual feedback */
.custom-dropdown .Select-option.is-selected {
    /* FIX 1: Darker Purple Background for Selected State */
    background: rgba(167, 139, 250, 0.7) !important; /* More opaque purple */
    background-color: rgba(167, 139, 250, 0.7) !important;
    color: #ffffff !important; /* White text maintains visibility */
    font-weight: 700 !important; /* Bold for selected item */
}

/* Force no truncation anywhere */
.custom-dropdown * {
    overflow: visible !important;
    text-overflow: clip !important;
}

.custom-dropdown .Select-value-label,
.custom-dropdown .Select-option {
    text-overflow: clip !important;
    overflow: visible !important;
}

/* Global selectors as fallback - target all Select components */
.Select-control {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid rgba(167, 139, 250, 0.4) !important;
    color: white !important;
}

.Select-value-label {
    color: #ffffff !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    max-width: none !important;
}

/* =====================================================
   GLOBAL DROPDOWN STYLES (Fallback for all dropdowns)
   =====================================================
   These styles apply to ALL Select components as a fallback
   to ensure dark backgrounds even if custom-dropdown class
   isn't applied correctly
   ===================================================== */

/* Global Menu Outer - Fallback Dark Background */
.Select-menu-outer {
    /* FIX 1: Dark background for all dropdowns */
    background: #1a1a4a !important;
    background-color: #1a1a4a !important;
    /* FIX 2: High z-index to prevent overlap */
    z-index: 9999 !important;
}

/* Global Menu - Fallback Dark Background */
.Select-menu {
    /* FIX 1: Dark background inheritance */
    background: #1a1a4a !important;
    background-color: #1a1a4a !important;
}

/* Global Options - Fallback Styling */
.Select-option {
    /* FIX 1: Dark background with white text */
    background: #1a1a4a !important;
    background-color: #1a1a4a !important;
    color: #ffffff !important; /* White text for contrast */
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* Global Option Hover State */
.Select-option:hover,
.Select-option.is-focused {
    /* FIX 1: Purple hover maintains white text visibility */
    background: rgba(167, 139, 250, 0.5) !important;
    background-color: rgba(167, 139, 250, 0.5) !important;
    color: #ffffff !important; /* White text remains visible */
}

/* Radio items styling */
.custom-radio {
    color: white !important;
    font-size: 1.1rem !important;
}

.custom-radio input[type="radio"] {
    accent-color: #a78bfa !important;
    width: 20px !important;
    height: 20px !important;
    margin-right: 10px !important;
}

.custom-radio label {
    margin-right: 30px !important;
    cursor: pointer !important;
    transition: color 0.3s ease !important;
}

.custom-radio label:hover {
    color: #a78bfa !important;
}

/* Result display styling */
.result-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
    border: 1px solid rgba(167, 139, 250, 0.3);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    font-size: 1.1rem;
    color: #e9d5ff;
    box-shadow: 0 4px 15px rgba(118, 75, 162, 0.2);
}

/* Label styling */
.cosmic-label {
    font-family: 'Orbitron', sans-serif;
    font-weight: 600;
    color: #c4b5fd;
    font-size: 1.2rem;
    margin: 15px 0 10px 0;
    letter-spacing: 1px;
}

/* Graph container */
.graph-container {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.graph-container:hover {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(167, 139, 250, 0.3);
    box-shadow: 0 8px 25px rgba(118, 75, 162, 0.2);
}

/* Plotly graph styling */
.js-plotly-plot .plotly .modebar {
    background: rgba(26, 26, 74, 0.9) !important;
    border: 1px solid rgba(167, 139, 250, 0.3) !important;
    border-radius: 8px !important;
}

.js-plotly-plot .plotly .modebar-btn {
    color: #a78bfa !important;
}

.js-plotly-plot .plotly .modebar-btn:hover {
    background: rgba(167, 139, 250, 0.2) !important;
}

/* Main container */
.main-container {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    padding: 20px;
}

/* Markdown content styling */
.markdown-content {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.8;
    font-size: 1.1rem;
}

.markdown-content h1, .markdown-content h2, .markdown-content h3 {
    color: #a78bfa;
    font-family: 'Orbitron', sans-serif;
}

/* Responsive design */
@media (max-width: 768px) {
    .cosmic-title {
        font-size: 2.5rem;
    }
    
    .glass-card {
        padding: 20px;
        margin: 10px;
    }
}
"""

# Custom index string with CSS and stars animation script
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
        ''' + custom_css + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
        (function() {
            function createStars() {
                var container = document.getElementById("stars-container");
                if (!container) {
                    setTimeout(createStars, 100);
                    return;
                }
                
                container.innerHTML = '';
                
                for (let i = 0; i < 200; i++) {
                    let star = document.createElement("div");
                    star.classList.add("star");
                    star.style.position = "absolute";
                    star.style.background = "white";
                    star.style.borderRadius = "50%";
                    star.style.left = Math.random() * 100 + "%";
                    star.style.top = Math.random() * 100 + "%";
                    star.style.width = (Math.random() * 3 + 1) + "px";
                    star.style.height = star.style.width;
                    star.style.animationDelay = Math.random() * 3 + "s";
                    star.style.animationDuration = (Math.random() * 2 + 2) + "s";
                    star.style.animation = "twinkle 3s infinite";
                    star.style.opacity = Math.random() * 0.8 + 0.2;
                    star.style.pointerEvents = "none";
                    container.appendChild(star);
                }
            }
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', createStars);
            } else {
                setTimeout(createStars, 100);
            }
        })();
        </script>
    </body>
</html>'''

#--- Layout
app.layout= html.Div([
    html.Div(id="stars-container", style={"position": "fixed", "top": "0", "left": "0", "width": "100%", "height": "100%", "pointerEvents": "none", "zIndex": "0"}),
    html.Div(className="main-container", style={"position": "relative", "zIndex": "1"}, children=[
        html.H1("Rotating Wall Vessel Bioreactor", className="cosmic-title"),
        html.Div(
            dcc.Tabs(
                id="tab_ex",
                value="simulation_tab",
                className="custom-tabs",
                children=[
                    dcc.Tab(label="🚀 Simulation", value="simulation_tab", className="tab"),
                    dcc.Tab(label="📐 Math Behind It All", value="math_tab", className="tab")
                ]
            ),
            style={"maxWidth": "600px", "margin": "30px auto"}
        ),
        html.Div(id="tabs_content")
    ])
], style={
    "background": "linear-gradient(135deg, #0c0c2e 0%, #1a1a4a 25%, #2d1b4e 50%, #1a1a4a 75%, #0c0c2e 100%)",
    "backgroundImage": 'url("https://static.vecteezy.com/system/resources/previews/013/141/947/large_2x/pretty-purple-nebula-galaxy-astrology-deep-outer-space-cosmos-background-beautiful-abstract-illustration-art-dust-free-photo.jpg")',
    "backgroundSize": "cover",
    "backgroundAttachment": "fixed",
    "minHeight": "100vh",
    "position": "relative"
}) 

#simulation
simulation_layout= html.Div([
    html.H2("🌌 Simulation", className="section-title"),
    
    dbc.Card(className="glass-card", children=[
        html.Label("Bioreactor Radius", className="cosmic-label"),
        dbc.Input(
            id="input_radius_bioreactor",
            type="number",
            placeholder="Enter Radius of Bioreactor (m)",
            className="custom-input",
            style={"maxWidth": "500px", "margin": "0 auto"}
        ),
    ], style={"maxWidth": "600px", "margin": "30px auto"}),
    
    dbc.Card(className="glass-card", children=[
        html.Label("Select Zone", className="cosmic-label"),
        html.Div(
            dcc.Dropdown(
                id="zone_choice",
                options=[
                    {"label": "🌍 Inner Zone", "value": "Inner Zone"},
                    {"label": "🌎 Middle Zone", "value": "Middle Zone"},
                    {"label": "🌏 Outer Zone", "value": "Outer Zone"},
                    {"label": "🌐 All Zones", "value": "All Zones"},
                    {"label": "🔴 Outer Radius", "value": "Outer Radius"}
                ],
                value="Middle Zone",
                clearable=False,
                className="custom-dropdown",
                style={"width": "100%", "minWidth": "100%"}
            ),
            className="custom-dropdown",
            style={"maxWidth": "500px", "margin": "0 auto", "width": "100%"}
        ),
    ], style={"maxWidth": "600px", "margin": "30px auto"}),
    
    dbc.Card(className="glass-card", children=[
        html.Label("Input Mode", className="cosmic-label"),
        dbc.RadioItems(
            id="mode_selection",
            options=[
                {"label": "Use RPM and Tilt", "value": "rpm_n_tilt"},
                {"label": "Use Intended Gravity", "value": "gravity_intended"}
            ],
            value="rpm_n_tilt",
            inline=True,
            className="custom-radio"
        ),
        html.Div(id="conditional_inputs"),
    ], style={"maxWidth": "600px", "margin": "30px auto"}),
    
    dbc.Card(className="glass-card", children=[
        html.Label("Particle Simulation", className="cosmic-label"),
        dbc.RadioItems(
            id="particles",
            options=[
                {"label": "Particles Off", "value": "off"},
                {"label": "Particles On", "value": "on"}
            ],
            value="off",
            inline=True,
            className="custom-radio"
        ),
        html.Div(id="particle_inputs"),
    ], style={"maxWidth": "600px", "margin": "30px auto"}),
    
    html.Div(
        dbc.Button("🚀 Run Simulation", id="run_button", className="cosmic-button"),
        style={"textAlign": "center", "margin": "40px 0"}
    ),
    
    dbc.Card(className="glass-card", children=[
        html.Div(id="computed_g_intended", className="result-box"),
        html.Div(id="computed_rpm_tilt", className="result-box"),
        html.Div(id="particle_output", className="result-box"),
    ], style={"maxWidth": "800px", "margin": "30px auto"}),
    
    html.H3("📊 Heatmaps", className="section-title", style={"marginTop": "50px"}),
    
    html.Div(className="graph-container", children=[
        dcc.Graph(id="heatmap_gravity_along")
    ]),
    
    html.Div(className="graph-container", children=[
        dcc.Graph(id="heatmap_gravity_perpendicular")
    ]),
    
    html.Div(className="graph-container", children=[
        dcc.Graph(id="heatmap_gravity_xz")
    ]),
    
], style={"textAlign": "center", "color": "white", "padding": "40px 20px", "maxWidth": "1400px", "margin": "0 auto"})

#math
math_layout= html.Div([
    html.H2("📐 Math Behind It All", className="section-title"),
    html.Div(
        dcc.Markdown(full_text, mathjax=True, className="markdown-content"),
        style={"maxWidth": "900px", "margin": "0 auto"}
    )
], style={"textAlign": "center", "color": "white", "padding": "40px 20px", "minHeight": "100vh"}) 


#--- Definition

def send_arduino(rpm, tilt, arduino_ip= ""): ##############################
    url= f"http://{arduino_ip}/set?rpm={rpm}&tilt={tilt}"
    try: 
        req= requests.get(url, timeout= 1)
        if req.status_code== 200:
            print(f"Arduino updated: RPM= {rpm} | Tilt= {tilt}")
        else: 
            print(f"Arduino error: {req.status_code}")
    except Exception as e:
        print(f"Failed to send to Arduino: {e}")

#--- Callback

#tab choice 
@app.callback(Output("tabs_content", "children"), Input("tab_ex", "value"))
def tab_choice(tab_type):
    if tab_type== "simulation_tab":
        return simulation_layout
    elif tab_type== "math_tab":
        return math_layout
    return app.layout


#input options
@app.callback(Output("conditional_inputs", "children"), Input("mode_selection", "value"))
def input_updates(selected_modes):
    inputs= []
    if  selected_modes== "rpm_n_tilt":
        inputs+= [
            dbc.Input(id= {"type": "dynamic_input", "index": "rpm"}, type= "number", placeholder= "Enter RPM", className="custom-input", style= {"maxWidth": "500px", "margin": "15px auto"}),
            dbc.Input(id= {"type": "dynamic_input", "index": "tilt"}, type= "number", placeholder= "Enter Tilt (deg)", className="custom-input", style= {"maxWidth": "500px", "margin": "15px auto"}),
        ]
    elif selected_modes== "gravity_intended": 
        inputs+= [
            dbc.Input(id= {"type": "dynamic_input", "index": "g_intended"}, type= "number", placeholder= "Enter the Intended Gravity", className="custom-input", style= {"maxWidth": "500px", "margin": "15px auto"}),
        ]
    return inputs

# particles
@app.callback(Output("particle_inputs", "children"), Input("particles", "value"))
def show_particle(particle_mode):
    if particle_mode== "on":
        particle_fields= [
            {"index": "initial_conc", "placeholder": "Initial Particle Concentration"},
            {"index": "particle_radius", "placeholder": "Particle Radius (m)"},
            {"index": "particle_density", "placeholder": "Particle Density"},
            {"index": "growth_rate", "placeholder": "Particle Growth Rate"},
            {"index": "fluid_density", "placeholder": "Fluid Density"},
            {"index": "fluid_viscosity_initial", "placeholder": "Initial Fluid Viscosity"},
            {"index": "duration", "placeholder": "Trial Duration"},
            {"index": "max_fraction", "placeholder": "Maximum Fraction"},
            {"index": "max_ss", "placeholder": "Maximum Shear Stress"},
            {"index": "d_radius", "placeholder": "Change of Radius for Falling Permitted"},
            {"index": "intrinsic_viscosity", "placeholder": "Intrinsic Viscosity"},
            {"index": "hindrance_exponent", "placeholder": "Hindrance Exponent"}
        ]

        inputs= []
        for f in particle_fields: 
            inputs.append(
                dbc.Input(id= {"type": "particle_input", "index": f["index"]}, type= "number", placeholder= f"Enter {f['placeholder']}", className="custom-input", style= {"maxWidth": "500px", "margin": "10px auto"})
            )
        return inputs
    else: 
        return []

#finding rpm and tilt and g_intend
@app.callback(
    Output("computed_g_intended", "children"),
    Output("computed_rpm_tilt", "children"),
    Output("particle_output", "children"),
    Output("heatmap_gravity_along", "figure"),
    Output("heatmap_gravity_perpendicular", "figure"),
    Output("heatmap_gravity_xz", "figure"),
    Input("run_button", "n_clicks"),
    State("mode_selection", "value"),
    State("particles", "value"),
    State("input_radius_bioreactor", "value"),
    State("zone_choice", "value"),
    State({"type": "dynamic_input", "index": ALL}, "value"),
    State({"type": "particle_input", "index": ALL}, "value")
)
def computed_values(
    n_clicks,
    mode,
    particle_mode,
    radius,
    zone_choice,
    dynamic_values,
    particle_values
):
    g_text= html.Div("⏳ Waiting for Input...", style={"color": "rgba(255, 255, 255, 0.6)", "fontSize": "1.1rem"})
    rpm_tilt_text= html.Div("⏳ Waiting for Input...", style={"color": "rgba(255, 255, 255, 0.6)", "fontSize": "1.1rem"})
    particle_text= html.Div("⏳ Waiting for Input...", style={"color": "rgba(255, 255, 255, 0.6)", "fontSize": "1.1rem"})
    empty_fig= go.Figure()

    if not n_clicks or not radius: 
        return g_text, rpm_tilt_text, particle_text, empty_fig, empty_fig, empty_fig

    rpm= None
    tilt= None
    g_intended= None

    g_along_2d= np.array([])
    g_perp_2d= np.array([])

    if mode== "rpm_n_tilt": 
        if len(dynamic_values)>= 2: 
            rpm= dynamic_values[0]
            tilt= dynamic_values[1]

            if rpm is not None and tilt is not None:
                (
                    g_intended,
                    _,
                    _,
                    _,
                    g_along_2d,
                    g_perp_2d,
                ) = gravity(radius, rpm, tilt, zone_choice)

                g_text= html.Div(f"✨ Calculated Intended Gravity: {g_intended: .2f} m/s²", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#a78bfa"})
                rpm_tilt_text= html.Div(f"⚙️ RPM: {rpm: .2f} rpm | Plane Tilt: {tilt: .2f}°", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#c4b5fd"})

    elif mode== "gravity_intended": 
        if len(dynamic_values)>= 1: 
            g_intended= dynamic_values[0]
            if g_intended is not None:
                rpm_chosen, tilt_chosen= gravity_to_rpm_n_tilt(radius, g_intended, zone_choice)
                g_text= html.Div(f"✨ Intended Gravity: {g_intended: .2f} m/s²", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#a78bfa"})
                rpm_tilt_text= html.Div(f"⚙️ Calculated RPM: {rpm_chosen: .2f} rpm | Tilt: {tilt_chosen: .2f}°", style={"fontSize": "1.2rem", "fontWeight": "600", "color": "#c4b5fd"})

                (
                    _,
                    _,
                    _,
                    _,
                    g_along_2d,
                    g_perp_2d,
                ) = gravity(radius, rpm_chosen, tilt_chosen, zone_choice)
    else:
        g_along_2d= np.array([])
        g_perp_2d= np.array([])

    # Particle calculations
    if particle_mode== "on": 
        if None in particle_values or len(particle_values)<12:
            particle_text= html.Div("⚠️ Please fill all the particle parameters.", style={"color": "#fbbf24", "fontSize": "1.1rem", "fontWeight": "600"})
        else: 
            (
                initial_conc,
                particle_radius,
                particle_density,
                growth_rate,
                fluid_density,
                fluid_viscosity_initial,
                duration,
                max_fraction,
                max_ss,
                d_radius,
                intrinsic_viscosity,
                hindrance_exponent,
            )= particle_values

            # Convert duration to array for time-dependent calculations
            time_array = np.array([duration])
            particle_conc= particle_concentration_time(initial_conc, growth_rate, duration)
            particle_frac_scalar= particle_fraction(particle_conc, particle_radius)
            # Convert to array for functions that expect arrays
            particle_frac= np.array([particle_frac_scalar])
            fluid_visc_array= fluid_viscosity_time(particle_frac, fluid_viscosity_initial, intrinsic_viscosity, max_fraction)
            # g_intended is needed for sedimentation_velocity - use calculated value if available
            g_for_sed = g_intended if g_intended is not None else 9.81
            sediment_vel_array= sedimentation_velocity(particle_density, fluid_density, particle_radius, particle_frac, fluid_visc_array, g_for_sed, hindrance_exponent)
            reynolds_array= reynolds_number(fluid_density, particle_radius, sediment_vel_array, fluid_visc_array)
            flow_array= flow_type(reynolds_array)
            # Extract scalar values for display
            flow = flow_array[0] if flow_array.size > 0 else "Unknown"
            # Convert single values to arrays for ang_linear_v_and_shear
            max_ss_array = np.array([max_ss])
            d_radius_array = np.array([d_radius])
            ang_vel, linear_vel, shear= ang_linear_v_and_shear(max_ss_array, fluid_visc_array, zone_choice, radius, d_radius_array)
            # Extract scalar values for display (first element of arrays)
            ang_vel = ang_vel[0, 0] if ang_vel.size > 0 else 0
            linear_vel = linear_vel[0, 0] if linear_vel.size > 0 else 0
            shear = shear[0, 0] if shear.size > 0 else 0
            # Extract scalar values for display
            fluid_visc = fluid_visc_array[0] if fluid_visc_array.size > 0 else 0
            sediment_vel = sediment_vel_array[0] if sediment_vel_array.size > 0 else 0
            reynolds = reynolds_array[0] if reynolds_array.size > 0 else 0
            particle_properties_result= particles_property(time_array, particle_radius, particle_density, initial_conc, growth_rate, fluid_density, fluid_viscosity_initial, intrinsic_viscosity, max_fraction, max_ss, g_for_sed, hindrance_exponent, radius, zone_choice, d_radius_array)

            particle_text= html.Div([
                html.Div(f"📊 Particle Concentration (time-dependent): {particle_conc:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"📈 Particle Fraction: {particle_frac_scalar:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"💧 Fluid Viscosity (time-dependent): {fluid_visc:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"⬇️ Sedimentation Velocity: {sediment_vel:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"🌀 Reynolds Number: {reynolds:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"🌊 Flow Type: {flow}", style={"marginBottom": "10px"}),
                html.Div(f"🔄 Angular Velocity: {ang_vel:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"⚡ Linear Velocity: {linear_vel:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"💨 Shear: {shear:.3f}", style={"marginBottom": "10px"}),
                html.Div(f"🔬 Particle Properties Result: {particle_properties_result}", style={"marginTop": "15px", "fontWeight": "600", "color": "#a78bfa"})
            ], style={"textAlign": "left", "fontSize": "1.05rem", "lineHeight": "1.8"})
    else: 
        particle_text= html.Div("🔴 Particle mode OFF.", style={"color": "rgba(255, 255, 255, 0.6)", "fontSize": "1.1rem"})

    # Generate heatmaps from 2D arrays or empty if no data
    if g_along_2d.size and g_perp_2d.size:
        
        fig_along = circular_heatmap(g_along_2d.T)
        fig_perp= circular_heatmap(g_perp_2d.T)
    else: 
        fig_along= empty_fig
        fig_perp= empty_fig

    fig_xz= empty_fig # Placeholder, can add later

    return g_text, rpm_tilt_text, particle_text, fig_along, fig_perp, fig_xz


if __name__== "__main__":
    app.run(debug= True)
