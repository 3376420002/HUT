<template>
  <div class="upload-wrapper" :class="{ 'is-disabled': disabled }">
    <div class="upload-container" @dragover.prevent="handleDragOver" @dragleave="handleDragLeave"
      @drop.prevent="handleDrop" :style="{ borderColor: dragActive ? '#BAE67E' : '#dcdfe6' }">
      <!-- 隐藏原生文件输入控件 -->
      <img v-if="previewUrl" :src="previewUrl" class="preview-image">
      <!-- 浮动操作图标 -->
      <div class="upload" v-if="isUpload">
        <input type="file" ref="fileInput" hidden accept="image/*" @change="handleFileSelect" :disabled="disabled">
        <div class="action-icon" @click.stop="triggerFileSelect" :title="previewUrl ? '更换图片' : '上传图片'">
          <i class="el-icon-plus" v-if="!previewUrl"></i>
          <i class="el-icon-refresh-right" v-if="previewUrl"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    imageFile: {
      type: String,
      default: ""
    },
    isUpload: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dragActive: false,  // 拖拽激活状态
      previewUrl: null,    // 存储图片预览的DataURL（Base64）
      isDragging: false // 正在拖拽
    };
  },
  watch: {
    imageFile: {
      handler(newValue) {
        this.previewUrl = newValue;
        console.log(this.previewUrl);
      },
      deep: true
    }
  },
  created(){
    if(this.imageFile)
    this.previewUrl=this.imageFile;
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
      this.isDragging = true;
    },
    handleDragLeave() {
      this.dragActive = false;
      this.isDragging = false;
    },

    //处理文件拖放事件
    handleDrop(e) {
      this.dragActive = false;
      this.isDragging = false; // 明确重置拖拽状态
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
        console.log(this.previewUrl);
        // 向父组件传递文件对象
        this.$emit('file-uploaded', {
          file: file,
          base64: e.target.result
        });
      };
      reader.readAsDataURL(file);
    }
  }
};
</script>

<style scoped>
/* .upload-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start; 
  gap: 20px;
} */

.upload-container {
  position: relative;
  /* 为绝对定位图标提供参照 */
  width: 250px;
  height: 250px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background: #1A1F28;
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
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  opacity: 1;
  /* 默认显示 */
  transition: opacity 0.3s;
  cursor: pointer;
  /* 禁止文本选择 */
  user-select: none;
  border-radius: 50%;
}

/* 有预览图时悬停显示 */
.upload-container:hover .action-icon {
  opacity: 1;
}

/* 有预览图时默认隐藏 */
.upload-container:has(.preview-image) .action-icon {
  opacity: 0;
  transition: opacity 0.3s;
}

/* 有预览图时悬停显示 */
.upload-container:has(.preview-image):hover .action-icon {
  opacity: 1;
}

.el-icon-refresh-right,
.el-icon-plus {
  color: #909399;
  font-size: 40px;
  text-align: center;
}

.image-uploader-container.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.image-uploader-container.is-disabled input {
  pointer-events: none;
}
</style>