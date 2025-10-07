🎧 Advanced Podcast Summarizer & Analyzer 🔬

An intelligent podcast analysis web app built with **Streamlit**, **AssemblyAI**, **ListenNotes API**, and **spaCy NLP**.  
This tool automatically fetches podcast audio, generates transcripts, summarizes chapters, detects entities, and analyzes sentiment — all in one dashboard.

---

🚀 Features

✅ Fetch podcast metadata directly from **ListenNotes**  
✅ Generate **automatic transcripts** using **AssemblyAI**  
✅ Split podcast into **auto-chapters** with summaries  
✅ Perform **NLP analysis**:
- 🧠 Chapter Summarization (via `pytextrank`)
- ❤️ Sentiment Detection (via `spacytextblob`)
- 🏷️ Named Entity Recognition (via `spaCy`)

✅ View all results in an **interactive Streamlit dashboard**

---

🧩 Project Structure

```
📦 podcast-analyzer
│
├── main.py            # Streamlit frontend + NLP logic
├── api_04.py          # Handles API calls (ListenNotes + AssemblyAI)
├── api_secrets.py     # API keys (replace with your own)
└── requirements.txt   # Dependencies list
```

---

⚙️ Installation & Setup

1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/podcast-analyzer.git
cd podcast-analyzer
```

2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

🔑 Add Your API Keys

Create a file named `api_secrets.py` in the root directory and add:

```python
API_KEY_ASSEMBLYAI = "your_assemblyai_api_key"
API_KEY_LISTENNOTES = "your_listennotes_api_key"
```

> 💡 *Tip:* For production, store these keys securely as environment variables instead of hardcoding them.

---

▶️ Run the App

Start the Streamlit app:

```bash
streamlit run main.py
```

Then open the provided localhost URL in your browser.

---

💡 How It Works

1. Enter a **ListenNotes Episode ID** in the sidebar.  
   Example: `4d3fe717742d4963a85562e9f84d8c79`

2. The app:
   - Fetches podcast details (title, thumbnail, and audio URL)
   - Sends the audio to AssemblyAI for transcription
   - Waits for the transcript (with chapters)
   - Runs NLP analysis on each chapter

3. Finally, you’ll get:
   - 📚 Summarized chapters  
   - 💬 Sentiment (Positive / Neutral / Negative)  
   - 🧍 Entities (people, places, orgs, etc.)  
   - 🧾 A clean dashboard with insights

---

🧠 Technologies Used

| Technology | Purpose |
|-------------|----------|
| [Streamlit](https://streamlit.io/) | Interactive web interface |
| [spaCy](https://spacy.io/) | NLP pipeline |
| [PyTextRank](https://github.com/DerwenAI/pytextrank) | Text summarization |
| [SpacyTextBlob](https://spacytextblob.netlify.app/) | Sentiment analysis |
| [AssemblyAI](https://www.assemblyai.com/) | Audio-to-text transcription |
| [ListenNotes](https://www.listennotes.com/api/) | Podcast data and metadata |
| [Pandas](https://pandas.pydata.org/) | Data handling and display |

---

📊 Output Preview

🎙️ Podcast Details
Displays podcast cover, title, and episode name.

🧾 Summary Table
| Chapter | Start Time (s) | Sentiment | Entities Found |
|----------|----------------|------------|----------------|
| Intro | 0 | Neutral | 3 |
| Guest Talk | 245 | Positive | 5 |

🧠 Chapter Breakdown
Expandable sections showing:
- Generated summaries
- Detected named entities
- Chapter sentiment

---

🔐 Security Notes
- Never commit your real API keys to public repos.
- Use `.env` files or GitHub secrets for deployment.

---

🤝 Contributing
Contributions are welcome!  
If you’d like to add features (e.g., keyword extraction, emotion detection, etc.), feel free to fork and submit a PR.

---

🧾 License
This project is licensed under the **MIT License**.

---

💬 Author
Miti Bhatt 
Naincy Rahuja
  
Built with ❤️ for creators who love podcasts.
