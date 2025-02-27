<template>
  <div id="app">
    <!-- 图片上传组件 -->
    <image-uploader @file-uploaded="handleUpload" />
  </div>
</template>

<script>
import ImageUploader from './components/ImageUploader.vue';

export default {
  name: 'App',
  components: {
    ImageUploader // 注册图片上传组件
  },
  data() {
    return {
      uploadedFile: null // 存储上传的文件对象
    };
  },
  methods: {
    handleUpload({ file }) {
      // 存储上传的文件
      this.uploadedFile = file;
      // 开发调试用日志
      console.log('收到上传文件：', file);
      // 实际应用中可在此处添加文件上传逻辑
    }
  }
};
</script>

<style>
/* 应用主容器样式 */
#app {
  padding: 20px;         /* 内边距 */
  max-width: 800px;      /* 最大宽度限制 */
  margin: 0 auto;        /* 水平居中 */
  box-sizing: border-box;/* 盒模型设置 */
}
</style> 