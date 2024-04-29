"""
This script is used to generate program advertisements in email
and SMS formats using Streamlit.

It imports necessary libraries and functions for creating a user
interface that allows users to selecta language, program title,
generate email and SMS advertisements, and provide feedback.

Note:
    This script requires Streamlit to be installed and other
    functions to be properly defined in the code.

Example:
    Run this script in your terminal to launch the Streamlit app:
    ```
    streamlit run your_script_name.py
    ```
"""

# IMPORTING LIBRARIES
import time
import pandas as pd
from PIL import Image
import streamlit as st
import openai
from googletrans import Translator
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# SET UP OPEN AI API KEY
#openai.api_key = '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'


# LOAD PROGRAM OVERVIEW DATA
course_data = pd.read_csv('course.csv')

# OPEN AI FUNCTIONS

def generate_email_advertisement(program_description, language, tone):
    """
    Generate a creative email advertisement for a given Humber College program.

    Args:
        program_description (str): Description of the Humber College program.
        language (str): Language of the advertisement (either 'English' or 'French').

    Returns:
        str: Generated email advertisement text.
    """
    if language == 'English':
        email_prompt = f"Create a {tone.lower()} email advertisement for the following Humber College program:\n{program_description}\n\n and do not add subject line, dear reference and closing sentiment or salutation."
    elif language == 'French':
        # Translation code for French (as in your original example)
        email_prompt = f"Créez une publicité par courrier électronique {tone.lower()} pour le programme suivant du Collège Humber :\n{program_description}\n\n et n'ajoutez pas de ligne d'objet, de référence chère et de salutation ou de formule de clôture. "

    response = openai.Completion.create(
        engine="text-davinci-003",
        temperature=0.5,
        prompt=email_prompt,
        max_tokens=500
    )
    return response['choices'][0]['text'].strip()

def generate_sms_advertisement(program_description, language, tone):
    """
    Generate an SMS advertisement for a given Humber College program.

    Args:
        program_description (str): Description of the Humber College program.
        language (str): Language of the advertisement (either 'English' or 'French').

    Returns:
        str: Generated SMS advertisement text.
    """
    if language == 'English':
        sms_prompt = f"Create an {tone.lower()} SMS advertisement for the following Humber College program:\n{program_description}\n\n"
    elif language == 'French':
        sms_prompt = f"Créez une publicité par {tone.lower()} SMS pour le programme suivant du Collège Humber :\n{program_description}\n\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        temperature=0.5,
        prompt=sms_prompt,
        max_tokens=400
    )
    return response['choices'][0]['text'].strip()

def post_process_email(email_text, language, tone):
    """
    Post-process an email by adding standardized components based on the language.

    Args:
        email_text (str): The main content of the email.
        language (str): Language of the email ('English' or 'French').

    Returns:
        str: Processed email with standardized subject, salutation, conclusion, and contact information.
    """
    if language == 'English':
        subject = "Exciting New Program at Humber College!"
        salutation = "Dear Prospective Student,"
        conclusion = "Don't miss out on this amazing opportunity. Apply now and embark on a journey to a brighter future!"
        regards = "Regards,\nHumber College Institute of Technology and Advanced Learning"
        email = " If you have any question contact us on +1.416.675.5067 or international.humber.ca/contact"

    elif language == 'French':
        subject = "Nouveau programme passionnant au Collège Humber !"
        salutation = "Cher futur étudiant,"
        conclusion = "Ne manquez pas cette incroyable opportunité. Postulez dès maintenant et embarquez pour un avenir plus radieux !"
        regards = "Cordialement,\nL'équipe du Collège Humber"
        email = "Si vous avez des questions, contactez-nous au +1.416.675.5067 ou international.humber.ca/contact"

    processed_email = f"Subject: {subject}\n\n{salutation}\n\n{email_text}\n\n{conclusion}\n\n{email}\n\n{regards}"
    return processed_email

def post_process_sms(sms_text, language, tone):
    """
    Post-process an SMS text by adding a standardized introduction based on the language.

    Args:
        sms_text (str): The main content of the SMS.
        language (str): Language of the SMS ('English' or 'French').

    Returns:
        str: Processed SMS text with a standardized introduction.
    """
    if language == 'English':
        intro = "Discover exciting opportunities at Humber College!"
    elif language == 'French':
        intro = "Découvrez des opportunités passionnantes au Collège Humber !"

    processed_sms = f"{intro}\n\n{sms_text}"
    return processed_sms

# STREAMLIT FUNCTIONS

def email_ready():
    """
    Display a sequence of toast notifications to indicate the progress of generating an email.

    This function simulates the process of generating an email by displaying a series of toast
    notifications with different messages and delays.

    Note:
        This function is designed for demonstration purposes and may need to be adapted for specific use cases.

    Example:
        To use this function in a Streamlit app, you can call it like this:
        ```
        email_ready()
        ```

    Returns:
        None
    """
    msg = st.toast('Generating email...')
    time.sleep(4)
    msg.toast('Waiting...')
    time.sleep(2)
    msg.toast('Ready!', icon="🥞")

def sms_ready():
    """
    Display a sequence of toast notifications to indicate the progress of generating an SMS.

    This function simulates the process of generating an SMS by displaying a series of toast
    notifications with different messages and delays.

    Note:
        This function is designed for demonstration purposes and may need to be adapted for specific use cases.

    Example:
        To use this function in a Streamlit app, you can call it like this:
        ```
        sms_ready()
        ```

    Returns:
        None
    """
    msg = st.toast('Generating sms...')
    time.sleep(3)
    msg.toast('Waiting...')
    time.sleep(2)
    msg.toast('Ready!', icon="🥞")


def main():
    """
    Run a Streamlit app to generate program advertisements in email and SMS formats.

    This function creates a Streamlit user interface that allows users to select a language, choose a program title,
    generate email and SMS advertisements, and provide feedback.

    Note:
        This function assumes the presence of other functions like `email_ready`, `sms_ready`,
        `generate_email_advertisement`, `generate_sms_advertisement`, `post_process_email`, and `post_process_sms`.

    Example:
        To run this Streamlit app, simply call the `main` function:
        ```
        main()
        ```

    Returns:
        None
    """
    image = Image.open('humber.png')
    st.image(image, width=300)
    st.title(":blue[Program Advertisement Generator]")

    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("\n\n\n")

    # Create a dropdown menu for language selection
    language = st.sidebar.selectbox(":blue[Select Language]:", ['English', 'French'])
    # st.selectbox("Select Language:", ['English', 'French'])

    # Get unique program titles from the course data
    program_titles = course_data['Title'].tolist()

    program_title = st.sidebar.selectbox(":blue[Select Program]:", program_titles)

    # Create a dropdown menu for selecting the tone
    selected_tone = st.sidebar.selectbox(":blue[Select Tone]:", ['Cool', 'Friendly', 'Positive', 'Assertive', 'Encouraging', 'Creative', 'Emotional', 'Happy'])

    st.sidebar.markdown("\n\n\n")
    st.sidebar.divider()

    st.sidebar.markdown("## About")
    st.sidebar.markdown("### Welcome to The Bilingual Hawk!")
    st.sidebar.markdown("Effortlessly generate SMS and email advertisements for IT program promotions at Humber College."
                        " Boost your marketing efforts with creative content tailored to your target audience.")
    # st.sidebar.markdown("Simplify your campaign planning and engage your prospective students like never before.")

    # Fetch program description based on selected title
    program_description = course_data.loc[course_data['Title'] == program_title, 'description'].values[0]

    # Translate program description if selected language is French
    if language == 'French':
        translator = Translator()
        translated_description = translator.translate(program_description, dest='fr')
        program_description = translated_description.text

    # Create a text area for user input
    user_prompt = st.text_area("Enter Your Own Prompt:", height=50)

    col1, col2 = st.columns(2)

    # Create generate email button
    if col1.button(":blue[Generate Email]"):
        email_ready()  # Call the email_ready function here

        if user_prompt:
            email_advertisement = generate_email_advertisement(user_prompt, language, selected_tone)
            processed_email = post_process_email(email_advertisement, language, selected_tone)
        else:
            email_advertisement = generate_email_advertisement(program_description, language, selected_tone)
            processed_email = post_process_email(email_advertisement, language, selected_tone)

        if language == 'English':
            st.subheader("Generated {selected_tone} Email Advertisement: :e-mail:")
            st.text_area("Email Content:", value=processed_email, height=600)
            # st.write(processed_email)

        elif language == 'French':
            st.subheader("Publicité par courrier électronique {selected_tone} générée : :e-mail:")
            st.text_area("Contenu de l'e-mail :", value=processed_email, height=600)
            # st.write(processed_email)

        col3, col4 = st.columns(2)
        positive = col3.button('👍')
        negative = col4.button('👎')

        if negative:
            feedback_text = st.text_area("Enter your feedback:", height=100)
        if st.button("Submit Feedback"):
            # Incorporate the feedback into the prompt and generate a new message
            new_prompt = f"Program Description: {program_description}\nFeedback: {feedback_text}"
            new_email_advertisement = generate_email_advertisement(new_prompt, language, selected_tone)
            new_processed_email = post_process_email(new_email_advertisement, language, selected_tone)
            st.subheader("New Generated Email Advertisement:")
            st.text_area("Email Content:", value=new_processed_email, height=600)
            st.success("Thanks for your feedback and input!")

    # Add another button
    if col2.button(":blue[Generate SMS]"):
        sms_ready()

        if user_prompt:
            sms_advertisement = generate_sms_advertisement(user_prompt, language, selected_tone)
            processed_sms = post_process_sms(sms_advertisement, language, selected_tone)
        else:
            sms_advertisement = generate_sms_advertisement(program_description, language, selected_tone)
            processed_sms = post_process_sms(sms_advertisement, language, selected_tone)

        if language == 'English':
            st.subheader("Generated {selected_tone} SMS Advertisement: :envelope_with_arrow: ")
            st.text_area("SMS Content:", value=processed_sms, height=300)
            # st.write(processed_email)
        elif language == 'French':
            st.subheader("Publicité par courrier électronique {selected_tone} générée : :envelope_with_arrow:")
            st.text_area("Contenu de l'e-mail :", value=processed_sms, height=300)
            # st.write(processed_email)

        col3, col4 = st.columns(2)
        positive = col3.button('👍')
        negative = col4.button('👎')

        if negative:
            feedback_text = st.text_area("Enter your feedback:", height=100)
        if st.button("Submit Feedback"):
            # Incorporate the feedback into the prompt and generate a new message
            new_prompt = f"Program Description: {program_description}\nFeedback: {feedback_text}"
            new_email_advertisement = generate_email_advertisement(new_prompt, language, selected_tone)
            new_processed_email = post_process_email(new_email_advertisement, language, selected_tone)
            st.subheader("New Generated Email Advertisement:")
            st.text_area("Email Content:", value=new_processed_email, height=600)
            st.success("Thanks for your feedback and input!")

if __name__ == "__main__":
    main()
