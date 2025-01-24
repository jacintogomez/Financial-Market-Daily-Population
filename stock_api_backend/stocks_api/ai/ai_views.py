from django.shortcuts import render
from dotenv import load_dotenv
from decouple import config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import requests
import json
load_dotenv()

api_key=os.getenv('OPENAI_API_KEY')
fmp_key=config('FMP_API_KEY')
fundamental_url='https://financialmodelingprep.com/api/v3/quotes/index?apikey='
news_url='https://financialmodelingprep.com/api/v3/stock_news?tickers=AAPL,FB&page=3&from=2024-01-01&to=2024-03-01&apikey='
fx_url=''
acquisitions_url='https://financialmodelingprep.com/api/v4/mergers-acquisitions-rss-feed?page=0&apikey='

def ai_summary(request):
    llm=ChatOpenAI()
    fundamentals=requests.get(fx_url+fmp_key).json()
    formatted_data=json.dumps(fundamentals,indent=4)
    #task=f'Based on the received json data, please give a general summary of the market so far today\n{formatted_data}'
    #task=f'Please give a general summary of the merges and acquisitions this week\n{formatted_data}'
    task=f'Please give a general summary of the relevant financial news stories today\n{formatted_data}'

    prompt = ChatPromptTemplate.from_template("You are an expert financial analyst. {input}")

    output_parser=StrOutputParser()
    chain= prompt | llm | output_parser
    ai_response={'summary':chain.invoke({'input':task})}
    print(ai_response['summary'])
    return render(request,'ai_summary.html',ai_response)