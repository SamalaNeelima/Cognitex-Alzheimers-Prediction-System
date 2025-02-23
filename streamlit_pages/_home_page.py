import streamlit as st
from config import BANNER

def home_page():
    
    st.write("""
       ## Understanding Alzheimer's Disease
        Alzheimer's disease is a progressive neurodegenerative disorder that affects millions of people worldwide. 
        It primarily impacts memory, cognitive function, and behavior, making daily activities increasingly difficult over time. 
        While aging is a significant risk factor, genetics, lifestyle, and environmental factors also contribute to the disease's onset. 
        Despite ongoing research, there is currently no cure for Alzheimer's, making early detection and intervention crucial.

        ## Why Early Detection is Critical
        Identifying Alzheimer's disease in its early stages allows for timely medical intervention and lifestyle adjustments that 
        can slow its progression. Early diagnosis provides individuals and their families with the opportunity to explore treatment options, 
        seek cognitive therapies, and make informed healthcare decisions. Additionally, it enables participation in clinical trials that may 
        contribute to the advancement of future treatments. By detecting Alzheimer's early, we can help improve quality of life and prolong 
        independent living for those affected.

       ## About This Project
        This platform leverages Artificial Intelligence (AI) and Machine Learning (ML) to analyze MRI scans and predict 
        the likelihood of Alzheimer's disease. Our advanced model assists healthcare professionals by providing accurate 
        and data-driven insights, supporting early detection and proactive treatment planning.

        The goal of this project is to create an accessible and reliable screening tool that enhances medical decision-making. 
        By combining technology with healthcare, we strive to improve patient outcomes and contribute to the ongoing fight 
        against Alzheimer's disease.
        
        <br>
                
        """, unsafe_allow_html=True)

    st.caption('Finished reading? Navigate to the `Prediction Page` to make some predictions')