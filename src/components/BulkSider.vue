<template>
  <div id="bulkBar">
    <div class="thumbnail">
      <!-- 根据条件显示二进制图片或路径图片 -->
      <template v-if="images.length > 0">
        <!-- 这一行需要修改image为对象 -->
        <img v-for="(image, index) in images" :key="index" :src="image.path" class="thumbnail-image"
          :class="{ 'selected-thumbnail': currentImageIndex === index }" alt="Thumbnail"
          @click="handleThumbnailClick(index)">
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 800
    },
    images: {
      type: Array,
      default: () => []
    },
    imageChoice: {
      type: Number,
      default: 0
    },
    currentImageIndex: {
      type: Number,
      default: 0
    }
  },
}
</script>

<style scoped>
#bulkBar{
  width:100%;
  height:100%;
}

.thumbnail {
  width: 100%;
  height: 30%;
  display: flex;
  flex-wrap: wrap;
}

.thumbnail-image {
  width: 30%;
  height: 40%;
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
</style>