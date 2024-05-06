import streamlit as st
import requests

def shorten_url(api_key, long_url, tag, crawlable, forward_query, slug="0", short_code_length=6, domain='', main_domain='6886889.xyz'):
    url = f'https://{main_domain}/rest/v3/short-urls'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'longUrl': long_url,
        'tags': [tag],
        'crawlable': crawlable,
        'forwardQuery': forward_query,
        'shortCodeLength': short_code_length,
        'slug': slug,
        'domain': domain,
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['shortUrl']
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("URL Shortener")

    # Input fields
    api_key = st.text_input("Enter your Shlink API key:")
    long_url = st.text_input("Enter the long URL:")
    domain_text = st.text_area("Enter the list of domains (one domain per line):")

    if st.button("Shorten URL"):
        if api_key and long_url and domain_text:
            tag = "initDomain"
            crawlable = False  # You can customize this if needed
            forward_query = False  # You can customize this if needed

            # Split domain text area by lines and remove empty lines
            domains = [domain.strip() for domain in domain_text.split("\n") if domain.strip()]

            # Process short links for each domain
            short_links = {}
            for domain in domains:
                short_link = shorten_url(api_key, long_url, tag, crawlable, forward_query, domain=domain)
                short_links[domain] = short_link

            # Display short links
            for domain, short_link in short_links.items():
                st.write(f"Short link for {domain}: {short_link}")
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
