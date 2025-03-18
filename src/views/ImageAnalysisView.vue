<template>
  <div id="imageAnalysis" v-loading.lock="isLoading" element-loading-text="正在分析">
    <div class="submit-and-results">
      <div class="submit">
        <div class="tool-bar">
          <div class="button-group">
            <button class="fundus-btn" @click="addImageUploader(1)" :class="{ active: imageKind[1] }">
              <span class="short-text">左眼底</span>
              <span class="full-text">左眼眼底图</span>
            </button>
            <button class="fundus-btn" @click="addImageUploader(2)" :class="{ active: imageKind[2] }">
              <span class="short-text">右眼底</span>
              <span class="full-text">右眼眼底图</span>
            </button>
            <button class="oct-btn" @click="addImageUploader(3)" :class="{ active: imageKind[3] }">
              <span class="short-text">左OCT</span>
              <span class="full-text">左眼OCT图像</span>
            </button>
            <button class="oct-btn" @click="addImageUploader(4)" :class="{ active: imageKind[4] }">
              <span class="short-text">右OCT</span>
              <span class="full-text">右眼OCT图像</span>
            </button>
          </div>
        </div>
        <div class="images-container">
          <div v-for="index in 4" :key="index">
            <div v-if="imageKind[index]" class="images">
              <ImageUploader :isUpload="true" @file-uploaded="(payload) => imageUpload(payload, index)" />
            </div>
          </div>
        </div>
        <div class="results">
          <button @click="observationMode">观察模式</button>
        </div>
        <div v-if="hasCommitted" class="images-container">
          <div v-for="(image, index) of imageResult" :key="index" class="images">
            <ImageUploader :imageFile="image.path" />
          </div>
        </div>
      </div>
    </div>
    <div class="states">
      <div class="setUp">
        <button @click="getResults">{{ setUpName }}</button>
      </div>
      <div class="probabilities">
        <StatusBar :progresses="probabilities"></StatusBar>
      </div>
    </div>
  </div>
</template>

<script>
import StatusBar from '@/components/IllnessExpectationColumn.vue'
// import textImage2 from '@/assets/text2.jpg';
import ImageUploader from '@/components/ImageUploader.vue'

export default {
  name: 'ImageAnalysisView', // 添加组件名称
  components: {
    StatusBar,
    ImageUploader,
  },
  data() {
    return {
      imageKind: {//四种按钮的bool，点击显示对应的组件  //10:38 
        1: false,
        2: false,
        3: false,
        4: false
      },
      imageFundus: [],//两种眼底图
      imageOCT: [],//两种OCT图像
      hasCommitted: false,//是否已上传    //10:38
      initialImages: [],
      resultImages: [],
      setUpName: "启动AI分析",
      probabilities: [],
      isLoading: false,
      images: [],
      // octImage: [],
      imageSrc: "",
      imagePaths: [],
      imageResult: [],
      // imageResult: [{
      //   name: "oct",
      //   path: textImage2,
      //   hasLegend: true,
      //   legends: [
      //     { "color": "#FF5733", "name": "活力橙" },
      //     { "color": "#33FF57", "name": "清新绿" },
      //     { "color": "#5733FF", "name": "梦幻紫" },
      //     { "color": "#FFFF33", "name": "灿烂黄" },
      //     { "color": "#33FFFF", "name": "澄澈蓝" },
      //     { "color": "#FF33C1", "name": "浪漫粉" },
      //     { "color": "#9933FF", "name": "深邃靛" },
      //     { "color": "#33FF99", "name": "盎然碧" },
      //     { "color": "#FF9933", "name": "暖阳橘" },
      //     { "color": "#3399FF", "name": "宁静海蓝" }
      //   ]
      // }],
      uploadedImg: [],
      isUploadImg: false,
    };
  },
  methods: {
    addImageUploader(type) {//10:38
      this.imageKind[type] = !this.imageKind[type];
    },
    imageUpload(payload, type) {
      if (type === 1) {
        this.imageFundus.push({
          name: "left",
          path: payload.base64
        })
      } else if (type === 2) {
        this.imageFundus.push({
          name: "right",
          path: payload.base64
        })
      } else if (type === 3) {
        this.imageOCT.push({
          name: "left-oct",
          path: payload.base64
        })
      } else {
        this.imageOCT.push({
          name: "right-oct",
          path: payload.base64
        })
      }
      this.handleImageUpload();
    },
    handleImageUpload() {
      this.images = [
        ...this.imageFundus,
        ...this.imageOCT
      ];
      this.isUploadImg = true;
    },//10:38
    InitImagePaths() {

    },
    uploadImages() {
      this.imagePaths = this.uploadedImg;
      console.log(Array.isArray(this.imagePaths))
      // this.hasCommitted = true;
    },
    async getResults() {
      this.isLoading = true;
      this.hasCommitted = true;
      // 这里模拟加载过程，假设 3 秒后加载完成，隐藏加载动画，模拟获取答案
      setTimeout(() => {
        this.isLoading = false;
        this.setUpName = "重新进行分析";
        this.probabilities = [
          { name: "轻度非增生性病变", probability: 1 },
          { name: "中度非增生性病变", probability: 0.12 },
          { name: "重度非增生性病变", probability: 0.04 },
          { name: "增生性病变", probability: 0.03 },
          { name: "疑似青光眼病变", probability: 0.02 },
          { name: "早期青光眼", probability: 0.01 },
          { name: "中期青光眼", probability: 0.01 },
          { name: "晚期青光眼", probability: 0.01 },
          { name: "病理性近视", probability: 0.01 }
        ];
        // this.imagePaths = this.imageResult;
        this.imageResult = this.images;
        this.isUploadImg = true;
      }, 3000);
    },
    observationMode() {
      if (!this.isUploadImg) {
        this.$alert('请先上传图片!', '注意', {
          confirmButtonText: '确定',
          callback: () => {}
        });
      } else {
        this.$router.push({
          path: '/imageObservation',
          query: {
            images: this.images,
            imagePaths: this.imagePaths,
            imageSrc: this.imageSrc,
            probabilities: this.probabilities
          }
        })
      }
    },
    onRectangleAdded(rectangle) {
      console.log("这是父组件的矩形框添加:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如保存矩形框信息
    },
    onRectangleRemoved(rectangle) {
      console.log("这是父组件的矩形框删除:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如更新数据等
    }
  },
};
</script>

<style scoped>
#imageAnalysis {
  background: linear-gradient(135deg, #f5f5f5 0%, #e3f2fd 100%);
  display: flex;
  height: 100%;
}

.submit-and-results {
  width: 70%;
  border: 2px solid black;
  border-bottom-left-radius: 10px;
}

.states {
  width: 30%;
  border: 2px solid black;
  /* background: linear-gradient(135deg, #e0f7fa 0%, #e8f5e9 100%); */
  /* background: linear-gradient(135deg, #fff8e1 0%, #e1f5fe 100%); */
  background: linear-gradient(135deg, #f5f5f5 0%, #e3f2fd 100%);
  border-bottom-right-radius: 10px;
}

.setUp {
  padding: 20px;
  height: 10%;
  border-bottom: 2px solid black;
}

.setUp button {
  width: 100%;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.probabilities {
  padding: 20px;
  border-bottom-right-radius: 10px;
  text-align: center;
}

.images-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.images {
  margin: 0 15px 0 15px;
}

/* 新增按钮样式 */
.tool-bar {
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin: 15px;
}

.button-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

button {
  padding: 10px 15px;
  border: 2px solid transparent;
  color: #4CAF50;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  font-weight: 500;
}

button.active {
  background: #2d2d2d;
  border: 2px solid #4CAF50;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.4);
  transform: scale(1.05);
}

button:hover {
  background: #2d2d2d;
  border-color: #4CAF50;
}

/* 移除之前的after伪元素相关样式 */

/* 响应式设计 */
@media (max-width: 768px) {
  .button-group {
    grid-template-columns: repeat(2, 1fr);
  }

  .short-text {
    display: inline;
  }

  .full-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .button-group {
    grid-template-columns: 1fr;
  }

  button {
    padding: 12px;
    font-size: 0.85em;
  }
}
</style>