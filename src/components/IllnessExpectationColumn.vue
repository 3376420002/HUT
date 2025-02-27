<template>
  <div id="IllnessExpectation">
    <!-- 循环渲染每个进度条项 -->
    <div class="progress-item" v-for="(item, index) in progresses" :key="index">
      <!-- 显示疾病名称 -->
      <span class="progress-name">{{ item.name }}</span>
      <div class="progress-container">
        <!-- 进度条 -->
        <div class="progress-bar" :style="{ width: (item.probability * currentRatio * 100) + '%' }"></div>
      </div>
      <!-- 显示概率百分比 -->
      <span class="progress-percentage">{{ (item.probability * currentRatio * 100).toFixed(2) }}%</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    progress: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      progresses: [
        { name: "轻度非增生性病变", probability: 0.76 },
        { name: "中度非增生性病变", probability: 0.12 },
        { name: "重度非增生性病变", probability: 0.04 },
        { name: "增生性病变", probability: 0.03 },
        { name: "疑似青光眼病变", probability: 0.02 },
        { name: "早期青光眼", probability: 0.01 },
        { name: "中期青光眼", probability: 0.01 },
        { name: "晚期青光眼", probability: 0.01 },
        { name: "病理性近视", probability: 0.01 },
      ],
      currentRatio: 0, // 当前增长比例，范围从 0 到 1
      animationDuration: 100, // 动画总时长，单位为毫秒
      intervalTime: 50, // 每次更新的时间间隔，单位为毫秒
      totalSteps: null, // 总共的增长步数
      step: 0 // 当前步数
    };
  },
  mounted() {
    // 计算总共的增长步数
    this.totalSteps = this.animationDuration / this.intervalTime;
    const intervalId = setInterval(() => {
      if (this.step < this.totalSteps) {
        this.step++;
        // 计算当前比例
        this.currentRatio = this.step / this.totalSteps;
      } else {
        clearInterval(intervalId);
      }
    }, this.intervalTime);
  },
  methods: {}
};
</script>

<style scoped>
/* 每个进度条项的样式 */
.progress-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

/* 疾病名称的样式，设置右对齐 */
.progress-name {
  width: 150px; /* 可根据实际情况调整宽度 */
  margin-right: 10px;
  text-align: right;
}

/* 进度条容器的样式 */
.progress-container {
  flex: 1;
  background-color: #f3f3f3;
  border-radius: 5px;
  overflow: hidden;
}

/* 进度条的样式 */
.progress-bar {
  height: 15px;
  background: linear-gradient(
    to right,
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
    hsl(209, 70%, 80%) 100%
  );
  border-radius: 5px;
  width: 0;
  text-align: center;
  color: white;
  transition: width 0.5s ease;
}

/* 概率百分比的样式 */
.progress-percentage {
  margin-left: 10px;
  color: red;
}
</style>