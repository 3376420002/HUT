<template>
  <div>
    <!-- 页面其他内容 -->
    <div class="page-content">
      <h1>页面主要内容</h1>
      <p>这是页面的主要内容。</p>
    </div>
    <!-- 引入对话框子组件 -->
    <AIDialog :shortcutButtons="shortcutButtons" :shortcutFunctions="shortcutFunctions" @CaseAnalysis="caseAnalysis" />
  </div>
</template>

<script>
import AIDialog from '@/components/AIDialog.vue';

export default {
  components: {
    AIDialog
  },
  data() {
    return {
      shortcutButtons: ["病例综合分析","左眼分析","右眼分析"],
      shortcutFunctions: ["caseAnalysis"]
    }
  },
  mounted() {

  },
  methods: {
    caseAnalysis() {
      return 1;
    }
  }
};
</script>

<style scoped>
.page-content {
  padding: 20px;
}
</style>