import streamlit as st
from PIL import Image
import time
import numpy as np

import sys
import os
import cv2
from remove_api import remove_inference, remove_inference_opencv
from parser.inference_single import inference  as parse_inference
from parser.inference_single import init_model
from vton.inference import inference as vton_inference

parse_model = init_model("./models/LIP_best.pth")
cloth_path = './Database/val/cloth'
cloth_mask_path = './Database/val/cloth-mask'

st.title("Virtual Try ON")

dirs = os.listdir(cloth_mask_path)
print(dirs)
cloth_names_list = []
cloth_list = []
for file in dirs:
    file_name = file.split('.')
    if file_name[-1] == 'jpg':
        im_name = file_name[:-1]
        cloth = Image.open(os.path.join(cloth_path, file))
        cloth_list.append(cloth)
        cloth_names_list.append(im_name[0][:-2])

uploaded_cloth = st.sidebar.file_uploader("Upload a Cloth Photo")
uploaded_selected = st.sidebar.selectbox('Or select an image from below:', [''] + cloth_names_list, format_func=lambda x: 'Select an option' if x == '' else x)

if uploaded_cloth is not None or uploaded_selected is not '':
    if uploaded_cloth is not None: 
        cloth = Image.open(uploaded_cloth)
    else:
        cloth = Image.open('./Database/val/' + 'cloth/' + uploaded_selected + "_1.jpg")
    cloth = cloth.resize((192, 256))
    st.sidebar.write("Cloth Image Uploaded")
    st.sidebar.image(cloth, width=100, use_column_width=False)
    ti = time.localtime()
    ti = '%d-%d-%d-%d' % (ti[2], ti[3], ti[4], ti[5])
    temp_path = "./Database/val/temp/"+ti+"_1.jpg"
    cloth.save(temp_path)
    thres = st.sidebar.slider("Threshold", min_value=1, max_value=30, value=10, step=1)
    result, mask = remove_inference_opencv(temp_path, thres)
    # result, mask = remove_inference(temp_path)
    st.sidebar.image(mask, caption="mask", width=100, use_column_width=False)
    st.sidebar.image(result, caption="processed cloth", width=100, use_column_width=False)

    user_input = st.sidebar.text_input("Please Input the Cloth Image Name... eg. Red1")
    if st.sidebar.button('Commit Upload'):
        if user_input == '':
            st.sidebar.write("Please enter the cloth name")
        else:
            mask_path = "./Database/val/cloth-mask/"+user_input+"_1.jpg"
            im_path = "./Database/val/cloth/"+user_input+"_1.jpg"
            
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            cv2.imwrite(im_path, result)
            cv2.imwrite(mask_path, mask)
            st.write("Cloth Image Committed")
        
class opt():
    def __init__(self, name, stage, data_path, imname, cname, result_dir, checkpoint):
        self.name = name
        self.gpu_ids = ""
        self.workers = 1
        self.batch_size = 4
        self.data_path = data_path
        self.stage = stage
        self.imname = imname
        self.cname = cname
        self.fine_width = 192
        self.fine_height = 256
        self.radius = 5
        self.grid_size = 5
        self.grid_image = 'vton/grid.png'
        self.result_dir = result_dir
        self.checkpoint = checkpoint
        self.shuffle = False

uploaded_person = st.file_uploader("Upload a Human Photo")
UPLOAD_FLAG = False
if uploaded_person is not None:
    ti = time.localtime()
    ti = '%d-%d-%d-%d' % (ti[2], ti[3], ti[4], ti[5])
    im_path = "./Database/val/cloth/"+ti+"_1.jpg"
    person = Image.open(uploaded_person)
    st.write("Human Image Uploaded")
    st.image(person, width=100, use_column_width=False)
    im_path = "./Database/val/image/"+ti+".jpg"
    person.save(im_path)
    UPLOAD_FLAG = True

selected = st.selectbox('Select the Item Id:', [
                        ''] + cloth_names_list, format_func=lambda x: 'Select an option' if x == '' else x)
if selected is not '':
    cloth = Image.open('./Database/val/' + 'cloth/' + selected + "_1.jpg")
    st.write("Cloth Selected")
    st.image(cloth, width=100, use_column_width=False)

if selected is not '' and UPLOAD_FLAG:
    st.write("Click the Button to get the result")
    if st.button('Execute'):
        st.write("Generating Mask and Pose")
        parse_inference(parse_model, im_path=im_path, save_dir="./Database/val")
        parsing_result = Image.open("./Database/val/image-parse/" +ti+".png")
        parsing_result = parsing_result.convert('RGB')
        st.image(parsing_result , caption="Parsing Result" , width=300 , use_column_width=False)
        st.write("Doing virtual try-on")
        execute_bar = st.progress(0)
        imname = ti+".jpg"
        cname = selected + "_1.jpg"
        gmm_opt = opt(name="gmm_traintest_new", stage="GMM", data_path='./Database/val', result_dir='./Database/val', imname=imname, cname=cname, checkpoint='models/gmm_050000.pth')
        vton_inference(gmm_opt)
        tom_opt = opt(name="tom_test_new", stage="TOM", data_path='./Database/val', result_dir='./output', imname=imname, cname=cname, checkpoint='models/tom_100000.pth')
        vton_inference(tom_opt)
        for percent_complete in range(100):
            time.sleep(0.01)
            execute_bar.progress(percent_complete + 1)
        result = Image.open("./output/" + imname)
        st.image(result , caption="Result" , width=300 , use_column_width=False)
