import streamlit as st
import requests
import pandas as pd
import concurrent.futures
import time
from config import VALID_DOMAIN_TLCT
from domainHelper import generate_full_domains

def shorten_url(api_key, long_url, tags, crawlable, forward_query, domain='',short_code_length=6):
    url = 'https://200799.xyz/rest/v3/short-urls'
    # url = 'https://250499.xyz/rest/v3/short-urls'
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
        'domain': domain
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['shortUrl']
    else:
        return f"Error: {response.status_code} - {response.text}"

def process_urls(api_key, urls, tags_list, crawlable, forward_query, domains, short_code_length):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda data: shorten_url(api_key, data[0], data[1], crawlable, forward_query, data[2], short_code_length), zip(urls, tags_list,domains)))
    end_time = time.time()
    total_time = end_time - start_time
    return results, total_time

def main():
    st.title("URL Shortener")

    api_key = '8d1cbf9a-100f-46b0-b7b7-dbdabd630836'
    crawlable = True
    forward_query = True
    short_code_length = 6
    domain = '200799.xyz'

    st.markdown("### URL Shortener using xlsx")

    st.markdown(
        """
        Please upload a xlsx file containing a column named 'Long URL' and 'Tags'. The app will create short URLs
        for each long URL in the CSV and display the result as a DataFrame.
        """
    )

    uploaded_file = st.file_uploader("Choose a xlsx file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            if 'Long URL' not in df.columns or 'Tags' not in df.columns:
                st.error("The xlsx file must contain columns named 'Long URL' and 'Tags'.")
                return

            urls = df['Long URL'].tolist()
            domainsList= generate_full_domains(valid_domains=VALID_DOMAIN_TLCT,prefixLen=1,times=len(df))
            tags_list = df['Tags'].apply(lambda tags: tags.split(',')).tolist()
            short_urls, total_time = process_urls(api_key, urls, tags_list, crawlable, forward_query, domainsList, short_code_length)
            df['Short URL'] = short_urls

            st.dataframe(df)
            csv=df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Press to Download",
                csv,
                f"finishedFile.csv",
                "text/csv",
                key='download-csv'
            )

            st.write(f"Total runtime: {total_time:.2f} seconds")
            st.write(f"Average time per link: {total_time / len(urls):.4f} seconds")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
