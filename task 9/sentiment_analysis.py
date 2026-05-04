import PyPDF2
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Extract text from PDF
pdf_path = 'put_your_pdf_file_here.pdf'
#if you want your sentiment to be read from a pdf
try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        
        print(f"Total pages: {len(pdf_reader.pages)}\n")
        print("=" * 80)
        print("EXTRACTING TEXT FROM PDF")
        print("=" * 80)
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text += page_text + '\n'
            print(f"Page {page_num + 1} extracted successfully")
        
        print("\n" + "=" * 80)
        print("EXTRACTED TEXT")
        print("=" * 80)
        print(text[:1000] + "..." if len(text) > 1000 else text)
        
        # Sentiment Analysis using TextBlob
        print("\n" + "=" * 80)
        print("SENTIMENT ANALYSIS - TextBlob")
        print("=" * 80)
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        print(f"Polarity: {polarity:.4f} (Range: -1 to 1)")
        print(f"  -1: Very Negative")
        print(f"  0: Neutral")
        print(f"  1: Very Positive")
        print(f"\nSubjectivity: {subjectivity:.4f} (Range: 0 to 1)")
        print(f"  0: Very Objective")
        print(f"  1: Very Subjective")
        
        if polarity > 0.1:
            sentiment_label = "POSITIVE"
        elif polarity < -0.1:
            sentiment_label = "NEGATIVE"
        else:
            sentiment_label = "NEUTRAL"
        
        print(f"\nOverall Sentiment: {sentiment_label}")
        
        # Sentiment Analysis using VADER
        print("\n" + "=" * 80)
        print("SENTIMENT ANALYSIS - VADER (Valence Aware Dictionary and sEntiment Reasoner)")
        print("=" * 80)
        
        sia = SentimentIntensityAnalyzer()
        vader_scores = sia.polarity_scores(text)
        
        print(f"Positive: {vader_scores['pos']:.4f}")
        print(f"Negative: {vader_scores['neg']:.4f}")
        print(f"Neutral: {vader_scores['neu']:.4f}")
        print(f"Compound Score: {vader_scores['compound']:.4f} (Range: -1 to 1)")
        
        # Sentence-level sentiment analysis
        print("\n" + "=" * 80)
        print("SENTENCE-LEVEL SENTIMENT ANALYSIS")
        print("=" * 80)
        
        sentences = blob.sentences
        print(f"\nTotal sentences: {len(sentences)}\n")
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for idx, sentence in enumerate(sentences[:10]):  # Show first 10 sentences
            sent_blob = TextBlob(str(sentence))
            polarity = sent_blob.sentiment.polarity
            
            if polarity > 0.1:
                label = "POSITIVE"
                positive_count += 1
            elif polarity < -0.1:
                label = "NEGATIVE"
                negative_count += 1
            else:
                label = "NEUTRAL"
                neutral_count += 1
            
            print(f"Sentence {idx + 1} [{label}] (Polarity: {polarity:.4f})")
            print(f"  \"{str(sentence)[:100]}...\"")
        
        print(f"\nSummary of first 10 sentences:")
        print(f"  Positive: {positive_count}")
        print(f"  Negative: {negative_count}")
        print(f"  Neutral: {neutral_count}")
        
except FileNotFoundError:
    print(f"Error: PDF file not found at {pdf_path}")
except Exception as e:
    print(f"Error: {str(e)}")
    print("\nMake sure you have installed required packages:")
    print("pip install PyPDF2 textblob nltk")
