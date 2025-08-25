<template>
    <div class="min-h-screen bg-gray-50">
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
              <!-- 修复：移除标题下划线（通过样式类单独控制） -->
              <h1 class="text-xl font-semibold text-gray-900 header-title">Kora 语音面试</h1>
            </div>
            <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              问题 {{ currentQuestion }}/3
            </div>
          </div>
        </div>
      </header>
  
      <!-- Progress Bar -->
      <div class="bg-white border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="w-full bg-gray-200 h-1">
            <div 
              class="bg-green-600 h-1 transition-all duration-300"
              :style="{ width: `${(currentQuestion / 3) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
  
      <!-- Main Content -->
      <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Welcome Phase -->
        <div v-if="phase === 'welcome'" class="text-center">
          <div class="bg-white rounded-xl p-8 shadow-sm border border-gray-100 max-w-2xl mx-auto">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <h2 class="text-2xl font-bold text-gray-900 mb-4">欢迎参加面试</h2>
            
            <p class="text-gray-600 mb-8">
              您好，我是Kora的语音面试官，接下来我会用中文向您提问一些常见面试问题，请用语音作答。
            </p>
  
            <!-- Interview Style Selection -->
            <div class="mb-8">
              <label class="block text-sm font-medium text-gray-700 mb-3">选择面试风格：</label>
              <select 
                v-model="selectedStyle" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="friendly">亲切友好</option>
                <option value="formal">正式严肃</option>
                <option value="casual">校园风格</option>
              </select>
              <p class="text-sm text-gray-500 mt-2">请选择您的面试氛围</p>
            </div>
  
            <!-- Interview Guidelines -->
            <div class="text-left mb-8">
              <h3 class="font-semibold text-gray-900 mb-4">面试须知：</h3>
              <ul class="space-y-2 text-sm text-gray-600">
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  请确保您的麦克风已开启并正常工作
                </li>
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  在安静的环境中进行面试，避免背景噪音
                </li>
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  每个问题请尽量在2-3分钟内回答完成
                </li>
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  AI面试官会根据您的回答提供个性化反馈
                </li>
              </ul>
            </div>
  
            <button 
              @click="startQuestions"
              class="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors duration-200"
            >
              开始面试
              <svg class="w-5 h-5 ml-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
  
        <!-- Question Phase -->
        <div v-else-if="phase === 'question'" class="max-w-3xl mx-auto">
          <div class="bg-white rounded-xl p-8 shadow-sm border border-gray-100">
            <!-- AI Response -->
            <div v-if="aiResponse" class="mb-8 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
              <div class="flex items-start">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                  <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <p class="text-blue-800 font-medium mb-1">AI 面试官</p>
                  <p class="text-blue-700">{{ aiResponse }}</p>
                </div>
              </div>
            </div>
  
            <!-- Current Question -->
            <div class="text-center mb-8">
              <h3 class="text-xl font-semibold text-gray-900 mb-4">
                {{ questions[currentQuestion - 1] }}
              </h3>
            </div>
  
            <!-- Voice Recording -->
            <div class="text-center mb-8 flex flex-col items-center">
              <button 
                @click="toggleRecording"
                :class="[
                  'w-20 h-20 rounded-full flex items-center justify-center transition-all duration-200 shadow-lg',
                  isRecording 
                    ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                    : 'bg-green-600 hover:bg-green-700'
                ]"
              >
                <!-- 修复：恢复不录音状态的SVG路径（之前混入CSS代码导致图标失效） -->
                <svg v-if="!isRecording" class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clip-rule="evenodd" />
                </svg>
                <svg v-else class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a2 2 0 114 0v4a2 2 0 11-4 0V7z" clip-rule="evenodd" />
                </svg>
              </button>
              <p class="text-sm text-gray-600 mt-4">
                {{ isRecording ? '点击停止录音' : '点击开始录音' }}
              </p>
              
              <!-- 临时识别结果 -->
              <p v-if="isRecording && interimResult" class="text-sm text-blue-500 mt-2 italic">
                正在识别: {{ interimResult }}
              </p>
              
              <!-- 录音错误信息 -->
              <p v-if="recordingErrorMessage" class="text-sm text-red-500 mt-2">
                {{ recordingErrorMessage }}
              </p>
              
              <!-- 浏览器不支持提示 -->
              <p v-if="browserSupport === false" class="text-sm text-red-500 mt-2">
                您的浏览器不支持语音识别功能，请使用Chrome、Edge或Safari浏览器，或者直接使用文字输入。
              </p>
            </div>
  
            <!-- Transcript -->
            <div v-if="currentTranscript" class="mb-6">
              <h4 class="font-medium text-gray-900 mb-2">您的回答：</h4>
              <div class="p-4 bg-gray-50 rounded-lg border">
                <p class="text-gray-700">{{ currentTranscript }}</p>
              </div>
            </div>
  
            <!-- Alternative Text Input -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                或者直接输入文字回答：
              </label>
              <textarea 
                v-model="textInput"
                rows="4"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="在这里输入您的回答..."
                @blur="provideImmediateFeedback"
              ></textarea>
            </div>
  
            <!-- Action Buttons -->
            <div class="flex justify-between">
              <button 
                @click="previousQuestion"
                :disabled="currentQuestion === 1"
                class="px-4 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                上一题
              </button>
              <button 
                @click="nextQuestion"
                :disabled="!canProceed"
                class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ currentQuestion === 3 ? '完成面试' : '下一题' }}
              </button>
            </div>
          </div>
        </div>
      </main>
  
      <!-- 修复：将弹窗移到template内部（之前在外部导致Vue模板解析错误） -->
      <div v-if="showCompletionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl">
          <div class="text-center mb-6">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">面试完成！</h2>
            <p class="text-gray-600">恭喜您完成了本次面试，即将为您生成面试总结。</p>
          </div>
          <div class="flex justify-center">
            <button 
              @click="goToSummary"
              class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
            >
              查看总结
            </button>
          </div>
        </div>
      </div>
      
      <!-- 新增：AI反馈弹窗 -->
      <div v-if="showFeedbackModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl">
          <div class="text-center mb-6">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">面试官反馈</h2>
            <p class="text-gray-600 text-left">{{ currentFeedback }}</p>
          </div>
          <div class="flex justify-center">
            <button 
              @click="proceedAfterFeedback"
              class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
            >
              好的，继续
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* 添加渐变背景 */
  .min-h-screen {
    background: linear-gradient(135deg, #f0f9ff 0%, #e6fffa 100%);
  }
  
  /* 美化卡片 */
  .bg-white.rounded-xl {
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border: none;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .bg-white.rounded-xl:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transform: translateY(-2px);
  }
  
  /* 美化录音按钮 */
  .w-20.h-20.rounded-full {
    box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.3), 0 4px 6px -2px rgba(5, 150, 105, 0.2);
    transition: all 0.3s;
  }
  
  .w-20.h-20.rounded-full:hover {
    transform: scale(1.05);
    box-shadow: 0 15px 20px -3px rgba(5, 150, 105, 0.4), 0 8px 10px -2px rgba(5, 150, 105, 0.2);
  }
  
  /* 美化AI回复区域 */
  .bg-blue-50.rounded-lg {
    background: linear-gradient(to right, #e6f7ff, #f0f9ff);
    border-left: 4px solid #3b82f6;
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
    transition: all 0.3s;
  }
  
  .bg-blue-50.rounded-lg:hover {
    box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.15);
  }
  
  /* 修复：移除Header标题下划线（用户需求） */
  .header-title {
    position: static !important; /* 取消定位 */
    padding-bottom: 0 !important; /* 取消底部内边距 */
  }
  .header-title::after {
    display: none !important; /* 隐藏下划线伪元素 */
  }
  
  /* 保留问题标题的下划线（仅移除Header标题） */
  .text-xl.font-semibold.text-gray-900:not(.header-title) {
    position: relative;
    display: inline-block;
    padding-bottom: 0.5rem;
  }
  .text-xl.font-semibold.text-gray-900:not(.header-title)::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 3px;
    background: linear-gradient(to right, #059669, #10b981);
    border-radius: 3px;
  }
  
  /* 美化进度条 */
  .bg-green-600.h-1 {
    background: linear-gradient(to right, #059669, #10b981);
    border-radius: 1px;
    box-shadow: 0 1px 2px rgba(5, 150, 105, 0.3);
  }
  
  /* 美化按钮 */
  button.bg-green-600 {
    background: linear-gradient(to right, #059669, #10b981);
    box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3), 0 2px 4px -1px rgba(5, 150, 105, 0.2);
    transition: all 0.3s;
  }
  
  button.bg-green-600:hover {
    background: linear-gradient(to right, #047857, #059669);
    box-shadow: 0 6px 10px -1px rgba(5, 150, 105, 0.4), 0 2px 6px -1px rgba(5, 150, 105, 0.2);
    transform: translateY(-1px);
  }
  
  /* 美化文本输入框 */
  textarea {
    transition: all 0.3s;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
  
  textarea:focus {
    box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.1), 0 2px 4px -1px rgba(5, 150, 105, 0.06);
    border-color: #10b981;
  }
  
  /* 添加动画效果 */
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.7;
    }
  }
  
  .animate-pulse {
    animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
  </style>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Interview',
    data() {
      return {
        phase: 'welcome', // 'welcome', 'question'
        currentQuestion: 1,
        selectedStyle: 'friendly',
        isRecording: false,
        showCompletionModal: false,
        preparedInterviewData: null,
        currentTranscript: '',
        showFeedbackModal: false,
        currentFeedback: '',
        textInput: '',
        aiResponse: '',
        recognition: null,
        answers: [],
        aiResponses: [], // 新增：存储所有问题的反馈
        questions: [
          '请简单介绍一下您自己，包括您的背景和主要经历。',
          '请描述一次您在工作或学习中遇到挑战并成功解决的经历。',
          '您认为自己最大的优势是什么？请举例说明。'
        ],
        interviewStyles: {
          friendly: {
            systemPrompt: `你是一位亲切友好的面试官，名叫Kora。你的特点是：
  - 语气温和亲切亲切，像朋友一样交流
  - 会适当使用鼓励性的语言，如"很好"、"不错"、"您的回答很有见地"
  - 追问时会说"能再详细说说吗？"、"这听起来很有趣，能举个例子吗？"
  - 保持专业但不失温暖的态度，经常使用"我理解"、"确实如此"等共情表达
  - 会给予积极的肯定和建设性的建议
  - 使用一些轻松的过渡语，如"让我们继续聊聊"、"接下来想了解"
  - 回答简洁，控制在50字以内`,
            greeting: '您好！很高兴见到您，我是Kora。今天的面试会很轻松，请放松心情，我们开始吧！'
          },
          formal: {
            systemPrompt: `你是一位正式严肃的面试官，名叫Kora。你的特点是：
  - 语气正式专业，保持商务礼仪和适当的距离感
  - 使用标准的面试用语，如"请详细阐述"、"能否具体说明"、"请举例说明"
  - 追问时会说"请进一步说明"、"能否提供更多细节"、"请具体阐述您在该情境中的角色和贡献"
  - 保持客观中性的态度，避免过多情感表达
  - 会使用一些专业术语和行业词汇
  - 注重逻辑性和结构化的对话方式
  - 会针对回答中的关键点进行有深度的追问
  - 回答简洁，控制在50字以内`,
            greeting: '您好，我是面试官Kora。今天我将对您进行正式面试，请认真回答每个问题。我们现在开始。'
          },
          casual: {
            systemPrompt: `你是一位轻松随和的校园面试官，名叫Kora。你的特点是：
  - 语气轻松自然，像学长学姐一样，有时会用一些网络流行语
  - 会使用一些校园化的表达，如"挺棒的"、"很赞"、"这个回答给满分"
  - 追问时会说"能多聊聊吗？"、"这个很有意思呢"、"有什么有趣的经历可以分享一下吗？"
  - 营造轻松的校园面试氛围，减轻面试压力
  - 会使用一些年轻人常用的表达方式，如"太酷了"、"这个思路很新颖"
  - 适当使用表情符号增加亲和力
  - 会关注应聘者的兴趣爱好和校园经历
  - 回答简洁，控制在50字以内`,
            greeting: '嗨！我是Kora，今天来和你聊聊。就像平时和学长学姐交流一样，放轻松就好！'
          }
        },
        // 补充未声明的变量
        interimResult: '', // 临时语音识别结果
        recordingErrorMessage: '', // 录音错误提示
        browserSupport: null, // 浏览器是否支持语音识别
        autoRestart: false, // 是否自动重启录音
        recordingError: null, // 录音错误信息
        isProcessingFeedback: false // 是否正在处理AI反馈
      }
    },
    computed: {
      canProceed() {
        return this.currentTranscript.trim() || this.textInput.trim()
      }
    },
    mounted() {
      this.initSpeechRecognition()
    },
    methods: {
      // 初始化语音识别
      initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
          this.recognition = new SpeechRecognition()
          this.recognition.continuous = true
          this.recognition.interimResults = true
          this.recognition.lang = 'zh-CN'
  
          this.recognition.onresult = (event) => {
            let finalTranscript = ''
            let interimTranscript = ''
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
              const transcript = event.results[i][0].transcript
              if (event.results[i].isFinal) {
                finalTranscript += transcript
              } else {
                interimTranscript += transcript
              }
            }
            
            if (finalTranscript) {
              this.currentTranscript = (this.currentTranscript + ' ' + finalTranscript).trim()
            }
            
            // 显示临时识别结果
            this.interimResult = interimTranscript || ''
          }
  
          this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error)
            this.isRecording = false
            this.recordingError = event.error
            
            // 友好错误提示
            if (event.error === 'not-allowed') {
              this.recordingErrorMessage = '无法访问麦克风。请确保您已授予麦克风访问权限。'
            } else if (event.error === 'network') {
              this.recordingErrorMessage = '网络错误。请检查您的网络连接。'
            } else {
              this.recordingErrorMessage = '录音出错，请重试。'
            }
          }
  
          this.recognition.onend = () => {
            this.isRecording = false
            // 自动重启录音（无错误时）
            if (this.autoRestart && !this.recordingError) {
              this.recognition.start()
              this.isRecording = true
            }
          }
        } else {
          this.browserSupport = false
        }
      },
      
      // 切换录音状态
      toggleRecording() {
        this.recordingError = null
        this.recordingErrorMessage = ''
        
        if (!this.recognition && this.browserSupport !== false) {
          this.initSpeechRecognition()
        }
        
        if (!this.recognition) {
          this.browserSupport = false
          alert('您的浏览器不支持语音识别功能，请使用Chrome、Edge或Safari浏览器，或者直接使用文字输入。')
          return
        }
  
        if (this.isRecording) {
          this.autoRestart = false
          this.recognition.stop()
          this.isRecording = false
          // 停止录音后自动反馈
          if (this.currentTranscript.trim()) {
            this.provideImmediateFeedback()
          }
        } else {
          try {
            // 请求麦克风权限
            navigator.mediaDevices.getUserMedia({ audio: true })
              .then(() => {
                this.autoRestart = true
                this.recognition.start()
                this.isRecording = true
              })
              .catch(error => {
                console.error('Microphone permission denied:', error)
                this.recordingErrorMessage = '无法访问麦克风。请确保您已授予麦克风访问权限。'
              })
          } catch (error) {
            console.error('Speech recognition start error:', error)
            this.recordingErrorMessage = '启动录音失败，请重试。'
          }
        }
      },
      
      // 即时反馈（停止录音/输入文字后）
      async provideImmediateFeedback() {
        const answer = this.currentTranscript.trim() || this.textInput.trim()
        if (answer && !this.isProcessingFeedback) {
          this.isProcessingFeedback = true
          await this.getAIResponse(answer)
          this.isProcessingFeedback = false
        }
      },
      
      // 开始面试（进入问题阶段）
      startQuestions() {
        this.phase = 'question'
        this.aiResponse = this.interviewStyles[this.selectedStyle].greeting
      },
      
      // 上一题
      previousQuestion() {
        if (this.currentQuestion > 1) {
          this.currentQuestion--
          // 恢复上一题答案
          const previousAnswer = this.answers[this.currentQuestion - 1] || ''
          this.currentTranscript = previousAnswer
          this.textInput = ''
          this.aiResponse = '' // 清空上一题反馈
        }
      },
      
      // 下一题/完成面试
      async nextQuestion() {
        // 正在录音时先停止
        if (this.isRecording) {
          this.autoRestart = false
          this.recognition.stop()
          this.isRecording = false
        }
        
        // 保存当前答案
        const answer = this.currentTranscript.trim() || this.textInput.trim()
        this.answers[this.currentQuestion - 1] = answer
        
        // 获取AI反馈
        if (answer) {
          await this.getAIResponse(answer)
        }
        
        // 第3题：显示完成弹窗
        if (this.currentQuestion === 3) {
          // 准备面试数据（传给总结页）
          this.preparedInterviewData = {
            questions: this.questions.map((text, index) => ({
              text,
              answer: this.answers[index] || '',
              feedback: this.aiResponses[index] || '' // 新增：收集反馈
            })),
            style: this.selectedStyle,
            completedAt: new Date().toISOString()
          }
          // 显示弹窗
          this.showCompletionModal = true
        } else {
          // 下一题：重置输入
          this.currentQuestion++
          this.currentTranscript = ''
          this.textInput = ''
          this.aiResponse = ''
        }
      },
      
      // 跳转到总结页
      goToSummary() {
        this.showCompletionModal = false
        // 传递数据（JSON.stringify避免数组/对象丢失）
        this.$router.push({
          name: 'Summary',
          query: {
            interviewData: JSON.stringify(this.preparedInterviewData)
          }
        })
      },
      
      // 获取AI反馈
      async getAIResponse(userAnswer) {
        this.isProcessingFeedback = true
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/feedback', {
            answer: userAnswer,
            question: this.questions[this.currentQuestion - 1],
            style: this.selectedStyle
          })
          this.aiResponse = response.data.feedback
          // 保存当前问题的反馈
          this.aiResponses[this.currentQuestion - 1] = this.aiResponse
        } catch (error) {
          console.error('AI response error:', error)
          this.aiResponse = '抱歉，AI面试官暂时无法连接，请稍后再试。'
        }
        this.isProcessingFeedback = false
      }
    }
  }
  </script>