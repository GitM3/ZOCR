import streamlit as st
import numpy as np 
from PIL import Image
import ZOCR_SCAN as zs 
from streamlit_gsheets import GSheetsConnection
import gspread
import re



def process_text(text):
    rows = list()
    for item in text:
        match = re.search(r'R(\d+\.\d+)',item)
        if match:
            # Check negatives: places like checkers use this to mark specials
            negative_match = re.search(r'\-R(\d+\.\d+)',item)
            if negative_match:
                # subtract from previous item: assuming never first
                # But then don't add to row, just note special/saving
                rows[-1][1] = rows[-1][1] - float(negative_match.group(1))
                rows[-1][0] = rows[-1][0] + "SPECIAL"
            else:
                prefix = item[:match.start()].rstrip()
                value = float(match.group(1))
                #print(prefix," : ", value)
                if prefix.upper() != "TOTAL":
                    rows.append([prefix,value])
        else:
            print("eish")
            # Handle No match
            # Check if bussiness name: auto matically add skip name setting
    if rows:
        location = st.text_input("Enter Store Name")
    if location:
        _ = [row.append(location) for row in rows]
        btn = st.button("Submit")
        if btn:
            append_to_db(rows)
            st.session_state['upload'] = False
    return    

def append_to_db(rows):
    # conn.update(
    #    worksheet="Test",
    #    data= text
    # )
    # st.write("Success ")
    gc = gspread.service_account(".streamlit/happy.json")
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JrjyQG9aJStzoSNkTOrZQvYPh-y1GqV7gDE3f9Jgcr0/edit#gid=243609202")
    worksheet = spreadsheet.worksheet("Test")
    worksheet.append_rows(rows)
    print(rows)
    return  

def main():
    
    st.title("ZOCR")
    if 'key' not in st.session_state:
        st.session_state['upload'] = False
    # picture = st.camera_input("Take a picture")
    # if picture:
    #     st.image(picture)
    #     image = np.array(picture)
    #     text = zs.scanImage(image)
    #     st.write("Extracted Text: ", text)
    
    #sheet_connection = st.connection("gsheets",type=GSheetsConnection)
    #df = sheet_connection.read()

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None and st.session_state['upload']== False:
        st.session_state['upload'] = True
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