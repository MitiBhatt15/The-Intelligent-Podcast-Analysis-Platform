# --- FINAL CODE with pytextrank for Summarization ---

import streamlit as st
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
import pytextrank # New import
import api_04

st.set_page_config(layout="wide")
st.title("Advanced Podcast Analyzer 🔬")

# --- NLP Functions (Now with pytextrank for Summarization) ---
@st.cache_resource
def load_spacy_model():
    """Loads the spaCy model and adds the pytextrank and spacytextblob pipes."""
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe("textrank") # Add pytextrank to the pipeline
    nlp.add_pipe('spacytextblob')
    return nlp

nlp = load_spacy_model()

def analyze_chapter_text(text):
    """Performs NLP analysis on a chapter's text."""
    if not text or len(text.split()) < 50:
        return {'summary': 'Not enough text to generate a meaningful summary.', 'entities': [], 'sentiment': 'N/A'}
    
    doc = nlp(text)
    
    # 1. Summarization with pytextrank (extract top 3 sentences)
    summary_sentences = [sent.text for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=3)]
    summary = " ".join(summary_sentences)
    
    # 2. Named Entity Recognition
    entities = [{'text': ent.text, 'type': ent.label_} for ent in doc.ents]
    
    # 3. Sentiment Analysis
    polarity = doc._.blob.polarity
    sentiment = 'Positive' if polarity > 0.1 else 'Negative' if polarity < -0.1 else 'Neutral'
    
    return {'summary': summary, 'entities': entities, 'sentiment': sentiment}

# --- Sidebar ---
st.sidebar.header("Instructions")
st.sidebar.info("Enter a Listen Notes Episode ID to analyze.")
episode_id = st.sidebar.text_input("Episode ID")

if st.sidebar.button("Analyze Episode"):
    st.session_state.clear()
    with st.spinner('Step 1/3: Fetching podcast details...'):
        details, error = api_04.get_episode_details(episode_id)
    if error: st.error(error)
    else:
        with st.spinner('Step 2/3: Transcribing audio...'):
            transcript, error = api_04.get_full_transcript_data(details['audio'])
        if error: st.error(error)
        else:
            with st.spinner('Step 3/3: Analyzing chapters...'):
                # Helper function to extract text for each chapter
                def get_text_for_chapters(chapters, words):
                    chapter_texts = {}
                    for chap in chapters:
                        start, end = chap['start'], chap['end']
                        chapter_words = [word['text'] for word in words if start <= word['start'] < end]
                        chapter_texts[chap['gist']] = ' '.join(chapter_words)
                    return chapter_texts

                chapter_texts = get_text_for_chapters(transcript.get('chapters', []), transcript.get('words', []))
                
                chapter_analysis = []
                for chap in transcript.get('chapters', []):
                    gist = chap['gist']
                    analysis = analyze_chapter_text(chapter_texts.get(gist, ''))
                    chapter_analysis.append({
                        'Chapter': gist,
                        'Start Time (s)': chap['start'] // 1000,
                        'Summary': analysis['summary'],
                        'Sentiment': analysis['sentiment'],
                        'Entities': analysis['entities'],
                        'Entities Found': len(analysis['entities'])
                    })
            st.session_state.analysis = chapter_analysis
            st.session_state.details = details

# --- Display Results ---
if 'analysis' in st.session_state:
    details = st.session_state.details
    analysis_df = pd.DataFrame(st.session_state.analysis)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.header(details['podcast']['title'])
        st.subheader(details['title'])
        st.image(details['thumbnail'], width=250)

    with col2:
        st.header("Analysis Dashboard")
        
        summary_table = analysis_df[['Chapter', 'Start Time (s)', 'Sentiment', 'Entities Found']]
        st.dataframe(summary_table)

        st.header("Detailed Chapter Breakdown")
        for index, row in analysis_df.iterrows():
            with st.expander(f"{row['Chapter']} ({row['Sentiment']})"):
                st.subheader("Chapter Summary")
                st.write(row['Summary'])
                
                st.subheader("Entities Found in this Chapter")
                if row['Entities']:
                    for ent in row['Entities']:
                        st.markdown(f"- **{ent['text']}** ({ent['type']})")
                else:
                    st.write("No entities detected in this chapter.")