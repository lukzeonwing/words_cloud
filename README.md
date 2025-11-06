# Word Cloud Generator

A professional Python tool for generating customizable word clouds from CSV text data with support for Chinese text segmentation.

## Features

- 🎨 **Customizable Colors**: Use built-in colormaps or define your own color gradients
- 📊 **Word Frequency Analysis**: Automatically generates word frequency statistics
- 🈯 **Chinese Text Support**: Uses jieba for accurate Chinese text segmentation
- ⚙️ **Flexible Configuration**: YAML-based configuration for easy customization
- 📝 **Comprehensive Logging**: Detailed logging for debugging and monitoring
- 🎯 **Word Filtering**: Configurable minimum word length and stopwords support
- 💻 **CLI Support**: Command-line arguments for advanced usage

## Project Structure

```
words_cloud/
├── config.yaml              # Configuration file
├── main.py                  # Main program
├── README.md                # Documentation
├── data/                    # Input data directory
│   ├── input.csv           # Input CSV file
│   └── stopwords.txt       # Optional stopwords file
└── output/                  # Output directory
    ├── wordcloud.png       # Generated word cloud image
    ├── segmented_words.txt # Segmented words list
    └── word_counts.csv     # Word frequency statistics
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install pandas jieba wordcloud matplotlib pyyaml numpy
```

## Quick Start

1. **Prepare Your Data**
   
   Place your CSV file in the `data/` folder. The CSV should have a column containing the text you want to analyze (default column name: `title`).

2. **Configure Settings**
   
   Edit `config.yaml` to customize your word cloud:
   - Input/output file paths
   - Image dimensions
   - Colors and styling
   - Text processing parameters

3. **Run the Program**
   
   ```bash
   python main.py
   ```

4. **View Results**
   
   Check the `output/` folder for:
   - `wordcloud.png` - Your word cloud image
   - `word_counts.csv` - Word frequency statistics
   - `segmented_words.txt` - All extracted words

## Configuration Guide

### Basic Settings

```yaml
csv_path: data/input.csv          # Input CSV file path
text_column: title                # Column name containing text
output_img: output/wordcloud.png  # Output image path
width: 1920                       # Image width (pixels)
height: 1080                      # Image height (pixels)
background_color: white           # Background color
```

### Word Processing

```yaml
min_word_length: 2                # Filter out words shorter than this
max_words: 200                    # Maximum words to display
relative_scaling: 0.5             # Word size variation (0.0-1.0)
```

### Color Customization

#### Option 1: Built-in Colormap

```yaml
use_custom_colors: false
colormap: viridis                 # Choose from matplotlib colormaps
```

Popular colormaps:
- **Sequential**: `viridis`, `plasma`, `inferno`, `magma`, `Blues`, `Greens`, `Reds`
- **Diverging**: `coolwarm`, `RdYlBu`, `Spectral`
- **Qualitative**: `Accent`, `Set1`, `Paired`, `tab10`

#### Option 2: Custom Color Gradient

```yaml
use_custom_colors: true
custom_colors:
  - '#0000FF'    # Blue
  - '#00FFFF'    # Cyan
  - '#00FF00'    # Green
  - '#FFFF00'    # Yellow
  - '#FF0000'    # Red
```

## Advanced Usage

### Command-Line Arguments

```bash
# Use a different config file
python main.py --config my_config.yaml

# Display the word cloud after generation
python main.py --display

# Combine options
python main.py --config my_config.yaml --display
```

### Custom Stopwords

Create a `data/stopwords.txt` file with one word per line to exclude specific words from the word cloud:

```
的
了
是
在
```

### Font Configuration

For Chinese text support, specify a font that supports Chinese characters:

**macOS:**
```yaml
font_path: /System/Library/Fonts/STHeiti Medium.ttc
```

**Windows:**
```yaml
font_path: C:/Windows/Fonts/simhei.ttf
```

**Linux:**
```yaml
font_path: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
```

## Output Files

### 1. Word Cloud Image (`wordcloud.png`)
The main visual output showing words sized by frequency.

### 2. Word Frequency Statistics (`word_counts.csv`)
CSV file with two columns:
- `word`: The word
- `count`: Number of occurrences

### 3. Segmented Words (`segmented_words.txt`)
List of all extracted words (one per line) after filtering.

## Troubleshooting

### Error: "CSV file not found"
- Ensure your CSV file is in the `data/` folder
- Check the `csv_path` in `config.yaml` matches your file name

### Error: "Column not found"
- Verify the `text_column` name in `config.yaml` matches your CSV column
- Check for typos or extra spaces in column names

### Word cloud looks empty
- Check if your text data contains actual content
- Reduce `min_word_length` in config
- Review your stopwords list - it might be too aggressive

### Chinese characters not displaying
- Ensure `font_path` points to a valid font file that supports Chinese
- Check that the font file path is correct for your operating system

## Examples

### Example 1: Ocean-Themed Word Cloud

```yaml
use_custom_colors: true
custom_colors:
  - '#003366'
  - '#006699'
  - '#0099CC'
  - '#66FFFF'
background_color: '#001a33'
```

### Example 2: High-Contrast Word Cloud

```yaml
use_custom_colors: false
colormap: RdYlBu_r
background_color: black
max_words: 100
relative_scaling: 0.8
```

## Contributing

Feel free to submit issues or pull requests to improve this tool.

## License

This project is open source and available for personal and commercial use.

## Acknowledgments

- **jieba**: Chinese text segmentation
- **WordCloud**: Word cloud generation library
- **Matplotlib**: Visualization and color management 