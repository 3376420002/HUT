<template>
  <div :class="{ 'is-disabled': disabled }">
    <div class="upload-container" :class="{ 'finish-upload': hasFinish }" @dragover.prevent="handleDragOver"
      @dragleave="handleDragLeave" @drop.prevent="handleDrop"
      :style="{ borderColor: dragActive ? '#BAE67E' : '#dcdfe6' }">
      
      <img v-if="previewUrl" :src="previewUrl" class="preview-image">
      
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
      dragActive: false,  
      previewUrl: null,    
      isDragging: false, 
      hasFinish: false
    };
  },
  watch: {
    imageFile: {
      handler(newValue) {
        this.previewUrl = newValue;
      },
      deep: true
    }
  },
  created() {
    if (this.imageFile)
      this.previewUrl = this.imageFile;
  },
  methods: {
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },
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
    
    handleDrop(e) {
      this.dragActive = false;
      this.isDragging = false; 
      this.processFile(e.dataTransfer.files[0]);
    },
    processFile(file) {
      
      if (!file.type.startsWith('image/')) {
        return alert('请选择图片文件！');
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewUrl = e.target.result;
        this.hasFinish = true;
        
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
.upload-container {
  position: relative;
  width: 100%;
  height: 100%;
  aspect-ratio: 1/1;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: border-color 0.3s;
}

.finish-upload {
  background-color: black;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  z-index: 1;
  
}

.upload {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  
}

.action-icon {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  
  opacity: 1;
  transition: opacity 0.3s;
  
  cursor: pointer;
  user-select: none;
  border-radius: 50%;
}


.upload-container:hover .action-icon {
  opacity: 1;
}


.upload-container:has(.preview-image) .action-icon {
  opacity: 0;
  transition: opacity 0.3s;
}


.upload-container:has(.preview-image):hover .action-icon {
  opacity: 1;
}

.el-icon-refresh-right,
.el-icon-plus {
  position: relative;
  top: calc(50% - 20px);
  left: calc(50% - 20px);
  color: #909399;
  font-size: 40px;
}
</style>