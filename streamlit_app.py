import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_and_plot_ratings(url):
  """Fetches chess rating data from URL, creates DataFrame, and plots it."""
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  table = soup.find('table', class_ = "profile-table profile-table_chart-table")

  # Handle potential errors if table not found
  if not table:
      st.error("Error: Couldn't find ratings table on the given URL.")
      return

  df = pd.read_html(StringIO(str(table)))[0]
  df = df.fillna(0)

  ratings = df["RTNG"]
  dates = df["Period"]

  # Convert dates to datetime objects for plotting on x-axis
  date_objects = [datetime.strptime(date, "%Y-%b") for date in dates]

  # Plot ratings vs dates
  plt.figure(figsize=(10, 6))  # Adjust figure size for better visuals
  plt.plot(date_objects, ratings)

  # Label the axes
  plt.xlabel("Date")
  plt.ylabel("Chess Rating")

  # Add a title
  plt.title("Chess Rating Progress Over Time")

  # Rotate x-axis labels for better readability if many dates
  plt.xticks(rotation=45)

  # Display the plot within Streamlit
  st.pyplot()

st.title("Chess Rating Tracker")

# Input field for the FIDE profile URL
url = st.text_input("Enter FIDE Profile URL:", "https://ratings.fide.com/profile/1503014/chart")

# Button to trigger data fetching and plotting
if st.button("Visualize Ratings"):
  fetch_and_plot_ratings(url)


