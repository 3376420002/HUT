<template>
  <div id="imageAnalysis" v-loading.lock="isLoading" element-loading-text="正在分析">
    <div class="submit-and-results">
      <div class="submit">
        <!-- 单张点击上传 -->
        <div v-if="!isBulkUpload" class="imageSelectorContainer">
          <div class="imageSelector">
            <button @click="ImageUploaderButton(1)" :class="{ active: imageKind[1] }">
              <span>左眼眼底图</span>
            </button>
            <button @click="ImageUploaderButton(2)" :class="{ active: imageKind[2] }">
              <span>右眼眼底图</span>
            </button>
            <button @click="ImageUploaderButton(3)" :class="{ active: imageKind[3] }">
              <span>左眼OCT图像</span>
            </button>
            <button @click="ImageUploaderButton(4)" :class="{ active: imageKind[4] }">
              <span>右眼OCT图像</span>
            </button>
          </div>
        </div>
        <!-- 单张上传预览 -->
        <div v-if="!isBulkUpload" class="imageContainer">
          <div v-for="index in 4" :key="index">
            <div v-if="imageKind[index]" class="images">
              <ImageUploader :isUpload="true" @file-uploaded="(payload) => imageUpload(payload, index)" />
            </div>
          </div>
        </div>
        <!--批量上传预览-->
        <div v-if="isBulkUpload" class="bulkImageContainer">
          <button @click="prevPage" :disabled="currentPage === 0">L</button>
          <div class="imageContainer">
            <div v-for="(image, index) of currentCommittedImages" :key="index" class="images">
              <ImageUploader :imageFile="image.path" />
            </div>
          </div>
          <button @click="nextPage" :disabled="currentPage === totalPages">R</button>
        </div>
      </div>
      <!-- 单张结果图 -->
      <div v-if="!isBulkUpload" class="results">
        <div v-if="hasCommitted" class="imageContainer">
          <div v-for="(image, index) of imageResult" :key="index" class="images">
            <ImageUploader :imageFile="image.path" />
          </div>
        </div>
      </div>
      <!--批量上传结果图-->
      <div v-if="isBulkUpload" class="results">
        <div v-if="hasCommitted" class="imageContainer">
          <div v-for="(image, index) of currentResultImages" :key="index" class="images">
            <ImageUploader :imageFile="image.path" />
          </div>
        </div>
      </div>
    </div>
    <div class="states">
      <div class="setUp">
        <button @click="observationMode">观察模式</button>
        <!-- 隐藏的原生文件输入 -->
        <input type="file" webkitdirectory directory multiple @change="startBulkUpload" hidden ref="folderInput">
        <button @click="$refs.folderInput.click(), setBulkStatus()"> 批量上传 </button>
        <button @click=" setBulkStatus()">单张上传</button>
        <button @click="getResults">{{ setUpName }}</button>
      </div>
      <div class="probabilities" v-if="hasAnalysis">
        <button v-for="(image, index) in images" :key="index" @click="showProbabilities(index)">
          显示 {{ image.name }} 的概率
        </button>
        <!-- 根据当前激活的索引展示对应的 probabilities -->
        <div v-if="activeIndex !== null" class="progress">
          <StatusBar :progresses="images[activeIndex].probabilities"></StatusBar>
        </div>
      </div>
      <div v-else class="progresses-empty">
        启动AI分析以获取结果
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
      hasAnalysis: false,//是否已分析
      initialImages: [],
      resultImages: [],
      setUpName: "启动AI分析",
      activeIndex: 0, //分析部分的按钮选择的下标
      probabilities: [],
      isLoading: false,
      images: [],
      imageResult: [],
      // imageSrc: "",
      // imagePaths: [],
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
      // uploadedImg: [],
      isUploadImg: false,
      isBulkUpload: false,  //是否为批量上传
      currentPage: 0//批量上传时的预览页码
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.images.length / 2) - 1;
    },
    currentCommittedImages() {
      const start = this.currentPage * 2;
      return this.images.slice(start, start + 2);
    },
    currentResultImages() {
      const start = this.currentPage * 2;
      return this.imageResult.slice(start, start + 2);
    }
  },
  methods: {
    //批量上传左切预览图
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
    },
    //批量上传右切预览图
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    //点击切换上传模式
    setBulkStatus() {
      this.isBulkUpload = !this.isBulkUpload;
    },
    //多张上传
    async startBulkUpload(event) {
      this.isBulkUpload = true;
      const files = Array.from(event.target.files);
      const folderStructure = {};
      let idx = 1;
      files.forEach(file => {
        const pathParts = file.webkitRelativePath.split('/');
        if (pathParts.length <= 2) {
          this.fff = file;//无效语句，如果不是子文件夹文件or空文件夹，就不放入数组
        }
        else {
          const folderName = pathParts[1];//子文件夹名称
          //索引作为名称,如果遍历到新文件夹，创建一个存储数组
          if (!folderStructure[folderName]) {
            folderStructure[folderName] = [];
          }
          folderStructure[folderName].push(file);
        }
      });

      if (Object.entries(folderStructure).length) {//有新数据才置空
        this.images = [];
        this.resultImages = [];
        this.hasCommitted = false;
        this.currentPage = 0;
      }
      //每一个子文件夹的图片
      for (const [folderName, files] of Object.entries(folderStructure)) {
        this.folderName = folderName;
        for (const file of files) {
          const base64 = await this.readFileAsBase64(file);
          this.images.push({
            index: idx,
            path: base64,
            probabilities: []
          });
        }
        idx++;
      }
      // 根据索引排序
      this.images.sort((a, b) => a.index - b.index);
    },
    // 文件转Base64
    async readFileAsBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
      });
    },
    ImageUploaderButton(type) {//10:38
      this.imageKind[type] = !this.imageKind[type];
    },
    imageUpload(payload, type) {
      if (type === 1) {
        this.imageFundus.push({
          index: 1,
          name: "left",
          path: payload.base64,
          probabilities: []
        })
      } else if (type === 2) {
        this.imageFundus.push({
          index: 2,
          name: "right",
          path: payload.base64,
          probabilities: []
        })
      } else if (type === 3) {
        this.imageOCT.push({
          index: 3,
          name: "left-oct",
          path: payload.base64,
          probabilities: []
        })
      } else {
        this.imageOCT.push({
          index: 4,
          name: "right-oct",
          path: payload.base64,
          probabilities: []
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
    async getResults() {
      this.isLoading = true;
      this.hasCommitted = true;
      // 这里模拟加载过程，假设 3 秒后加载完成，隐藏加载动画，模拟获取答案
      setTimeout(() => {
        this.isLoading = false;
        this.setUpName = "重新进行分析";
        // this.probabilities = [
        //   { name: "轻度非增生性病变", probability: 1 },
        //   { name: "中度非增生性病变", probability: 0.12 },
        //   { name: "重度非增生性病变", probability: 0.04 },
        //   { name: "增生性病变", probability: 0.03 },
        //   { name: "疑似青光眼病变", probability: 0.02 },
        //   { name: "早期青光眼", probability: 0.01 },
        //   { name: "中期青光眼", probability: 0.01 },
        //   { name: "晚期青光眼", probability: 0.01 },
        //   { name: "病理性近视", probability: 0.01 }
        // ];
        // // this.imagePaths = this.imageResult;
        this.imageResult = this.images;
        this.isUploadImg = true;
        this.hasAnalysis = true;//是否测试改为true
      }, 3000);
    },
    observationMode() {
      if (!this.isUploadImg) {
        this.$alert('请先上传图片!', '注意', {
          confirmButtonText: '确定',
          callback: () => { }
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
    },
    //点击“显示...概率”按钮时触发切换显示
    showProbabilities(index) {
      this.activeIndex = index;
    },
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
  background-color: #1A1F28;
  border-bottom-left-radius: 10px;
}

.submit {
  width: 100%;
  height: 50%;
  border-bottom: 2px dashed #cccccc60;
}

.results {
  width: 100%;
  height: 50%;
}

.states {
  width: 30%;
  border: 2px solid black;
  /* background: linear-gradient(135deg, #e0f7fa 0%, #e8f5e9 100%); */
  /* background: linear-gradient(135deg, #fff8e1 0%, #e1f5fe 100%); */
  /* background: linear-gradient(135deg, #f5f5f5 0%, #e3f2fd 100%); */
  background-color: #1A1F28;
  border-bottom-right-radius: 10px;
}

.setUp {
  display: flex;
  height: 15%;
  border-bottom: 2px solid black;
  align-items: center;
  justify-content: center;
}

/* .setUp button {
  width: 100%;
  padding: 10px 20px;
  background-color: #CCCCCC;
  color: #528708;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
} */

.probabilities {
  padding: 20px;
  border-bottom-right-radius: 10px;
  text-align: center;
  color: #CCCCCC;
}

.progress {
  margin-top: 10px;
}

.progresses-empty {
  width: 100%;
  text-align: center;
  font-size: 30px;
}

.imageContainer,
.bulkImageContainer {
  display: flex;
  align-items: center;
  justify-content: center;
}

.images {
  margin: 0 12px 0 12px;
}

/* 新增按钮样式 */
.imageSelectorContainer {
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.imageSelector {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

button {
  padding: 10px 15px;
  border: 2px solid transparent;
  color: #4CAF50;
  background-color: #CCCCCC;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  font-weight: 500;
}

button.active {
  background: #2d2d2d;
  border: 2px solid #4CAF50;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.4);
  transform: scale(1.04);
}

button:hover {
  background: #2d2d2d;
  border-color: #4CAF50;
}
</style>