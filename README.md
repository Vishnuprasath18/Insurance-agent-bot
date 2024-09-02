AI Insurance Agent Bot
Overview
AI Insurance Agent Bot is a Streamlit-based application that uses NeuralDB and OpenAI's GPT-3.5-turbo model to provide intelligent answers to insurance-related queries. This chatbot helps users understand their options by delivering accurate and relevant information about various insurance plans.

Features
PDF Document Ingestion: Uploads and processes PDF documents to extract relevant information.
Intelligent Query Handling: Generates multiple search queries based on user input and retrieves relevant references.
Reciprocal Rank Fusion: Reranks the search results using a reciprocal rank fusion technique.
Concise Answer Generation: Generates short, informative responses to user queries using OpenAI's GPT-3.5-turbo.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/ai-insurance-agent-bot.git
cd ai-insurance-agent-bot
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Download NLTK data: The app uses the NLTK library to tokenize text. Ensure that the necessary data is downloaded:

python
Copy code
import nltk
nltk.download("punkt")
Set up your API keys:

ThirdAI License Key: Replace the placeholder "THIRDAI" with your actual ThirdAI license key.
OpenAI API Key: Replace the placeholder os.environ["OPENAI_API_KEY"] with your actual OpenAI API key.
Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Upload your PDF documents: The app can process insurance-related PDFs to extract information.

Ask your questions: Enter your insurance-related questions in the text input field, and the bot will provide concise, informative answers.

Code Structure
app.py: The main Streamlit app script.
requirements.txt: Contains the required Python packages for the project.
README.md: Project documentation.
Configuration
PDF Files: Place your PDF documents in the specified directory.
API Keys: Ensure your ThirdAI and OpenAI API keys are correctly set up.
Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Streamlit
ThirdAI
OpenAI
