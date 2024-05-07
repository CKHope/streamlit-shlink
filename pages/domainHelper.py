import streamlit as st
import requests

def get_domain_names(api_key, secret_api_key):
    url = "https://porkbun.com/api/json/v3/domain/listAll"
    payload = {
        "secretapikey": secret_api_key,
        "apikey": api_key
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "SUCCESS":
            domains = [domain_info["domain"] for domain_info in data.get("domains", [])]
            return domains
        else:
            st.error("Failed to fetch domain names. Please check your API keys.")
    else:
        st.error(f"Failed to fetch domain names. Status code: {response.status_code}")

def main():
    st.title("Porkbun Domain List")
    
    # Input fields for API keys
    api_key = st.text_input("Enter your API key:")
    secret_api_key = st.text_input("Enter your secret API key:")

    if st.button("Fetch Domain Names"):
        if api_key and secret_api_key:
            domains = get_domain_names(api_key, secret_api_key)
            if domains:
                st.text_area("Domain Names", "\n".join(domains))
        else:
            st.error("Please enter both API key and secret API key.")

if __name__ == "__main__":
    main()
