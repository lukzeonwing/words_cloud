"""
Word Cloud Generator
Generates word clouds from CSV text data with customizable settings.
"""

import os
import sys
import logging
import argparse
from typing import Dict, Set, Counter as CounterType
from pathlib import Path
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import yaml
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yaml') -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration values
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


def validate_config(config: Dict) -> Dict:
    """
    Validate and set default configuration values.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Validated configuration dictionary
    """
    defaults = {
        'csv_path': 'data/input.csv',
        'text_column': 'title',
        'output_img': 'output/wordcloud.png',
        'font_path': '/System/Library/Fonts/STHeiti Medium.ttc',
        'background_color': 'white',
        'width': 1920,
        'height': 1080,
        'colormap': 'viridis',
        'min_word_length': 2,
        'max_words': 200,
        'relative_scaling': 0.5,
        'use_custom_colors': False,
        'custom_colors': []
    }
    
    for key, default_value in defaults.items():
        if key not in config:
            config[key] = default_value
            logger.debug(f"Using default value for {key}: {default_value}")
    
    # Validate numeric values
    if config['width'] <= 0 or config['height'] <= 0:
        logger.warning("Invalid width/height, using defaults")
        config['width'] = defaults['width']
        config['height'] = defaults['height']
    
    if config['min_word_length'] < 1:
        config['min_word_length'] = 1
    
    return config


def ensure_directories(*dirs: str) -> None:
    """
    Ensure directories exist, create if they don't.
    
    Args:
        *dirs: Variable number of directory paths
    """
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")


def load_stopwords(stopwords_path: str = 'data/stopwords.txt') -> Set[str]:
    """
    Load stopwords from file.
    
    Args:
        stopwords_path: Path to stopwords file
        
    Returns:
        Set of stopwords
    """
    if not os.path.exists(stopwords_path):
        logger.warning(f"Stopwords file not found: {stopwords_path}. Using empty set.")
        return set()
    
    try:
        with open(stopwords_path, encoding='utf-8') as f:
            stopwords = set(line.strip() for line in f if line.strip())
        logger.info(f"Loaded {len(stopwords)} stopwords from {stopwords_path}")
        return stopwords
    except Exception as e:
        logger.error(f"Error loading stopwords: {e}")
        return set()


def read_csv_data(csv_path: str, text_column: str) -> pd.DataFrame:
    """
    Read CSV file and validate column exists.
    
    Args:
        csv_path: Path to CSV file
        text_column: Name of the text column to read
        
    Returns:
        DataFrame containing the data
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If specified column doesn't exist
    """
    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found: {csv_path}")
        raise FileNotFoundError(f"Please place your CSV file at {csv_path}")
    
    try:
        df = pd.read_csv(csv_path)
        logger.info(f"CSV file loaded: {csv_path} ({len(df)} rows)")
        
        if text_column not in df.columns:
            available_columns = ', '.join(df.columns)
            logger.error(f"Column '{text_column}' not found. Available columns: {available_columns}")
            raise ValueError(f"Column '{text_column}' not found in CSV. Available: {available_columns}")
        
        return df[[text_column]]
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty")
        raise ValueError("CSV file is empty")
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise


def segment_text(text: str, stopwords: Set[str], min_length: int = 2) -> list:
    """
    Segment Chinese text into words using jieba and filter.
    
    Args:
        text: Text to segment
        stopwords: Set of words to exclude
        min_length: Minimum word length to include
        
    Returns:
        List of segmented words
    """
    logger.info("Starting text segmentation...")
    words = jieba.cut(text)
    word_list = [
        w.strip() 
        for w in words 
        if w.strip() 
        and len(w.strip()) >= min_length
        and w.strip() not in stopwords
    ]
    logger.info(f"Segmentation complete: {len(word_list)} words extracted")
    return word_list


def save_segmented_words(word_list: list, output_path: str) -> None:
    """
    Save segmented words to a text file.
    
    Args:
        word_list: List of words to save
        output_path: Path to output file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in word_list:
                f.write(word + '\n')
        logger.info(f"Segmented words saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving segmented words: {e}")
        raise


def save_word_counts(word_counts: CounterType, output_path: str) -> None:
    """
    Save word frequency counts to CSV.
    
    Args:
        word_counts: Counter object with word frequencies
        output_path: Path to output CSV file
    """
    try:
        df = pd.DataFrame(word_counts.most_common(), columns=['word', 'count'])
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"Word frequency counts saved to {output_path} (top word: '{df.iloc[0]['word']}' with {df.iloc[0]['count']} occurrences)")
    except Exception as e:
        logger.error(f"Error saving word counts: {e}")
        raise


def create_custom_colormap(colors: list) -> LinearSegmentedColormap:
    """
    Create a custom colormap from a list of colors.
    
    Args:
        colors: List of color strings (hex or named colors)
        
    Returns:
        Custom LinearSegmentedColormap
    """
    from matplotlib.colors import to_rgb
    try:
        rgb_colors = [to_rgb(color) for color in colors]
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('custom', rgb_colors, N=n_bins)
        logger.info(f"Custom colormap created with {len(colors)} colors")
        return cmap
    except Exception as e:
        logger.error(f"Error creating custom colormap: {e}")
        raise


def generate_wordcloud(
    word_counts: CounterType,
    config: Dict
) -> WordCloud:
    """
    Generate word cloud from word frequencies.
    
    Args:
        word_counts: Counter object with word frequencies
        config: Configuration dictionary
        
    Returns:
        WordCloud object
    """
    try:
        logger.info("Generating word cloud...")
        
        # Prepare WordCloud parameters
        wc_params = {
            'font_path': config['font_path'],
            'width': config['width'],
            'height': config['height'],
            'background_color': config['background_color'],
            'max_words': config['max_words'],
            'relative_scaling': config['relative_scaling']
        }
        
        # Handle color configuration
        if config.get('use_custom_colors') and config.get('custom_colors'):
            custom_cmap = create_custom_colormap(config['custom_colors'])
            wc_params['colormap'] = custom_cmap
        elif config.get('colormap'):
            wc_params['colormap'] = config['colormap']
        
        wc = WordCloud(**wc_params)
        wc.generate_from_frequencies(word_counts)
        logger.info("Word cloud generated successfully")
        return wc
    except Exception as e:
        logger.error(f"Error generating word cloud: {e}")
        raise


def save_wordcloud(wc: WordCloud, output_path: str) -> None:
    """
    Save word cloud to image file.
    
    Args:
        wc: WordCloud object
        output_path: Path to output image file
    """
    try:
        wc.to_file(output_path)
        logger.info(f"Word cloud image saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving word cloud image: {e}")
        raise


def display_wordcloud(wc: WordCloud) -> None:
    """
    Display word cloud using matplotlib.
    
    Args:
        wc: WordCloud object
    """
    try:
        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.show()
        logger.info("Word cloud displayed")
    except Exception as e:
        logger.error(f"Error displaying word cloud: {e}")


def main(config_path: str = 'config.yaml', display: bool = False) -> None:
    """
    Main function to orchestrate word cloud generation.
    
    Args:
        config_path: Path to configuration file
        display: Whether to display the word cloud
    """
    try:
        # Load and validate configuration
        config = load_config(config_path)
        config = validate_config(config)
        
        # Ensure directories exist
        ensure_directories('data', 'output')
        
        # Read CSV data
        df = read_csv_data(config['csv_path'], config['text_column'])
        
        # Combine all text content
        text = ' '.join(df[config['text_column']].astype(str))
        logger.info(f"Combined text length: {len(text)} characters")
        
        # Load stopwords
        stopwords = load_stopwords('data/stopwords.txt')
        
        # Segment text
        word_list = segment_text(text, stopwords, config['min_word_length'])
        
        if not word_list:
            logger.error("No words extracted from text. Check your data and stopwords.")
            sys.exit(1)
        
        # Save segmented words
        save_segmented_words(word_list, 'output/segmented_words.txt')
        
        # Count word frequencies
        word_counts = Counter(word_list)
        logger.info(f"Unique words: {len(word_counts)}")
        
        # Save word counts
        save_word_counts(word_counts, 'output/word_counts.csv')
        
        # Generate word cloud
        wc = generate_wordcloud(word_counts, config)
        
        # Save word cloud
        save_wordcloud(wc, config['output_img'])
        
        # Optionally display word cloud
        if display:
            display_wordcloud(wc)
        
        logger.info("Word cloud generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate word cloud from CSV text data')
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--display',
        action='store_true',
        help='Display the word cloud after generation'
    )
    
    args = parser.parse_args()
    main(config_path=args.config, display=args.display) 