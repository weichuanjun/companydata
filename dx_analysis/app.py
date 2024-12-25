from flask import Flask, render_template, jsonify, request
import os
from utils.pdf_converter import convert_pdf_to_markdown
from utils.openai_analyzer import analyze_company
import json

app = Flask(__name__)

# 配置
app.config['PDF_FOLDER'] = 'pdf'
app.config['MD_FOLDER'] = 'md'
app.config['OPENAI_API_KEY'] = ''  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdfs():
    try:
        # 获取PDF文件夹中的所有PDF文件
        pdf_files = [f for f in os.listdir(app.config['PDF_FOLDER']) if f.endswith('.pdf')]
        results = []
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_file)
            md_file = pdf_file.replace('.pdf', '_v2.md')
            md_path = os.path.join(app.config['MD_FOLDER'], md_file)
            
            # 转换PDF到Markdown
            convert_pdf_to_markdown(pdf_path, md_path)
            results.append({
                'filename': pdf_file,
                'status': 'success',
                'md_path': md_path
            })
        
        return jsonify({'status': 'success', 'results': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/analyze', methods=['POST'])
def analyze_companies():
    try:
        # 获取所有Markdown文件
        md_files = [f for f in os.listdir(app.config['MD_FOLDER']) if f.endswith('_v2.md')]
        analyses = []
        
        for md_file in md_files:
            company_name = md_file.replace('_v2.md', '')
            md_path = os.path.join(app.config['MD_FOLDER'], md_file)
            
            # 分析公司
            analysis_result = analyze_company(md_path, company_name)
            analyses.append(analysis_result)
        
        # 按评分排序
        analyses.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({'status': 'success', 'analyses': analyses})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 