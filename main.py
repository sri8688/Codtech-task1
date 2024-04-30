import re
import streamlit as st
import wikipedia

basic_questions = {
    "What is your name?": "I am a chatterbot!",
    "who are you?": "I am a chatterbot!",
    "How are you?": "I'm doing well, thanks for asking!",
    "about yourself": "I am a chatterbot! created by Vishal. how can i help you today",
    # add more general questions if you want
}


def is_greeting(question):
    clean_question = re.sub(r'[^\w\s]', '', question.lower())
    greetings = ["hi", "hello", "hey", "hii"]
    for greeting in greetings:
        if greeting in clean_question:
            return True
    return False


def respond_to_question(question):
    clean_question = re.sub(r'[^\w\s]', '', question.lower())

    # Check for greetings
    if is_greeting(clean_question):
        return "Hello, how may I help you today?"

    for q in basic_questions:
        clean_key = re.sub(r'[^\w\s]', '', q.lower())
        if clean_key in clean_question:
            return basic_questions[q]

    try:
        search_results = wikipedia.search(question)
        if search_results:
            page = wikipedia.page(search_results[0])
            response = " ".join(page.content.split()[:100])
            basic_questions[question] = response
            return response + "..."
        else:
            return "Sorry, I couldn't find any information on that topic."
    except wikipedia.exceptions.DisambiguationError as e:
        return "It seems there are multiple meanings for that term. Can you be more specific?"
    except wikipedia.exceptions.PageError as e:
        return "Sorry, I couldn't find any information on that topic."
    except wikipedia.exceptions.WikipediaException as e:
        return "Sorry, I encountered an error while searching. Please try again later."


def main():
    st.title("General Chatbot")
    question = st.text_input("You:")
    if st.button("Send"):
        if question.strip():
            response = respond_to_question(question)
            st.markdown(
                f'<div style="background-color:gray; color:white; padding:10px; border-radius:5px;">{response}</div>',
                unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()


