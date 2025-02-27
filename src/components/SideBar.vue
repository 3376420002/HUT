<template>
  <div id="sideBar">
    <div class="basic-information-container">
      <div class="patient-information">
        <div>
          <span class="inform-unit">
            <img src="@/assets/generalIcons/visitor.png" width="30">
          </span>
          <span class="inform-unit">{{ patientName }}</span>
          <span class="inform-unit">{{ patientSex }}</span>
          <span class="inform-unit">{{ String(patientAge) + "岁" }}</span>
        </div>
        <div>
          检查单号：{{ trackingNumber }}
        </div>
      </div>
      <div class="import-status">

      </div>
    </div>
    <hr>
    <div class="thumbnail">
      <!-- 根据条件显示二进制图片或路径图片 -->
      <template v-if="imageSrc">
        <img :src="imageSrc" class="thumbnail-image selected-thumbnail" alt="Thumbnail"
          @click="handleThumbnailClick(0)">
      </template>
      <template v-else-if="images.length > 0">
        <img v-for="(image, index) in images" :key="index" :src="imageUrl(image)" class="thumbnail-image"
          :class="{ 'selected-thumbnail': currentImageIndex === index }" alt="Thumbnail"
          @click="handleThumbnailClick(index)">
      </template>
      <template v-else-if="imagePaths.length > 0">
        <img v-for="(imagePath, index) in imagePaths" :key="index" :src="imagePath" class="thumbnail-image"
          :class="{ 'selected-thumbnail': currentImageIndex === index + images.length }" alt="Thumbnail"
          @click="handleThumbnailClick(index)">
      </template>
    </div>
    <!-- <hr> -->
    <!-- <div class="tab-container">
      <div v-for="(labelName, index) in tabs" :key="index" class="tab"
        :class="{ 'active-tab': currentImageIndex === index }" @click="handleTabClick(index)">
        {{ labelName }}
      </div>
    </div> -->
    <div class="exchange-tools">
      <button class="tool-button" :class="{ 'button-active': toolChoose === 1 }" @click="handleExchangeTool(1)">
        诊断建议
      </button>
      <button class="tool-button" :class="{ 'button-active': toolChoose === 2 }" @click="handleExchangeTool(2)">
        AI检测结果
      </button>
    </div>
    <div v-if="toolChoose === 1" class="input-container">
      <!-- 根据当前显示图片的索引显示对应的输入框 -->
      <div v-for="(inputWrapper, inputIndex) in inputElements[currentImageIndex]" :key="inputIndex"
        class="input-wrapper">
        <span class="input-index">{{ String(Number(inputIndex) + 1) }}.</span>
        <input class="tech-input" :placeholder="'输入与矩形相关信息'" v-model="inputWrapper.value" />
        <!-- 仅在输入框个数大于 1 时显示删除按钮 -->
        <span class="delete-btn" @click="handleDelete(currentImageIndex, inputIndex)">×</span>
      </div>
    </div>
    <div v-if="toolChoose === 2" class="ai-suggest">
      这里是ai检测结果显示区域！还没做
    </div>
    <div class="report-container">
      <hr>
      <div class="generate-report">
        <button class="report-button">生成报告</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    patientName: {
      type: String,
      default: "测试患者"
    },
    patientSex: {
      type: String,
      default: "男"
    },
    patientAge: {
      type: Number,
      default: 0
    },
    trackingNumber: {
      type: String,
      default: "1111111111"
    },
    images: {
      type: Array,
      default: () => []
    },
    imagePaths: {
      type: Array,
      default: () => []
    },
    imageSrc: {
      type: String,
      default: "",
    },
    currentImageIndex: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      imageName: ["图片1", "图片2", "图片3"],
      inputElements: [],
      toolChoose: 1,
      tabs: []
    };
  },
  created() {
    this.updateInputElementsLength();
  },
  methods: {
    updateInputElementsLength() {
      let imageCount = 0;
      if (this.imageSrc) {
        imageCount = 1;
      } else if (this.imagePaths.length > 0) {
        imageCount = this.imagePaths.length;
      } else if (this.images.length > 0) {
        imageCount = this.images.length;
      }
      this.inputElements = Array.from({ length: imageCount }, () => []);
      this.tabs = Array.from({ length: imageCount }, (_, index) => `图片${index + 1}`);
    },
    addInputElement(imageIndex) {
      const newIndex = this.inputElements[imageIndex].length + 1;
      const inputWrapper = {
        index: newIndex,
        value: ''
      };
      this.inputElements[imageIndex].push(inputWrapper);
    },
    handleDelete(imageIndex, inputIndex) {
      if (this.inputElements[imageIndex].length > 0) {
        this.inputElements[imageIndex].splice(inputIndex, 1);
        this.$emit('rectangleRemoved', imageIndex, inputIndex);
      }
    },
    imageUrl(image) {
      return URL.createObjectURL(new Blob([image]));
    },
    handleThumbnailClick(index) {
      if (index == this.currentImageIndex) return;
      this.$emit('imageIndexChanged', index);
    },
    handleTabClick(index) {
      this.$emit('imageIndexChanged', index);
    },
    handleExchangeTool(index) {
      this.toolChoose = index;
    }
  },
  watch: {
    // 监听 images 和 imagePaths 的变化
    $: {
      deep: true,
      handler() {
        this.updateInputElementsLength();
      }
    }
  }
};
</script>

<style scoped>
#sideBar {
  width: 510px;
  height: 100vh;
  position: relative;
  /* margin-left: 10px; */
  background-color: rgb(25, 55, 95)
}

.basic-information-container {
  height: 35px;
  display: flex;
  padding: 20px;
}

.patient-information {
  color: rgb(255, 255, 255, 0.8);
}

.inform-unit {
  margin: 0px 10px 0px 10px;
  vertical-align: middle;
}

.thumbnail {
  width: 100%;
  height: 30%;
  display: flex;
  flex-wrap: wrap;
}

.thumbnail-image {
  width: 150px;
  height: 100px;
  margin: 15px;
  cursor: pointer;
  border: 2px solid rgb(38, 173, 187);
  object-fit: contain;
  background-color: black;
  /* 设置鼠标指针为手指形状 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.thumbnail-image:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgb(38, 173, 187);
}

.selected-thumbnail {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgb(38, 173, 187);
}

.exchange-tools {
  width: 100%;
  height: 8vh;
  border-top: 1px solid rgb(238, 238, 238);
  background-color: rgb(15, 26, 72, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.tool-button {
  width: 25%;
  height: 50%;
  background-color: transparent;
  border: 1px solid rgb(38, 173, 187);
  font-size: 15px;
  font-weight: bold;
  color: rgb(38, 173, 187);
  cursor: pointer;
  transition: background-color 0.3s ease
}

.tool-button:hover {
  background-color: rgb(38, 173, 187, 0.5)
}

.button-active {
  background-color: rgb(38, 173, 187);
  color: white;
}

/* .tab-container {
  display: flex;
  margin-bottom: 10px;
}

.tab {
  padding: 10px 20px;
  background-color: rgb(23, 46, 76);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tab:hover {
  border-top: 1px solid rgb(204, 204, 204);
  border-right: 1px solid rgb(204, 204, 204);
  background-color: rgb(224, 224, 224, 0.5);
}

.active-tab {
  border-top: 1px solid rgb(204, 204, 204);
  border-right: 1px solid rgb(204, 204, 204);
  background-color: rgb(204, 204, 204, 0.5);
} */


.input-container {
  width: 100%;
  height: 43vh;
  display: inline-block;
  vertical-align: top;
  overflow: scroll;
}

.input-wrapper {
  position: relative;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px;
}

.input-wrapper input {
  width: calc(100%-50px);
  margin-left: 5px;
}

.input-wrapper .delete-btn {
  display: inline-block;
  margin-left: 10px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: rgb(235, 109, 109);
  color: white;
  font-size: 20px;
  text-align: center;
  line-height: 22px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-btn:hover {
  background-color: #e53935;
}

.input-index {
  min-width: 20px;
  text-align: center;
  font-size: 20px;
  color: white
}

.tech-input {
  position: relative;
  width: 350px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(to bottom, #2c3e50, #34495e);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3), inset 0 0 10px rgba(0, 255, 255, 0.1);
  font-size: 16px;
  color: #ecf0f1;
  overflow: hidden;
}

.tech-input::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(45deg);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.tech-input:focus::before {
  opacity: 1;
}

.tech-input:focus {
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.5), inset 0 0 15px rgba(0, 255, 255, 0.2);
}

.ai-suggest {
  width: 100%;
  height: 43vh;
  color: white;
  font-size: 40px;
  display: inline-block;
  vertical-align: top;
  overflow: scroll;
}

.report-container {
  position: absolute;
  width: 100%;
  height: 50px;
  bottom: 20px;
}

.generate-report {
  display: flex;
  justify-content: center;
}

.generate-report button {
  width: 90%;
  height: 40px;
  color: white;
  font-size: 18px;
  background-color: rgba(38, 173, 187);
  cursor: pointer;
}
</style>