import streamlit as st

if len(st.session_state.df)>0:
    st.success('Got data')
    st.dataframe(st.session_state.df)
    df=st.session_state.df
    csv=df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Press to Download",
        csv,
        f"finishedFile.csv",
        "text/csv",
        key='download-csv'
    )
else:
    st.warning('No data')
    
            
# st.dataframe(st.session_state.df)
