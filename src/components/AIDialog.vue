<template>
  <div>
    <!-- 悬浮按钮 -->
    <button v-if="!isDialogOpen" id="toggle-dialog" class="toggle-button" @click="openDialog">
      <span class="button-text">AI小助手</span>
    </button>
    <!-- 人工智能对话框（侧边栏） -->
    <div :class="['dialog', { open: isDialogOpen }]">
      <div class="dialog-header">
        <div class="title">
          <h3>眼科智能小助手</h3>
        </div>
        <button id="close-dialog" class="close-button" @click="closeDialog">
          &times;
        </button>
      </div>
      <div class="dialog-content" id="dialog-content">
        <div v-for="(message, index) in conversationHistory" :key="index"
          :class="message.role === 'user' ? 'user-message-wrapper' : 'answer-wrapper'">
          <div :class="message.role === 'user' ? 'user-message' : 'answer'"
            v-html="message.role === 'assistant' && message.isTyping ? message.currentPart : message.content">
          </div>
        </div>
        <div v-if="isLoading && !hasAnswerTyping" class="loading dot-dance"></div>
      </div>
      <div class="input-section">
        <div class="shortcut-buttons">
          <div v-for="(content, index) in shortcutButtons" :key="index">
            <button @click="getExternalMessage(index)">{{ content }}</button>
          </div>
        </div>
        <div class="user-input">
          <input type="text" v-model="userInput" placeholder="输入你的消息" @keydown.enter="sendMessageByInput" />
          <button :disabled="!canSendMessage || isLoading || hasAnswerTyping" @click="sendMessageByInput">
            <span class="button-icon">
              <span v-if="!(isLoading || hasAnswerTyping)" class="submit">&uarr;</span>
              <span v-else class="spinner"></span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    shortcutButtons: {
      type: Array,
      default: () => []
    },
    shortcutFunctions: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isDialogOpen: false,
      userInput: "",
      conversationHistory: [],
      isLoading: false,
      canSendMessage: false,
      hasAnswerTyping: false,
    };
  },
  watch: {
    userInput(newValue) {
      // if (!(this.isLoading || this.hasAnswerTyping)) {
      this.canSendMessage = newValue.trim() !== "";
      // }
    },
  },
  methods: {
    openDialog() {
      this.isDialogOpen = true;
      this.$emit('open');
    },
    closeDialog() {
      this.isDialogOpen = false;
      this.$emit('close')
    },
    //这里用于获取外部函数数据并得到外部传送的答案
    async getExternalMessage(index) {
      this.isLoading = true;
      this.conversationHistory.push({ role: "user", content: this.shortcutButtons[index] });
      setTimeout(() => {
        this.scrollToBottom();
      }, 1);
      try {
        const functionNum = this.shortcutFunctions.length;
        if (functionNum === 0) {
          this.setAnswer("您还未提供外部函数接口,请重新设置!");
        } else if (functionNum < index) {
          this.setAnswer("未在提供的函数中找到想要的接口,请重新设置");
        } else {
          const functionName = this.shortcutFunctions[index];
          // 检查该函数名对应的函数是否存在
          if (typeof this.$parent[functionName] === 'function') {
            const result = await this.$parent[functionName]();
            const processedAnswer=this.processAnswer(result);
            this.setAnswer(processedAnswer);
          } else {
            this.setAnswer(`未在父组件中找到名为 ${functionName} 的函数不存在`);
          }
        }
        this.isLoading = false;
        await this.typeAnswer(this.conversationHistory.length - 1);
      } catch (error) {
        console.error("获取答案出错:", error);
        // 显示错误信息
        this.conversationHistory.push({
          role: "error",
          content: "获取答案时出错",
        });
      }
    },
    sendMessageByInput() {
      if (!this.canSendMessage || this.isLoading || this.hasAnswerTyping) return;
      const message = this.userInput.trim();
      if (message === "") return;
      this.canSendMessage = false;
      // 显示用户消息
      this.conversationHistory.push({ role: "user", content: message });
      this.userInput = "";
      this.displayAnswer(message)
    },
    async displayAnswer(message) {
      setTimeout(() => {
        this.scrollToBottom();
      }, 1);
      this.isLoading = true;
      this.hasAnswerTyping = false;
      try {
        // 获取答案
        const answer = await this.getAnswer(message);
        // 处理格式
        const processedAnswer = this.processAnswer(answer);
        // 准备以打字机效果显示答案
        this.setAnswer(processedAnswer);
        this.hasAnswerTyping = true;
        this.isLoading = false;
        await this.typeAnswer(this.conversationHistory.length - 1);
      } catch (error) {
        console.error("获取答案出错:", error);
        // 显示错误信息
        this.conversationHistory.push({
          role: "error",
          content: "获取答案时出错",
        });
      } finally {
        this.hasAnswerTyping = false;
        const message = this.userInput.trim();
        if (message != "")
          this.canSendMessage = true;
        else this.canSendMessage = false;
      }
    },
    setAnswer(answer) {
      this.conversationHistory.push({
        role: "assistant",
        content: answer,
        isTyping: true,
        currentPart: "",
      });
    },
    //向后端发送数据并获取答案
    getAnswer(userMessage) {
      return new Promise((resolve) => {
        setTimeout(() => {
          // 这里简单返回用户输入的倒序作为示例答案
          resolve("针对50岁男性患者晚期青光眼的情况，以下是针对性的诊断建议和治疗流程：\n\n### 1. 治疗建议\n- **眼内压控制**：在晚期青光眼患者中，眼内压的控制是防止进一步视神经损害的关键。可以考虑如下方式：\n  - **药物治疗**：根据患者的个体耐受性及以往用药记录，选择合适的降眼压药物组合。\n  - **激光治疗**：如需要可考虑进行处于相对安全的范围内的激光小梁成形术或激光周边虹膜切开术，以改善房水流出。\n  - **手术治疗**：对于需要手术干预的患者，可以考虑进行青光眼滤过手术（如小梁切除术）或管状阀植入手术。\n\n### 2. 检查计划\n- **眼压监测**：定期监测眼内压，评估治疗效果。\n- **视野检查**：使用电脑视野计定期进行视野检测，记录视野缺损的进展情况。\n- **视神经检查**：使用OCT（光学相干断层扫描）检查视网膜神经纤维层厚度，评估视神经的损伤程度。\n- **房角检查**：使用前房角镜检查房角的开放情况，如有必要进行房水动力学检查。\n\n### 3. 用药建议\n根据患者的具体情况，可以考虑以下几类降眼压药物：\n- **β-adrenergic拮抗剂**（如美托洛尔眼药水）\n- **前列腺素类**（如拉坦前列素眼药水）\n- **碳酸酐酶抑制剂**（如乙酰唑胺口服或磺酰胺眼药水）\n- **α2-adrenergic激动剂**（如布林佐胺眼药水）\n\n在实施药物治疗时，务必注意患者可能的副作用和合并症，同时对药物的相互作用进行评估。如果患者对某些药物有过敏或不良反应，需及时调整用药计划。\n\n### 总结\n鉴于患者已经处于青光眼的晚期阶段，治疗的重点在于降低眼内压，减缓视神经进一步损害的进展。通过综合的检查与个体化的用药计划，可以为患者提供最佳的管理方案。同时，患者的生活方式调整（如合理控制体重、避免剧烈运动等）也对病情有一定影响，建议进行相应的指导和提醒。");
          console.log(userMessage)
        }, 3000);
      });
    },
    processAnswer(answer) {
      // 处理换行和加粗格式
      answer = answer.replace(/\n/g, '<br>');
      answer = answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // 替换短横线'-'为'·'
      answer = answer.replace(/-/g, '&#8226');
      // 在###和\n之间的内容用<h3></h3>包围
      answer = answer.replace(/###(.*?)(<br>)/g, '<h3>$1</h3>');
      // 处理连续换行符，只保留前两个
      answer = answer.replace(/(<br>){2,}/g, '<br>');
      return answer;
    },
    typeAnswer(index) {
      return new Promise((resolve) => {
        const message = this.conversationHistory[index];
        const typeNextChar = () => {
          if (message.currentPart.length < message.content.length) {
            message.currentPart += message.content[message.currentPart.length];
            setTimeout(typeNextChar, 5);
          } else {
            // 打字完成，移除打字机效果标识
            delete this.conversationHistory[index].isTyping;
            delete this.conversationHistory[index].currentPart;
            this.scrollToBottom();
            resolve();
          }
        };
        typeNextChar();
      });
    },
    scrollToBottom() {
      const dialogContent = this.$el.querySelector("#dialog-content");
      dialogContent.scrollTop = dialogContent.scrollHeight;
    },
  },
};
</script>

<style scoped>
/* 全局样式 */
/* body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
} */

/* 悬浮按钮样式 */
.toggle-button {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1001;
  padding: 20px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-top-right-radius: 50px;
  border-bottom-right-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  width: 20px;
}

.toggle-button:hover {
  background-color: #0056b3;
}

.button-text {
  margin-right: 5px;
}

.icon {
  font-size: 18px;
}

/* 对话框（侧边栏）样式 */
.dialog {
  position: absolute;
  left: -100%;
  /* top: 5%;
  bottom: 5%; */
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e6f0f8 0%, #d9e8f2 100%);
  border-right: 1px solid #ccc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: left 0.3s ease;
}

.dialog.open {
  left: 0;
}

.title{
  width:90%;
  text-align: center;
}

.dialog-header {
  height:8;
  padding: 15px;
  background-color: #c6e0f0;
  border-bottom: 1px solid #b3d5e9;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #ffffff;
}

.close-button:hover {
  color: #ffffff;
}

.dialog-content {
  padding: 15px;
  overflow-y: auto;
  height: 63%;
}

.input-section {
  border-top: 1px solid #e0e8f1;
}

.shortcut-buttons {
  width: 100%;
  height: 35px;
  padding-bottom:3px;
  /* border-top:2px solid rgb(245, 249, 252); */
  display:flex;
  align-items: center;
  /* background-color: rgb(244, 244, 244); */
}

.shortcut-buttons button {
  border: 0.5px solid rgb(190, 190, 190);
  border-radius:10px;
  padding-top:5px;
  padding-bottom:5px;
  margin-left:3px;
  cursor: pointer;
  color:rgb(114, 114, 114);
  background-color: rgb(255, 255, 255);
}

.shortcut-buttons button:hover {
  color:black;
  background-color: rgb(245, 245, 245);
}

.user-input {
  /* width:100%; */
  height:30%;
  padding: 15px;
  display: flex;
  background-color: #f5f9fc;
}

.user-input input {
  width: calc(100% - 80px);
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 20px;
}

.user-input button {
  padding: 10px;
  color: white;
  font-size: 30px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-input button:disabled {
  background-color: #ccc;
}

.user-input button:not(:disabled) {
  background-color: #007bff;
}

.button-icon {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit {
  transform: scaleX(1.3);
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* 抖动的省略号样式 */
.dot-dance::after {
  content: "";
  animation: dot-dance 1.5s infinite linear;
  text-align: center;
  font-size: 12px;
  padding-left: 5px;
  border-radius: 10px;
  background-color: rgb(255, 255, 255);
  /* 设置行高，让显示更美观，可根据需求调整 */
  line-height: 1;
}

@keyframes dot-dance {
  0% {
    content: "正在分析.";
  }

  33% {
    content: "正在分析..";
  }

  66% {
    content: "正在分析...";
  }

  100% {
    content: "正在分析.";
  }
}

/* 用户消息包裹样式 */
.user-message-wrapper {
  text-align: right;
  margin-bottom: 10px;
}

/* 用户消息样式 */
.user-message {
  background-color: #e8f4fc;
  border-radius: 8px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.05);
  font-family: 'Open Sans', sans-serif;
  font-size: 16px;
  color: #333;
  padding: 8px;
  display: inline-block;
  max-width: 80%;
  text-align: left;
}

/* AI 消息包裹样式 */
.answer-wrapper {
  text-align: left;
  margin-bottom: 10px;
}

/* AI 消息样式 */
.answer {
  background-color: #e8f4fc;
  border-radius: 8px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.05);
  font-family: 'Open Sans', sans-serif;
  font-size: 16px;
  color: #333;
  padding: 8px;
  display: inline-block;
  max-width: 80%;
}
</style>