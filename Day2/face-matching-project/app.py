import boto3
import streamlit as st
from PIL import Image
import os

def load_image(image_file):
    img=Image.open(image_file)
    return img

st.header("FACE MAPPING USING AWS")
#create ui
col1,col2 = st.columns(2)

col1.subheader('Enter source image')
src_imgae_file=col1.file_uploader("Upload Images",type=["png","jpg","jpeg"],key=1)

col2.subheader('Enter target image')
target_imgae_file=col2.file_uploader("Upload Images",type=["png","jpg","jpeg"],key=2)

if(src_imgae_file is not  None):
    file_details={"filename":src_imgae_file,"filetype":src_imgae_file.type,"filesize":src_imgae_file.size}
    col1.write(file_details)
    col1.image(load_image(src_imgae_file),width=250)
    with open(os.path.join("uploads","src.jpg"),"wb") as f:
        f.write(src_imgae_file.getbuffer())
        col1.success('File saved')
if(target_imgae_file is not  None):
    file_details={"filename":target_imgae_file,"filetype":target_imgae_file.type,"filesize":target_imgae_file.size}
    col2.write(file_details)
    col2.image(load_image(target_imgae_file),width=250)
    with open(os.path.join("uploads","target.jpg"),"wb") as f:
        f.write(target_imgae_file.getbuffer())
        col2.success('File saved')
        


if st.button("Comapre Faces"):
    # st.warning("Faces Comparision Called")
    imageSource=open("uploads/src.jpg","rb")
    imageTarget=open("uploads/target.jpg","rb")
    #create a client object
    client=boto3.client('rekognition')
    response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})
    #st.warning(response)
    try:
        print(response['FaceMatches'][0])
        st.success('Faces Matches')
    except:
        st.error("Faces not matched")