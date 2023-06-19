import os
from apikey import apikey
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = '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'  # change with your OpenAI key

# Function to generate repository based on user prompt
def generate_repository(chain, prompt):
    repository = chain.run(prompt)
    return repository

# Function to generate link based on the generated repository
def generate_link(chain, repository):
    link = chain.run(repository)
    return link

# Function to measure complexity of each repository and find the repository with the highest complexity
def measure_complexity(repositories):
    complexity_scores = {}  # Dictionary to store complexity scores for each repository
    # TODO: Measure complexity of each repository and store the scores in complexity_scores dictionary

    if complexity_scores:  # Check if complexity_scores dictionary is not empty
        highest_complexity_repo = max(complexity_scores, key=complexity_scores.get)
        return highest_complexity_repo
    else:
        return None

# Main function
def main():
    st.title('GITHUB AUTOMATED ANALYSIS')
    user_prompt = st.text_input('Enter your prompt here')

    repository_template = PromptTemplate(
        input_variables=['topic'],
        template='Which GitHub repositories exhibit the highest level of technical complexity in the context of {topic}?'
    )

    link_template = PromptTemplate(
        input_variables=['repository'],
        template='Provide a link to the GitHub repository with the most technical complexity: {repository}'
    )

    repository_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    link_memory = ConversationBufferMemory(input_key='repository', memory_key='chat_history')

    llm = OpenAI(temperature=0.9)
    repository_chain = LLMChain(llm=llm, prompt=repository_template, verbose=True, output_key='repository',
                                memory=repository_memory)

    link_chain = LLMChain(llm=llm, prompt=link_template, verbose=True, output_key='link', memory=link_memory)

    if user_prompt:
        repository = generate_repository(repository_chain, user_prompt)
        link = generate_link(link_chain, repository)

        st.write(repository)
        st.write(link)

        highest_complexity_repo = measure_complexity([repository])
        if highest_complexity_repo:
            st.write(f"Repository with the highest complexity: {highest_complexity_repo}")
        else:
            st.write("No complexity scores calculated.")

if __name__ == '__main__':
    main()
