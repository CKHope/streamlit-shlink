import streamlit as st
import requests

def update_redirects(api_key, domain, regular_redirect, invalid_redirect):
    url = f"https://{domain}/rest/v3/domains/redirects"
    headers = {
        "accept": "application/json",
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "domain": domain,
        "regular404Redirect": regular_redirect,
        "invalidShortUrlRedirect": invalid_redirect
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        st.success("Redirects updated successfully.")
    else:
        st.error(f"Error: {response.status_code}")

def main():
    st.title("Redirects Updater")
    domain = st.text_input("Enter the domain:", value="6886889.xyz")
    api_key = st.text_input("Enter your API key:")
    regular_redirect = st.text_input("Enter the regular redirect URL:", value="https://6886889.xyz/68")
    invalid_redirect = st.text_input("Enter the invalid redirect URL:", value="https://6886889.xyz/68")

    if st.button("Update Redirects"):
        if api_key and domain and regular_redirect and invalid_redirect:
            update_redirects(api_key, domain, regular_redirect, invalid_redirect)
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
