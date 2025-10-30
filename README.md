# Log Analysis POC

This project is a Proof of Concept (POC) for a log analysis tool. It uses a large language model to analyze system logs and provide a summary of any anomalies, errors and improvements.

## Setup

To set up this project on your local system, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GauravASY/IPSec_Tunnel_Agent.git
   cd IPSec_Tunnel_Agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file:**
   Create a file named `.env` in the root directory of the project and add the following environment variables:
   ```
   API_URL=<your_api_url>
   API_TOKEN=<your_api_token>
   ```

## Usage

To run the application, execute the following command:
```bash
python main.py
```
This will launch a Gradio interface in your web browser.

## Requirements

The project requires the following Python libraries:

- `dotenv>=0.9.9`
- `gradio>=5.49.1`
- `langchain>=1.0.2`
- `langchain-core>=1.0.1`
- `requests>=2.32.5`
