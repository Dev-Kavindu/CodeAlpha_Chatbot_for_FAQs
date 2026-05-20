---
title: DeepScholar-AI
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
python_version: "3.10"
---

# 🧠 DeepScholar AI: Multi-Modal RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot that provides intelligent answers about Deep Learning concepts using a knowledge base built from premium textbooks. The system combines LangChain, Groq (Llama 3), Chroma vector database, and Gradio with Text-to-Speech capabilities.

## ✨ Features

- **Multi-Modal RAG System**: Retrieves relevant information from both text and image descriptions
- **Powered by Llama 3**: Uses Groq's high-performance Llama 3.1-8B-Instant model for fast, accurate responses
- **Vector Database**: ChromaDB with HuggingFace embeddings (all-MiniLM-L6-v2) for efficient semantic search
- **Text-to-Speech**: Edge-TTS integration for audio responses with natural voice output
- **Interactive UI**: Modern Gradio interface with custom theming
- **Auto-Cleanup**: Background thread automatically removes old audio files to manage disk space
- **Production-Ready**: Optimized for Hugging Face Spaces deployment

## 📚 Knowledge Base

The AI is grounded on the following textbooks:

1. **Artificial Intelligence For Dummies** - John Paul Mueller & Luca Massaron
2. **Grokking Deep Learning** - Andrew W. Trask
3. **TensorFlow 2.0 Pocket Primer** - Oswald Campesato

## 🛠️ Tech Stack

- **Framework**: LangChain
- **LLM**: Groq (Llama 3.1-8B-Instant)
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **UI**: Gradio
- **Text-to-Speech**: Edge-TTS
- **Python**: 3.8+

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API Key ([Get one here](https://console.groq.com/))

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "Chatbot for FAQs"
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the project root
echo "GROQ_API_KEY=your_api_key_here" > .env
```

5. Ensure the vector database exists:
   - The `my_vector_db` directory should contain your pre-built Chroma database
   - If you need to build it from scratch, use the notebook `notebooks/task 01.ipynb`

6. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:7860`

## 🚀 Deployment on Hugging Face Spaces

### Prerequisites

- Hugging Face account
- Groq API Key

### Steps

1. **Create a new Space**:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Select a hardware tier (CPU Basic is sufficient)

2. **Upload files**:
   - Upload `app.py`
   - Upload `requirements.txt`
   - Upload the `my_vector_db` directory (essential for RAG functionality)
   - Create a `.env` file with your `GROQ_API_KEY` (add as a secret in Space settings)

3. **Set Secrets**:
   - Go to your Space settings
   - Add a new secret: `GROQ_API_KEY` with your API key value

4. **Deploy**:
   - The Space will automatically build and deploy
   - Once ready, your app will be accessible at the Space URL

## 📁 Project Structure

```
Chatbot for FAQs/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (not committed)
├── my_vector_db/              # Chroma vector database (pre-built)
├── knowledge-base/            # Source PDF textbooks
└── notebooks/
    └── task 01.ipynb          # Development notebook
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

### Vector Database

The application loads a pre-built Chroma database from the `my_vector_db` directory. To rebuild or modify the database:

1. Use the notebook `notebooks/task 01.ipynb`
2. Follow the cells marked for database creation
3. The database will be saved to `my_vector_db`

## 🎯 Usage

1. **Ask a Question**: Type your question about Deep Learning concepts in the input field
2. **Get Answers**: The AI retrieves relevant information from the knowledge base and generates a comprehensive response
3. **Listen to Audio**: Enable the audio feature to hear the response spoken aloud
4. **Explore**: The system provides context from the textbooks, including references to diagrams and figures

## 🧹 Maintenance

### Audio Cleanup

The application includes a background thread that automatically:
- Checks for `.mp3` and `.wav` files every 5 minutes
- Deletes files older than 1 hour
- Helps manage disk space on deployment platforms

### Monitoring

- Check the console logs for database loading status
- Monitor audio cleanup operations
- Track API usage through Groq dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is for educational purposes. Please respect the copyright of the textbooks used in the knowledge base.

## 🙏 Acknowledgments

- **LangChain** for the RAG framework
- **Groq** for providing fast LLM inference
- **HuggingFace** for embeddings and model hosting
- **Gradio** for the UI framework
- **Edge-TTS** for text-to-speech capabilities

## 📞 Support

For issues or questions, please open an issue in the repository.

---

<div align="center">

## 👨‍💻 Developer

**Developed by [Kavindu Chamod](https://github.com/Dev-Kavindu)**

*AI Engineering Project*

<br>

### 🔗 Connect with Me

[![GitHub](https://img.shields.io/badge/GitHub-Dev--Kavindu-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dev-Kavindu)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kavindu--chamod--7159a1235-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kavindu-chamod-7159a1235)
[![Email](https://img.shields.io/badge/Email-kchamod1124@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kchamod1124@gmail.com)

<br>

**Built with ❤️ for Deep Learning education**

</div>
