import streamlit as st
import random
import string
import pandas as pd
import pickle
import os

# Constants
DEFAULT_DOMAINS_FILE = "default_domains.pkl"
DEFAULT_MAX_RANDOM_SUBDOMAIN_LENGTH = 8
DEFAULT_NUM_LINKS = 5
DEFAULT_STEP = 5
DEFAULT_UNIQUE_SUBDOMAIN_LENGTH = True
APP_VERSION = "1.5"
APP_FEATURES = """
Features:
- Import links from an Excel file
- Generate customized links based on input links and default domains
- Specify the number of links to generate
- Choose between random or source-based subdomain length
- Each link can have a different random subdomain length
- Display the generated links in a DataFrame
- Merge the generated links with the source DataFrame
"""

def load_default_domains():
    try:
        with open(DEFAULT_DOMAINS_FILE, "rb") as file:
            default_domains = pickle.load(file)
    except FileNotFoundError:
        default_domains = []
    return default_domains

def save_default_domains(default_domains):
    with open(DEFAULT_DOMAINS_FILE, "wb") as file:
        pickle.dump(default_domains, file)

def remove_default_domain(domain):
    default_domains = load_default_domains()
    if domain in default_domains:
        default_domains.remove(domain)
        save_default_domains(default_domains)

def extract_links_from_excel(file_path, column_name):
    df = pd.read_excel(file_path)
    return df

def extract_key_index(link):
    return link.split("/")[-1].split("#")[0]

def generate_links(links, source_links, domains, num_links, subdomain_length_option, max_random_subdomain_length, unique_subdomain_length):
    generated_links = []
    num_domains = len(domains)
    
    for i, (link, source_link) in enumerate(zip(links, source_links)):
        # Extract the key index from the link
        key_index = extract_key_index(link)
        
        # Extract the subdomain from the source link
        subdomain_source = link.split("//")[-1].split(".")[0]
        
        if unique_subdomain_length:
            subdomain_lengths = [random.randint(1, max_random_subdomain_length) for _ in range(num_links)]
        else:
            subdomain_lengths = [random.randint(1, max_random_subdomain_length)] * num_links
        
        for j in range(num_links):
            # Determine the domain index to use
            domain_index = j % num_domains
            domain = domains[domain_index]
            
            # Determine the subdomain length
            subdomain_length = subdomain_lengths[j]
            
            # Generate a random or source-based subdomain
            subdomain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=subdomain_length))
            # Generate a random 8-digit or character fragment
            fragment = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            
            generated_link = f"https://{subdomain}.{domain}/{key_index}#{fragment}"
            generated_links.append((generated_link, source_link, key_index, subdomain))
    
    return generated_links

def main():
    st.title("Link Generator")
    
    # Display app version and features
    st.subheader("App Version and Features")
    st.text(f"Version: {APP_VERSION}")
    st.text_area("Features:", value=APP_FEATURES, height=200)

    # Load default domains
    default_domains = load_default_domains()

    # Input: File uploader for Excel file
    st.subheader("Import Excel File")
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the Excel file
        df = extract_links_from_excel(uploaded_file, "link")

        # Select column for links
        st.subheader("Select Column for Links")
        link_column = st.selectbox("Select the column containing links:", df.columns)

        # Extract links from selected column
        links = df[link_column].tolist()

        # Display the extracted links
        if links:
            st.write("Imported Links:")
            for link in links:
                st.write(link)
        else:
            st.error("No links found in the selected column.")

        # Input: Text area for default domains
        st.subheader("Enter Default Domains")
        default_domains_text = st.text_area("Paste your default domains here (one domain per line):")

        # Button to update default domains
        if st.button("Update Default Domains"):
            default_domains = default_domains_text.split("\n")
            save_default_domains(default_domains)

        # Display default domains with checkbox for removal
        st.subheader("Default Domains")
        domains_to_remove = []
        for domain in default_domains:
            remove_domain = st.checkbox(domain, key=domain)
            if remove_domain:
                domains_to_remove.append(domain)

        # Button to remove selected domains
        if domains_to_remove:
            st.button("Remove Selected Domains")
            for domain in domains_to_remove:
                remove_default_domain(domain)

        # Input: Number input for the number of links to generate
        st.subheader("Number of Links to Generate")
        num_links = st.number_input("Enter the number of links to generate:", value=DEFAULT_NUM_LINKS, min_value=1, step=DEFAULT_STEP)

        # Input: Selectbox for subdomain length
        st.subheader("Subdomain Length")
        subdomain_length_option = st.selectbox("Select the subdomain length option:", ["random", "source"])

        unique_subdomain_length = st.checkbox("Each link has a different random subdomain length", value=DEFAULT_UNIQUE_SUBDOMAIN_LENGTH)

        if subdomain_length_option == "random":
            max_random_subdomain_length = st.number_input("Enter the maximum random subdomain length:", value=DEFAULT_MAX_RANDOM_SUBDOMAIN_LENGTH, min_value=1, step=1)
        else:
            max_random_subdomain_length = None

        if st.button("Generate Links"):
            if links and default_domains and num_links:
                # Generate links for each default domain
                generated_links = generate_links(links, links, default_domains, num_links, subdomain_length_option, max_random_subdomain_length, unique_subdomain_length)
                # Create DataFrame to display generated links
                result_df = pd.DataFrame({"Generated Links": [x[0] for x in generated_links], "Source Link": [x[1] for x in generated_links], "KeyIndex": [x[2] for x in generated_links], "Subdomain": [x[3] for x in generated_links]})
                # Merge result_df with the source_df on Source Link
                merged_df = pd.merge(df, result_df, left_on=link_column, right_on="Source Link")
                # Output: Display the merged DataFrame
                st.subheader("Merged DataFrame")
                st.dataframe(merged_df)
            else:
                st.error("Please upload an Excel file, input default domains, and select the number of links to generate.")

if __name__ == "__main__":
    main()