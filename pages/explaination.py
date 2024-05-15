import streamlit as st
import pandas as pd
import random
import asyncio
from datetime import datetime
from telegram import Bot
from time import sleep

# Title and introduction
st.title("Understanding the IPython Notebook")
st.write("""
Welcome to the interactive guide to understanding the IPython notebook.
We'll walk through the key sections and allow you to interact with important variables and parameters.
""")

# Code explanation sections
st.header("Code Explanation")

# Section 1: Imports and Setup
st.subheader("Imports and Setup")
st.code("""
import pandas as pd
from helper import getTimeStampWA
from telegram import Bot
from time import sleep
import random
import asyncio
from datetime import datetime

BOT_TOKEN = "your_bot_token_here"
TIME_DIFF=1
GROUP_LINK_START,GROUP_LINK_END=0,7
""", language='python')
st.write("""
This section imports necessary libraries and sets up initial variables. 
- `pandas`: for data manipulation.
- `getTimeStampWA`: a custom function to get the current timestamp.
- `telegram`: to interact with the Telegram API.
- `sleep` and `asyncio`: for timing and asynchronous operations.
- `datetime`: to work with date and time.

`BOT_TOKEN`, `TIME_DIFF`, and `GROUP_LINK_START/GROUP_LINK_END` are key variables.
""")

# Section 2: Helper Functions
st.subheader("Helper Functions")
st.code("""
def addLinkIndex(linkList):
    contentStr=''
    for i,link in enumerate(linkList):
        contentStr+=f"LINK {i+1}:\n{link}"
    return contentStr

def get_RUN_Data(updateMark='🌼', dataExcelFile='allLinkTLCTChannel.xlsx', dataSheet='Post', linkSheet='Link', reportedSheet='Reported'):
    dfData = pd.read_excel(dataExcelFile, sheet_name=dataSheet)
    dfLink = pd.read_excel(dataExcelFile, sheet_name=linkSheet)
    dfReported = pd.read_excel(dataExcelFile, sheet_name=reportedSheet)
    listReportedLink = list(dfReported['link'])
    dfLink = dfLink[~dfLink.link.isin(listReportedLink)]
    
    dfDataType = dfData["type"].unique().tolist()
    dfLinkType = dfLink["type"].unique().tolist()
    allPostData = {}
    backIndexString = "<a href='https://t.me/tailieuchantuong/339'>🌟Quay về Mục Lục🌟</a>"
    updateString = getTimeStampWA(timediff=TIME_DIFF)
    countKV = 0
    listKV = ['VSCNL','VSCPCDCS']
    postStringKV = ''
    
    for i, linkType in enumerate(dfLinkType):
        postString = ''
        if linkType in ['webDKN']:
            data2Process = dfLink[dfLink.type == linkType][GROUP_LINK_START:GROUP_LINK_END]['link'].to_list()
        elif linkType in ['webctcbth','webNTD']:
            data2Process = dfLink[dfLink.type == linkType][GROUP_LINK_START:GROUP_LINK_END]['link'].to_list()
        elif linkType in listKV:
            tempHeader = dfData[dfData.type == linkType]['header'].to_list()[0]
            postStringKV += f"<b>{tempHeader}</b>\n{backIndexString}\nCập nhật ngày: {updateString}\n\n"
            data2ProcessTemp = dfLink[dfLink.type == linkType][GROUP_LINK_START:GROUP_LINK_END]['link'].to_list()
            postStringKV += addLinkIndex(data2ProcessTemp) + "\n"
            countKV += 6
            if countKV > 6:
                allPostData['VSCNL'] = postStringKV
        else:
            data2Process = dfLink[dfLink.type == linkType][GROUP_LINK_START:GROUP_LINK_END]['link'].to_list()
        
        tempHeader = dfData[dfData.type == linkType]['header'].to_list()[0]
        postString += f"<b>{tempHeader}</b>\n{backIndexString}\nCập nhật ngày: {updateString}\n"
        postString += addLinkIndex(data2Process) + "\n"
        footerString = str(dfData[dfData.type == linkType]['footer'].to_list()[0])
        if footerString != 'nan':
            postString += footerString
        postString += updateMark
        allPostData[linkType] = postString
        
    return {'allPostData': allPostData, 'dfLinkType': dfLinkType, "dfData": dfData}
""", language='python')
st.write("""
This section defines helper functions:
- `addLinkIndex`: Adds index to each link.
- `get_RUN_Data`: Processes data from Excel file, filters reported links, and prepares post content.

Key variables:
- `updateMark`, `dataExcelFile`, `dataSheet`, `linkSheet`, `reportedSheet`.
""")

# Section 3: Main Functions
st.subheader("Main Functions")
st.code("""
async def updateCaption(caption='THIS IS AUTO TESTING CONTENT', chat_id='-1001737736508', message_id=2625, parse_mode='html'):
    bot = Bot(token=BOT_TOKEN)
    await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, parse_mode=parse_mode)

async def updateChannelPosts(updateMark='🌼'):
    RUN_Data = get_RUN_Data(updateMark=updateMark)
    allPostData = RUN_Data['allPostData']
    dfLinkType = RUN_Data['dfLinkType']
    dfData = RUN_Data['dfData']
    
    for i, linkType in enumerate(dfLinkType):
        if linkType != 'VSCPCDCS':
            content_RUN = allPostData[linkType]
            message_id = dfData[dfData.type == linkType].get('Post ID').tolist()[0]
            headerString = dfData[dfData.type == linkType]['header'].to_list()[0]
            await updateCaption(caption=content_RUN, chat_id='-1001556007495', message_id=message_id)
            sleep(2)
    print("🌸🌸🌸DONE UPDATE TLCT FOR TODAY, GOOD JOB!🌸🌸🌸")

randomUpdateMark = random.sample([*str('🌟🌸🍀✨🌷🌺🔥✨')], 1)[0]
timesOfMark = random.randint(1, 3)
print(datetime.now())
await updateChannelPosts(randomUpdateMark * 3)
""", language='python')
st.write("""
This section defines the main asynchronous functions:
- `updateCaption`: Updates the caption of a Telegram message.
- `updateChannelPosts`: Updates multiple channel posts using data from `get_RUN_Data`.

Key variables:
- `updateMark`, `caption`, `chat_id`, `message_id`, `parse_mode`.
""")

# Interactive Variables Section
st.header("Interactive Variables/Parameters")
st.write("You can change the values of these parameters and see how they affect the code.")

# Interactive input for BOT_TOKEN
bot_token = st.text_input("BOT_TOKEN", value="5672913980:AAFsPu5JkIBy0x2e-rInpbq_dYu5tv3M3V4")

# Interactive input for TIME_DIFF
time_diff = st.number_input("TIME_DIFF", value=1)

# Interactive inputs for GROUP_LINK_START and GROUP_LINK_END
group_link_start = st.number_input("GROUP_LINK_START", value=0)
group_link_end = st.number_input("GROUP_LINK_END", value=7)

st.write(f"Updated Parameters:\n- BOT_TOKEN: {bot_token}\n- TIME_DIFF: {time_diff}\n- GROUP_LINK_START: {group_link_start}\n- GROUP_LINK_END: {group_link_end}")

# Additional interactive elements can be added as needed

# Conclusion
st.header("Conclusion")
st.write("""
This interactive guide helps you understand the structure and key components of the provided code.
You can modify variables and parameters to see how they affect the code's functionality.
""")

# Run the Streamlit app by executing `streamlit run <filename>.py` in your terminal.
