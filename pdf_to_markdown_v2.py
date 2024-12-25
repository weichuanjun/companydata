from pdfminer.high_level import extract_text
import os
import codecs

def ensure_md_folder_exists():
    """确保 md 文件夹存在"""
    if not os.path.exists('md'):
        os.makedirs('md')

def get_unconverted_pdfs():
    """获取未转换的PDF文件列表"""
    # 获取 pdf 文件夹下的所有PDF文件
    pdf_files = [f for f in os.listdir('pdf') if f.endswith('.pdf')]
    
    # 获取已经转换的文件列表
    converted_files = [f.replace('_v2.md', '.pdf') for f in os.listdir('md') if f.endswith('_v2.md')]
    
    # 返回未转换的文件列表
    return [f for f in pdf_files if f not in converted_files]

def convert_pdf_to_markdown(pdf_path, output_path):
    # 提取文本
    text = extract_text(pdf_path)
    
    # 创建markdown文件
    with codecs.open(output_path, 'w', encoding='utf-8') as md_file:
        # 写入标题
        filename = os.path.basename(pdf_path)
        md_file.write(f'# {filename}\n\n')
        
        # 写入内容
        md_file.write(text)

if __name__ == '__main__':
    # 确保 md 文件夹存在
    ensure_md_folder_exists()
    
    # 获取未转换的PDF文件
    unconverted_pdfs = get_unconverted_pdfs()
    
    if not unconverted_pdfs:
        print('没有需要转换的PDF文件')
    else:
        print(f'发现 {len(unconverted_pdfs)} 个未转换的PDF文件')
        
        for pdf_file in unconverted_pdfs:
            # 构建完整的输入输出路径
            input_path = os.path.join('pdf', pdf_file)
            output_file = pdf_file.replace('.pdf', '_v2.md')
            output_path = os.path.join('md', output_file)
            
            print(f'正在转换 {pdf_file} 为 {output_file}...')
            try:
                convert_pdf_to_markdown(input_path, output_path)
                print(f'成功转换 {pdf_file}')
            except Exception as e:
                print(f'转换 {pdf_file} 时发生错误: {str(e)}') 