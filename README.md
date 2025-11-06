# 词云工具项目

## 文件结构

- `data/`：用于存放输入的 Excel 文件（如 `data/input.xlsx`）。
- `output/`：用于存放生成的词云图片（如 `output/wordcloud.png`）。
- `main.py`：主程序文件。

## 使用方法

1. 将你的 Excel 文件（如 `input.xlsx`）放入 `data/` 文件夹。
2. 修改 `main.py` 中的文件名和列名（如有需要）。
3. 运行主程序：

```bash
python main.py
```

4. 生成的词云图片会保存在 `output/` 文件夹中。

## 依赖安装

```bash
pip install pandas jieba wordcloud matplotlib openpyxl
```

## 注意事项
- 请确保 `data/` 和 `output/` 文件夹存在。
- 需指定支持中文的字体文件路径（如 Mac 可用 `/System/Library/Fonts/STHeiti Medium.ttc`）。 