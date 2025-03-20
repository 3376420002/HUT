<template>
  <div id="bulkBar">
    <div class="thumbnail">
      <div v-for="(group, groupIndex) in groupedImages" :key="groupIndex">
        <div class="image-row">
          <img v-for="(image, index) in group" :key="index" :src="image.path" class="thumbnail-image"
            :class="{ 'selected-thumbnail': currentImageIndex === index }" alt="Thumbnail"
            @click="handleThumbnailClick(index)">
        </div>
      </div>
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
  data() {
    return {

    }
  },
  computed: {
    groupedImages() {
      const groups = {};
      this.images.forEach((image) => {
        if (!groups[image.index]) {
          groups[image.index] = [];
        }
        groups[image.index].push(image);
      });
      return Object.values(groups);
    }
  },
  methods: {
    handleThumbnailClick(index) {
      this.currentImageIndex = index;
    }
  }
}
</script>

<style scoped>
#bulkBar {
  width: 100%;
  height: 100%;
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