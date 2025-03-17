<template>
  <div>
    <ImageRectangleDrawer :images="images" :imageSrc="imageSrc" :imagePaths="imagePaths" :canvasWidth="imgWidth" :canvasHeight="imgHeight"
      :probabilities="probabilities" @rectangleAdded="onRectangleAdded" @rectangleRemoved="onRectangleRemoved" />
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
      probabilities: []
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
  created () {
    this.computedCanvasWidth();
    this.computedCanvasHeight();
    this.InitImagePaths();
    this.InitProbabilities();
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
    InitProbabilities() {
      if (this.$route.query && this.$route.query.probabilities) {
        this.probabilities = this.$route.query.probabilities;
      }
    },
    computedCanvasWidth() {
      this.imgWidth = window.innerWidth * 0.7;
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
    //动态获取视窗大小
    handleWindowResize() {
      this.computedCanvasWidth();
      this.computedCanvasHeight();
      console.log(this.imgWidth + "+" + this.imgHeight);
    }
  },
};
</script>