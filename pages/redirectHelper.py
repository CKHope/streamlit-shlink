import streamlit as st
import requests

def get_shlink_domains(mainDomain,api_token):
  """
  This function retrieves the list of used domains from the Shlink.io API.

  Args:
      api_token (str): Your Shlink.io API access token.

  Returns:
      list: A list of used domain names if successful, otherwise None.
  """

  # Base URL for the API endpoint
  base_url = f'https://{mainDomain}/rest/v3/domains'

  # Headers with your access token
  headers = {"Authorization": f"Bearer {api_token}"}

  try:
    # Send GET request to list domains
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Raise error for non-2xx status codes

    # Parse JSON response
    data = response.json()

    # Extract list of domains used for short URLs
    used_domains = [domain["domain"] for domain in data["domains"] if domain["usedForShortUrls"]]

    return used_domains

  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return None

st.title("Shlink.io Used Domain Checker")

# Input field for API token
api_token = st.text_input("Enter your Shlink.io API Token:")

# Submit button
if st.button("Get Used Domains"):
  # Call function to retrieve domains
  used_domains = get_shlink_domains(api_token)

  if used_domains:
    st.success("**Used Domains:**")
    for domain in used_domains:
      st.write(domain)
  else:
    st.error("Failed to retrieve domains. Check your API token or try again later.")

