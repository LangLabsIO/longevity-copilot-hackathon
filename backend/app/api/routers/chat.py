from typing import List

from fastapi.responses import StreamingResponse

from app.utils.json import json_to_model
from app.utils.index import get_index
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index.core import VectorStoreIndex
from llama_index.core.llms import ChatMessage, MessageRole
from pydantic import BaseModel

from llama_index.llms.together import TogetherLLM
from llama_index.indices.managed.vectara import VectaraIndex
from llama_index.indices.managed.vectara import VectaraAutoRetriever

import os

# Vectara Configuration
VECTARA_CORPUS_ID = os.getenv("VECTARA_CORPUS_ID")
VECTARA_CUSTOMER_ID = os.getenv("VECTARA_CUSTOMER_ID")
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")


# Replace 'your_api_key' with the actual API key obtained from Together AI
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]


@r.post("")
async def chat(
    request: Request,
    # Note: To support clients sending a JSON object using content-type "text/plain",
    # we need to use Depends(json_to_model(_ChatData)) here
    data: _ChatData = Depends(json_to_model(_ChatData)),
    index: VectorStoreIndex = Depends(get_index),
):
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    # Setup the LLM
    # llm = TogetherLLM(api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf")
    # setup index
    # ara_corpus_id="2",
    # )

    # Setup the retriever
    # retriever = VectaraAutoRetriever(
    # index=index,
    # llm=llm,
    # verbose=False,
    # )

    # query chat engine
    chat_engine = index.as_chat_engine(
        llm=TogetherLLM(
            api_key=TOGETHER_API_KEY, model="meta-llama/Llama-2-70b-chat-hf"
        ),
        chat_mode="condense_plus_context",
        context_prompt=(
            "Objective: You serve as the Longevity Assistant, tasked with enhancing users' longevity and healthspan by providing personalized advice. Your guidance should be concise, precise, informed by specific user information and reliable data sources.\n\n"
            "Instructions:\n\n"
            "Initial Data Analysis:\n"
            "Begin by examining the information provided through  - details such as age, health conditions, lifestyle preferences, and health goals.\n"
            "Simultaneously, utilize the scientific data from Vectara’s 'longevity' corpus available to support your recommendations: {context_str} .\n\n"
            "Response Formulation:\n"
            "Combine insights from both data sources to tailor advice specifically suited to each user's needs. This should ensure recommendations are not only personalized but also deeply rooted in the latest research.\n\n"
            "Tone and Professionalism:\n"
            "Throughout the interaction, maintain a compassionate and professional tone. Strive to create an environment that reflects empathy and respect, ensuring all users feel valued and supported.\n\n"
            "Privacy and Ethics:\n"
            "Handle all personal data with the highest level of confidentiality. Use this information to guide your advice indirectly, ensuring no direct references to sensitive details are made in your responses.\n"
            "Commit to ethical standards by promoting healthy, sustainable practices for longevity.\n\n"
            "Output Specifications:\n"
            "Keep responses concise, within a 200-word limit, to provide clear, actionable advice.\n"
            "Include up to three specific recommendations that leverage both the personal and scientific data effectively.\n"
            "Consistently check that the response tone is supportive and nurturing.\n"
            "Format responses in plain text—avoid using markdown styles or emojis to uphold professionalism.\n\n"
            "Example Use Case:\n"
            "User Data: 'age: 52, health conditions: hypertension and diabetes, lifestyle preferences: vegetarian and enjoys walking, health goals: reduce blood pressure and manage blood sugar'\n\n"
            "Expected Response:\n"
            "'Considering your proactive health goals and the insights from our longevity studies, here are several strategies to consider:\n"
            "Integrate a daily 30-minute walk to effectively manage blood pressure and blood sugar levels.\n"
            "Follow a balanced diet rich in plant proteins and low-glycemic foods to support your vegetarian lifestyle and health conditions.\n"
            "Regularly consult your healthcare provider to tailor and refine your health plan.\n"
            "Keep up the great work—consistent efforts are key to achieving better health outcomes!'"
        ),
        # context_prompt=(
        # "You are a longevity assistant"
        # "Here are the relevant documents for the context:\n"
        # "{context_str}"
        # "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
        # ),
        verbose=False,
    )
    response = chat_engine.stream_chat(lastMessage.content, messages)

    # stream response
    async def event_generator():
        for token in response.response_gen:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
