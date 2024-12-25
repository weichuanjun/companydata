from pdfminer.high_level import extract_text
import os
import codecs

def convert_pdf_to_markdown(pdf_path, output_path):
    """
    将PDF文件转换为Markdown格式
    
    Args:
        pdf_path (str): PDF文件路径
        output_path (str): 输出Markdown文件路径
    """
    # 提取文本
    text = extract_text(pdf_path)
    
    # 创建markdown文件
    with codecs.open(output_path, 'w', encoding='utf-8') as md_file:
        # 写入标题
        filename = os.path.basename(pdf_path)
        md_file.write(f'# {filename}\n\n')
        
        # 写入内容
        md_file.write(text) 