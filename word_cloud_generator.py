import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys
import os

# Try to import nltk for additional stopwords
try:
    import nltk
    from nltk.corpus import stopwords
    # Download if not present
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    nltk_stopwords = set(stopwords.words('english'))
except ImportError:
    nltk_stopwords = set()

# Combine stopwords
all_stopwords = STOPWORDS.union(nltk_stopwords)

def generate_word_cloud(text, background_color='white', colormap='viridis', max_words=100, width=800, height=400, save_path=None, min_font_size=10, max_font_size=100, relative_scaling=0.5):
    """
    Generate and display a word cloud from the given text.

    Parameters:
    - text: The input text
    - background_color: Background color of the word cloud
    - colormap: Color map for the words
    - max_words: Maximum number of words to include
    - width: Width of the word cloud image
    - height: Height of the word cloud image
    - save_path: Path to save the word cloud image (optional)
    - min_font_size: Minimum font size for single-occurrence words
    - max_font_size: Maximum font size for frequently occurring words
    - relative_scaling: How much font size scales with word frequency (0.1-1.0)
    """
    wordcloud = WordCloud(
        stopwords=all_stopwords,
        background_color=background_color,
        colormap=colormap,
        max_words=max_words,
        width=width,
        height=height,
        min_font_size=min_font_size,  # Smaller font for single words
        max_font_size=max_font_size,  # Larger font for frequent words
        relative_scaling=relative_scaling  # Controls frequency scaling
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    if save_path:
        wordcloud.to_file(save_path)
        print(f"Word cloud saved to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a word cloud from text.')
    parser.add_argument('input', nargs='?', help='Path to text file (optional)')
    parser.add_argument('-o', '--output', default='wordcloud.png', help='Output image file (default: wordcloud.png)')
    parser.add_argument('--bg', default='white', help='Background color (default: white)')
    parser.add_argument('--cmap', default='viridis', help='Colormap (default: viridis)')
    parser.add_argument('--max-words', type=int, default=100, help='Maximum number of words (default: 100)')
    parser.add_argument('--width', type=int, default=800, help='Image width (default: 800)')
    parser.add_argument('--height', type=int, default=400, help='Image height (default: 400)')
    parser.add_argument('--min-font-size', type=int, default=10, help='Minimum font size for single words (default: 10)')
    parser.add_argument('--max-font-size', type=int, default=100, help='Maximum font size for frequent words (default: 100)')
    parser.add_argument('--relative-scaling', type=float, default=0.5, help='Frequency scaling factor 0.1-1.0 (default: 0.5)')
    
    args = parser.parse_args()
    
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            print(f"File {args.input} not found.")
            sys.exit(1)
    else:
        print("Enter your text (press Ctrl+D on Unix/Linux or Ctrl+Z on Windows to finish):")
        text = sys.stdin.read()

    if text.strip():
        generate_word_cloud(
            text,
            background_color=args.bg,
            colormap=args.cmap,
            max_words=args.max_words,
            width=args.width,
            height=args.height,
            save_path=args.output,
            min_font_size=args.min_font_size,
            max_font_size=args.max_font_size,
            relative_scaling=args.relative_scaling
        )
    else:
        print("No text provided.")