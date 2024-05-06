import streamlit as st
import asyncio
import aiohttp

async def shorten_url(session, api_key, long_url, tags, crawlable, forward_query, slug, short_code_length=6, domain='', main_domain='6886889.xyz'):
    url = f'https://{main_domain}/rest/v3/short-urls'
    headers = {
        'accept': 'application/json',
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'longUrl': long_url,
        'tags': tags,
        'crawlable': crawlable,
        'forwardQuery': forward_query,
        'shortCodeLength': short_code_length,
        'domain': domain,
        'customSlug': slug
    }

    async with session.post(url, headers=headers, json=data) as response:
        if response.status == 200:
            result = await response.json()
            return result['shortUrl']
        else:
            return f"Error: {response.status} - {await response.text()}"

async def main():
    st.title("URL Shortener")

    # Input fields
    api_key = st.text_input("Enter your Shlink API key:")
    main_domain = st.text_input("Enter the main domain:", value="6886889.xyz")
    long_url = st.text_input("Enter the long URL:")
    domain_text = st.text_area("Enter the list of domains (one domain per line):")

    # Default tag and slug inputs
    default_tag = st.text_input("Enter the default tag:", value="initDomain")
    default_slug = st.text_input("Enter the default slug:", value="000000")

    if st.button("Shorten URL"):
        if api_key and main_domain and long_url and domain_text:
            tags = [default_tag]  # Default tag
            crawlable = False  # You can customize this if needed
            forward_query = False  # You can customize this if needed

            # Split domain text area by lines and remove empty lines
            domains = [domain.strip() for domain in domain_text.split("\n") if domain.strip()]

            # Create an aiohttp session
            async with aiohttp.ClientSession() as session:
                # Make asynchronous requests for shortening URLs for each domain
                tasks = [shorten_url(session, api_key, long_url, tags, crawlable, forward_query, default_slug, domain=domain) for domain in domains]
                short_links = await asyncio.gather(*tasks)

            # Display short links
            for domain, short_link in zip(domains, short_links):
                st.write(f"Short link for {domain}: {short_link}")
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    asyncio.run(main())
