// Antigravity 2.34.0 local UI translation. No network, storage, IPC or model changes.
(() => {
  'use strict';
  if (typeof document === 'undefined' || !/^https:\/\/127\.0\.0\.1:\d+$/.test(location.origin)) return;
  const dict = {
    'Workspace':'工作区','View':'视图','Window':'窗口','New Conversation':'新建对话',
    'Automations':'自动化','Customizations':'自定义','Projects':'项目','Settings':'设置',
    'General':'常规','Application':'应用','Appearance':'外观','Shortcuts':'快捷键',
    'Notifications':'通知','Models':'模型','Browser':'浏览器','Not in Project':'未关联项目',
    'Conversations':'对话','Give Feedback':'意见反馈','Close':'关闭','Open':'打开',
    'Cancel':'取消','Save':'保存','Apply':'应用','Done':'完成','Delete':'删除','Rename':'重命名',
    'Search':'搜索','Search Conversations':'搜索对话','Toggle Sidebar':'切换侧边栏',
    'Go Back':'后退','Go Forward':'前进','Display Options':'显示选项','Create New Project':'新建项目',
    'No Project':'未选择项目','Add context':'添加上下文','Send message':'发送消息',
    'Record voice memo':'录制语音备忘','Select Model':'选择模型','More actions':'更多操作',
    'Build me a web app':'帮我构建网页应用','Add a Gemini feature to my app':'为我的应用添加 Gemini 功能',
    'Bring over my setup from other Agentic Developer Tools':'从其他智能开发工具迁移我的配置',
    'Dismiss suggestion':'关闭建议','Announcements and tips':'公告与提示','Dismiss':'关闭',
    'Introducing Gemini 4 Neon':'Gemini 4 Neon 全新登场',
    'Our best balance of intelligence, cost, and latency. Get building today with Neon.':'兼顾智能、成本与响应速度，立即使用 Neon 开始构建。',
    'Configure agent execution, queued message delivery, and permissions.':'配置智能体执行方式、消息队列与权限。',
    'Interface Layout':'界面布局','Knowledge Work':'知识工作','Software Engineering':'软件工程',
    'Simplified interface for research, writing, and everyday tasks.':'适用于研究、写作和日常任务的简洁界面。',
    'Full interface for coding, developer tools, and managing agents.':'适用于编程、开发工具及智能体管理的完整界面。',
    'Global Permissions':'全局权限','Configure global allowed and denied resource permissions.':'配置全局资源的允许与拒绝权限。',
    'Learn more.':'了解更多。','Learn more':'了解更多','Permission preset':'权限预设',
    'Controls the actions the agent can take.':'控制智能体可以执行的操作。',
    'Default':'默认','Tool permissions':'工具权限','Modify permissions for file, terminal, and MCP tools.':'调整文件、终端与 MCP 工具的权限。',
    'Network access rules':'网络访问规则','Configure allowed and denied URLs for reading.':'配置允许与禁止读取的网址。',
    'Input Box':'输入框','Queued messages':'消息队列','Configure when follow-up messages are sent.':'设置后续消息的发送时机。',
    'Queue until after the current turn.':'排队等待当前轮次结束。','Interrupt the agent and send immediately.':'中断智能体并立即发送。',
    'Queue':'排队','Send Immediately':'立即发送','Keyboard shortcuts':'键盘快捷键',
    'Choose which key sends a message in the chat composer.':'选择在对话输入框中发送消息的按键。',
    'Press Enter to send, Shift+Enter for a new line.':'按 Enter 发送，Shift+Enter 换行。',
    'Press Ctrl+Enter to send, Enter for a new line.':'按 Ctrl+Enter 发送，Enter 换行。',
    'Voice mode':'语音模式','Voice':'声音','The voice used in Voice mode. Powered by Gemini Live.':'语音模式使用的声音，由 Gemini Live 提供支持。',
    'Not set':'未设置','Change':'更改','Microphone':'麦克风','Input device for voice mode and dictation.':'语音模式与语音输入使用的设备。',
    'System default':'系统默认','Volume':'音量',"How loud Antigravity’s voice is.":'Antigravity 语音的播放音量。',
    "How loud Antigravity's voice is.":'Antigravity 语音的播放音量。','Voice volume':'语音音量',
    'Manage Antigravity app settings.':'管理 Antigravity 应用设置。','Prevent Sleep':'防止休眠',
    'Prevent the computer from sleeping while the app is running.':'应用运行时阻止电脑休眠。','Keep In Menu Bar':'保留在菜单栏',
    'Keep the app accessible from the menu bar and running in the background when all windows are closed.':'关闭所有窗口后，应用仍在后台运行并可从菜单栏访问。',
    'Remote Control':'远程控制','Enable Remote Control':'启用远程控制','Work with local agents from another device.':'通过其他设备使用本地智能体。',
    'Notification Settings':'通知设置',"To modify notification settings, open your operating system's system preferences.":'请打开操作系统设置以修改通知选项。',
    'Open System Preferences':'打开系统设置','Version':'版本','App version':'应用版本','Advanced Settings':'高级设置',
    "Configure the agent's visual theme and display preferences.":'配置智能体的视觉主题与显示偏好。',
    'Chat':'对话','Conversation Steps':'对话步骤','Choose how much detail is shown during a conversation.':'选择对话中显示的详细程度。',
    'Verbose':'详细','Theme':'主题','System':'跟随系统','Light':'浅色','Dark':'深色','Contrast':'对比度',
    'Strong':'高','Font':'字体','Font Size':'字号','Dark Theme':'深色主题','Light Theme':'浅色主题','Preset':'预设',
    'Default Dark':'默认深色','Default Light':'默认浅色','Background':'背景','Foreground':'前景','Accent':'强调色',
    'Background color picker':'背景颜色选择器','Foreground color picker':'前景颜色选择器','Accent color picker':'强调色选择器',
    'Code Preview':'代码预览','Chat Layout':'对话布局','Conversation Width':'对话宽度',
    'Configure the maximum width of the conversation panel.':'配置对话面板的最大宽度。',
    'Narrow':'窄','Wide':'宽','Fill':'填满','Accessibility':'无障碍','Screen Reader Mode':'屏幕阅读器模式',
    'Optimize the interface and terminal output for screen readers.':'为屏幕阅读器优化界面与终端输出。',
    'Keyboard Shortcuts':'键盘快捷键','Action':'操作','Shortcut':'快捷键','Search shortcuts':'搜索快捷键',
    'New Project':'新建项目','Open Project':'打开项目','Add Project':'添加项目','Select project':'选择项目',
    'Recent':'最近','Name':'名称','Description':'描述','Create':'创建','Import':'导入','Export':'导出',
    'Enabled':'已启用','Disabled':'已禁用','Enable':'启用','Disable':'禁用','Connect':'连接','Disconnect':'断开连接',
    'Connected':'已连接','Not connected':'未连接','Add':'添加','Remove':'移除','Reset':'重置','Edit':'编辑',
    'Copy':'复制','Copied':'已复制','Retry':'重试','Continue':'继续','Back':'返回','Next':'下一步',
    'Loading...':'加载中…','Loading…':'加载中…','Check for Updates':'检查更新','About Antigravity':'关于 Antigravity',
    'Quit Antigravity':'退出 Antigravity','New Window':'新建窗口','Minimize':'最小化','Zoom In':'放大','Zoom Out':'缩小',
    'Actual Size':'实际大小','Toggle Full Screen':'切换全屏','Help':'帮助','Documentation':'文档','Docs':'文档',
    'Rules':'规则','Skills':'技能','Workflows':'工作流','MCP Servers':'MCP 服务器','Extensions':'扩展',
    'Search models':'搜索模型','Manage Models':'管理模型','Default Model':'默认模型',
    'Select a model':'选择模型','All':'全部','Recommended':'推荐','Install':'安装','Installed':'已安装',
    'Configure notifications':'配置通知','Sound':'声音','Desktop notifications':'桌面通知',
    'Sort by':'排序方式','Last modified':'最后修改','Alphabetical':'按名称','Show all':'显示全部',
    'Start Voice mode':'开始语音模式','Message input':'消息输入框',
    'Ask anything, @ to mention, / for actions':'输入问题，使用 @ 引用内容，使用 / 选择操作',
    'Keyboard shortcuts for quick navigation and control.':'用于快速导航与操作的键盘快捷键。',
    'Navigation':'导航','Open Conversation Picker':'打开对话选择器','Open File Search':'打开文件搜索',
    'Open Command Palette':'打开命令面板','Close Tab':'关闭标签页','New Tab':'新建标签页','Reopen Closed Tab':'重新打开已关闭标签页',
    'Select Previous Conversation':'选择上一个对话','Select Next Conversation':'选择下一个对话',
    'Move Conversation Up':'上移对话','Move Conversation Down':'下移对话','Previous Side Panel Tab':'上一个侧面板标签页',
    'Next Side Panel Tab':'下一个侧面板标签页','Open Keyboard Shortcuts':'打开快捷键设置','Open Settings':'打开设置',
    'Conversation':'对话','Focus Input':'聚焦输入框','Submit Prompt (Alternate to Enter)':'提交提示词（Enter 的备用快捷键）',
    'Enter always submits. This adds a second shortcut.':'Enter 始终用于提交，可在此添加另一组快捷键。',
    'Jump to Previous Prompt':'跳转到上一个提示词','Jump to Next Prompt':'跳转到下一个提示词','Cancel Generation':'取消生成',
    'Toggle Model Selector':'切换模型选择器','Toggle Project Selector':'切换项目选择器','Toggle Environment Selector':'切换环境选择器',
    'Toggle Voice Recording':'切换语音录制','Mute Voice Mic':'麦克风静音','Mute Voice Speaker':'扬声器静音',
    'Find in Conversation':'在对话中查找','Find in Pane':'在面板中查找','Add to Chat/Quote':'添加到对话／引用',
    'Comment on Selection':'评论所选内容','Side Question Selection':'针对所选内容提问',
    'Split Conversation Horizontally':'水平拆分对话','Split Conversation Vertically':'垂直拆分对话',
    'Pin / Unpin Conversation':'置顶／取消置顶对话','Archive This Conversation':'归档当前对话','Layout Controls':'布局控制',
    'Toggle Side Panel':'切换侧面板','Toggle Maximize Side Panel':'切换侧面板最大化','Toggle Overview Panel':'切换概览面板',
    'Toggle Terminal':'切换终端','Split Terminal':'拆分终端','New Terminal Tab':'新建终端标签页',
    'Terminal: Add to Chat':'终端：添加到对话','Terminal: Select All':'终端：全选','Reset Zoom':'重置缩放',
    'Manage your notification preferences.':'管理通知偏好。','Enable Notifications for Agent':'启用智能体通知',
    'Show system notifications when your action is needed or the agent finishes.':'需要你操作或智能体完成任务时显示系统通知。',
    'Enable Sounds for Agent':'启用智能体提示音','Play a sound when your action is needed or the agent finishes.':'需要你操作或智能体完成任务时播放提示音。',
    'Set the volume of agent sounds.':'设置智能体提示音音量。','Chime volume':'提示音音量',
    'Models & Usage':'模型与用量','Refresh quota and credits data':'刷新配额与积分数据','Manage your model quota and credits.':'管理模型配额与积分。',
    'Plan':'订阅方案','Your Plan: Google AI Pro':'你的方案：Google AI Pro','You can upgrade to a Google AI Ultra plan to receive higher rate limits.':'可升级至 Google AI Ultra 方案以获取更高的使用限额。',
    'Upgrade':'升级','Model Credits':'模型积分','Enable AI Credit Overages':'启用超额 AI 积分使用',
    "When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota. Antigravity will always use your model quota first before using AI credits.":'开启后，模型配额耗尽时，Antigravity 将使用 AI 积分继续处理模型请求。系统始终优先使用模型配额。',
    'Orchestrator Settings':'统筹智能体设置',
    'Choose the models Orchestrator uses. A larger, smarter orchestrator model with a faster, cheaper executor gives high quality for fewer tokens.':'选择统筹智能体使用的模型。高智能的统筹模型搭配更快、更经济的执行模型，可用更少的词元获得较高质量。',
    'Orchestrator Model':'统筹模型','Plans the work, makes design decisions, and reviews the result. Pick a top-tier model. You can also pick one per conversation from the Orchestrator row in the model menu.':'负责规划任务、作出设计决策并审查结果，建议选择高性能模型。也可从模型菜单的统筹选项中为每个对话单独选择。',
    'Executor Model':'执行模型','Carries out the plan: searches, edits, builds, and tests. Pick a faster, cheaper model.':'执行计划，包括搜索、编辑、构建与测试，建议选择更快、更经济的模型。','Model Quota':'模型配额',
    'Configure built-in browser, link opening, and browser subagent preferences.':'配置内置浏览器、链接打开方式与浏览器子智能体偏好。',
    'Built-in Browser':'内置浏览器','Open Links In':'链接打开方式','Choose where links open by default when clicked.':'选择点击链接时默认使用的浏览器。',
    'External Browser':'外部浏览器','Download Location':'下载位置','Folder where files downloaded in the built-in browser are saved.':'保存内置浏览器下载文件的文件夹。',
    'Change…':'更改…','Browsing History':'浏览记录','Clear visited URLs and autocomplete suggestions from the built-in browser.':'清除内置浏览器访问过的网址与自动补全建议。',
    'Clear':'清除','Browser Subagent':'浏览器子智能体','Browser Actuation Rules':'浏览器操作规则',
    'Configure allowed and denied URLs for the browser subagent. It runs in the built-in browser, so no separate browser install is needed.':'配置浏览器子智能体允许与禁止访问的网址。它在内置浏览器中运行，无需单独安装浏览器。'
  };
  const skip = 'script,style,pre,code,textarea,input,[contenteditable]:not([contenteditable="false"]),[role="textbox"],[role="combobox"]:not(button),.monaco-editor,[data-message-id],[data-message-author-role],[data-testid*="message"],[class*="markdown"],[class*="prose"],article';
  const chrome = 'nav,button,[role="button"],[role="dialog"],[role="menu"],[role="menuitem"],[role="tooltip"],[role="tab"],[role="navigation"],[role="status"],[role="alert"],h1,h2,h3,label';
  function translate(text) {
    const key = text.trim();
    if (Object.prototype.hasOwnProperty.call(dict,key)) return text.replace(key,dict[key]);
    const hello = /^Hey ([^\n]{1,80}), what should we build today\?$/.exec(key);
    if(hello) return text.replace(key,`你好，${hello[1]}，今天想构建什么？`);
    const welcome=/^Welcome back, ([^\n]{1,80})\. Where should we pick up\?$/.exec(key);
    if(welcome) return text.replace(key,`欢迎回来，${welcome[1]}。我们从哪里继续？`);
    const next=/^Good to see you, ([^\n]{1,80})\. What's next\?$/.exec(key);
    return next ? text.replace(key,()=>`很高兴见到你，${next[1]}。接下来做什么？`) : text;
  }
  function eligible(el) {
    if (!el || el.closest(skip)) return false;
    // Project and conversation links can carry user-authored names.
    const link=el.closest('a');
    if(link && el.closest('nav,[role="navigation"]') && !['/','/customizations'].includes(new URL(link.href,location.href).pathname)) return false;
    return !!el.closest(chrome);
  }
  function visit(root) {
    if (root.nodeType === 3) {
      if (eligible(root.parentElement)) { const t=translate(root.nodeValue); if(t!==root.nodeValue) root.nodeValue=t; }
      return;
    }
    if (root.nodeType!==1 || root.matches(skip)) return;
    // Attribute translations change display/accessibility strings, never values or identifiers.
    if(eligible(root)) for(const attr of ['title','aria-label']) {
      const value=root.getAttribute(attr);
      if(value) {const translated=translate(value); if(translated!==value) root.setAttribute(attr,translated);}
    }
    for (const child of Array.from(root.childNodes)) visit(child);
  }
  function start() {
    if (!document.body) return;
    const pending=new Set(); let scheduled=false;
    const observer=new MutationObserver(records=>{
      for(const r of records) {
        if(r.type==='characterData' || r.type==='attributes') pending.add(r.target);
        else for(const n of r.addedNodes) pending.add(n);
      }
      if(!scheduled && pending.size) {
        scheduled=true;
        setTimeout(()=>{scheduled=false; const nodes=Array.from(pending); pending.clear(); for(const n of nodes) if(n.isConnected) visit(n);},60);
      }
    });
    visit(document.body);
    observer.observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['title','aria-label']});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();
