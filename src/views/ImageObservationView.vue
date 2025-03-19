<template>
  <div id="ImageObserve">
    <ImageRectangleDrawer :images="images" :imageSrc="imageSrc" :imagePaths="imagePaths" :canvasWidth="imgWidth"
     :isBulkUpload="isBulkUpload" :canvasHeight="imgHeight" @rectangleAdded="onRectangleAdded" @rectangleRemoved="onRectangleRemoved" />
  </div>
</template>

<script>
import ImageRectangleDrawer from "@/components/ImageRectangleDrawer.vue";
export default {
  components: {
    ImageRectangleDrawer,
  },
  data() {
    return {
      imgWidth: 0,
      imgHeight: 0,
      images: [],
      imageSrc: "",
      imagePaths: [],
      // probabilities: [],
      isBulkUpload: false
    };
  },
  computed: {
    // computedCanvasWidth() {
    //   return window.innerWidth * 0.7;
    // },
    // computedCanvasHeight() {
    //   return window.innerHeight - 50;
    // }
  },
  created() {
    // this.computedCanvasWidth();
    // this.computedCanvasHeight();
    this.InitBulkUploadStatus()
    this.InitImagePaths();
    // this.InitProbabilities();
  },
  mounted() {
    // 在组件挂载时添加 resize 事件监听器
    window.addEventListener('resize', this.handleWindowResize);
  },
  beforeDestroy() {
    // 在组件销毁前移除 resize 事件监听器，避免内存泄漏
    window.removeEventListener('resize', this.handleWindowResize);
  },
  methods: {
    InitImagePaths() {
      if (this.$route.query && this.$route.query.imagePaths) {
        this.imagePaths = this.$route.query.imagePaths;
      }
      if (this.$route.query && this.$route.query.imageSrc) {
        this.imageSrc = this.$route.query.imageSrc;
      }
      if (this.$route.query && this.$route.query.images) {
        this.images = this.$route.query.images;
      }
    },
    //检测是否是批量上传
    InitBulkUploadStatus() {
      if (this.$route.query && this.$route.query.isBulkUpload) {
        if (this.$route.query.isBulkUpload === "true")
          this.isBulkUpload = true;
      }
      console.log(this.isBulkUpload)
      this.computedCanvasWidth(this.isBulkUpload);
      this.computedCanvasHeight();
    },
    // InitProbabilities() {
    //   if (this.$route.query && this.$route.query.probabilities) {
    //     this.probabilities = this.$route.query.probabilities;
    //   }
    // },
    computedCanvasWidth(mul) {
      this.imgWidth = window.innerWidth * 0.7 - mul * 100;
      console.log(this.imgWidth);
    },
    computedCanvasHeight() {
      this.imgHeight = window.innerHeight - 50;
    },
    onRectangleAdded(rectangle) {
      console.log("这是父组件的矩形框添加:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如保存矩形框信息
    },
    onRectangleRemoved(rectangle) {
      console.log("这是父组件的矩形框删除:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如更新数据等
    },
    //根据是否是批量上传动态获取视窗大小
    handleWindowResize() {
      this.computedCanvasWidth(this.isBulkUpload);
      this.computedCanvasHeight();
      // console.log(this.imgWidth + "+" + this.imgHeight);
    }
  },
};
</script>

<style scoped>
#ImageObserve {
  width: 100%
}
</style>