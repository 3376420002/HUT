<template>
  <div class="upload-wrapper">
    <!-- 拖拽区域容器 -->
    <div class="upload-container" @dragover.prevent="handleDragOver" @dragleave="handleDragLeave"
      @drop.prevent="handleDrop" :style="{ borderColor: dragActive ? '#409eff' : '#dcdfe6' }">
      <!-- 隐藏原生文件输入控件 -->
      <input type="file" ref="fileInput" hidden accept="image/*" @change="handleFileSelect">
      <div class="upload-content">
        <img v-if="previewUrl" :src="previewUrl" class="preview-image">
        <p class="upload-text" v-else>将图片拖到此处或点击下方图标</p>
      </div>
    </div>

    <!-- 下方操作图标 -->
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
      previewUrl: null    // 存储图片预览的DataURL（Base64）
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
    handleDragOver() {
      this.dragActive = true;
    },
    handleDragLeave() {
      this.dragActive = false;
    },

    //处理文件拖放事件
    handleDrop(e) {
      this.dragActive = false;
      this.processFile(e.dataTransfer.files[0]);
    },

    processFile(file) {
      // 文件类型验证
      if (!file.type.startsWith('image/')) {
        return alert('请选择图片文件！');
      }
      // 创建FileReader读取文件
      const reader = new FileReader();
      reader.onload = (e) => {
        // 生成Base64预览图
        this.previewUrl = e.target.result;

        // 向父组件传递文件对象
        this.$emit('file-uploaded', {
          file: file,  // 原始文件对象
          base64: e.target.result //Base64传递
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
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}

.upload-container {
  width: 300px;
  height: 300px;
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