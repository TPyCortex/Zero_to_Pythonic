import string
import re
import os
from collections import Counter

# --- Configuration ---
# Change this to your actual file path
TRANSCRIPT_FILE_PATH = "sample_transcript.txt"
# Alternative examples:
# Windows: "C:/Users/yourname/Documents/Meeting1.txt"
# Mac: "/Users/yourname/Desktop/Meeting1.txt"
# Linux: "/home/yourname/documents/Meeting1.txt"

def load_transcript():
    """Load transcript from file path with error handling."""
    try:
        if not os.path.exists(TRANSCRIPT_FILE_PATH):
            print(f"Error: File not found at {TRANSCRIPT_FILE_PATH}")
            print("Please update TRANSCRIPT_FILE_PATH in the script with your actual file location.")
            return ""
        
        with open(TRANSCRIPT_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print("Warning: File appears to be empty.")
            return content
            
    except PermissionError:
        print(f"Error: Permission denied accessing {TRANSCRIPT_FILE_PATH}")
        return ""
    except Exception as e:
        print(f"Error loading file: {e}")
        return ""

def clean_and_tokenize(text):
    """Remove punctuation and convert to lowercase tokens."""
    # Remove timestamps first (format: 00:00:00)
    text = re.sub(r'\d{1,2}:\d{2}:\d{2}', '', text)
    # Remove speaker names (format: **Name:** or Name:)
    text = re.sub(r'\*\*[^:]+:\*\*|\b[A-Z][a-zA-Z\s]+:', '', text)
    
    translator = str.maketrans("", "", string.punctuation)
    return text.lower().translate(translator).split()

def filter_stopwords(words):
    """Remove common English stopwords."""
    stopwords = {
        "the", "and", "is", "in", "to", "of", "that", "a", "on", "for", 
        "it", "with", "as", "this", "at", "by", "an", "be", "or", "from", 
        "so", "are", "was", "were", "have", "has", "had", "but", "not", 
        "they", "we", "you", "i", "me", "my", "he", "she", "his", "her",
        "can", "will", "would", "could", "should", "do", "did", "does"
    }
    return [w for w in words if w not in stopwords and len(w) > 2]

def word_frequencies(filtered_words):
    """Calculate word frequency distribution."""
    return Counter(filtered_words)

def split_sentences(text):
    """Split text into sentences with improved logic."""
    # Remove timestamps and speaker labels first
    text = re.sub(r'\d{1,2}:\d{2}:\d{2}', '', text)
    text = re.sub(r'\*\*[^:]+:\*\*', '', text)
    
    # Split on sentence endings but avoid common abbreviations
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\!|\?)\s+', text)
    
    # Filter out very short sentences and clean up
    return [s.strip() for s in sentences if len(s.strip()) > 15]

def score_sentences(sentences, word_freq):
    """Score sentences based on word frequency and length."""
    scores = {}
    for sentence in sentences:
        words = clean_and_tokenize(sentence)
        filtered_words = filter_stopwords(words)
        
        # Calculate score as sum of word frequencies
        raw_score = sum(word_freq.get(w, 0) for w in filtered_words)
        
        # Normalize by sentence length to avoid bias toward long sentences
        word_count = len(filtered_words)
        if word_count > 0:
            normalized_score = raw_score / word_count
            scores[sentence] = normalized_score
            
    return scores

def summarize(text, top_n=3):
    """Generate summary by extracting top-scoring sentences."""
    if not text.strip():
        return []
        
    words = clean_and_tokenize(text)
    filtered_words = filter_stopwords(words)
    
    if not filtered_words:
        return []
        
    word_freq = word_frequencies(filtered_words)
    sentences = split_sentences(text)
    
    if not sentences:
        return []
        
    sentence_scores = score_sentences(sentences, word_freq)
    
    if not sentence_scores:
        return []
        
    # Return top N sentences sorted by score
    return sorted(sentence_scores.keys(), key=sentence_scores.get, reverse=True)[:top_n]

def extract_action_items(text):
    """Extract potential action items using pattern matching."""
    action_patterns = [
        r"I'll\s+\w+.*",
        r"we'll\s+\w+.*", 
        r"let's\s+\w+.*",
        r"going to\s+\w+.*",
        r"need to\s+\w+.*",
        r"have to\s+\w+.*",
        r"should\s+\w+.*",
        r"will\s+\w+.*",
        r"must\s+\w+.*",
        r"action item.*",
        r"follow up.*",
        r"next step.*",
        r"to do.*",
        r"homework.*"
    ]
    
    actions = []
    sentences = split_sentences(text)
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for pattern in action_patterns:
            if re.search(pattern, sentence_lower):
                actions.append(sentence)
                break  # Avoid duplicate matches
                
    return actions

def extract_key_topics(text, top_n=5):
    """Extract most frequently mentioned topics."""
    words = clean_and_tokenize(text)
    filtered_words = filter_stopwords(words)
    word_freq = word_frequencies(filtered_words)
    
    # Get top N most frequent words
    return [word for word, count in word_freq.most_common(top_n)]

def extract_participants(text):
    """Extract participant names from transcript."""
    # Look for speaker patterns: **Name:** or Name:
    speaker_pattern = r'\*\*([^:]+):\*\*|^([A-Z][a-zA-Z\s]+):'
    matches = re.findall(speaker_pattern, text, re.MULTILINE)
    
    # Flatten the tuple results and remove empty strings
    speakers = set()
    for match in matches:
        speaker = match[0] if match[0] else match[1]
        if speaker.strip():
            speakers.add(speaker.strip())
    
    return list(speakers)

def main():
    """Main function to run the transcript analysis."""
    print("=== Meeting Transcript Analyzer ===\n")
    
    # Load transcript
    print(f"Loading transcript from: {TRANSCRIPT_FILE_PATH}")
    transcript = load_transcript()
    
    if not transcript:
        print("Failed to load transcript. Exiting.")
        return
    
    print(f"Transcript loaded successfully ({len(transcript)} characters)\n")
    
    # Extract participants
    participants = extract_participants(transcript)
    if participants:
        print("--- Participants ---")
        for participant in sorted(participants):
            print(f"- {participant}")
        print()
    
    # Generate summary
    print("--- Meeting Summary ---")
    summary_sentences = summarize(transcript, top_n=3)
    if summary_sentences:
        for i, sentence in enumerate(summary_sentences, 1):
            print(f"{i}. {sentence.strip()}")
    else:
        print("Could not generate summary from transcript.")
    print()
    
    # Extract action items
    print("--- Action Items ---")
    action_items = extract_action_items(transcript)
    if action_items:
        for i, action in enumerate(action_items, 1):
            print(f"{i}. {action.strip()}")
    else:
        print("No clear action items found.")
    print()
    
    # Extract key topics
    print("--- Key Topics Discussed ---")
    key_topics = extract_key_topics(transcript, top_n=5)
    if key_topics:
        print(", ".join(key_topics))
    else:
        print("Could not identify key topics.")
    print()
    
    print("=== Analysis Complete ===")

if __name__ == "__main__":
    main()