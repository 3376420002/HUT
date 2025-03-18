<template>
  <div id="IllnessExpectation">
    <!-- 循环渲染每个进度条项 -->
    <div v-if="progresses.length">
      <div class="progress-item" v-for="(item, index) in progresses" :key="index">
        <!-- 显示疾病名称 -->
        <span class="progress-name">{{ item.name }}</span>
        <div class="progress-container">
          <!-- 进度条 -->
          <div class="progress-bar" :style="{ width: (item.probability * currentRatio * 100) + '%' }">
            <!-- 显示概率百分比 -->
            <span class="progress-percentage">{{ (item.probability * currentRatio * 100).toFixed(2) }}%</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="progresses-empty">
      启动AI分析以获取结果
    </div>
  </div>
</template>

<script>
export default {
  props: {
    progresses: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      currentRatio: 0, // 当前增长比例，范围从 0 到 1
      animationDuration: 100, // 动画总时长，单位为毫秒，这里修改为 1000 让动画更明显
      intervalTime: 50, // 每次更新的时间间隔，单位为毫秒
      totalSteps: null, // 总共的增长步数
      step: 0, // 当前步数
      intervalId: null // 保存定时器 ID
    };
  },
  watch: {
    progresses: {
      handler() {
        // 当 progresses 变化时，重置进度条状态
        this.resetProgress();
        this.Init();
      },
      deep: true // 深度监听 progresses 数组的变化
    }
  },
  mounted() {
    this.resetProgress();
    this.Init();
  },
  methods: {
    resetProgress() {
      // 清除定时器
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      // 重置当前步数和比例
      this.step = 0;
      this.currentRatio = 0;
    },
    Init() {
      // 计算总共的增长步数
      this.totalSteps = this.animationDuration / this.intervalTime;
      this.intervalId = setInterval(() => {
        if (this.step < this.totalSteps) {
          this.step++;
          // 计算当前比例
          this.currentRatio = this.step / this.totalSteps;
        } else {
          clearInterval(this.intervalId);
        }
      }, this.intervalTime);
    }
  }
};
</script>

<style scoped>
#IllnessExpectation{
  width:100%;
}

/* 每个进度条项的样式 */
.progress-item {
  width:100%;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

/* 疾病名称的样式，设置右对齐 */
.progress-name {
  width: 30%;
  /* 可根据实际情况调整宽度 */
  margin-right: 10px;
  text-align: center;
}

/* 进度条容器的样式 */
.progress-container {
  width:70%;
  background-color: #ececec;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

/* 进度条的样式 */
.progress-bar {
  height: 15px;
  background: linear-gradient(to right,
      hsl(209, 70%, 30%) 0%,
      hsl(209, 70%, 32%) 4%,
      hsl(209, 70%, 34%) 8%,
      hsl(209, 70%, 36%) 12%,
      hsl(209, 70%, 38%) 16%,
      hsl(209, 70%, 40%) 20%,
      hsl(209, 70%, 42%) 24%,
      hsl(209, 70%, 44%) 28%,
      hsl(209, 70%, 46%) 32%,
      hsl(209, 70%, 48%) 36%,
      hsl(209, 70%, 50%) 40%,
      hsl(209, 70%, 52%) 44%,
      hsl(209, 70%, 54%) 48%,
      hsl(209, 70%, 56%) 52%,
      hsl(209, 70%, 58%) 56%,
      hsl(209, 70%, 60%) 60%,
      hsl(209, 70%, 62%) 64%,
      hsl(209, 70%, 64%) 68%,
      hsl(209, 70%, 66%) 72%,
      hsl(209, 70%, 68%) 76%,
      hsl(209, 70%, 70%) 80%,
      hsl(209, 70%, 72%) 84%,
      hsl(209, 70%, 74%) 88%,
      hsl(209, 70%, 76%) 92%,
      hsl(209, 70%, 78%) 96%,
      hsl(209, 70%, 80%) 100%);
  border-radius: 5px;
  width: 100%;
  position: relative;
  text-align: center;
  color: white;
  transition: width 0.5s ease;
}

/* 概率百分比的样式 */
.progress-percentage {
  position: absolute;
  top: 50%;
  left:calc(80% + 20px);
  transform: translate(-50%, -50%);
  color: black;
  font-size: 12px;
  /* 可根据需要调整字体大小 */
}

.progresses-empty {
  width:100%;
  text-align: center;
  font-size: 30px;
}
</style>