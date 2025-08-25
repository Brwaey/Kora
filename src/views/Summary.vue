<template>
    <div class="summary">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
                </svg>
              </div>
              <h1 class="text-xl font-semibold text-gray-900">Kora 语音面试</h1>
            </div>
            <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              面试完成
            </div>
          </div>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="main">
        <div class="container">
          <!-- Summary Header -->
          <section class="summary-header">
            <h1>🎉 面试总结</h1>
            <p>恭喜您完成了本次语音面试！以下是您的面试记录和表现总结。</p>
            <div class="interview-info">
              <div class="info-item">
                <span class="label">面试风格：</span>
                <span class="value">{{ getStyleName(interviewData.style) }}</span>
              </div>
              <div class="info-item">
                <span class="label">完成时间：</span>
                <span class="value">{{ formatDate(interviewData.completedAt) }}</span>
              </div>
              <div class="info-item">
                <span class="label">问题数量：</span>
                <span class="value">{{ interviewData.questions.length }} 个</span>
              </div>
            </div>
          </section>
  
          <!-- Interview Records -->
          <section class="interview-records">
            <h2>📝 面试记录</h2>
            
            <div class="records-list">
              <div 
                v-for="(question, index) in interviewData.questions" 
                :key="question.id"
                class="record-item"
              >
                <div class="question-header">
                  <span class="question-number">问题 {{ index + 1 }}</span>
                  <span class="question-length">{{ getAnswerLength(question.answer) }} 字</span>
                </div>
                
                <div class="question-content">
                  <h3>{{ question.text }}</h3>
                </div>
                
                <div class="answer-content">
                  <h4>您的回答：</h4>
                  <p>{{ question.answer || '未回答' }}</p>
                </div>
                
                <div class="feedback-content">
                  <h4>面试官反馈：</h4>
                  <p>{{ question.feedback }}</p>
                </div>
              </div>
            </div>
          </section>
  
          <!-- 新增：AI 专业分析 -->
          <section class="ai-analysis">
            <h2>🤖 AI 专业分析</h2>
            <div class="analysis-card">
              <div v-if="isAnalysisLoading" class="loading-state">
                <div class="spinner"></div>
                <p>正在生成您的专属分析报告，请稍候...</p>
              </div>
              <div v-else v-html="marked(llmAnalysisReport)" class="analysis-report"></div>
            </div>
          </section>

          <!-- Performance Analysis -->
          <section class="performance-analysis">
            <h2>📊 表现分析</h2>
            
            <div class="analysis-grid">
              <div class="analysis-card">
                <div class="analysis-icon">💬</div>
                <h3>回答完整度</h3>
                <div class="score">{{ completionRate }}%</div>
                <p>{{ getCompletionFeedback() }}</p>
              </div>
              
              <div class="analysis-card">
                <div class="analysis-icon">📏</div>
                <h3>回答长度</h3>
                <div class="score">{{ averageLength }} 字</div>
                <p>{{ getLengthFeedback() }}</p>
              </div>
              
              <div class="analysis-card">
                <div class="analysis-icon">⭐</div>
                <h3>整体表现</h3>
                <div class="score">{{ overallRating }}</div>
                <p>{{ getOverallFeedback() }}</p>
              </div>
            </div>
          </section>
  
          <!-- Export Options -->
          <section class="export-section">
            <h2>📤 导出选项</h2>
            <div class="export-buttons">
              <button @click="exportJSON" class="export-btn">
                📄 导出 JSON
              </button>
              <button @click="exportText" class="export-btn">
                📝 导出文本
              </button>
              <button @click="printSummary" class="export-btn">
                🖨️ 打印总结
              </button>
            </div>
          </section>
  
          <!-- Action Buttons -->
          <section class="actions">
            <button @click="startNewInterview" class="action-btn primary">
              🔄 重新面试
            </button>
            <button @click="goHome" class="action-btn secondary">
              🏠 返回首页
            </button>
          </section>
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { marked } from 'marked'
  import axios from 'axios'; // 1. 导入 axios
  
  const router = useRouter()
  const route = useRoute()
  
  const interviewData = ref({
    questions: [],
    style: 'professional',
    completedAt: new Date().toISOString()
  })
  
  // Navigation functions
  const startNewInterview = () => {
    router.push('/interview')
  }
  
  const goHome = () => {
    router.push('/')
  }
  
  // Computed properties for analysis
  const completionRate = computed(() => {
    const answered = interviewData.value.questions.filter(q => q.answer && q.answer.trim()).length
    return Math.round((answered / interviewData.value.questions.length) * 100)
  })
  
  const averageLength = computed(() => {
    const answers = interviewData.value.questions.filter(q => q.answer && q.answer.trim())
    if (answers.length === 0) return 0
    const totalLength = answers.reduce((sum, q) => sum + q.answer.length, 0)
    return Math.round(totalLength / answers.length)
  })
  
  const overallRating = computed(() => {
    const completion = completionRate.value
    const avgLen = averageLength.value
    
    if (completion >= 100 && avgLen >= 100) return '优秀'
    if (completion >= 80 && avgLen >= 50) return '良好'
    if (completion >= 60) return '一般'
    return '需改进'
  })
  
  // Helper functions
  const getStyleName = (style) => {
    const styles = {
      friendly: '亲切友好', // 2. 修正键名
      formal: '正式严肃',
      casual: '校园风格' // 2. 修正键名
    }
    return styles[style] || '未知'
  }
  
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  const getAnswerLength = (answer) => {
    return answer ? answer.length : 0
  }
  
  const getCompletionFeedback = () => {
    const rate = completionRate.value
    if (rate >= 100) return '所有问题都得到了回答，表现出色！'
    if (rate >= 80) return '大部分问题都有回答，整体表现良好。'
    if (rate >= 60) return '回答了部分问题，还有提升空间。'
    return '建议完整回答所有问题以获得更好的面试效果。'
  }
  
  const getLengthFeedback = () => {
    const avgLen = averageLength.value
    if (avgLen >= 150) return '回答详细充实，能够充分展示您的经历。'
    if (avgLen >= 100) return '回答长度适中，内容比较完整。'
    if (avgLen >= 50) return '回答相对简短，可以更详细地描述。'
    return '建议提供更详细的回答以更好地展示自己。'
  }
  
  const getOverallFeedback = () => {
    const rating = overallRating.value
    switch (rating) {
      case '优秀': return '面试表现优秀，回答完整且详细！'
      case '良好': return '面试表现良好，继续保持！'
      case '一般': return '面试表现一般，还有改进空间。'
      default: return '建议多练习，提升面试表现。'
    }
  }
  
  // Export functions
  const exportJSON = () => {
    const dataStr = JSON.stringify(interviewData.value, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `面试记录_${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }
  
  const exportText = () => {
    let content = `Kora 语音面试记录\n`
    content += `==================\n\n`
    content += `面试风格：${getStyleName(interviewData.value.style)}\n`
    content += `完成时间：${formatDate(interviewData.value.completedAt)}\n`
    content += `问题数量：${interviewData.value.questions.length} 个\n\n`
    
    interviewData.value.questions.forEach((question, index) => {
      content += `问题 ${index + 1}：${question.text}\n`
      content += `回答：${question.answer || '未回答'}\n`
      content += `反馈：${question.feedback}\n\n`
    })
    
    content += `表现分析：\n`
    content += `- 回答完整度：${completionRate.value}%\n`
    content += `- 平均回答长度：${averageLength.value} 字\n`
    content += `- 整体评价：${overallRating.value}\n`
    
    const dataBlob = new Blob([content], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `面试记录_${new Date().toISOString().split('T')[0]}.txt`
    link.click()
    URL.revokeObjectURL(url)
  }
  
  const printSummary = () => {
    window.print()
  }
  
  const llmAnalysisReport = ref('') // 新增：存储LLM分析报告
  const isAnalysisLoading = ref(true) // 新增：分析加载状态
  
  const getLLMAnalysis = async () => {
    isAnalysisLoading.value = true
    try {
        // 直接传递原始对象，与后端测试用例格式一致
        const response = await axios.post('http://127.0.0.1:5000/api/analyze', {
        interviewData: interviewData.value // 传递对象而非字符串
        })
        llmAnalysisReport.value = response.data.analysis
    } catch (error) {
        console.error('LLM analysis error:', error)
        llmAnalysisReport.value = '抱歉，AI分析报告生成失败...'
    } finally {
        isAnalysisLoading.value = false
    }
  }

  onMounted(() => {
    const data = route.query.interviewData || route.params.interviewData
    if (data) {
      try {
        interviewData.value = JSON.parse(data)
        getLLMAnalysis() // 获取数据后调用LLM分析
      } catch (error) {
        console.error('Failed to parse interview data:', error)
        llmAnalysisReport.value = '无法解析面试数据，报告生成失败。'
        isAnalysisLoading.value = false
      }
    } else {
      llmAnalysisReport.value = '未找到面试数据，无法生成报告。'
      isAnalysisLoading.value = false
    }
  })
</script>

<style scoped>
  /* 在现有样式中添加 */
  .summary {
    min-height: 100vh;
    background: linear-gradient(135deg, #f0f9ff 0%, #e6fffa 100%);
  }
  
  .header {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(226, 232, 240, 0.7);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .summary-header h1 {
    background: linear-gradient(to right, #059669, #10b981);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: inline-block;
  }
  
  .record-item {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transition: transform 0.3s, box-shadow 0.3s;
    border: 1px solid rgba(226, 232, 240, 0.7);
  }
  
  .record-item:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transform: translateY(-2px);
  }
  
  .question-number {
    background: linear-gradient(to right, #059669, #10b981);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 500;
    box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
  }
  
  .analysis-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
    border: 1px solid rgba(226, 232, 240, 0.7);
  }
  
  .analysis-card:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transform: translateY(-2px);
  }
  
  .score {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(to right, #059669, #10b981);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.5rem;
  }
  
  .export-btn {
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 500;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3), 0 2px 4px -1px rgba(99, 102, 241, 0.2);
  }
  
  .export-btn:hover {
    background: linear-gradient(to right, #4f46e5, #7c3aed);
    transform: translateY(-1px);
    box-shadow: 0 6px 10px -1px rgba(99, 102, 241, 0.4), 0 2px 6px -1px rgba(99, 102, 241, 0.2);
  }
  
  .action-btn.primary {
    background: linear-gradient(to right, #059669, #10b981);
    color: white;
    box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3), 0 2px 4px -1px rgba(5, 150, 105, 0.2);
  }
  
  .action-btn.primary:hover {
    background: linear-gradient(to right, #047857, #059669);
    transform: translateY(-1px);
    box-shadow: 0 6px 10px -1px rgba(5, 150, 105, 0.4), 0 2px 6px -1px rgba(5, 150, 105, 0.2);
  }
  
  .logo-icon {
    width: 2rem;
    height: 2rem;
    background: #059669;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    position: relative;
  }
  
  .logo-icon span {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .analysis-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 4rem;
  }
  
  .status {
    background: #10b981;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .main {
    padding: 2rem 0;
  }
  
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 2rem;
  }
  
  .summary-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .summary-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #1e293b;
  }
  
  .summary-header p {
    font-size: 1.125rem;
    color: #64748b;
    margin-bottom: 2rem;
    line-height: 1.6;
  }
  
  .interview-info {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
  }
  
  .info-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .label {
    font-weight: 500;
    color: #64748b;
  }
  
  .value {
    font-weight: 600;
    color: #1e293b;
  }
  
  .interview-records, .performance-analysis, .export-section, .actions {
    margin-bottom: 3rem;
  }
  
  .interview-records h2, .performance-analysis h2, .export-section h2 {
    font-size: 1.875rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: #1e293b;
  }
  
  .records-list {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  
  .record-item {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .question-number {
    background: #059669;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 500;
  }
  
  .question-length {
    color: #64748b;
    font-size: 0.875rem;
  }
  
  .question-content h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 1rem;
    line-height: 1.4;
  }
  
  .answer-content, .feedback-content {
    margin-bottom: 1rem;
  }
  
  .answer-content h4, .feedback-content h4 {
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
  
  .answer-content p {
    color: #475569;
    line-height: 1.6;
    background: #f1f5f9;
    padding: 1rem;
    border-radius: 0.5rem;
  }
  
  .feedback-content p {
    color: #059669;
    line-height: 1.6;
    font-style: italic;
  }
  
  .analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
  
  .analysis-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .analysis-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  
  .analysis-card h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
  
  .score {
    font-size: 2rem;
    font-weight: 700;
    color: #059669;
    margin-bottom: 0.5rem;
  }
  
  .analysis-card p {
    color: #64748b;
    font-size: 0.875rem;
    line-height: 1.4;
  }
  
  .export-buttons {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .export-btn {
    background: #6366f1;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 500;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .export-btn:hover {
    background: #4f46e5;
    transform: translateY(-1px);
  }
  
  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .action-btn {
    border: none;
    padding: 1rem 2rem;
    font-size: 1.125rem;
    font-weight: 600;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .action-btn.primary {
    background: #059669;
    color: white;
  }
  
  .action-btn.primary:hover {
    background: #047857;
    transform: translateY(-1px);
  }
  
  .action-btn.secondary {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #d1d5db;
  }
  
  .action-btn.secondary:hover {
    background: #e2e8f0;
    transform: translateY(-1px);
  }
  
/* 在<style scoped>中添加/修改以下样式 */
.ai-analysis {
  margin: 3rem 0;
  padding: 1rem;
}

.ai-analysis h2 {
  font-size: 1.875rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #059669;
  display: inline-block;
}

.analysis-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f0f0f0;
}

.analysis-report {
  line-height: 1.8;
  color: #333;
  font-size: 1rem;
  text-align: left;
}

/* 报告标题样式 */
.analysis-report > strong:first-child {
  font-size: 1.5rem !important;
  display: block;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eee;
  color: #1e293b;
}

/* 主要部分标题样式 */
.analysis-report ol > li > strong {
  color: #059669;
  font-size: 1.15rem !important;
  display: block;
  margin: 1.5rem 0 0.75rem 0;
}

/* 子项样式 */
.analysis-report ol > li > ol {
  margin-left: 0.5rem;
  padding-left: 1.5rem;
}

/* 引用内容样式强化 */
.analysis-report p:has(> span:contains("> ")) {
  background-color: #f8fafc;
  border-left: 4px solid #059669;
  padding: 1rem;
  margin: 0.75rem 0;
  border-radius: 0 4px 4px 0;
  font-style: italic;
  color: #475569;
}

/* 潜力预估和匹配度部分特殊样式 */
.analysis-report ol > li:nth-child(4),
.analysis-report ol > li:nth-child(5),
.analysis-report ol > li:nth-child(6) {
  margin-top: 1rem;
}

/* 加载状态优化 */
.loading-state {
  text-align: center;
  padding: 3rem 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1.5rem;
  border: 4px solid #f0f9ff;
  border-top: 4px solid #059669;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

  @media (max-width: 768px) {
    .container {
      padding: 0 1rem;
    }
    
    .summary-header h1 {
      font-size: 2rem;
    }
    
    .interview-info {
      flex-direction: column;
      gap: 1rem;
    }
    
    .record-item {
      padding: 1.5rem;
    }
    
    .analysis-grid {
      grid-template-columns: 1fr;
    }
    
    .export-buttons, .actions {
      flex-direction: column;
      align-items: center;
    }
  }
  
  @media print {
    .header, .export-section, .actions {
      display: none;
    }
    
    .main {
      padding: 0;
    }
    
    .container {
      max-width: none;
      padding: 0;
    }
  }
  </style>
  