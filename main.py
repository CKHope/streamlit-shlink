# import streamlit as st
# import requests
# import pandas as pd
# import concurrent.futures

# def shorten_url(api_key, long_url, tags, crawlable, forward_query, short_code_length=6):
#     url = 'https://130592.xyz/rest/v3/short-urls'
#     headers = {
#         'accept': 'application/json',
#         'X-Api-Key': api_key,
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'longUrl': long_url,
#         'tags': tags,
#         'crawlable': crawlable,
#         'forwardQuery': forward_query,
#         'shortCodeLength': short_code_length
#     }

#     response = requests.post(url, headers=headers, json=data)

#     if response.status_code == 200:
#         return response.json()['shortUrl']
#     else:
#         return f"Error: {response.status_code} - {response.text}"

# def process_urls(api_key, urls, tags_list, crawlable, forward_query, short_code_length):
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda data: shorten_url(api_key, data[0], data[1], crawlable, forward_query, short_code_length), zip(urls, tags_list)))
#     return results

# def main():
#     st.title("URL Shortener")

#     api_key = '9d5c4ffd-8885-4809-afef-dfb30b8f3e46'
#     crawlable = True
#     forward_query = True
#     short_code_length = 10

#     st.markdown("### URL Shortener using CSV")

#     st.markdown(
#         """
#         Please upload a CSV file containing a column named 'Long URL' and 'Tags'. The app will create short URLs
#         for each long URL in the CSV and display the result as a DataFrame.
#         """
#     )

#     uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file)
#             if 'Long URL' not in df.columns or 'Tags' not in df.columns:
#                 st.error("The CSV file must contain columns named 'Long URL' and 'Tags'.")
#                 return

#             urls = df['Long URL'].tolist()
#             tags_list = df['Tags'].apply(lambda tags: tags.split(',')).tolist()
#             short_urls = process_urls(api_key, urls, tags_list, crawlable, forward_query, short_code_length)
#             df['Short URL'] = short_urls

#             st.dataframe(df)

#         except Exception as e:
#             st.error(f"Error: {e}")

# if __name__ == "__main__":
#     main()
