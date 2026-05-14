import os
import glob
import time
import uuid
import threading
import asyncio
from datetime import datetime, timedelta

from dotenv import load_dotenv
import edge_tts
from groq import Groq
import gradio as gr

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load environment variables
load_dotenv(override=True)

# Configuration
TEXT_MODEL = "llama-3.1-8b-instant"
persist_folder = "my_vector_db"

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")
client = Groq(api_key=api_key)

# Load embedding model
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load existing Chroma database
print(f"Loading vector database from {persist_folder}...")
vector_db = Chroma(
    persist_directory=persist_folder,
    embedding_function=embeddings
)

# --- DEBUGGING PRINTS ---
# මෙතනින් අපිට බලාගන්න පුළුවන් DB එක ඇතුළේ ඇත්තටම documents තියෙනවද කියලා
try:
    doc_count = vector_db._collection.count()
    print(f"✅ Database loaded successfully!")
    print(f"🔍 DEBUG - Total documents in database: {doc_count}")
    if doc_count == 0:
        print("⚠️ WARNING: The database is EMPTY! Please make sure you uploaded the 'my_vector_db' folder to the space.")
except Exception as e:
    print(f"⚠️ DEBUG - Could not count documents: {e}")


# --- Background Audio Cleanup Thread ---
def cleanup_old_audio_files():
    """
    Background thread that periodically checks the temporary directory
    and deletes .mp3 or .wav files older than 1 hour.
    """
    while True:
        try:
            current_time = datetime.now()
            temp_dir = os.getcwd()  
            
            for ext in ['*.mp3', '*.wav']:
                pattern = os.path.join(temp_dir, ext)
                for file_path in glob.glob(pattern):
                    try:
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if current_time - file_time > timedelta(hours=1):
                            os.remove(file_path)
                            print(f"Deleted old audio file: {file_path}")
                    except Exception as e:
                        pass  
        except Exception as e:
            pass  
        
        time.sleep(300)

# Start the cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_audio_files, daemon=True)
cleanup_thread.start()
print("✅ Audio cleanup thread started")


# --- Chatbot Response Function (Made fully Async) ---
async def chatbot_response(user_query):
    try:
        # Retrieve top 5 relevant documents from vector database
        docs = vector_db.similarity_search(user_query, k=5)
        
        # --- DEBUGGING PRINT ---
        print(f"🔍 DEBUG - Retrieved {len(docs)} documents for query: '{user_query}'")
        
        # Build context from retrieved documents
        context_parts = []
        for d in docs:
            source = os.path.basename(d.metadata.get('source', 'Unknown'))
            content_type = d.metadata.get('type', 'text')
            context_parts.append(f"[{content_type} from {source}]: {d.page_content}")
        
        context = "\n\n".join(context_parts)
        
        # --- DEBUGGING PRINT ---
        print(f"🔍 DEBUG - Context passed to AI:\n{context[:500]}...\n(Truncated for logs)")

        # System prompt for the AI
        system_prompt = f"""You are an expert AI Educator specialized in Deep Learning. Your goal is to explain complex concepts from the provided book context in a clear, conversational, and highly understandable manner.

        Follow these instructions strictly:
        1. **Analyze and Synthesize**: Do not just copy-paste text from the context. Read the provided excerpts and explain the underlying concept as if you are teaching a student.
        2. **Explain the 'Why' and 'How'**: When a concept or function (like tf.constant) is mentioned, explain why it is used and how it works according to the book's logic.
        3. **Incorporate Visuals**: If the context includes image descriptions (e.g., Figure X), refer to them naturally in your explanation (e.g., "As illustrated in the diagram of the neural network...").
        4. **Tone**: Maintain a professional yet accessible tone. Use analogies if they help clarify the book's points.
        5. **Grounding**: Ensure your explanation is rooted in the provided books. If you add general knowledge to improve clarity, make sure it does not contradict the book's content.
        6. **Structure**: Use bullet points and bold text to highlight key terms and make the answer easy to scan.

        Context from Books:
        {context}

        If the context does not contain enough information, state that clearly but provide a helpful explanation based on general AI principles."""
        
        # Generate response using Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model=TEXT_MODEL,
        )
        
        answer = chat_completion.choices[0].message.content
        
        # Generate audio using edge-tts (proper async await)
        unique_id = str(uuid.uuid4())
        audio_file = f"speech_{unique_id}.mp3"
        
        communicate = edge_tts.Communicate(answer, "en-US-AndrewNeural")
        await communicate.save(audio_file)  # Changed from asyncio.run to await
        
        return answer, audio_file
        
    except Exception as e:
        print(f"❌ ERROR in chatbot_response: {e}")
        return f"Error occurred: {str(e)}", None


# --- Gradio UI ---
custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("<h1 style='text-align: center;'>🧠 DeepScholar AI: Multi-Modal RAG</h1>")
    gr.Markdown("<p style='text-align: center; font-size: 16px;'>Explore AI concepts with visual and textual knowledge from premium deep learning books.</p>")
    
    with gr.Accordion("📚 Knowledge Base (Powered by RAG)", open=False):
        gr.Markdown("""
        **This AI is grounded on the following textbooks:**
        1. *Artificial Intelligence For Dummies* - John Paul Mueller & Luca Massaron
        2. *Grokking Deep Learning* - Andrew W. Trask
        3. *TensorFlow 2.0 Pocket Primer* - Oswald Campesato
        """)
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(
                label="Ask your question:",
                placeholder="e.g., Explain the structure of a neural network...",
                lines=4
            )
            ask_btn = gr.Button("Generate Answer 🚀", variant="primary")
            
            gr.Markdown("<br>### 🎧 Audio Response")
            audio_output = gr.Audio(label="Listen to Answer")
            
        with gr.Column(scale=2):
            text_output = gr.Textbox(
                label="AI Response",
                placeholder="The generated answer will appear here...",
                interactive=False,
                lines=18
            )

    ask_btn.click(
        fn=chatbot_response,
        inputs=query_input,
        outputs=[text_output, audio_output]
    )


# --- Launch Application ---
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)