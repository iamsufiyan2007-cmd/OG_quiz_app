import streamlit as st
from google import genai
import json

client = genai.Client(api_key=st.secrets['GOOGLE_API_KEY'])

st.title("Goated Quiz")

topic = st.text_input("give a topic for genrating quiz questions")

if st.button("Generate quiz questions"):


    #formatted string

    prompt = f"""You are an expert in generating quiz questions.

        for the following topic - {topic}, genrate 25 quize questions in the following form

        {{ "question":"text" ,
        "options": [A,B,C,D],
        "correct":"correct answer",
        "explanation":"short explanation"
        }}

        dont add anything before or after this."""

        
    response = client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = prompt,
                config = {"response_mime_type":"application/json"}
                )

    data = json.loads(response.text)
    #st.write(data)
    st.session_state.quiz = data

if 'quiz' in st.session_state:
            st.header("quiz questions")
            num = 1
            for ques in  st.session_state.quiz:
                st.write(str(num) + ". " + ques['question'])
                st.radio('choose:',ques["options"],key='chosen_answer'+str(num))
                num += 1

            if st.button("submit"):
                st.header('Result')

                st.session_state.points = 0
                numb = 1
                for j in st.session_state.quiz:
                    if j['correct'] == st.session_state['chosen_answer' +str(numb)]:
                        st.session_state.points += 1
                    numb += 1

                st.write(f"you have answered {st.session_state.points} questions correctly")

                st.header('explanation')
                number = 1
                for j in st.session_state.quiz:
                    st.write(str(number) + ") " + j['explanation'])
                    number += 1
