<template>
  <div class="upload-wrapper">
    <!-- 拖拽区域容器 -->
    <!-- 处理拖拽相关事件并动态改变边框颜色 -->
    <div 
      class="upload-container"
      @dragover.prevent="handleDragOver"
      @dragleave="handleDragLeave"
      @drop.prevent="handleDrop"
      :style="{ borderColor: dragActive ? '#409eff' : '#dcdfe6' }"
    >
      <!-- 隐藏的原生文件输入控件 -->
      <input
        type="file"
        ref="fileInput"
        hidden
        accept="image/*"
        @change="handleFileSelect"
      >
      
      <!-- 内容展示区域 -->
      <div class="upload-content">
        <!-- 图片预览：当有预览地址时显示 -->
        <img 
          v-if="previewUrl" 
          :src="previewUrl" 
          class="preview-image"
        >
        <p class="upload-text" v-else>将图片拖到此处或点击右侧图标</p>
      </div>
    </div>
    
    <!-- 右侧操作图标 -->
    <!-- 鼠标悬停icon显示提示文字 -->
    <div 
      class="action-icon" 
      @click="triggerFileSelect"
      :title="previewUrl ? '更换图片' : '上传图片'"
    >
      <el-icon :size="24">
        <i :class="previewUrl ? 'el-icon-refresh-right' : 'el-icon-upload2'" />
      </el-icon>
    </div>
  </div>
</template>

<script>
import { ElIcon } from 'element-ui'

export default {
  components: { 
    ElIcon // 注册ElementUI图标组件
  },
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
        this.previewUrl = e.target.result; // 存储预览地址
        // 向父组件传递上传完成事件
        this.$emit('file-uploaded', { 
          file: file,
          preview: this.previewUrl 
        });
      };
      /*1. 浏览器无法直接使用File对象作为图片源，需要将
      二进制文件数据转换为可显示的URL格式；
      2. readAsDataURL 是异步操作，必须等待onload事件
      触发后才能获取有效数据
      */
      reader.readAsDataURL(file);
    }
  }
};
</script>

<style scoped>
/* 主容器样式 */
.upload-wrapper {
  display: flex;
  align-items: flex-start;  /* 顶部对齐 */
  gap: 20px;               /* 元素间距 */
}

/* 拖拽容器样式 */
.upload-container {
  width: 250px;            /* 固定宽度 */
  height: 200px;           /* 固定高度 */
  border: 2px dashed #dcdfe6; /* 虚线边框 */
  border-radius: 8px;      /* 圆角效果 */
  background: #fafafa;      /* 浅灰色背景 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  overflow: hidden;        /* 隐藏溢出内容 */
  transition: border-color 0.3s; /* 边框颜色过渡动画 */
}

/* 图片预览样式 */
.preview-image {
  width: 100%;            /* 撑满容器宽度 */
  height: 100%;           /* 撑满容器高度 */
  object-fit: contain;    /* 保持比例完整显示 */
}

/* 操作图标样式 */
.action-icon {
  cursor: pointer;        /* 鼠标手型 */
  /* 禁止文本选择 */
  user-select: none;
  
  padding: 8px;           /* 内边距 */
  border-radius: 50%;    /* 圆形效果 */
  transition: all 0.3s;  /* 过渡动画 */
}

/* 鼠标悬停效果 */
.action-icon:hover {
  background: #f5f7fa;    /* 浅蓝色背景 */
}

/* 图片上传提示文字样式 */
.upload-text {
  color: #909399;          /* 灰色文字 */
  font-size: 14px;        /* 字体大小 */
  text-align: center;      /* 水平居中 */
}
</style> 