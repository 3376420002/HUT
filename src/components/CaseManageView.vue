<template>
  <div id="case-manage">
    <div class="body">
      <!-- 引入对话框子组件 -->
      <div class="dialog-container">
        <AIDialog :shortcutButtons="shortcutButtons" :shortcutFunctions="shortcutFunctions" @CaseAnalysis="caseAnalysis"
          @open="open" @close="close" />
      </div>
      <div class="right-content" :class="{ 'shrink': isOpen }">
        <div class="page-content">
          <!-- 页面其他内容 -->
          <!-- <h1>页面主要内容</h1>
          <p>这是页面的主要内容。</p> -->
          <TestForm />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AIDialog from '@/components/AIDialog.vue';
import axios from 'axios'
import TestForm from '@/components/TestForm.vue'
export default {
  components: {
    AIDialog,
    TestForm
  },
  data() {
    return {
      isOpen: false,
      shortcutButtons: ["病例综合分析", "左眼分析", "右眼分析"],
      shortcutFunctions: ["caseAnalysis"]//供AIDialog调用获得父组件的信息
    }
  },
  mounted() {

  },
  methods: {
    async caseAnalysis() {
      console.log("测试输出")
      //获取该页面病例的信息并返回给对话框，这里返回1
      const response = await axios.get("http://192.168.1.136:8800");
      const data = String(response.data.message);
      console.log(data);
      return data;
      // return String("针对50岁男性患者晚期青光眼的情况，以下是针对性的诊断建议和治疗流程：\n\n### 1. 治疗建议\n- **眼内压控制**：在晚期青光眼患者中，眼内压的控制是防止进一步视神经损害的关键。可以考虑如下方式：\n  - **药物治疗**：根据患者的个体耐受性及以往用药记录，选择合适的降眼压药物组合。\n  - **激光治疗**：如需要可考虑进行处于相对安全的范围内的激光小梁成形术或激光周边虹膜切开术，以改善房水流出。\n  - **手术治疗**：对于需要手术干预的患者，可以考虑进行青光眼滤过手术（如小梁切除术）或管状阀植入手术。\n\n### 2. 检查计划\n- **眼压监测**：定期监测眼内压，评估治疗效果。\n- **视野检查**：使用电脑视野计定期进行视野检测，记录视野缺损的进展情况。\n- **视神经检查**：使用OCT（光学相干断层扫描）检查视网膜神经纤维层厚度，评估视神经的损伤程度。\n- **房角检查**：使用前房角镜检查房角的开放情况，如有必要进行房水动力学检查。\n\n### 3. 用药建议\n根据患者的具体情况，可以考虑以下几类降眼压药物：\n- **β-adrenergic拮抗剂**（如美托洛尔眼药水）\n- **前列腺素类**（如拉坦前列素眼药水）\n- **碳酸酐酶抑制剂**（如乙酰唑胺口服或磺酰胺眼药水）\n- **α2-adrenergic激动剂**（如布林佐胺眼药水）\n\n在实施药物治疗时，务必注意患者可能的副作用和合并症，同时对药物的相互作用进行评估。如果患者对某些药物有过敏或不良反应，需及时调整用药计划。\n\n### 总结\n鉴于患者已经处于青光眼的晚期阶段，治疗的重点在于降低眼内压，减缓视神经进一步损害的进展。通过综合的检查与个体化的用药计划，可以为患者提供最佳的管理方案。同时，患者的生活方式调整（如合理控制体重、避免剧烈运动等）也对病情有一定影响，建议进行相应的指导和提醒。");
    },
    // 打开操作，将 isOpen 设为 true
    open() {
      this.isOpen = true;
    },
    // 关闭操作，将 isOpen 设为 false
    close() {
      this.isOpen = false;
    }
  }
};
</script>

<style scoped>
#case-manage {
  width: 100%;
  height: 100%;
  /* 确保容器有足够的高度 */
}

.body {
  display: flex;
  height: 100%;
  position: relative;
  /* 为父容器添加相对定位 */
}

.page-content {
  padding: 20px;
}

.dialog-container {
  width: 500px;
  position: relative;
}

.right-content {
  position: absolute;
  /* 使用绝对定位 */
  top: 0;
  right: 0;
  left: 0;
  width: 100%;
  transition: width 0.3s ease, left 0.3s ease;
  /* 添加 left 属性的过渡效果 */
}

.right-content.shrink {
  left: 500px;
  width: calc(100% - 500px);
}
</style>