from django.shortcuts import render
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()

fundamental_url=''
api_key=os.getenv('OPENAI_API_KEY')


def ai_summary(request):
    llm=ChatOpenAI()
    #task='Based on the received json data, please give a general summary of what happened in the market (so far) today'
    task='what is 2+2?'
    prompt = ChatPromptTemplate.from_template(
        "You are an elementary school kid. {input}"
    )

    output_parser=StrOutputParser()
    chain= prompt | llm | output_parser
    ai_response={'summary':chain.invoke({'input':task})}
    print(ai_response['summary'])
    return render(request,'ai_summary.html',ai_response)