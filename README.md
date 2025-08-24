# :book: English Guidelines Agent

Application that provides detailed assessment report and modifies documents based on given guidelines.

LLM used: Llama3.2:3b via Ollama (running locally!)

Framework used: LangGraph

## Screenshots

![Screenshot ](examples/Example%20-%20Assessing%20resume%20Part%20I.png)

![Screenshot 2](examples/Example%20-%20Assessing%20resume%20Part%20II.png)

## Setup

1. Clone the repository:
```bash
$ git clone https://github.com/AvneeshAFC/English-Guidelines-Agent.git
$ cd English-Guidelines-Agent
```

2. Install dependencies:
```bash
$ pip install -r requirements.txt
```

3. Run the application:
```bash
$ python src/main.py
$ streamlit run src/ui.py
```

## API Endpoints

![FastAPI Endpoints](examples/FastAPI%20Endpoints.png)

1. Assess Document
```bash
POST /assess/
```

2. Modify Document
```bash
POST /modify/
```

## Parameters

1. file: The document to be assessed or modified (PDF or DOCX format).
2. guidelines: The guidelines to be used for assessment or modification.
3. request: The modification request (optional).

## Response

1. assessment_report: The assessment report for the document.
2. modified_document: The modified document (optional).
3. error: Error message (optional).
