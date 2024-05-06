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
        return response.json()["domains"]["data"]
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
                configured_domains = []
                domains_without_redirects = []

                for domain_info in domains_data:
                    domain = domain_info["domain"]
                    redirects = domain_info["redirects"]
                    if redirects.get("regular404Redirect") or redirects.get("invalidShortUrlRedirect"):
                        configured_domains.append(domain)
                    else:
                        domains_without_redirects.append(domain)

                st.session_state.domains_without_redirects = domains_without_redirects

                st.write("Domains with configured redirects:")
                st.write(configured_domains)

                st.write("Domains without configured redirects:")
                st.write(domains_without_redirects)

        else:
            st.error("Please enter your API key.")

if __name__ == "__main__":
    main()
