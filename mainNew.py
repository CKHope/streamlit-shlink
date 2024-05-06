import streamlit as st
import requests
import pandas as pd
import concurrent.futures
import time
import itertools
from datetime import datetime

# from config import VALID_DOMAIN_TLCT
# from domainHelper import generate_full_domains,get_domains
from time import sleep

resutlHolder=st.empty()

#! shlink 688699.xyz
VALID_DOMAIN_TLCT=[
    '6686668.xyz',
    '6888688.xyz',
    '8668866.xyz',
    '8868886.xyz',
    '68888688.xyz',
    '68866688.xyz',
    '66866668.xyz',
    '88688868.xyz',
    '86688668.xyz',
    '68666866.xyz',
    '66866686.xyz',
    '86668666.xyz',
    '68888886.xyz',
    '68868668.xyz',
    '68866886.xyz',
]

def get_sublist_based_on_date(current_date, days_per_cycle, domains_per_cycle):
    day = current_date.day
    cycle = (day - 1) // days_per_cycle
    start_index = cycle * days_per_cycle * domains_per_cycle
    return VALID_DOMAIN_TLCT[start_index:start_index + domains_per_cycle]

current_date = datetime.now()
days_per_cycle = 4
domains_per_cycle = 5
sublist = get_sublist_based_on_date(current_date, days_per_cycle, domains_per_cycle)
print("Sublist for the current date:", sublist)

VALID_DOMAIN_TLCT=sublist

# #! shlink6
# VALID_DOMAIN_TLCT=[
#     "877988.xyz",
#     "866977.xyz",
#     "855966.xyz",
#     "822933.xyz",
#     "766877.xyz",
#     "755866.xyz",
#     "722833.xyz",
#     "655766.xyz",
#     "622733.xyz",
#     "251305.xyz",
# ]


# now=datetime.now()
# if int(now.strftime("%d")) % 2==0:
#     VALID_DOMAIN_TLCT=VALID_DOMAIN_TLCT[:5]
# else:
#     VALID_DOMAIN_TLCT=VALID_DOMAIN_TLCT[5:]
    
def get_domains(valid_domains, times,fixPrefix='i'):
    domains = []
    domain_iterator = itertools.cycle(valid_domains)
    
    for _ in range(times):
        domain = next(domain_iterator)
        # random_chars = generate_random_string(prefixLen)
        # full_domain = f"{random_chars}.{domain}"
        if fixPrefix != '':
            domains.append(f'{fixPrefix}.{domain}')
        else:
            domains.append(domain)
    
    return domains

# Initialization
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

    
def shorten_url(api_key, long_url, tags, crawlable, forward_query, short_code_length=6,domain='',mainDomain='200799.xyz'):
    url=f'https://{mainDomain}/rest/v3/short-urls'
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
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f'{long_url} DONE')
        return response.json()['shortUrl']
    else:
        return f"Error: {response.status_code} - {response.text}"

def process_urls_in_batches(api_key, urls, tags_list, crawlable, forward_query, short_code_length, domains,batch_size=10,mainDomain='200799.xyz'):
    start_time = time.time()
    total_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            batch_tags = tags_list[i:i + batch_size]
            batch_domains = domains[i:i + batch_size]
            
            batch_results = list(
                executor.map(
                    lambda data: shorten_url(api_key, data[0], data[1], crawlable, forward_query, short_code_length,data[2],mainDomain=mainDomain),
                    zip(batch_urls, batch_tags, batch_domains)
                )
            )
            total_results.extend(batch_results)
            sleep(1)

            resutlHolder.warning(f'{i+batch_size}/{len(urls)} links DONE ~ {(i+batch_size)/len(urls)}')
            
    end_time = time.time()
    total_time = end_time - start_time
    return total_results, total_time

def main():
    st.title("URL Shortener")
    # main_domain='200799.xyz'
    API_KEY=st.text_input("API Key", key="api_key")
    MAIN_DOMAIN=st.text_input("Main Domain", key="main_domain")
    FIX_PREFIX=st.text_input("Prefix", key="prefix")
    st.warning('TEST')
    if not API_KEY:
        st.warning("Please input your API key to proceed.")
        return
    if not MAIN_DOMAIN:
        st.warning("default domain is 200799.xyz")
    else:
        mainDomain=MAIN_DOMAIN
    if not FIX_PREFIX:
        st.warning("default domain is: i")
    else:
        fixPrefix=FIX_PREFIX
        
    api_key = API_KEY
    crawlable = False
    forward_query = False
    short_code_length = 9
    batch_size=40

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
            domainsList= get_domains(valid_domains=VALID_DOMAIN_TLCT,times=len(df),fixPrefix=fixPrefix)
            tags_list = df['Tags'].apply(lambda tags: tags.split(',')).tolist()
            short_urls, total_time = process_urls_in_batches(api_key, urls, tags_list, crawlable, forward_query, short_code_length, domainsList, batch_size,mainDomain=mainDomain)
            df['Short URL'] = short_urls

            if len(df)>0:
                st.session_state.df=df
            
            
            st.dataframe(df)
            df.to_csv(f'shlink/result.csv',encoding='utf-8',index=False)

        except Exception as e:
            st.error(f"Error: {e}")
        st.write(f"Total runtime: {total_time:.2f} seconds")
        st.write(f"Average time per link: {total_time / len(urls):.4f} seconds")

if __name__ == "__main__":
    main()