import streamlit as st
import numpy as np 
from PIL import Image
import ZOCR_SCAN as zs 
from streamlit_gsheets import GSheetsConnection
import gspread
import re

def process_text(text):
    pattern = r'R\d+\.\d+'
    rows = list()
    for item in text:
        st.write(item)
        match = re.search(pattern,item)
        if match:
            prefix = item[:match.start()]
            value = match.group(0)
            st.write("Prefix:", repr(prefix))
            st.write("Matched Value:", repr(value))

def append_to_db(rows):
    # conn.update(
    #    worksheet="Test",
    #    data= text
    # )
    # st.write("Success ")
    gc = gspread.service_account(".streamlit/happy.json")
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JrjyQG9aJStzoSNkTOrZQvYPh-y1GqV7gDE3f9Jgcr0/edit#gid=243609202")
    worksheet = spreadsheet.worksheet("Test")
    worksheet.append_rows([rows])
    print(rows)
    return  

def main():
    # Set the title of the app
    st.title("ZOCR")
    # picture = st.camera_input("Take a picture")
    # if picture:
    #     st.image(picture)
    #     image = np.array(picture)
    #     text = zs.scanImage(image)
    #     st.write("Extracted Text: ", text)
    
    #sheet_connection = st.connection("gsheets",type=GSheetsConnection)
    #df = sheet_connection.read()

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)
        try:
            text,borderedImage = zs.scanImage(image)
            st.image(borderedImage,caption="Detected Receipt",use_column_width=True)
            st.write(text)
            st.success("Receipt outline found!")
            process_text(text)

        except Exception as e:
            st.error(str(e))

# Run the main function
if __name__ == "__main__":
    main()