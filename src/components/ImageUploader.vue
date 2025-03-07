<template>
  <div class="upload-wrapper">
    <!-- 拖拽区域容器 -->
    <!-- 处理拖拽相关事件并动态改变边框颜色 -->
    <div class="upload-container" @dragover.prevent="handleDragOver" @dragleave="handleDragLeave"
      @drop.prevent="handleDrop" :style="{ borderColor: dragActive ? '#409eff' : '#dcdfe6' }">
      <!-- 隐藏的原生文件输入控件 -->
      <input type="file" ref="fileInput" hidden accept="image/*" @change="handleFileSelect">

      <!-- 内容展示区域 -->
      <div class="upload-content">
        <!-- 浏览器限制：<img>标签的src属性只能接受以下格式：
          相对/绝对URL路径
          Base64 DataURL（即previewUrl）
          Blob URL
        安全策略：浏览器不允许直接访问本地文件路径（如C:\files\img.jpg） -->
        <img v-if="previewUrl" :src="previewUrl" class="preview-image">
        <p class="upload-text" v-else>将图片拖到此处或点击右侧图标</p>
      </div>
    </div>

    <!-- 右侧操作图标 -->
    <div class="action-icon" @click="triggerFileSelect" :title="previewUrl ? '更换图片' : '上传图片'">
      <el-button circle :icon="previewUrl ? 'el-icon-refresh-right' : 'el-icon-upload2'" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dragActive: false,  // 拖拽激活状态标识（用于边框高亮）
      previewUrl: null    // 存储图片预览的DataURL
    };
  },
  methods: {
    //点击触发文件选择对话框
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },
    //处理文件选择事件
    handleFileSelect(e) {
      this.processFile(e.target.files[0]);
    },

    //激活拖拽状态
    handleDragOver() {
      this.dragActive = true;
    },

    //取消拖拽状态
    handleDragLeave() {
      this.dragActive = false;
    },

    //处理文件拖放事件
    handleDrop(e) {
      this.dragActive = false;
      this.processFile(e.dataTransfer.files[0]);
    },

    //处理文件验证和预览
    processFile(file) {
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        return alert('请选择图片文件！');
      }

      // 创建文件阅读器生成预览图
      const reader = new FileReader();
      // 文件加载完成回调
      reader.onload = (e) => {
        this.previewUrl = e.target.result;
        this.$emit('file-uploaded', {
          file: file
        });
      };
      reader.readAsDataURL(file);
    }
  }
};
</script>

<style scoped>
.upload-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.upload-container {
  width: 250px;
  height: 200px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: border-color 0.3s;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.action-icon {
  cursor: pointer;
  /* 禁止文本选择 */
  user-select: none;
  border-radius: 50%;
  transition: all 0.3s;
  /* 过渡动画 */
}

/* 鼠标悬停效果 */
.action-icon:hover {
  background: #f5f7fa;
}

.upload-text {
  color: #909399;
  font-size: 14px;
  text-align: center;
}
</style>