<template>
  <div>

    <!-- <ImageRectangleDrawer
      :imagePaths="imagePaths"
      :canvasWidth="1180"
      :canvasHeight="800"
      @rectangleAdded="onRectangleAdded"
      @rectangleRemoved="onRectangleRemoved"
    /> -->
  </div>
</template>

<script>
// import ImageRectangleDrawer from "@/components/ImageRectangleDrawer.vue";
import textImage1 from '@/assets/text.jpg';
import textImage2 from '@/assets/text2.jpg';
export default {
  // components: {
  //   ImageRectangleDrawer,
  // },
  data() {
    return {
      imageSrc: textImage1,
      imagePaths:[textImage1,textImage2]
    };
  },
  methods: {
    InitImagePaths(){
      
    },
    onRectangleAdded(rectangle) {
      console.log("这是父组件的矩形框添加:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如保存矩形框信息
    },
    onRectangleRemoved(rectangle) {
      console.log("这是父组件的矩形框删除:", rectangle);
      // 可以在这里添加父组件的处理逻辑，如更新数据等
    },
  },
};
</script>