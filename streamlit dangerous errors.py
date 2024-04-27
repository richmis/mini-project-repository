import numpy as np
import pickle
import streamlit as st

# Load the trained model
loaded_model = pickle.load(open('trained_model (1).sav', 'rb'))

# Function to classify nutritional status
def classify_nutritional_status(prediction):
    try:
        # Convert input data to numpy array and ensure all inputs are numeric
        input_data_as_numpy_array = np.asarray(prediction[1:], dtype=float)
        # Check if gender is 'Girl' or 'Boy' and replace it with 0 or 1 respectively
        gender = 0 if prediction[0] == 'Girl' else 1
        input_data_as_numpy_array = np.insert(input_data_as_numpy_array, 0, gender)
    except ValueError:
        st.error("Please make sure all inputs are numeric.")
        return

    if len(input_data_as_numpy_array) != 4:
        st.error("Please provide all 4 inputs: Gender, Age in months, Height (cm), Weight (kg)")
        return

    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Make predictions
    prediction = loaded_model.predict(input_data_reshaped)

    # Determine nutritional status based on prediction
    if 2.8 <= prediction <= 3.7:
        return "SEVERE STUNTING"
    elif 4.8 <= prediction <= 5.7:
        return "STUNTING"
    elif 3.8 <= prediction <= 4.7:
        return "SEVERE WASTING"
    elif 6.8 <= prediction <= 7.7:
        return "WASTING"
    elif 5.8 <= prediction <= 6.7:
        return "UNDERWEIGHT"
    elif prediction == 1:
        return "HEALTHY HEIGHT"
    elif 1.8 <= prediction <= 2.7:
        return "HEALTHY HEIGHT"

recommend_list = pickle.load(open("recommendations (1).pkl", 'rb'))
similarity = pickle.load(open("similarity.zip", 'rb'))


def recommend(typi):
    malnutrition_rows = recommend_list[recommend_list['MALNUTRITION TYPE'] == typi]
    if malnutrition_rows.empty:
        return []  # Return an empty list if no matching malnutrition type is found

    malnutrition_index = malnutrition_rows.index[0]
    distances = similarity[malnutrition_index]
    listi = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:3]

    recommended = []  # Initialize as an empty list
    for i in listi:
        recommended.append(recommend_list.iloc[i[0]]['RECOMMENDATIONS'])  # Access 'RECOMMENDATIONS' column
    return recommended



# Main function to create Streamlit web app
def main():
    st.set_page_config(
        page_title="NUTRI TRACKER APP"
    )
    st.sidebar.success("User Form")

    page = st.sidebar.radio("Navigation", ["Home", "NUTRI CALCULATOR","RECOMMENDATION"])

    if page == "Home":
        st.title('NUTRI-TRACKER WEB APP')
        html_temp = """
                             <div style="background-color: orange; padding: 20px; border-radius: 10px;">
                             <h2 style="color: #333333; text-align: center;">NUTRI-TRACKER WEB APP</h2> 
                             </div>
                             """
        st.markdown(html_temp, unsafe_allow_html=True)
        st.write('"NOURISHING TODAYS CHILDREN ENSURES A THRIVING TOMMORROW."')

    elif page == "NUTRI CALCULATOR":
        st.title('NUTRI CALCULATOR')
        html_temp = """
                   <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
                   <h2 style="color: #333333; text-align: center;">NUTRI CALCULATOR</h2> 
                   </div>
                   """
        st.markdown(html_temp, unsafe_allow_html=True)

        gender_option = st.selectbox('Select gender:', [('👧 Girl', 'Girl'), ('👦 Boy', 'Boy')], format_func=lambda x: x[0])

        if gender_option[1] == 'Girl':
            st.write('👧 Girl')
        elif gender_option[1] == 'Boy':
            st.write('👦 Boy')

        MONTH = st.text_input('Enter age in months')
        HEIGHT = st.text_input('Enter height in cm')
        WEIGHT = st.text_input('Enter weight in kg')

        if st.button('MALNUTRITION TYPE'):
            diagnosis = classify_nutritional_status([gender_option[1], MONTH, HEIGHT, WEIGHT])
            if diagnosis:
                st.success(f"Nutritional Status: {diagnosis}")

    elif page =="RECOMMENDATION":
        st.title('RECOMMENDATION SYSTEM OF MALNUTRITION')
        html_temp = """
                             <div style="background-color: #98fb98; padding: 20px; border-radius: 10px;">
                             <h2 style="color: #333333; text-align: center;">RECOMMENDATION SYSTEM OF MALNUTRITION</h2> 
                             </div>
                             """
        st.markdown(html_temp, unsafe_allow_html=True)

        selected_type = st.selectbox('Select type for which you want to get recommendations.', (
            'SEVEREWASTING(kg)', 'WASTING(kg)', 'SEVERESTUNTING', 'STUNTING', 'UNDERWEIGHT(kg)', 'HEALTHYHEIGHT(cm)',
            'HEALTHYWEIGHT(kg)'))
        if st.button('RECOMMEND'):
            rec = recommend(selected_type)
            for i in rec:
                st.write(i)

# Check if the script is run directly
if __name__ == '__main__':
    main()
