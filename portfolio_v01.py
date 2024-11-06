# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:56:13 2024

@author: amrit
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import numpy as np
from sklearn.neighbors import KernelDensity
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="App Portfolio - Amrit",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="auto"
)

common_css = """
<style>
/* Your common CSS styles here */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
/* Responsive adjustments */
@media (max-width: 768px) {
    /* Styles for smaller screens */
}
</style>
"""

intro_css="""
    <style>
    .intro-section {
        background-color: #f2f2f2;
        border-left: 4px solid #007bff;
        width: 70%;
        padding: 10px;
        margin: 10px auto;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
        font-style: italic;
    }

    .intro-section h2 {
        color: #333333;
        font-size: 24px;
        margin-bottom: 10px;
    }

    .intro-section p {
        color: #555555;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Media query for smaller screens */
    @media screen and (max-width: 768px) {
        .intro-section {
            padding: 5px; /* Smaller padding for smaller screens */
            font-size: 14px; /* Smaller font size */
        }

        .intro-section h2 {
            font-size: 20px; /* Smaller heading for smaller screens */
        }

        .intro-section p {
            font-size: 14px; /* Smaller paragraph font size */
        }
    }
</style>

    """

def create_section_intro(intro):
    return f"""
    <div class="intro-section"><p>{intro}</p></div>
    """

# CSS for the app card, image, text box, description, and collapsible section
app_card_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.app-card-container {
    border: 1px solid #ddd; /* Light border for card appearance */
    border-radius: 10px; /* Rounded corners */
    padding: 20px; /* Padding inside the card */
    margin: 20px auto; /* Margin for spacing between cards */
    max-width: 400px; /* Max width for the card */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Light shadow for depth */
    text-align: center; /* Center alignment for all content */
    background-color: #ffffff; /* White background for the card */
    display: flex; 
    flex-direction: column;
    align-items: center; /* Ensure all content is centered */
}

.solar-image-container {
    margin-top: 10px; /* Adjust this to position the image */
}

.solar-image {
    width: 80px; /* Adjust as needed */
    height: auto;
    transition: transform 0.3s ease;
}

.solar-image:hover {
    transform: translateY(-20px); /* Adjust the hover effect as needed */
}

.app-text-box {
    margin: 20px 0; /* Top and bottom margin for spacing */
    padding: 10px;
    background-color: var(--background-color); /* Dynamic background color */
    color: white; /* White text for contrast */
    border-radius: 10px; /* Rounded corners */
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow for depth */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    width: 70%;
}

.app-text-box:hover {
    transform: scale(1.05); /* Slight increase in size on hover */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Increased shadow on hover */
}

.app-name {
    font-size: 24px; /* Larger font size for the app name */
    font-weight: bold; /* Bold font for impact */
    margin: 10px 0; /* Spacing */
}

.app-description {
    margin: 10px 0; /* Spacing */
    font-size: 16px; /* Smaller font size for the description */
    color: #333; /* Darker gray text for the description */
    text-align: left; /* Align text to the left */
    width: 100%; /* Take up full width */
    font-family: Arial, sans-serif;
}

.app-link {
    margin-top: 10px; /* Spacing above the link */
    font-size: 16px;
    text-align: center; /* Center align the link */
    width: 100%;
}

.app-link a {
    color: #007bff; /* Blue color for links */
    text-decoration: none; /* Remove underline from links */
}

.app-link a:hover {
    text-decoration: underline; /* Underline on hover */
}

.collapsible {
    width: 100%; /* Take up full width */
    margin-top: 10px; /* Spacing above collapsible */
    text-align: left; /* Align text to the left */
}

.collapsible summary {
    font-size: 16px; /* Font size for the summary */
    font-weight: bold; /* Bold font for the summary */
    cursor: pointer; /* Pointer cursor on hover */
    margin-bottom: 10px; /* Spacing */
    font-family: 'Roboto', sans-serif; /* Use Roboto font */
}

.collapsible summary::-webkit-details-marker {
    display: none; /* Hide the default triangle */
}

.collapsible-content {
    font-size: 14px; /* Smaller font size for the content */
    color: #555; /* Darker gray text */
    margin-top: 10px; /* Spacing */
    font-family: 'Roboto', sans-serif; /* Use Roboto font */
    line-height: 1.6; /* Increased line height for better readability */
}
</style>
"""



# Function to display a complete app card with a collapsible section
def display_app_card(icon_path, app_name, app_description, background_color, app_url, key_features, unique_id):
    app_card_html = f"""
    <div class="app-card-container">
        <div class="solar-image-container">
            <img class="solar-image" src="{icon_path}" alt="App Icon">
        </div>
        <div class="app-text-box" style="--background-color: {background_color};">
            <div class="app-name">{app_name}</div>
        </div>
        <div class="app-description">
            {app_description}
        </div>
        <div class="app-link">
            <a href="{app_url}" target="_blank">Visit App Website</a>
        </div>
        <div class="collapsible">
            <details>
                <summary>Key Features</summary>
                <div class="collapsible-content">
                    {key_features}
                </div>
            </details>
        </div>
    </div>
    """
    components.html(app_card_css + app_card_html, height=500)  # Remove fixed height to make it responsive

# Streamlit app layout
st.title("Welcome to My App Portfolio Page")


col1,col2=st.columns(2)
# Display each app as a card with an icon, text box, description, website link, and collapsible section
with col1:
    display_app_card(
        "https://i.imgur.com/kescOjS.png", 
        "Solar Energy Estimator", 
        "Estimates solar energy production based on user inputs and location data.", 
        "#007bff", 
        "https://solarenergyestimatorv01.streamlit.app/", 
        "<ul><li>Get hourly, daily, and monthly solar energy metrics</li><li>Plot and download charts</li><li>Generate white-label PDF reports (Coming Soon)</li></ul>", 
        "1"
    )

with col2:
    display_app_card(
        "https://i.imgur.com/ElycPbr.png", 
        "Energy EDA Dashboard", 
        "An interactive dashboard for exploratory data analysis in the energy sector.", 
        "#28a745", 
        "https://energy-eda-v01.streamlit.app/", 
        "<ul><li>Pre-process and clean hourly energy data</li><li>Visualize key charts and metrics</li><li>Analyze solar PV potential and energy consumption vs. solar yield</li><li>Export white-label PDF reports and CSV datasets</li></ul>", 
        "2"
    )

with col1:
    display_app_card(
        "https://i.imgur.com/xtRdMB2.png", 
        "LinkCraft", 
        "AI-powered app to generate LinkedIn and social media content based on trending global news and topics.", 
        "#7F7FD5", 
        "https://linkcraft-v01.streamlit.app/", 
        "<ul><li>Get trending global news from the past week</li><li>Generate content based on mood and tone</li><li>Casual writing with emojis, sharable on social media</li><li>Get image prompts for post thumbnails</li></ul>", 
        "3"
    )


with col2:
    display_app_card(
        "https://i.imgur.com/p4GrSw9.png", 
        "AI HR Assistant App", 
        "An AI-powered assistant for streamlining HR tasks and queries.",
        "#FFC300", 
        "https://ai-hr-assist.streamlit.app/", 
       "<ul><li>Analyze CVs based on job descriptions and skill sets</li><li>Supports PDF CVs, cover letters, and form-based inputs</li><li>Generate comparison tables between profiles and candidate details</li></ul>", 
       "4"
    )
    




with col1:
    display_app_card(
        "https://i.imgur.com/R8j2aiq.png", 
        "Solar Finance Modeler", 
        "Models the financial performance of solar PV projects with key metrics.", 
        "#FF6B6B", 
        "https://solarfinc-v01.streamlit.app/", 
        "<ul><li>Financial analysis: IRR, payback, ROI, NPV, and cashflow</li><li>Environmental impact metrics like CO2 offset etc.</li><li>Dynamic visualizations and reporting</li><li>White-labeled PDF reports</li></ul>", 
        "5"
    )



with col2:
    display_app_card(
        "https://i.imgur.com/RdEBtpc.png", 
        "Solar Project Manager", 
        "Simplifies the process of submitting and managing solar PV project inquiries.", 
        "#17a2b8", 
        "https://amritpvre-solar-query-form-solar-inquery-v02-w0jlqr.streamlit.app/", 
        "<ul><li>Comprehensive Project Inquiry Form</li><li>Interactive Map Integration</li><li>Automated Data Collection and Emailing</li><li>Customizable Inputs for Different Project Types</li></ul>", 
        "6"
    )
    
    
with col1:
    display_app_card(
        "https://i.imgur.com/iy6N1L9.png", 
        "NSE Live Stock Monitor", 
        "Tracks and displays live stock prices from the NSE with real-time updates.", 
        "#28a745", 
        "https://yflivetracker-nse.streamlit.app/", 
        "<ul><li>Real-Time Stock Price Monitoring</li><li>Interactive Candlestick Charting</li><li>Customizable Stock Selection</li><li>Data Display and Analysis</li></ul>", 
        "7"
    )


with col2:
    display_app_card(
        "https://i.imgur.com/WlEXIOG.png", 
        "Solar GHI-GII Forecaster", 
        "Provides sub-hourly forecasts for global horizontal and global inclined irradiance.", 
        "#ff5733", 
        "https://amritpvre-hourly-ghi-sub-hourly-ghi-gii-forecast-app-v01-ubmari.streamlit.app/", 
        "<ul><li>Precise Sub-Hourly Solar Irradiance Forecasting</li><li>Customizable Geographical Inputs</li><li>Seasonal Comparison and Data Visualization</li><li>Downloadable Forecast Data</li></ul>", 
        "8"
    )


st.write('\n')
st.write("--------------")

st.title("About me:")

#-----Section Header CSS--------#

# CSS for the entire app
app_css = """
<style>
    .section-header {
        position: relative; /* Required for positioning the pseudo-elements */
        padding: 10px 20px;
        margin: 20px auto;
        background-color: #f9f9f9;
        color: #333333;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 22px;
        font-weight: bold;
        font-style: italic;
        border-left: 4px solid #007bff;
        border-right: 4px solid #007bff;
        transition: background-color 0.3s ease, border-color 0.3s ease;
        width: 80%;
        align: center;
    }
    .section-header:hover {
        background-color: #e9ecef;
        border-color: #0056b3;
        cursor: pointer;
    }

    /* Responsive adjustments */
@media (max-width: 768px) {{
    .header-card {{
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}

    /* Pseudo-elements for horizontal lines */
    .section-header:before, .section-header:after {
        content: '';
        position: absolute;
        top: 50%;
        width: 30%; /* Width of the lines */
        height: 0px; /* Thickness of the lines */
        background-color: #333333; /* Color of the lines */
        transform: translateY(-50%);
    }
    .section-header:before {
        left: 5%; /* Positioning the left line */
    }
    .section-header:after {
        right: 5%; /* Positioning the right line */
    }
</style>
"""

# Function to create HTML for section headers
def create_section_header(title):
    return f"""
    <div class="section-header">{title}</div>
    """

#------End of Section Header CSS-----#

#-----Header section-------#

# Function to encode image file to base64
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# Image path
image_path = 'profile_pic.png'  # Replace with your image file path
image_base64 = get_image_as_base64(image_path)

# HTML and CSS
header_html = f"""
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
.header-card {{
    padding: 20px;
    display: flex;
    align-items: center;
    background-color: #ffffff; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 15px;
    width: 50%;
    margin: 10px auto;
    transition: transform 0.3s, box-shadow 0.3s;
}}

.header-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}}

.profile-image {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background-image: url("{image_base64}");
    background-size: cover;
    margin-right: 20px;
}}

.profile-text {{
    font-family: 'Open Sans', sans-serif;
    font-size: 22px;
    color: #333333;
}}

.catchy-text {{
    font-family: 'Open Sans', sans-serif;
    font-size: 16px;
    color: #666666;
    margin-top: 5px;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .header-card {{
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}
    .profile-image {{
        margin-bottom: 10px;
        margin-right: 0;
        width: 100px; /* Smaller image */
        height: 100px;
    }}
    .profile-text {{
        font-size: 18px; /* Smaller text */
    }}
    .catchy-text {{
        font-size: 14px;
    }}
}}
</style>

<div class="header-card">
    <div class="profile-image"></div>
    <div>
        <div class="profile-text">Amrit Mandal</div>
        <div class="profile-text">Transformative Renewable Energy Manager</div>
        <div class="catchy-text">Driving Global Solar Projects with Cutting-Edge Innovations</div>
        <div class="catchy-text">PV | BESS | AI | ML</div>
    </div>
</div>
"""

# Render the custom HTML/CSS in the Streamlit app
components.html(header_html, height=300)

components.html(app_css + create_section_header("Global Impacts"), height=100)


#-----MW of Projects Done-------#


# CSS for the image
image_css = """
<style>
.solar-image-container {
    text-align: center;
    margin-top: 40px; /* Adjust this to position the image */
}

.solar-image {
    width: 80px; /* Adjust as needed */
    height: auto;
    transition: transform 0.3s ease;
}

.solar-image:hover {
    transform: translateY(-20px); /* Adjust the hover effect as needed */
}
</style>
"""

# HTML for the image
image_html = """
<div class="solar-image-container">
    <img class="solar-image" src="https://i.imgur.com/kescOjS.png" alt="Sun and Solar Array">
</div>
"""

# Display the image in Streamlit
components.html(image_css + image_html, height=120) # Adjust the height as needed

# CSS for the text box
text_box_css = """
<style>
.mw-showcase {
    align:center;
    text-align: center;
    margin: 10px auto; /* Top and bottom margin 20px, left and right auto for centering */
    padding: 10px;
    background-color: #007bff; /* Blue background for emphasis */
    color: white; /* White text for contrast */
    border-radius: 7px; /* Rounded corners */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow for depth */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    max-width: 55%; /* Adjust this value to set your desired width */
    font-family: Arial, sans-serif;
}

.mw-showcase:hover {
    transform: scale(1.05); /* Slight increase in size on hover */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Increased shadow on hover */
}

.mw-value {
    font-size: 36px; /* Large font size for the MW value */
    font-weight: bold; /* Bold font for impact */
    margin: 10px 0; /* Spacing */
}

.mw-description {
    font-size: 18px; /* Smaller font size for the description */
}
</style>
"""

# HTML for the text box
text_box_html = """
<div class="mw-showcase">
    <div class="mw-value">2.6 GWp</div>
    <div class="mw-description">Solar PV Projects Managed since 2013</div>
</div>
"""

# Display the text box in Streamlit
components.html(text_box_css + text_box_html, height=130) # Adjust the height as needed
    

#-----End of MW of Projects Done-------#

#-----Investments Managed------#
# Total cumulative investment and max value for the gauge
total_investment = 289.3  # in million USD
max_gauge_value = 500.0  # Max value of the gauge in million USD

# Custom HTML and JavaScript for the modified gauge chart
gauge_chart_html = f"""
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://bernii.github.io/gauge.js/dist/gauge.min.js"></script>
<style>
/* Card container */
.card {{
  border: 1px solid #dfdfdf;
  border-radius: 7px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 10px auto;
  width:50%;
  transition: box-shadow 0.3s ease-in-out;
  font-family: Arial, sans-serif;
}}
.card:hover {{
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}}

/* Gauge container */
#gauge-container {{
  position: relative;
  width: auto; /* Adjust as needed */
  height: auto; /* Adjust as needed */
  text-align: center; /* Center the canvas */
}}
    


/* Investment text beneath the gauge */
#investment-text {{
  font-size: 18px;
  margin-top: 15px; /* Space above the text */
  color: #333;
  text-align:center;
  font-weight: bold; /* Make text bold */
}}

/* Hover effect for gauge needle */
#gauge canvas {{
  cursor: pointer;
}}
#gauge canvas:hover {{
  opacity: 0.8;
}}

</style>
</head>
<body>

<div class="card">
  <div id="gauge-container">
    <canvas id="gauge" width="400" height="200"></canvas>
  </div>
  <div id="investment-text">Total Investments Managed: ${total_investment}M</div>
</div>

<script>
// JavaScript to initialize the gauge and handle hover effect
var gaugeValue = {total_investment}; // The value to display on the gauge

var opts = {{
  angle: 0, // The span of the gauge arc
  lineWidth: 0.2, // The line thickness, reduced from 0.44 to 0.2
  radiusScale: 1, // Relative radius
  pointer: {{
    length: 0.6, // Relative to gauge radius
    strokeWidth: 0.035, // The thickness
    color: '#000000' // Fill color
  }},
  limitMax: false,     // If false, max value will be higher if needed
  limitMin: false,     // If true, min value will be 0
  colorStart: '#6FADCF',   // Colors
  colorStop: '#8FC0DA',    // Just experiment with them
  strokeColor: '#E0E0E0',  // To see which ones work best for you
  generateGradient: true,
  highDpiSupport: true,     // High resolution support
staticZones: [
     {{strokeStyle: "#F03E3E", min: 0, max: {max_gauge_value} * 0.25}}, // Red from 0 to 25%
     {{strokeStyle: "#FFDD00", min: {max_gauge_value} * 0.25, max: {max_gauge_value} * 0.75}}, // Yellow from 25% to 75%
     {{strokeStyle: "#30B32D", min: {max_gauge_value} * 0.75, max: {max_gauge_value}}}, // Green from 75% to 100%
  ],
  staticLabels: {{
    font: "10px sans-serif",  // Specifies font
    labels: [0, {max_gauge_value} * 0.25, {max_gauge_value} * 0.5, {max_gauge_value} * 0.75, {max_gauge_value}],  // Print labels at these values
    labelsCount: 5,
    color: "#000000",  // Optional: Label text color
    fractionDigits: 0  // Optional: Numerical precision. 0=round off.
  }},
}};


var target = document.getElementById('gauge');
var gauge = new Gauge(target).setOptions(opts); // Create gauge
gauge.maxValue = 500; // Max value for the gauge
gauge.setMinValue(0);  // Min value for the gauge
gauge.animationSpeed = 32; // Animation speed
gauge.set(gaugeValue); // Set the current value
</script>
</body>
</html>
"""

# Use Streamlit components to embed the HTML/JavaScript in the app

gauge_chart_fin=gauge_chart_html+common_css
components.html(gauge_chart_fin, height=300)
    #st.markdown(gauge_chart_html, unsafe_allow_html=True)
    

#------End of Impact Section------#

#--------Projects Done Map------#
projectmap_intro=f"""Spanning the globe from the bustling streets of India to the expansive landscapes of Australia and beyond,
 my portfolio illuminates the breadth of my solar energy projects. With over 200MW managed in Tamilnadu, 
 a 140MW design in Iran, and innovative community projects in Nepal, 
 the map traces a story of sustainable impact and technical prowess in renewable energy solutions.

"""
components.html(app_css + create_section_header("Global Project Portfolio"), height=100)
components.html(intro_css + create_section_intro(projectmap_intro)
                                                 , height=200)




# Sample data with an additional 'brief' column for the tooltip
data = {
    "latitude": [
        22.3511148, 36.7014631, 27.7567667, 31.2638905, 13.4499943, -31.8759835, 24.638916, 24.0002488, 
        23.5882019, 23.7644025, -26.205, 9.6000359, -2.9814344, -1.9646631, 11.8145966, 32.6707877, 
        -10.3333333, 13.1500331, 10.9094334, 23.8143419, 26.8105777, 22.3850051, 22.9964948, 23.4559809, 
        15.9240905, 10.3528744, 14.5203896, 27.1303344, 18.9068356, 31.2496266
    ],
    "longitude": [
        78.6677428, -118.755997, -81.4639835, -98.5456116, 144.7651677, 147.2869493, 46.7160104, 53.9994829, 
        58.3829448, 90.389015, 28.049722, 7.9999721, 23.8222636, 30.0644358, 42.8453061, 51.6650002, 
        -53.2, -59.5250305, 78.3665347, 77.5340719, 73.7684549, 71.745261, 87.6855882, 85.2557301, 
        80.1863809, 76.5120396, 75.7223521, 80.859666, 75.6741579, 73.6632218
    ],
    "location": [
        "India", "California, USA", "Florida, USA", "Texas, USA", "Guam, USA", "NSW, Australia", 
        "Saudi Arabia", "UAE", "Oman", "Bangladesh", "South africa", "Nigeria", "congo", "rwanda", 
        "djibouti", "isfahan, iran", "brazil", "Barbados", "Tamilnadu", "Madhya Pradesh", 
        "Rajasthan", "Gujarat", "West Bengal", "Jharkhand", "Andhra Pradesh", "Kerala", "Karnataka", 
        "Uttar pradesh", "Maharastra", "Nepal"
    ],
    "brief": [
        "4MW,Consulted & Managed", "2MW,Consulted", "10MW+,Designed", "2MW,Designed & Consulted", 
        "3MW+,Designed", "1MW+,Consulted", "~0.5MW,Designed & Consulted", "~0.5MW,Designed & Consulted", 
        "10MW+,Managed", "1MW,Consulted", "40MW,Designed & Consulted", "PV MFG,Consulted", ",Consulted", 
        "1MW+,Consulted", "50MW+,Designed & Consulted", "140MW,Designed & Consulted", 
        "~0.5MW,Designed & Consulted", "~0.5MW,Designed & Consulted", "200MW+,Managed", 
        "75MW,Managed & Consulted", "100MW+,Managed & Consulted", "20MW,Designed & Consulted", 
        "~1MW,Managed", "MiniGrid Project,Managed", "20MW,Managed", "20MW,Designed & Consulted", 
        "~25MW,Managed", "2MW,Managed & Consulted", "~80MW,Managed & Consulted", "Pilot Community project,Consulted"
    ]
}

df = pd.DataFrame(data)



# Assuming df is your DataFrame with the latitude and longitude
coords = df[['latitude', 'longitude']]

# Use Kernel Density Estimation to estimate the density at each point
kde = KernelDensity(bandwidth=1.0, metric='haversine')
kde.fit(np.radians(coords))

# Evaluate the densities on the same points
scores = np.exp(kde.score_samples(np.radians(coords)))

# Normalize the scores to a scale that makes sense for your dot sizes
# We invert the scores because a high density should give a smaller size
max_radius = 500000  # adjust this to your needs
min_radius = 200000  # adjust this to your needs
df['radius'] = max_radius - scores / max(scores) * (max_radius - min_radius)


# Define the tooltip text
tooltip = {
    "html": "<b>{location}</b><br><b>{brief}</b>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Set the viewport location
view_state = pdk.ViewState(latitude=df["latitude"].mean(), longitude=df["longitude"].mean(), zoom=1, pitch=0)

# Use the radius column for the 'get_radius' attribute in your pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"],
    get_color="[180, 0, 200, 140]",  # Custom color
    get_radius="radius",  # Use the new radius column
    pickable=True  # Needed for the tooltip to work
)

# Render the map with the custom style
col1,col2,col3=st.columns([0.25,2.50,0.25])
col2.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',  # Here you can choose other styles like 'light-v9' or 'outdoors-v11'
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip  # Adding the tooltip here
))

#------End of Project Map-------#
#------software skills-------#
sw_intro=f""" Below are visual representations of my skills across various technical tools, 
illustrated through a horizontal bar chart and a radar chart. 
These charts reflect my expertise and proficiency levels in essential software tools like 
PVsyst, AutoCAD, SketchUp, and more, highlighting my comprehensive skill set in the Solar energy sector.
"""
components.html(app_css + create_section_header("Software Skills Proficiency"), height=100)
components.html(intro_css + create_section_intro(sw_intro)
                                                 , height=150)
#----radar chart w/o prfecieny level and with logos------#



# Function to encode image file to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Skills to display and their corresponding image file names
skills = ['PVsyst', 'AutoCAD', 'SketchUp', 'Helioscope', 'Python', 'pvlib']
# Assume the image names are the same as the skill names
image_folder = 'images'

# Create the radar chart
fig = go.Figure()

# Add radar chart trace
fig.add_trace(go.Scatterpolar(
    r=[1] * len(skills),  # Set a fixed radius for all skills
    theta=skills,
    fill='toself',
    fillcolor='rgba(135, 206, 250, 0.7)',  # Light blue with 70% opacity
    line_color='blue',  # Solid blue line color
    showlegend=False
))

# Calculate angle and radius for logo placement
angles = np.linspace(0, 2 * np.pi, len(skills), endpoint=False).tolist()  # Divide the circle into equal parts
angles += angles[:1]  # Ensure the list is cyclic
radius = 1.1  # Radius where logos will be placed

# Add logos as annotations
for skill, angle in zip(skills, angles):
    logo_path = os.path.join(image_folder, skill + '.png')
    if os.path.isfile(logo_path):
        encoded_image = encode_image(logo_path)
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{encoded_image}",
                xref="paper", yref="paper",
                x=0.5 + radius * np.cos(angle) / 3,
                y=0.5 + radius * np.sin(angle) / 2,
                sizex=0.2,  # Adjust based on the chart size and image resolution
                sizey=0.2,  # Adjust based on the chart size and image resolution
                xanchor="center",
                yanchor="middle",
                layer="above"
            )
        )
    else:
        st.error(f"Image for {skill} not found at path: {logo_path}")

# Update the layout to show the radial axis
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,  # Show the radial axis
            range=[0, 1],  # The range of your scale
        ),
        angularaxis=dict(
            tickfont=dict(
                color='white'  # Set the text color for software names to white
            ),
        )
    ),
    title=" ",
)

# Display the radar chart in Streamlit
col1, col2=st.columns(2)
col1.plotly_chart(fig, use_container_width=True)

#----------#

import plotly.express as px

# Define your skills and proficiency levels
skills_data = {
    'skills': ['PVsyst', 'AutoCAD', 'SketchUp', 'Helioscope', 'Python', 'PVlib'],
    'proficiency': [90, 80, 85, 95, 75, 65]  # Proficiency levels out of 100
}

# Create a DataFrame
df_skills = pd.DataFrame(skills_data)

# Define a list of colors for the bars
colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3']

# Create a horizontal bar chart with different colors
fig = px.bar(df_skills, x='proficiency', y='skills', orientation='h',
             color='skills', color_discrete_sequence=colors)
fig.update_layout(
    autosize=True,
width=None, # It will be set automatically to page width
xaxis=dict(
title='Proficiency Level',
range=[0, 100] # Define the range of proficiency levels
    ),
    yaxis=dict(
        title='Skills'
    ),
    title=" ", showlegend=False
)

# Display the horizontal bar chart in Streamlit
col2.plotly_chart(fig, use_container_width=True)

#----------#

#-------Wordcloud Matplotlib-------#
components.html(app_css + create_section_header("Management Skillset"), height=100)


# List of managerial skills, you can add more words or increase the frequency of the words to emphasize them
managerial_skills = [
    "Leadership", "Teamwork", "Communication", "Strategic Planning",
    "Project Management", "Budgeting", "Negotiation", "Conflict Resolution",
    "Decision Making", "Risk Management", "Time Management", "Adaptability",
    "Problem Solving", "Motivation", "Coaching", "Mentoring",
    "Crisis Management", "Organization", "Delegation", "Innovation"
]

# Generate the word cloud text as repeated instances of the skills
text = ' '.join(managerial_skills)

# Create the word cloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the generated image:
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)


def display_skill_info(skill_name, description):
    # Toggle button to show/hide skill information
    if st.button(skill_name, key=skill_name):
        st.info(description)

# Styling for the cards
st.markdown("""
    <style>
        .css-2trqyj {
            background-color: #f1f1f1;  /* Light grey background */
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .stButton>button {
            width: 100%;
            height: 3em;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            border: 1px solid #007BFF;
            color: #007BFF;
        }
    </style>
""", unsafe_allow_html=True)

# Display each skill as a clickable card
col1,col2=st.columns(2)

with col1:
    display_skill_info("Leadership", "Spearheaded diverse solar projects, leading a team of engineers through the successful completion of the groundbreaking PDO Noor project.")
with col2:
    display_skill_info("Project Management", "Expertly managed large-scale solar installations including a 5MW Smart City project for PDO.")
with col1:
    display_skill_info("Strategic Planning", "Devised and implemented strategic plans for the deployment of innovative solar solutions, notably in the 4MW+ mall rooftop projects for MAF.")
with col2:
    display_skill_info("Decision Making", "Efficiently made key decisions during the development of Battery Energy Storage Systems and electric vehicle charging infrastructures.")
with col1:
    display_skill_info("Risk Management", "Identified and mitigated project risks in high-stakes environments, ensuring the seamless execution of complex solar projects.")
with col2:  
    display_skill_info("Time Management", "Expertly managed project timelines, ensuring timely completion of solar installations like the 5MW Smart City project for PDO.")

#--------#

#-----Academic Qualification-----------#

edu_intro=f"""Thanks for scolling this far! I'm an Electrical Engineer with a lifelong commitment to learning.
 My postgraduate endeavors and certifications include advanced solar energy studies from TU Delft,
 business management from IIM Bangalore, financial modeling from Wharton, and data science from Harvard X. 
 These courses have equipped me with a robust foundation to excel in the renewable energy sector.
"""
components.html(app_css + create_section_header("Academic Qualification & Certifications"), height=100)
components.html(intro_css + create_section_intro(edu_intro)
                                                 , height=200)



education_html = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.education-section {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    margin-bottom: 20px;
}

.education-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    margin: 20px;
    overflow: hidden;
    width: 300px; /* Width of the card */
    display: flex; /* Added for flexbox layout */
    flex-direction: column; /* Stack children vertically */
    align-items: center; /* Center children horizontally */
    text-align: center; /* Center text */
    font-family: 'Roboto', sans-serif;
}

    .education-card img {
    max-width: calc(150px - 20px); /* Subtracting the total padding from the width */
    height: 150px; /* Maintain aspect ratio */
    object-fit: contain;
    padding: 10px; /* Padding around the image */
    }
    
    .card-content {
    padding: 15px;
    }
    
    .card-content h4 {
    margin-top: 0;
    color: #333;
    font-weight: 700; /* Roboto bold for headers */
    }
    
    .card-content p {
    color: #666;
    font-weight: 400; /* Roboto regular for paragraphs */
    }
    </style>
    
    <div class="education-section">
        <div class="education-card">
            <img src="https://i.imgur.com/8oLnZZt.png" alt="College Image">
            <div class="card-content">
                <h4>B.Tech in Electrical Engineering</h4>
                <p>West Bengal University of Technology, 2009-2013</p>
            </div>
        </div>
        <div class="
    education-card">
    <img src="https://i.imgur.com/o2BAJZl.png" alt="Certification Image">
    <div class="card-content">
    <h4>Certificate-Advanced Solar Energy</h4>
    <p>TU Delft (Online), 2013</p>
    </div>
    </div>
    
    <div class="
    education-card">
    <img src="https://i.imgur.com/o1Nu9QD.png" alt="Certification Image">
    <div class="card-content">
    <h4>Micro Masters in General Business Management</h4>
    <p>IIM Bangalore, 2017 - 2018</p>
    </div>
    </div>
    
    <div class="
    education-card">
    <img src="https://i.imgur.com/WzpTJib.jpg" alt="Certification Image">
    <div class="card-content">
    <h4>Certificate in Financial Modelling</h4>
    <p>Wharton Business School, 2017 - 2018</p>
    </div>
    </div>
    
    <div class="
    education-card">
    <img src="https://i.imgur.com/o7DVF65.png" alt="Certification Image">
    <div class="card-content">
    <h4>Certificate- Data Science using R</h4>
    <p>Harvard T. Chan School of Public Health, 2018</p>
    </div>
    </div>
    
    <div class="
    education-card">
    <img src="https://i.imgur.com/W8Hu1iN.jpg" alt="Certification Image">
    <div class="card-content">
    <h4>Certificate-Data Analysis & Visualization</h4>
    <p>PwC Academy (Online), 2017-2018</p>
    </div>
    </div>
    
    <!-- Add more cards as needed -->
    
    </div>
    <script>
    function sendHeightToParent() {
        // Send the current height of the body to the parent window
        window.parent.postMessage({
            'frameHeight': document.body.scrollHeight
        }, '*');
    }

    // Call the function on load and on resize
    window.onload = sendHeightToParent;
    window.onresize = sendHeightToParent;
    </script>
    
    
"""


# Render the custom HTML/CSS in the Streamlit app
components.html(education_html, height=800)
