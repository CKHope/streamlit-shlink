import streamlit as st
import requests

def get_domains(api_key):
    url = "https://6886889.xyz/rest/v3/domains"
    headers = {
        "accept": "application/json",
        "X-Api-Key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None

def main():
    st.title("Domain Data Viewer")
    api_key = st.text_input("Enter your API key:")
    if st.button("Get Domains"):
        if api_key:
            domains_data = get_domains(api_key)
            if domains_data:
                st.write("Domain Data:")
                st.write(domains_data)
        else:
            st.error("Please enter your API key.")

if __name__ == "__main__":
    main()
