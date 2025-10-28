from dotenv import load_dotenv
import json
import os
import re


load_dotenv()


def _get_groq_client():
    """Return a Groq client if GROQ_API_KEY is set, otherwise None."""
    
    try:
        from groq import Groq
    except ImportError:
        return None
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def classify_with_llm(log_message):
    """
    Generate a variant of the input sentence. For example,
    If input sentence is "User session timed out unexpectedly, user ID: 9250.",
    variant would be "Session timed out for user 9251"
    """
    
    prompt = f"""Classify the log message into one of these categories: 
    Workflow Error, Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category> </category> tags. 
    Log message: {log_message}"""
    
    groq_client = _get_groq_client()
    if groq_client is None:
        return "NOT_AVAILABLE"
    
    chat_completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    
    content = chat_completion.choices[0].message.content
    match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    category = "Unclassified"
    if match:
        category = match.group(1)
    
    return category.strip()



    