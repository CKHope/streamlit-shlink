import streamlit as st
import requests
import pandas as pd
import concurrent.futures
import time
from config import VALID_DOMAIN_TLCT
from domainHelper import generate_full_domains,get_domains

def shorten_url(api_key, long_url, tags, crawlable, forward_query, short_code_length=6,domain='',customSlug=''):
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
        'domain': domain,
        'customSlug': customSlug
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        st.success(f'{long_url} DONE')
        return response.json()['shortUrl']
    else:
        return f"Error: {response.status_code} - {response.text}"

def process_urls(api_key, urls, tags_list, crawlable, forward_query, short_code_length, domains, customSlugs):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda data: shorten_url(api_key, data[0], data[1], crawlable, forward_query, short_code_length,data[2], data[3]), zip(urls, tags_list,domains,customSlugs)))
    end_time = time.time()
    total_time = end_time - start_time
    return results, total_time

def process_urls_in_batches(api_key, urls, tags_list, crawlable, forward_query, short_code_length, domains, customSlugs,batch_size=10):
    start_time = time.time()
    total_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            batch_tags = tags_list[i:i + batch_size]
            batch_domains = domains[i:i + batch_size]
            
            batch_results = list(
                executor.map(
                    lambda data: shorten_url(api_key, data[0], data[1], crawlable, forward_query, short_code_length,data[2], data[3]),
                    zip(batch_urls, batch_tags, batch_domains,customSlugs)
                )
            )
            total_results.extend(batch_results)
            
    end_time = time.time()
    total_time = end_time - start_time
    return total_results, total_time

def main():
    st.title("URL Shortener")

    api_key = '4f53fddb-eb10-4a27-9808-5a8f72ac06ed'
    crawlable = False
    forward_query = False
    short_code_length = 12
    # domain = '200799.xyz'
    batch_size=100

    st.markdown("### URL Shortener using CSV")

    st.markdown(
        """
        Please upload a CSV file containing a column named 'Long URL','Tags' and 'customSlug'. The app will create short URLs
        for each long URL in the CSV and display the result as a DataFrame.
        """
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Long URL' not in df.columns or 'Tags' not in df.columns:
                st.error("The CSV file must contain columns named 'Long URL' and 'Tags'.")
                return

            urls = df['Long URL'].tolist()
            domainsList= get_domains(valid_domains=VALID_DOMAIN_TLCT,times=len(df))
            tags_list = df['Tags'].apply(lambda tags: tags.split(',')).tolist()
            customSlugList=df['customSlug'].tolist()
            short_urls, total_time = process_urls_in_batches(api_key, urls, tags_list, crawlable, forward_query, short_code_length, domainsList, customSlugList, batch_size)
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
