# Kora 语音面试官

一个基于 Vue 3 的智能中文语音面试系统，支持语音识别、AI 交互和面试记录导出。

## 功能特性

- 🎤 **语音识别**: 使用 Web Speech API 实现中文语音识别
- 🤖 **智能交互**: AI 驱动的面试官，提供个性化反馈
- 📝 **完整记录**: 自动记录面试问答，支持多种格式导出
- 🎨 **现代界面**: 响应式设计，支持移动端访问
- 🔄 **持续录音**: 支持连续语音录制，不会覆盖之前的内容
- 📊 **表现分析**: 提供详细的面试表现分析和建议

## 技术栈

- **前端框架**: Vue 3 + Composition API
- **路由管理**: Vue Router 4
- **构建工具**: Vite
- **语音识别**: Web Speech API
- **样式**: 原生 CSS (无第三方UI库)

## 项目结构

\`\`\`
kora-voice-interview/
├── public/                 # 静态资源
├── src/
│   ├── views/             # 页面组件
│   │   ├── Home.vue       # 首页
│   │   ├── Interview.vue  # 面试页面
│   │   └── Summary.vue    # 总结页面
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── index.html            # HTML 模板
├── package.json          # 项目配置
├── vite.config.js        # Vite 配置
└── README.md            # 项目说明
\`\`\`

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

项目将在 `http://localhost:3000` 启动

### 3. 构建生产版本

```bash
npm run build
```

构建文件将输出到 `dist` 目录

### 4. 预览生产版本

```bash
npm run preview
```

## 使用说明

### 面试流程

1. **欢迎页面**: 选择面试风格，了解面试须知
2. **语音面试**: 回答 3 个行为面试问题
3. **面试总结**: 查看回答记录和表现分析


### 语音功能

- 点击"开始录音"按钮开始语音识别
- 系统会持续录音直到再次点击"停止录音"
- 支持连续语音输入，不会覆盖之前的内容
- 提供文本输入作为语音识别的备选方案


### 面试风格

- **亲切友好**: 温和的交流方式
- **正式严肃**: 专业的面试氛围
- **校园风格**: 轻松的校园面试体验


## 浏览器兼容性

- Chrome 25+
- Firefox 44+
- Safari 14.1+
- Edge 79+


**注意**: 语音识别功能需要 HTTPS 环境或 localhost

## 部署建议

### Vercel 部署

1. 将代码推送到 GitHub
2. 在 Vercel 中导入项目
3. 自动部署完成


### Netlify 部署

1. 运行 `npm run build`
2. 将 `dist` 目录上传到 Netlify
3. 配置重定向规则支持 SPA


### GitHub Pages 部署

1. 修改 `vite.config.js` 设置正确的 base 路径
2. 运行 `npm run build`
3. 将 `dist` 目录内容推送到 gh-pages 分支


## 开发说明

### 语音识别实现

项目使用 Web Speech API 的 `SpeechRecognition` 接口：

- 设置 `continuous: true` 支持连续识别
- 设置 `interimResults: true` 显示实时结果
- 使用 `lang: 'zh-CN'` 支持中文识别


### 数据存储

面试数据通过 Vue Router 的 params 传递，支持：

- JSON 格式导出
- 文本格式导出
- 打印功能