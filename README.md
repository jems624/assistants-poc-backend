# Assistant Chat Frontend

Backend component for chatting with OpenAI Assitant

## Installation

This project was developed using Python 3.11.7. YMMV with other versions of Python.

It is recommended to use a virtual environment to install the project's dependencies. To install the project's dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Additionally you will need a `.env` file with the following variables:

- OPENAI_API_KEY - Your API key for OpenAI
- OPENAI_ASSISTANT_ID - The ID of the OpenAI Assistant you want to use
- BROWSERLESS_TOKEN - Your API key for Browserless. This is used to download the contents of webpages.
- SERPAPI_API_KEY - Your API key for SerpAPI. This is used to get the top search results for a query.

```bash
OPENAI_API_KEY = ""
OPENAI_ASSISTANT_ID = ""
BROWSERLESS_TOKEN = ""
SERPAPI_API_KEY = ""
```

To use the `download_webpage` function, your assistant will need to have a `download_webpage` function with the following parameters:

```JSON
{
  "name": "download_webpage",
  "description": "Downloads the rendered HTML content of a webpage",
  "parameters": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "description": "The URL of the webpage to download"
      }
    },
    "required": [
      "url"
    ]
  }
}
```

To use the `get_search_results` function, your assistant will need to have a `get_search_results` function with the following parameters:

```JSON
{
  "name": "get_search_results",
  "description": "Get a list of search results for a given set of keywords. The search results will be in JSON format",
  "parameters": {
    "type": "object",
    "properties": {
      "keywords": {
        "type": "string",
        "description": "Keyword or keywords to search for"
      }
    },
    "required": [
      "keywords"
    ]
  }
}
```

## Usage

To run the project, run the following command:

```bash
python main.py
```

You can access the OpenAPI documentation for the project at `http://localhost:8000/docs`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
