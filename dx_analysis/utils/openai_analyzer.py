import openai
import json
from flask import current_app

def split_content(content, max_tokens=4000):
    """
    将内容分成多个小段
    
    Args:
        content (str): 要分割的内容
        max_tokens (int): 每段的最大令牌数（近似值）
    
    Returns:
        list: 分割后的内容列表
    """
    # 按段落分割
    paragraphs = content.split('\n\n')
    
    # 初始化结果列表和当前段
    segments = []
    current_segment = []
    current_length = 0
    
    for paragraph in paragraphs:
        # 估算段落长度（假设每个字符约等于1个令牌）
        paragraph_length = len(paragraph)
        
        # 如果当前段加上新段落超过限制，保存当前段并开始新段
        if current_length + paragraph_length > max_tokens and current_segment:
            segments.append('\n\n'.join(current_segment))
            current_segment = []
            current_length = 0
        
        # 添加段落到当前段
        current_segment.append(paragraph)
        current_length += paragraph_length
    
    # 添加最后一段
    if current_segment:
        segments.append('\n\n'.join(current_segment))
    
    return segments

def get_analysis_prompt(company_name, content, is_partial=False):
    """生成简化的分析提示词"""
    segment_note = "（这是部分内容的分析）" if is_partial else ""
    return f"""分析[{company_name}]的财务报告{segment_note}，评估DX转型的可能性和商业机会。请提供每个方面的评分（1-10）和总评分（100分满分）。

1. DX现状
2. 业务流程挖掘
3. 销售能力
4. 云计算使用
5. 自动化
6. 核心系统

财务报告内容：
{content}

请以JSON格式返回结果：
{{
    "company_name": "公司名",
    "dx_status": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "process_mining": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "sales_enhancement": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "cloud_usage": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "automation": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "core_system": {{
        "score": 评分,
        "analysis": "分析内容"
    }},
    "total_score": 总评分
}}"""

def merge_analysis_results(results):
    """
    合并多个分析结果
    
    Args:
        results (list): 分析结果列表
    
    Returns:
        dict: 合并后的分析结果
    """
    if not results:
        return None
    
    # 使用第一个结果作为基础
    final_result = results[0].copy()
    
    # 如果只有一个结果，直接返回
    if len(results) == 1:
        return final_result
    
    # 合并多个结果
    categories = ['dx_status', 'process_mining', 'sales_enhancement', 
                 'cloud_usage', 'automation', 'core_system']
    
    for category in categories:
        scores = [r[category]['score'] for r in results]
        analyses = [r[category]['analysis'] for r in results]
        
        # 计算平均分数
        final_result[category]['score'] = round(sum(scores) / len(scores), 1)
        # 合并分析内容
        final_result[category]['analysis'] = ' '.join(analyses)
    
    # 计算总分
    total_scores = [r['total_score'] for r in results]
    final_result['total_score'] = round(sum(total_scores) / len(total_scores), 1)
    
    return final_result

def analyze_company(md_path, company_name):
    """
    使用OpenAI API分析公司数据
    
    Args:
        md_path (str): Markdown文件路径
        company_name (str): 公司名称
    
    Returns:
        dict: 分析结果
    """
    # 读取Markdown文件内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割内容
    segments = split_content(content)
    print(f"文件被分成了 {len(segments)} 段")
    
    # 创建OpenAI客户端
    client = openai.OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
    
    # 存储每段的分析结果
    segment_results = []
    
    # 分析每个段落
    for i, segment in enumerate(segments):
        print(f"\n开始处理第 {i+1} 段 (长度: {len(segment)} 字符)")
        
        # 生成提示词
        prompt = get_analysis_prompt(company_name, segment, is_partial=(len(segments) > 1))
        
        try:
            # 调用OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "你是一个专业的DX咨询顾问，擅长分析企业财务报告并评估DX转型机会。请确保返回有效的JSON格式数据。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # 获取响应内容
            response_content = response.choices[0].message.content
            print(f"API响应内容: {response_content[:200]}...")  # 只打印前200个字符
            
            try:
                # 解析响应
                result = json.loads(response_content)
                segment_results.append(result)
                print(f"第 {i+1} 段处理成功")
            except json.JSONDecodeError as je:
                print(f"JSON解析错误 (第 {i+1} 段): {str(je)}")
                print(f"完整响应内容: {response_content}")
                continue
            
        except Exception as e:
            print(f"API调用错误 (第 {i+1} 段): {str(e)}")
            continue
    
    # 合并所有段落的分析结果
    if segment_results:
        print(f"成功处理了 {len(segment_results)} 段内容")
        return merge_analysis_results(segment_results)
    else:
        print("没有成功处理任何段落")
        return {
            "company_name": company_name,
            "error": "无法完成分析",
            "raw_response": "所有段落处理都失败了"
        } 