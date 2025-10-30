import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage
import requests
import json


analysing_system_prompt = """You are a log analysis expert. Your task is to analyze the provided system logs and identify any anomalies, errors, or noteworthy patterns. 
Provide a concise summary of your findings along with any recommendations for further investigation or action. Provide the results in bullet points for clarity."""

API_URL = "https://litellm-litemaas.apps.prod.rhoai.rh-aiservices-bu.com/v1/chat/completions"
API_TOKEN = "sk-LszPuMF92HVEMDjhYO4KEQ"

def log_analyser(logs):
    messages = [
        {"role": "system", "content": analysing_system_prompt},
        {"role": "user", "content": logs}
    ]

    payload = {
        "model": "Mistral-Small-24B-W8A8",
        "messages": messages,
        "temperature": 0.2,
        "stream": True
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"Sending request to {API_URL}...")
    analysis_text = ""
    try:
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status() 
        
        print("\n--- API Response (Streaming) ---")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                
                # We are looking for lines that start with "data: "
                if decoded_line.startswith('data: '):
                    data_str = decoded_line[len('data: '):].strip()
                    
                    # Check for the end-of-stream signal
                    if data_str == '[DONE]':
                        print("\n--- Stream finished ---")
                        break
                        
                    # Try to parse the JSON chunk
                    try:
                        chunk = json.loads(data_str)
                        
                        # Check if the chunk contains the content
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            content_chunk = delta.get('content')
                            
                            if content_chunk:
                                # Add the new text chunk to our full response
                                analysis_text += content_chunk
                                
                                # Yield the *entire* updated text so far
                                yield analysis_text
                                
                    except json.JSONDecodeError:
                        print(f"\nError decoding JSON chunk: {data_str}")
                        
        # This return is no longer strictly needed for the happy path,
        # but yield ensures the final state is sent.
        yield analysis_text
        
    except requests.exceptions.RequestException as e:
        # Print the error response from the server
        print("\n--- API Response (Error) ---")
        if e.response is not None:
            try:
                print(json.dumps(e.response.json(), indent=2))
            except ValueError:
                print(e.response.text)
        else:
            print(str(e))
        return "Error occurred while processing the request."

def main():
    with gr.Blocks(theme=gr.themes.Glass()) as demo:
        gr.Markdown("# Log Analysis POC")
        inp = gr.Textbox(placeholder="Enter the system logs here", label="System Logs", lines=1, max_lines=10)
        out = gr.Markdown(label="Analysis Result")
        analyze = gr.Button("Analyze Logs")
        analyze.click(fn = log_analyser, inputs = inp, outputs = out, api_name="analyse" )

    demo.launch()

if __name__ == "__main__":
    main()
