# DX分析システム

企业财务报告的DX转型分析系统，支持批量PDF转换和OpenAI驱动的智能分析。

## 功能特点

- PDF文件批量转换为Markdown格式
- 使用OpenAI GPT-4进行智能分析
- 多维度DX转型评估
- 可视化分析结果展示
- 评分驱动的企业排序

## 安装步骤

1. 克隆项目并进入项目目录：
```bash
git clone [repository_url]
cd dx_analysis
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置OpenAI API密钥：
创建`.env`文件并添加以下内容：
```
OPENAI_API_KEY=your_api_key_here
```

5. 准备文件目录：
```bash
mkdir pdf md
```

## 使用方法

1. 将需要分析的PDF文件放入`pdf`文件夹

2. 运行应用：
```bash
python app.py
```

3. 在浏览器中访问：`http://localhost:5000`

4. 点击"PDFファイルを変換"按钮开始转换

5. 转换完成后，点击"分析開始"按钮进行分析

## 系统要求

- Python 3.8+
- OpenAI API密钥
- 现代浏览器（Chrome, Firefox, Safari等）

## 注意事项

- 请确保PDF文件采用UTF-8编码
- API调用可能需要一定时间，请耐心等待
- 分析结果仅供参考，具体实施方案请结合实际情况

## 许可证

MIT License 