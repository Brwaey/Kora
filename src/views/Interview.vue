<template>
  <div class="flex flex-col h-screen bg-gray-100 font-sans">
    <!-- Header - 调整标题位置与summary界面一致 -->
    <header class="bg-white shadow-sm flex-shrink-0 z-10">
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
            {{ interviewStatus }}
          </div>
        </div>
      </div>
    </header>

    <!-- Welcome Phase -->
    <div v-if="phase === 'welcome'" class="flex-grow flex items-center justify-center p-4">
        <div class="text-center bg-white rounded-2xl p-8 sm:p-12 shadow-xl border border-gray-200 max-w-2xl mx-auto transform hover:scale-105 transition-transform duration-300">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">开启您的专属面试体验</h2>
            <p class="text-gray-600 mb-8">请选择您偏好的面试风格，Kora将为您模拟最真实的面试场景。</p>
            <div class="mb-8">
              <select v-model="selectedStyle" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 text-lg">
                <option value="friendly">亲切友好型</option>
                <option value="formal">专业严肃型</option>
                <option value="casual">轻松校园型</option>
              </select>
            </div>
            <button @click="startInterview" class="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              立即开始
            </button>
        </div>
    </div>

    <!-- Chat Interface - 优化布局使其居中并调整宽度 -->
    <main v-else ref="chatArea" class="flex-grow overflow-y-auto p-4 sm:p-6">
      <div class="max-w-3xl mx-auto space-y-6"> <!-- 限制最大宽度并居中 -->
        <div v-for="(message, index) in messages" :key="index" class="chat-message-wrapper">
          <div :class="['flex items-end space-x-3', message.sender === 'ai' ? 'justify-start' : 'justify-end']">
            <!-- Avatar -->
            <div v-if="message.sender === 'ai'" class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
            
            <!-- Message Bubble -->
            <div :class="['max-w-[80%] px-4 py-3 rounded-2xl shadow-sm', 
                          message.sender === 'ai' ? 'bg-white text-gray-800 rounded-tl-none' : 
                                                  'bg-green-600 text-white rounded-tr-none']">
              <p v-html="formatMessage(message.text)"></p>
            </div>
            
            <!-- Avatar for user -->
            <div v-if="message.sender === 'user'" class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <!-- Typing indicator -->
        <div v-if="isAiTyping" class="flex justify-start">
          <div class="max-w-xs p-4 rounded-2xl shadow-md bg-white">
            <div class="typing-indicator"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>
    </main>

    <!-- Action Button Area - 修改为双按钮并排 -->
    <footer v-if="showNextButton" class="bg-transparent py-4 px-4 sm:px-6 flex-shrink-0">
        <div class="max-w-3xl mx-auto"> <!-- 与对话区域宽度保持一致 -->
            <div class="flex gap-3"> <!-- 使用flex布局实现并排 -->
                <button @click="continueAnswering" class="flex-1 px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-all duration-300 shadow-md">
                    继续回答该问题
                </button>
                <button @click="requestNextQuestion" class="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all duration-300 shadow-md">
                    {{ isLastQuestion ? '完成面试并查看总结' : '好的，请问下一题' }}
                </button>
            </div>
        </div>
    </footer>

    <!-- Input Area -->
    <footer v-if="phase === 'question' && !isAiTyping && !showNextButton" class="bg-white border-t p-3 sm:p-4 flex-shrink-0">
      <div class="max-w-3xl mx-auto flex items-center space-x-2 sm:space-x-4"> <!-- 与对话区域宽度保持一致 -->
        <button @click="toggleRecording" :class="['p-3 rounded-full text-white transition-all duration-300 shadow-md', isRecording ? 'bg-red-500 animate-pulse' : 'bg-green-600 hover:bg-green-700']">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path v-if="!isRecording" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4z"/><path v-else d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a2 2 0 114 0v4a2 2 0 11-4 0V7z" /></svg>
        </button>
        <textarea v-model="userInput" @keyup.enter.exact="sendMessage" placeholder="请在此输入或点击麦克风回答..." class="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-shadow" rows="1"></textarea>
        <button @click="sendMessage" :disabled="!userInput.trim() && !isRecording" class="px-5 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 disabled:opacity-50 transition-all duration-300 shadow-md">
          发送
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const chatArea = ref(null);

// --- State Management ---
const phase = ref('welcome');
const selectedStyle = ref('friendly');
const messages = ref([]);
const userInput = ref('');
const isRecording = ref(false);
const interimResult = ref('');
const recordingErrorMessage = ref('');
const currentQuestionIndex = ref(0);
const isAiTyping = ref(false);
const showNextButton = ref(false);

const questions = [
  "你最近完成的一件最有成就感的事是什么？你在其中扮演了什么角色？",
  "请讲讲一次你解决冲突或困难的经历。",
  "如果你加入一个你不熟悉的项目团队，你会如何快速融入？"
];

// --- Computed Properties ---
const interviewStatus = computed(() => {
  if (phase.value === 'finished') return '面试已完成';
  if (phase.value === 'question') return `问题 ${currentQuestionIndex.value + 1}/${questions.length}`;
  return '准备开始';
});
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.length - 1);

// --- Core Functions ---
const startInterview = () => {
  phase.value = 'question';
  addMessage('ai', `你好！我是你的AI面试官Kora。很高兴与你交流。\n\n我们开始吧，这是第一个问题：\n**${questions[0]}**`);
};

const sendMessage = async () => {
  const text = userInput.value.trim();
  if (!text) return;
  addMessage('user', text);
  userInput.value = '';
  isAiTyping.value = true;
  await processUserAnswer(text);
};

const processUserAnswer = async (answer) => {
  const currentQ = questions[currentQuestionIndex.value];
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/feedback', {
      question: currentQ, answer, style: selectedStyle.value
    });
    addMessage('ai', response.data.feedback);
  } catch (error) {
    addMessage('ai', '抱歉，网络似乎有些问题，我暂时无法连接。');
  } finally {
    isAiTyping.value = false;
    showNextButton.value = true; // 显示按钮组
  }
};

// 新增：继续回答当前问题
const continueAnswering = () => {
  showNextButton.value = false; // 隐藏按钮组，显示输入区域
};

const requestNextQuestion = () => {
    showNextButton.value = false;
    if (isLastQuestion.value) {
        endInterview();
    } else {
        isAiTyping.value = true;
        addMessage('ai', '好的，我们继续。');
        setTimeout(() => {
            currentQuestionIndex.value++;
            addMessage('ai', `接下来是这个问题：\n**${questions[currentQuestionIndex.value]}**`);
            isAiTyping.value = false;
        }, 1200);
    }
};

const endInterview = () => {
  phase.value = 'finished';
  isAiTyping.value = true;
  addMessage('ai', '非常感谢您的参与！本次面试的所有问题都已完成。\n\n我将根据我们刚才的对话，为您生成一份详细的面试表现总结报告。请稍候...');
  setTimeout(() => {
    // 构建完整对话记录
    const conversation = messages.value.map((msg, index) => ({
      id: index + 1,
      sender: msg.sender, // 'ai' 或 'user'
      text: msg.text,
      timestamp: new Date().toISOString() // 记录消息时间戳
    }));

    const interviewData = {
      style: selectedStyle.value,
      completedAt: new Date().toISOString(),
      questions: questions.map((q, index) => {
        // 查找对应问题的回答
        const answerMsg = messages.value.find(m => 
          m.sender === 'user' && 
          messages.value.indexOf(m) > messages.value.findIndex(mm => 
            mm.sender === 'ai' && mm.text.includes(q)
          )
        );
        
        // 查找对应问题的反馈
        const feedbackMsg = messages.value.find(m => 
          m.sender === 'ai' && 
          messages.value.indexOf(m) > (answerMsg ? messages.value.indexOf(answerMsg) : -1) &&
          messages.value.indexOf(m) < (index < questions.length - 1 ? 
            messages.value.findIndex(mm => mm.text.includes(questions[index + 1])) : 
            messages.value.length)
        );
        
        return {
          id: index + 1,
          text: q,
          answer: answerMsg ? answerMsg.text : '',
          feedback: feedbackMsg ? feedbackMsg.text : ''
        };
      }),
      // 新增：完整对话记录
      conversation: conversation
    };
    router.push({ name: 'Summary', query: { interviewData: JSON.stringify(interviewData) } });
  }, 2500);
};

// --- Helper Functions ---
const addMessage = (sender, text) => {
  messages.value.push({ sender, text });
  nextTick(() => {
    if (chatArea.value) chatArea.value.scrollTop = chatArea.value.scrollHeight;
  });
};

const formatMessage = (text) => {
  // 简单的markdown转换
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
};

// --- Voice Recording ---
let recognition = null;
onMounted(() => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'zh-CN';
    recognition.onresult = (event) => {
      let finalTranscript = '';
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript;
        else interimTranscript += event.results[i][0].transcript;
      }
      interimResult.value = interimTranscript;
      if (finalTranscript) userInput.value += (userInput.value ? ' ' : '') + finalTranscript;
    };
    recognition.onerror = (event) => {
      recordingErrorMessage.value = `语音识别错误: ${event.error}`;
      stopRecording();
    };
  } else {
    recordingErrorMessage.value = '您的浏览器不支持语音识别。';
  }
});

const toggleRecording = () => {
  if (!recognition) return;
  isRecording.value ? stopRecording() : startRecording();
};

const startRecording = () => {
  interimResult.value = '';
  recordingErrorMessage.value = '';
  recognition.start();
  isRecording.value = true;
};

const stopRecording = () => {
  if (recognition) recognition.stop();
  isRecording.value = false;
  if (userInput.value.trim()) sendMessage();
};
</script>

<style scoped>
.h-screen { height: 100vh; }
textarea { resize: none; }

.chat-message-wrapper {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.typing-indicator span {
  height: 8px; width: 8px; background-color: #9ca3af; border-radius: 50%;
  display: inline-block; margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>