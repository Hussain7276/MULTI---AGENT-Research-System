from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily= TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str: #query str input lega or string hi output krega
    """Search the web for recent and reliable information on a topic. Returns Titles,URLs and snippets."""
    results=tavily.search(query=query,max_results=5)
    # return results
#print(web_search.invoke("who won the ind vs nz match today?")) 
    out=[] #yeah humne islye kiya takkai result aike structure format mai ajai 
    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
    return "\n----\n".join(out)    
#print(web_search.invoke("who won the ind vs nz match today?"))#for our testing  

@tool
def scrape_url(url : str) -> str:
    """Scrape and return clean text content from a give URL for deeper reading """
    try:#kisi url ko hit krna chahai or wo hit na hoo tou
        response=requests.get(url, timeout=8, headers={"User-Agent" : "Mozilla/5.0"})
        soup =BeautifulSoup(response.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose() #in sb ko hata dia hai kio ke yea hammai nhi chahiyai 
        return soup.getText(separator="",strip=True)[:3000]
    except Exception as e:
        return f"could not escape URL: {str(e)}"
#print(scrape_url.invoke("https://www.youtube.com/watch?v=sWfh1CHeJCc")) # for testing