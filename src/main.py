import uuid

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

from chatbot import history, config, builder, limiters
from chatbot.context import SearchContext
from chatbot.conversation import Conversation
from settings import DEFAULT_TEMPLATE_STRING, HISTORY_TOKENS_LIMIT, CONTEXT_TOKENS_LIMIT

st.set_page_config(
    page_title="Interactive ChatBot with History",
    page_icon='💬',
    layout='wide',
)


def manage_configs():
    st.sidebar.header('PromptConfig Settings')
    input_key = st.sidebar.text_input('Input Key', value='question')
    history_key = st.sidebar.text_input('History Key', value='history')
    context_key = st.sidebar.text_input('Context Key', value='context')
    template_string = st.sidebar.text_area('Template String', value=DEFAULT_TEMPLATE_STRING)

    st.session_state.prompt_config = config.PromptConfig(
        input_key=input_key,
        history_key=history_key,
        context_key=context_key,
        template_string=template_string
    )

    st.sidebar.header('ChainConfig Settings')
    model = st.sidebar.text_input('OpenAI Model', value='gpt-3.5-turbo')
    temperature = st.sidebar.number_input(
        'Temperature', value=0.3, step=0.1, min_value=0.0, max_value=1.0
    )
    st.session_state.llm_config = config.LlmConfig(
        model=model,
        temperature=temperature,
    )

    st.sidebar.header('ChainConfig Settings')
    limit_history = st.sidebar.checkbox('Limit History', value=True)
    history_max_tokens = st.sidebar.number_input('History Max Tokens', value=HISTORY_TOKENS_LIMIT)
    limit_context = st.sidebar.checkbox('Limit Context', value=True)
    context_max_tokens = st.sidebar.number_input('Context Max Token', value=CONTEXT_TOKENS_LIMIT)

    st.session_state.chain_config = config.ChainConfig(
        limit_history=limit_history,
        history_max_tokens=history_max_tokens,
        limit_context=limit_context,
        context_max_tokens=context_max_tokens,
    )


def generate_new_session():
    session_id = str(uuid.uuid4()).replace('-', '')  # Generate unique session ID
    if 'sessions' not in st.session_state:
        st.session_state.sessions = []  # Initialize sessions list

    st.session_state.sessions.append(session_id)
    st.session_state.current_session = session_id  # Set the new session as current
    return session_id


def manage_sessions():
    st.sidebar.header('Session Configuration')

    # Initialize session state
    if 'current_session' not in st.session_state:
        generate_new_session()  # Generate the first session when the app starts

    # Button to create a new session
    if st.sidebar.button('Generate New Session'):
        generate_new_session()

    # Select chat session from history
    if 'sessions' in st.session_state:
        for session in st.session_state.sessions:
            if st.sidebar.button(f"Show chat for session {session}"):
                st.session_state.current_session = session

    # Display the current session_id
    st.subheader(f"Current session: {st.session_state.current_session}")


def manage_history():
    # current session history from Redis
    history_ = history.get_session_history(st.session_state.current_session)

    st.session_state.chat_history = history_.messages

    # Update conversation for current session
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)


def create_conversation():
    llm = builder.build_llm(st.session_state.llm_config)
    parser = StrOutputParser()
    chain_limiters = []
    if st.session_state.chain_config.limit_history:
        chain_limiters.append(
            limiters.get_history_trimmer(
                llm,
                st.session_state.prompt_config.history_key,
                st.session_state.chain_config.history_max_tokens,
            )
        )
    if st.session_state.chain_config.limit_context:
        chain_limiters.append(
            limiters.get_context_trimmer(
                llm,
                st.session_state.prompt_config.context_key,
                st.session_state.chain_config.context_max_tokens,
            )
        )

    chain_ = builder.build_chain(
        llm=llm,
        prompt=st.session_state.prompt_config.prompt,
        parser=parser,
        limiters=chain_limiters,
    )

    chain_with_history = builder.build_chain_with_history(
        chain=chain_,
        get_session_history=history.get_session_history,
        input_messages_key=st.session_state.prompt_config.input_key,
        history_messages_key=st.session_state.prompt_config.history_key,
    )

    conversation = Conversation(
        session_id=st.session_state.current_session,
        chain=chain_with_history,
    )
    return conversation


def manage_conversation():
    conversation = create_conversation()
    context_repository = SearchContext()

    user_query = st.chat_input(placeholder="Ask me anything!")

    if user_query:
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            st.write_stream(
                conversation.generate_stream(
                    input_={
                        st.session_state.prompt_config.input_key: user_query,
                        st.session_state.prompt_config.context_key: context_repository.generate_context(user_query),
                    },
                )
            )


if __name__ == '__main__':
    manage_sessions()
    manage_history()
    manage_configs()
    manage_conversation()
