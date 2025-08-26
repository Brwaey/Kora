import os
import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 加载环境变量（本地开发用，Vercel会自动注入）
if os.path.exists('.env'):
    load_dotenv()

app = Flask(__name__)

# 配置CORS，允许来自前端的请求
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins.split(","),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 通义千问API配置
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'

# 面试风格配置
INTERVIEW_STYLES = {
    'friendly': {
        'system_prompt': '''你是一位友善、亲切的面试官，像一位耐心的学长学姐。
你的目标是帮助应聘者放松，更好地展示自己。
你必须使用轻松、鼓励性的语言，可以适当使用emoji（如😊👍）。
请针对回答给出具体的、建设性的反馈，并自然地引出下一个问题或追问。
回复必须控制在50-80字之间。''',
    },
    'formal': {
        'system_prompt': '''你是一位专业、严谨的面试官，代表一家注重效率和专业能力的公司。
你的提问和反馈都应直接、客观、切中要点，避免任何情绪化表达。
必须引导应聘者使用STAR法则（情境、任务、行动、结果）来结构化地回答问题。
反馈应侧重于评估其解决问题的能力、专业知识和逻辑思维。
回复必须控制在50-80字之间。''',
    },
    'casual': {
        'system_prompt': '''你是一位随和、健谈的面试官，像是在咖啡馆里与应聘者进行一场非正式交流。
你的风格是对话式的，可以分享一些自己的看法来引导对方。
反馈是启发性的，旨在激发应聘者更深层次的思考，而不是进行严格的评判。
可以使用一些口语化表达，如"嗯，这个想法不错"、"我觉得..."等。
回复必须控制在50-80字之间。''',
    }
}

def call_dashscope_api(messages, max_tokens=150, temperature=0.75):
    """调用通义千问API（兼容OpenAI格式）"""
    if not DASHSCOPE_API_KEY:
        logger.error("DASHSCOPE_API_KEY环境变量未配置")
        return None, "服务器配置错误：缺少API密钥"
    
    try:
        logger.info(f"调用通义千问API，消息长度: {len(messages)}")
        
        response = requests.post(
            DASHSCOPE_API_URL,
            headers={
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'qwen-turbo',
                'messages': messages,
                'max_tokens': max_tokens,
                'temperature': temperature,
                'top_p': 0.8
            },
            timeout=30
        )
        
        # 检查HTTP状态码
        if response.status_code != 200:
            error_msg = f"API请求失败 (状态码: {response.status_code})"
            logger.error(f"{error_msg}，响应: {response.text[:500]}")
            return None, error_msg
            
        # 解析响应
        result = response.json()
        
        # 检查API错误
        if 'error' in result:
            error_detail = result['error'].get('message', '未知错误')
            error_msg = f"API错误: {error_detail}"
            logger.error(error_msg)
            return None, error_msg
            
        # 提取内容
        choices = result.get('choices', [])
        if not choices or not choices[0].get('message'):
            error_msg = "API返回格式异常"
            logger.error(f"{error_msg}，响应: {json.dumps(result, indent=2)[:500]}")
            return None, error_msg
            
        content = choices[0]['message'].get('content', '').strip()
        if not content:
            logger.warning("API返回空内容")
            return "", "获取内容为空，请重试"
            
        logger.info(f"API调用成功，返回内容长度: {len(content)}")
        return content, None
        
    except requests.exceptions.Timeout:
        error_msg = "API请求超时"
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"处理API响应时出错: {str(e)}"
        logger.error(error_msg)
        return None, f"服务器处理错误: {str(e)}"

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口，用于验证服务是否正常运行"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    """生成面试问题接口"""
    try:
        data = request.json
        job_position = data.get('position', '').strip()
        experience = data.get('experience', '').strip()
        style = data.get('style', 'friendly')
        
        if not job_position:
            return jsonify({'error': '缺少岗位信息'}), 400
            
        # 构建生成问题的提示词
        style_config = INTERVIEW_STYLES.get(style, INTERVIEW_STYLES['friendly'])
        messages = [
            {"role": "system", "content": f"{style_config['system_prompt']} 请根据应聘岗位和经验，生成一个相关的面试问题。"},
            {"role": "user", "content": f"应聘岗位: {job_position}\n工作经验: {experience}\n请生成一个合适的面试问题，不要有多余解释。"}
        ]
        
        question, error = call_dashscope_api(messages, max_tokens=100, temperature=0.8)
        
        if error:
            return jsonify({'error': error, 'question': question or ''}), 500
            
        return jsonify({'question': question})
        
    except Exception as e:
        logger.error(f"生成问题时出错: {str(e)}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    """获取面试反馈接口"""
    try:
        data = request.json
        user_answer = data.get('answer', '').strip()
        question = data.get('question', '').strip()
        style = data.get('style', 'friendly')

        if not user_answer or not question:
            return jsonify({'error': '缺少问题或回答内容'}), 400

        style_config = INTERVIEW_STYLES.get(style, INTERVIEW_STYLES['friendly'])
        
        messages = [
            {"role": "system", "content": style_config['system_prompt']},
            {"role": "user", "content": f"面试问题：{question}\n\n我的回答是：{user_answer}\n\n请根据我的回答，以面试官的身份给我一些反馈和引导。"}
        ]

        feedback, error = call_dashscope_api(messages, max_tokens=150, temperature=0.75)
        
        if error:
            return jsonify({'error': error, 'feedback': feedback or ''}), 500
            
        return jsonify({'feedback': feedback})
        
    except Exception as e:
        logger.error(f"处理反馈请求时出错: {str(e)}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_performance():
    """分析面试表现接口"""
    try:
        data = request.json
        interview_data = data.get('interviewData')

        if not interview_data or not interview_data.get('questions'):
            return jsonify({'error': '缺少有效的面试数据'}), 400

        # 格式化面试数据
        formatted_data = []
        for i, item in enumerate(interview_data.get('questions', []), 1):
            formatted_data.append(f"问题 {i}: {item.get('text', '')}")
            formatted_data.append(f"回答 {i}: {item.get('answer', '')}")
        
        formatted_data = "\n".join(formatted_data)
        
        # 构建分析提示词
        analysis_prompt = f"""作为资深HR专家，请根据以下面试记录，提供专业、全面的分析报告。

【报告标题】
**面试分析报告**

【报告结构】
1. **一、综合评价**：一句话总结核心优势和需提升点，从沟通风格、思维逻辑、内容深度评价
   
2. **二、亮点剖析**：2-3个具体优点，每个需引用面试中的具体回答作为证据（格式：> "引用内容"）
   
3. **三、发展建议**：2-3条具体、可执行的改进建议，每条需说明**为什么**和**怎么做**
   
4. **四、潜力预估**：对应聘者职业潜力和发展方向的中肯预估，结合行业趋势给出参考
   
5. **五、回答结构分析**：评估回答的逻辑性和条理性，是否使用**STAR法则**等结构化表达
   
6. **六、岗位匹配度**：基于回答内容推测与目标岗位的匹配程度

【格式要求】
- 标题"面试分析报告"必须加粗
- 主要部分标题需加粗
- 子项使用序号排序
- 回答引用格式：> "回答内容"
- 各部分之间用空行分隔
- "为什么"和"怎么做"需加粗
- "STAR法则"需加粗

使用专业、客观且鼓励的语气。推测性内容需标注"**推测：**"。

面试记录：
{formatted_data}
"""

        messages = [
            {"role": "system", "content": "你是一位资深的HR专家和职业发展顾问，擅长面试分析。"},
            {"role": "user", "content": analysis_prompt}
        ]

        analysis, error = call_dashscope_api(messages, max_tokens=1000, temperature=0.7)
        
        if error:
            return jsonify({'error': error, 'analysis': analysis or ''}), 500
            
        return jsonify({'analysis': analysis})
        
    except Exception as e:
        logger.error(f"处理面试分析时出错: {str(e)}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

# 处理预检请求
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Vercel Serverless Functions 入口
def handler(event, context):
    from flask import request
    from werkzeug.wrappers import Request, Response
    from datetime import datetime  # 在这里导入以避免Vercel冷启动问题
    
    # 修复导入问题
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # 将Vercel事件转换为Flask请求
    try:
        # 处理请求
        with app.request_context(Request(event['wsgi']['input'], environ=event['wsgi']['environ'])):
            response = app.full_dispatch_request()
            
            # 转换为Vercel响应格式
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
    except Exception as e:
        logger.error(f"处理请求时发生致命错误: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'服务器处理错误: {str(e)}'})
        }

# 本地开发用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
