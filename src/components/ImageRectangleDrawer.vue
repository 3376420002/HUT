<template>
  <div id="ImageDrawing">
    <div class="left" ref="fullDiv" :class="{ 'fullscreen': isFullscreen }">
      <div id="button-container" ref="buttonContainer">
        <button @click="toggleDrawing" :class="{ 'active-button': isStartDrawRectButtonActive }">
          <img src="@/assets/buttonIcons/drawing.png">
          {{ drawButtonText }}
        </button>
        <button @click="toggleBirdseye" :class="{ 'active-button': isBirdseyeVisible }">
          <img src="@/assets/buttonIcons/aerialView.png">
          {{ toggleBirdseyeText }}
        </button>
        <button @click="toggleBrightnessSlider" :class="{ 'active-button': isBrightnessButtonActive }">
          <img src="@/assets/buttonIcons/brightness.png">
          亮度
        </button>
        <button @click="toggleContrastSlider" :class="{ 'active-button': isContrastButtonActive }">
          <img src="@/assets/buttonIcons/contrast.png">
          对比度
        </button>
        <button @click="toggleFullscreen">
          <img :src="isFullscreen ? require('@/assets/buttonIcons/formalScreen.png') : require('@/assets/buttonIcons/fullScreen.png')">
          {{ isFullscreen ? '退出全屏' : '全屏模式' }}
        </button>
      </div>
      <div class="freedom-container">
        <span id="scale-value" ref="scaleValue"></span>
        <span id="brightness-value" ref="brightnessValue"></span>
        <span id="contrast-value" ref="contrastValue"></span>
        <div v-show="isFinishDrawing" class="rect-button rect-cancel" @click="cancelRect">
          x
        </div>
        <div v-show="isFinishDrawing" class="rect-button rect-confirm" @click="confirmRect">
          √
        </div>
        <button class="compare-original" @mousedown="showOriginalImage" @mouseup="restoreAdjustedImage" :style="{
          opacity: 0.7,
          display: isBrightnessOrContrastAdjusted ? 'inline-block' : 'none',
        }">
          <img src="@/assets/buttonIcons/originalCompared.png">
          对比原图
        </button>
      </div>
      <div class="slider-wrapper"
        :class="{ 'slide-in': isBrightnessSliderVisible, 'slide-out': !isBrightnessSliderVisible }" @click.stop>
        <label for="brightness-slider">亮度：</label>
        <input type="range" id="brightness-slider" ref="brightnessSlider" :min="brightnessMin" :max="brightnessMax"
          v-model="brightness" @input="handleBrightnessChange" />
      </div>
      <div v-show="isContrastSliderVisible" class="slider-wrapper"
        :class="{ 'slide-in': isContrastSliderVisible, 'slide-out': !isContrastSliderVisible }" @click.stop>
        <label for="contrast-slider">对比度：</label>
        <input type="range" id="contrast-slider" ref="contrastSlider" :min="contrastMin" :max="contrastMax"
          v-model="contrast" @input="handleContrastChange" />
      </div>
      <canvas ref="imageCanvas" :width="computedWidth" :height="computedHeight"></canvas>
      <!-- 新增左右箭头元素 -->
      <div class="arrow left-arrow" :class="{ 'show': isLeftArrowVisible }" @click="prevImage">&lt;</div>
      <div class="arrow right-arrow" :class="{ 'show': isRightArrowVisible }" @click="nextImage">&gt;</div>
      <div id="birdseye-container" ref="birdseyeContainer" :style="{ display: isBirdseyeVisible ? 'block' : 'none' }">
        <canvas ref="birdseyeView" :width="birdseyeWidth" :height="birdseyeHeight"></canvas>
        <div id="close-birdseye" @click="closeBirdseye">×</div>
      </div>
    </div>
    <div class="right">
      <SideBar ref="sideBar" :images="images" :imagePaths="imagePaths" :imageSrc="imageSrc"
        :currentImageIndex="currentImageIndex" @rectangleRemoved="handleRectangleRemoved"
        @imageIndexChanged="handleImageIndexChanged" />
    </div>
  </div>
</template>

<script>
import SideBar from './SideBar.vue';
export default {
  components: {
    SideBar
  },
  props: {
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
    canvasWidth: {
      type: [Number, String],
      default: 800,
    },
    canvasHeight: {
      type: [Number, String],
      default: 600,
    },
    brightnessMin: {
      type: Number,
      default: -100,
    },
    brightnessMax: {
      type: Number,
      default: 100,
    },
    contrastMin: {
      type: Number,
      default: -100,
    },
    contrastMax: {
      type: Number,
      default: 100,
    },
    birdseyeWidth: {
      type: Number,
      default: 150,
    },
    birdseyeHeight: {
      type: Number,
      default: 150,
    },
  },
  data() {
    return {
      scale: 1,
      offsetX: 0,
      offsetY: 0,
      brightness: 0,
      contrast: 0,
      isBrightnessOrContrastAdjusted: false,
      isBirdseyeVisible: false,
      isDrawing: false,
      isFinishDrawing: false,
      startX: null,
      startY: null,
      endX: null,
      endY: null,
      rectangles: [],
      // inputElements: [],
      nextIndex: [],
      currentRectIndex: [],
      currentImageIndex: 0,
      imageChoice: 0,
      imageCount:0,
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      initialOffsetX: 0,
      initialOffsetY: 0,
      drawButtonText: "绘制",
      toggleBirdseyeText: "鸟瞰图",
      isBrightnessSliderVisible: false,
      isContrastSliderVisible: false,
      isStartDrawRectButtonActive: false,
      isToggleBirdseyeButtonActive: false,
      isBrightnessButtonActive: false,
      isContrastButtonActive: false,
      isFullscreen: false,
      isLeftArrowVisible: false,
      isRightArrowVisible: false
    };
  },
  computed: {
    computedWidth() {
      if (typeof this.canvasWidth === 'number') {
        return `${this.canvasWidth}px`;
      } else if (typeof this.canvasWidth === 'string') {
        return this.canvasWidth;
      }
      return 'auto'; // 默认值
    },
    computedHeight() {
      if (typeof this.canvasHeight === 'number') {
        return `${this.canvasHeight}px`;
      } else if (typeof this.canvasHeight === 'string') {
        return this.canvasHeight;
      }
      return 'auto'; // 默认值
    }
  },
  mounted() {
    this.canvas = this.$refs.imageCanvas;
    this.ctx = this.canvas.getContext("2d");
    this.birdseyeCanvas = this.$refs.birdseyeView;
    this.birdseyeCtx = this.birdseyeCanvas.getContext("2d");
    this.buttonTools = this.$refs.buttonContainer;
    let imgUrl;
    if (this.imageSrc) {
      imgUrl = this.imageSrc;
      this.imageChoice = 1;
    } else if (this.images.length > 0) {
      imgUrl = this.imageUrl(this.images[0]);
      this.imageChoice = 2;
    } else if (this.imagePaths.length > 0) {
      imgUrl = this.imagePaths[0];
      this.imageChoice = 3;
    }
    if (imgUrl) {
      this.loadImg(imgUrl);
    }
    this.canvas.addEventListener("wheel", this.handleWheel);
    this.canvas.addEventListener("mousedown", this.handleMouseDown);
    this.canvas.addEventListener('mousemove', this.handleMouseMove);
    this.canvas.addEventListener("mouseup", () => {
      this.isDragging = false;
      this.canvas.style.cursor = "default"; // 松开时恢复默认样式
      this.canvas.removeEventListener("mousemove", this.dragImage);
    });
    // 根据图片数量初始化 rectangles
    this.initRectangles();
    // 在组件挂载后添加键盘事件监听器
    window.addEventListener('keydown', this.handleCtrlAndOne);

    // 监听全屏状态变化事件
    document.addEventListener('fullscreenchange', this.handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('MSFullscreenChange', this.handleFullscreenChange);
  },
  beforeDestroy() {
    // 在组件销毁前移除键盘事件监听器，防止内存泄漏
    window.removeEventListener('keydown', this.handleCtrlAndOne);

    // 移除全屏状态变化事件监听器
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('MSFullscreenChange', this.handleFullscreenChange);
  },
  methods: {
    entryLoadImg() {
      if (this.imageChoice == 1) {
        this.loadImg(this.imageSrc);
      } else if (this.imageChoice == 2) {
        this.loadImg(this.imageUrl(this.images[this.currentImageIndex]))
      } else {
        this.loadImg(this.imagePaths[this.currentImageIndex]);
      }
    },
    loadImg(url) {
      this.img = new Image();
      this.img.src = url;

      this.img.onload = () => {
        const scaleX = this.canvas.width / this.img.width;
        const scaleY = this.canvas.height / this.img.height;
        this.scale = Math.min(scaleX, scaleY);
        this.redrawCanvas();
        const scaledWidth = this.img.width * this.scale;
        const scaledHeight = this.img.height * this.scale;
        if (
          scaledWidth > this.canvas.width ||
          scaledHeight > this.canvas.height
        ) {
          this.isBirdseyeVisible = true;
          this.drawBirdseyeView();
          this.positionBirdseye();
          // this.toggleBirdseyeText = "鸟瞰图";
        } else {
          this.isBirdseyeVisible = false;
          // this.toggleBirdseyeText = "鸟瞰图";
        }
      };
      this.img.onerror = () => {
        console.error("图片加载失败，请检查图片路径:", this.imageSrc);
      };
    },
    prevImage() {
      // 获取当前图片索引
      let currentIndex = this.currentImageIndex;
      // 计算上一张图片的索引
      let prevIndex = (currentIndex - 1 + this.imageCount) % this.imageCount;
      // 更新当前图片索引
      this.currentImageIndex = prevIndex;
      // 加载新图片
      this.entryLoadImg();
    },
    nextImage() {
      // 获取当前图片索引
      let currentIndex = this.currentImageIndex;
      // 计算下一张图片的索引
      let nextIndex = (currentIndex + 1) % this.imageCount;
      // 更新当前图片索引
      this.currentImageIndex = nextIndex;
      // 加载新图片
      this.entryLoadImg();
    },
    imageUrl(image) {
      return URL.createObjectURL(new Blob([image]));
    },
    initRectangles() {
      if (this.imageChoice == 1) {
        this.imageCount = 1;
      } else if (this.imageChoice == 2) {
        this.imageCount = this.images.length;
      } else if (this.imageChoice == 3) {
        this.imageCount = this.imagePaths.length;
      }
      this.rectangles = Array.from({ length: this.imageCount }, () => []);
      this.nextIndex = Array.from({ length: this.imageCount }, () => 1);
      this.currentRectIndex = Array.from({ length: this.imageCount }, () => -1);
    },
    toggleDrawing() {
      if (this.isDrawing) {
        this.cancelDrawing();
      } else {
        this.startDrawingSession();
      }
      this.isStartDrawRectButtonActive = !this.isStartDrawRectButtonActive;
    },
    toggleBrightnessSlider() {
      if (this.isContrastButtonActive) {
        this.isContrastSliderVisible = !this.isContrastSliderVisible;
        this.isContrastButtonActive = this.isContrastSliderVisible;
      }
      this.isBrightnessSliderVisible = !this.isBrightnessSliderVisible;
      this.isBrightnessButtonActive = this.isBrightnessSliderVisible;
    },
    toggleContrastSlider() {
      if (this.isBrightnessButtonActive) {
        this.isBrightnessSliderVisible = !this.isBrightnessSliderVisible;
        this.isBrightnessButtonActive = this.isBrightnessSliderVisible;
      }
      this.isContrastSliderVisible = !this.isContrastSliderVisible;
      this.isContrastButtonActive = this.isContrastSliderVisible;
    },
    startDrawingSession() {
      // this.drawButtonText = "结束绘制";
      this.isDrawing = true;
      this.startX = null;
      this.startY = null;
      this.endX = null;
      this.endY = null;
      this.canvas.addEventListener("mousedown", this.startRectDrawing);
      this.canvas.addEventListener("mousemove", this.drawRect);
      this.canvas.addEventListener("mouseup", this.stopRectDrawing);
      this.canvas.removeEventListener("wheel", this.handleWheel);
      this.canvas.removeEventListener("mousedown", this.handleMouseDown);
      window.removeEventListener('keydown', this.handleCtrlAndOne);
    },
    cancelDrawing() {
      // this.drawButtonText = "开始绘制矩形框";
      this.isDrawing = false;
      this.startX = null;
      this.startY = null;
      this.endX = null;
      this.endY = null;
      this.canvas.removeEventListener("mousedown", this.startRectDrawing);
      this.canvas.removeEventListener("mousemove", this.drawRect);
      this.canvas.removeEventListener("mouseup", this.stopRectDrawing);
      this.redrawCanvas();
      this.canvas.addEventListener("wheel", this.handleWheel);
      this.canvas.addEventListener("mousedown", this.handleMouseDown);
      window.addEventListener('keydown', this.handleCtrlAndOne);
    },
    startRectDrawing(e) {
      this.startX = (e.offsetX - this.offsetX) / this.scale;
      this.startY = (e.offsetY - this.offsetY) / this.scale;
    },
    drawRect(e) {
      if (this.isDrawing && this.startX !== null && this.startY !== null) {
        this.redrawCanvas();
        this.endX = (e.offsetX - this.offsetX) / this.scale;
        this.endY = (e.offsetY - this.offsetY) / this.scale;
        this.ctx.strokeStyle = "red";
        this.ctx.strokeRect(
          this.startX * this.scale + this.offsetX,
          this.startY * this.scale + this.offsetY,
          (this.endX - this.startX) * this.scale,
          (this.endY - this.startY) * this.scale
        );
      }
    },
    stopRectDrawing() {
      if (this.isDrawing) {
        this.isDrawing = false;
        if (this.startX && this.startY && this.endX && this.endY) {
          const rectangle = {
            topLeft: { x: this.startX, y: this.startY },
            bottomRight: { x: this.endX, y: this.endY },
            index: this.nextIndex[this.currentImageIndex]
          };
          if (this.currentImageIndex >= 0 && this.currentImageIndex < this.rectangles.length) {
            this.currentRectIndex[this.currentImageIndex] = this.rectangles[this.currentImageIndex].length;
            this.rectangles[this.currentImageIndex].push(rectangle);
            this.showRectButtons(rectangle);
            this.canvas.addEventListener("mousedown", this.handleCanvasClick);
            this.$emit("rectangleAdded", rectangle);
          } else {
            console.error('当前图片索引超出 rectangles 数组范围:', this.currentImageIndex);
          }
        }
      }
    },
    // 新增 handleImageIndexChanged 方法，处理图片切换事件
    handleImageIndexChanged(index) {
      this.currentImageIndex = index;
      this.entryLoadImg();
      // this.redrawCanvas();
    },
    handleRectangleRemoved(imageIndex, inputIndex) {
      if (this.rectangles[imageIndex]) {
        const removedRectangle = this.rectangles[imageIndex].splice(inputIndex, 1)[0];
        this.updateIndices(imageIndex);
        this.redrawCanvas();
        //将矩形传递给父组件
        this.$emit("rectangleRemoved", removedRectangle);
      }
    },
    //修改绘制矩形后的确认按钮的样式
    showRectButtons(rectangle) {
      // 计算按钮的位置
      const buttonLeft = rectangle.bottomRight.x * this.scale + this.offsetX;
      // const buttonTop = rectangle.bottomRight.y * this.scale + this.offsetY + this.buttonTools.offsetHeight;
      const buttonTop = rectangle.bottomRight.y * this.scale + this.offsetY;
      // 获取取消按钮
      const cancelButtonCollection = document.getElementsByClassName("rect-button rect-cancel");
      if (cancelButtonCollection.length > 0) {
        const cancelButton = cancelButtonCollection[0];
        // 设置按钮的样式
        cancelButton.style.left = buttonLeft + "px";
        cancelButton.style.top = buttonTop + "px";
      }

      // 获取确认按钮
      const confirmButtonCollection = document.getElementsByClassName("rect-button rect-confirm");
      if (confirmButtonCollection.length > 0) {
        const confirmButton = confirmButtonCollection[0];
        // 设置按钮的样式
        confirmButton.style.left = (buttonLeft + 30) + "px"; // 稍微向右偏移
        confirmButton.style.top = buttonTop + "px";
      }
      this.isFinishDrawing = true;
      // document.body.appendChild(cancelButton);
      // document.body.appendChild(confirmButton);
    },
    cancelRect() {
      const removedRectangle = this.rectangles[this.currentImageIndex].splice(
        this.currentRectIndex[this.currentImageIndex],
        1
      )[0];
      this.isStartDrawRectButtonActive = false;
      // this.removeRectButtons();
      this.isFinishDrawing = false;
      this.redrawCanvas();
      // this.drawButtonText = "开始绘制矩形框";
      this.canvas.removeEventListener("mousedown", this.handleCanvasClick);
      this.canvas.addEventListener("wheel", this.handleWheel);
      this.canvas.addEventListener("mousedown", this.handleMouseDown);
      window.addEventListener('keydown', this.handleCtrlAndOne);
      this.$emit("rectangleRemoved", removedRectangle);
    },
    confirmRect() {
      // const rectangle = this.rectangles[this.currentRectIndex];
      this.$refs.sideBar.addInputElement(this.currentImageIndex);
      this.nextIndex[this.currentImageIndex]++;
      this.isStartDrawRectButtonActive = false;
      // this.removeRectButtons();
      this.isFinishDrawing = false;
      this.redrawCanvas();
      // this.drawButtonText = "开始绘制矩形框";
      this.canvas.removeEventListener("mousedown", this.handleCanvasClick);
      this.canvas.addEventListener("wheel", this.handleWheel);
      this.canvas.addEventListener("mousedown", this.handleMouseDown);
      window.addEventListener('keydown', this.handleCtrlAndOne);
    },
    // removeRectButtons() {
    //   const rectButtons = document.querySelectorAll(".rect-button");
    //   rectButtons.forEach((button) => {
    //     button.parentNode.removeChild(button);
    //   });
    // },
    handleCanvasClick() {
      this.confirmRect();
    },
    updateIndices(imageIndex) {
      if (this.rectangles[imageIndex]) {
        this.nextIndex[this.currentImageIndex] = 1;
        this.rectangles[imageIndex].forEach((rect) => {
          rect.index = this.nextIndex[this.currentImageIndex];
          this.nextIndex[this.currentImageIndex]++;
        });
      }
    },
    redrawCanvas(applyAdjustments = true) {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.drawImageWithScale(applyAdjustments);
      if (this.rectangles[this.currentImageIndex]) {
        this.rectangles[this.currentImageIndex].forEach((rectangle) => {
          this.ctx.strokeStyle = "red";
          this.ctx.strokeRect(
            rectangle.topLeft.x * this.scale + this.offsetX,
            rectangle.topLeft.y * this.scale + this.offsetY,
            (rectangle.bottomRight.x - rectangle.topLeft.x) * this.scale,
            (rectangle.bottomRight.y - rectangle.topLeft.y) * this.scale
          );
          this.ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
          this.ctx.fillRect(
            rectangle.topLeft.x * this.scale + this.offsetX,
            rectangle.topLeft.y * this.scale + this.offsetY,
            20,
            20
          );
          this.ctx.fillStyle = "black";
          this.ctx.font = "16px Arial";
          this.ctx.fillText(
            rectangle.index,
            rectangle.topLeft.x * this.scale + this.offsetX + 5,
            rectangle.topLeft.y * this.scale + this.offsetY + 15
          );
        });
      }
      if (this.isBirdseyeVisible) {
        this.drawBirdseyeView();
        this.positionBirdseye();
      }
    },
    drawImageWithScale(applyAdjustments = true) {
      if (!this.img.complete) {
        console.warn("图片还未加载完成，无法绘制");
        return;
      }
      // 先将整个画布填充为黑色
      this.ctx.fillStyle = "rgb(0, 0, 0)";
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      const scaledWidth = this.img.width * this.scale;
      const scaledHeight = this.img.height * this.scale;

      if (
        scaledWidth <= this.canvas.width &&
        scaledHeight <= this.canvas.height
      ) {
        this.offsetX = (this.canvas.width - scaledWidth) / 2;
        this.offsetY = (this.canvas.height - scaledHeight) / 2;
      } else {
        if (scaledWidth > this.canvas.width) {
          this.offsetX = Math.min(
            0,
            Math.max(this.offsetX, this.canvas.width - scaledWidth)
          );
        } else {
          this.offsetX = (this.canvas.width - scaledWidth) / 2;
        }

        if (scaledHeight > this.canvas.height) {
          this.offsetY = Math.min(
            0,
            Math.max(this.offsetY, this.canvas.height - scaledHeight)
          );
        } else {
          this.offsetY = (this.canvas.height - scaledHeight) / 2;
        }
      }

      if (applyAdjustments) {
        // 调整计算方式，使调节效果更平滑
        this.ctx.filter = `brightness(${(100 + this.brightness * 0.5) / 100
          }) contrast(${(100 + this.contrast * 0.5) / 100})`;
      } else {
        this.ctx.filter = "none";
      }
      // 添加抗失真设置
      this.ctx.imageSmoothingEnabled = true;
      this.ctx.imageSmoothingQuality = 'high';
      this.ctx.drawImage(
        this.img,
        this.offsetX,
        this.offsetY,
        scaledWidth,
        scaledHeight
      );
      this.ctx.filter = "none";
    },
    // handleResize() {
    //   this.redrawCanvas();
    // },
    handleWheel(e) {
      if (this.isDrawing) return;
      e.preventDefault();
      // 根据滚轮方向确定是放大还是缩小
      const isZoomIn = e.deltaY < 0;
      // 每次滑动滑轮要改变的总比例
      const totalChange = 0.15;
      // 每次改变的比例
      const stepChange = 0.01;
      // 计算循环次数
      const steps = totalChange / stepChange;
      let currentStep = 0;
      const intervalId = setInterval(() => {
        if (currentStep >= steps) {
          clearInterval(intervalId);
          return;
        }

        const delta = isZoomIn ? stepChange : -stepChange;
        const newScale = this.scale + delta;

        if (newScale > 0.1 && newScale < 5) {
          const centerX = this.canvas.width / 2;
          const centerY = this.canvas.height / 2;
          const oldScaledWidth = this.img.width * this.scale;
          const oldScaledHeight = this.img.height * this.scale;
          const newScaledWidth = this.img.width * newScale;
          const newScaledHeight = this.img.height * newScale;

          this.offsetX =
            centerX -
            (centerX - this.offsetX) * (newScaledWidth / oldScaledWidth);
          this.offsetY =
            centerY -
            (centerY - this.offsetY) * (newScaledHeight / oldScaledHeight);

          this.scale = newScale;
          this.redrawCanvas();

          if (this.$refs.scaleValue) {
            this.scaleValue = this.$refs.scaleValue;
            this.scaleValue.textContent = `${(this.scale * 100).toFixed(0)}%`;
            const canvasRect = this.canvas.getBoundingClientRect();
            const centerCanvasX = canvasRect.left + canvasRect.width / 2;
            const centerCanvasY = canvasRect.top + canvasRect.height / 2;
            this.scaleValue.style.left = centerCanvasX + "px";
            this.scaleValue.style.top = centerCanvasY + "px";
            this.scaleValue.style.transform = "translate(-50%, -50%)";
            this.scaleValue.style.display = "block";
            setTimeout(() => {
              this.scaleValue.style.display = "none";
            }, 1000);
          }

          if (
            newScaledWidth > this.canvas.width ||
            newScaledHeight > this.canvas.height
          ) {
            this.isBirdseyeVisible = true;
            this.drawBirdseyeView();
            this.positionBirdseye();
            // this.toggleBirdseyeText = "鸟瞰图";
          } else {
            this.isBirdseyeVisible = false;
            this.$refs.birdseyeContainer.style.display = "none";
            // this.toggleBirdseyeText = "鸟瞰图";
          }
        }
        currentStep++;
      }, 20);
    },
    handleMouseDown(e) {
      const brightnessSlider = this.$refs.brightnessSlider;
      const contrastSlider = this.$refs.contrastSlider;
      if (
        this.isBrightnessSliderVisible &&
        brightnessSlider &&
        !brightnessSlider.contains(e.target)
      ) {
        this.isBrightnessSliderVisible = false;
        this.isBrightnessButtonActive = false;
      }
      if (
        this.isContrastSliderVisible &&
        contrastSlider &&
        !contrastSlider.contains(e.target)
      ) {
        this.isContrastSliderVisible = false;
        this.isContrastButtonActive = false;
      }
      if (this.isDrawing) return;
      this.isDragging = true;
      this.dragStartX = e.offsetX;
      this.dragStartY = e.offsetY;
      this.initialOffsetX = this.offsetX;
      this.initialOffsetY = this.offsetY;
      this.canvas.style.cursor = "grab";
      this.canvas.addEventListener("mousemove", this.dragImage);
    },
    dragImage(e) {
      if (this.isDragging) {
        const dx = e.offsetX - this.dragStartX;
        const dy = e.offsetY - this.dragStartY;
        const scaledWidth = this.img.width * this.scale;
        const scaledHeight = this.img.height * this.scale;
        if (scaledWidth > this.canvas.width) {
          this.offsetX = this.initialOffsetX + dx;
        }
        if (scaledHeight > this.canvas.height) {
          this.offsetY = this.initialOffsetY + dy;
        }
        this.redrawCanvas();
      }
    },
    showOriginalImage() {
      if (this.isBrightnessOrContrastAdjusted) {
        this.redrawCanvas(false);
      }
    },
    restoreAdjustedImage() {
      if (this.isBrightnessOrContrastAdjusted) {
        this.redrawCanvas(true);
      }
    },
    handleBrightnessChange() {
      if (this.$refs.brightnessValue) {
        this.brightnessValue = this.$refs.brightnessValue;
        this.brightnessValue.textContent = `${this.brightness}%`;
        const canvasRect = this.canvas.getBoundingClientRect();
        const centerX = canvasRect.left + canvasRect.width / 2;
        const centerY = canvasRect.top + canvasRect.height / 2;
        this.brightnessValue.style.left = centerX + "px";
        this.brightnessValue.style.top = centerY + "px";
        this.brightnessValue.style.transform = "translate(-50%, -50%)";
        this.brightnessValue.style.display = "block";
        setTimeout(() => {
          this.brightnessValue.style.display = "none";
        }, 1000);
      }
      if (!this.isBrightnessOrContrastAdjusted) {
        this.isBrightnessOrContrastAdjusted = true;
      }
      this.redrawCanvas();
      if (this.isBirdseyeVisible) {
        this.drawBirdseyeView(); // 重新绘制鸟瞰图
        this.positionBirdseye();
      }
    },
    handleContrastChange() {
      if (this.$refs.contrastValue) {
        this.contrastValue = this.$refs.contrastValue;
        this.contrastValue.textContent = `${this.contrast}%`;
        const canvasRect = this.canvas.getBoundingClientRect();
        const centerX = canvasRect.left + canvasRect.width / 2;
        const centerY = canvasRect.top + canvasRect.height / 2;
        this.contrastValue.style.left = centerX + "px";
        this.contrastValue.style.top = centerY + "px";
        this.contrastValue.style.transform = "translate(-50%, -50%)";
        this.contrastValue.style.display = "block";
        setTimeout(() => {
          this.contrastValue.style.display = "none";
        }, 1000);
      }
      if (!this.isBrightnessOrContrastAdjusted) {
        this.isBrightnessOrContrastAdjusted = true;
      }
      this.redrawCanvas();
      if (this.isBirdseyeVisible) {
        this.drawBirdseyeView(); // 重新绘制鸟瞰图
        this.positionBirdseye();
      }
    },
    drawBirdseyeView() {
      this.birdseyeCtx.clearRect(
        0,
        0,
        this.birdseyeCanvas.width,
        this.birdseyeCanvas.height
      );
      const birdseyeScaleX = this.birdseyeCanvas.width / this.img.width;
      const birdseyeScaleY = this.birdseyeCanvas.height / this.img.height;
      const brightnessFactor = (100 + this.brightness * 0.5) / 100; // 使用调整后的计算方式
      const contrastFactor = (100 + this.contrast * 0.5) / 100; // 使用调整后的计算方式
      this.birdseyeCtx.filter = `brightness(${brightnessFactor}) contrast(${contrastFactor})`;
      this.birdseyeCtx.drawImage(
        this.img,
        0,
        0,
        this.img.width,
        this.img.height,
        0,
        0,
        this.birdseyeCanvas.width,
        this.birdseyeCanvas.height
      );
      this.birdseyeCtx.filter = "none";
      const viewportX = (-this.offsetX / this.scale) * birdseyeScaleX;
      const viewportY = (-this.offsetY / this.scale) * birdseyeScaleY;
      const viewportWidth = (this.canvas.width / this.scale) * birdseyeScaleX;
      const viewportHeight = (this.canvas.height / this.scale) * birdseyeScaleY;
      this.birdseyeCtx.strokeStyle = "white";
      this.birdseyeCtx.lineWidth = 2;
      this.birdseyeCtx.strokeRect(
        viewportX,
        viewportY,
        viewportWidth,
        viewportHeight
      );
    },
    positionBirdseye() {
      const canvasRect = this.canvas.getBoundingClientRect();
      this.$refs.birdseyeContainer.style.left =
        canvasRect.left +
        canvasRect.width -
        this.birdseyeCanvas.width -
        10 +
        "px";
      this.$refs.birdseyeContainer.style.top =
        canvasRect.top +
        canvasRect.height -
        this.birdseyeCanvas.height -
        10 +
        "px";
    },
    closeBirdseye() {
      this.isBirdseyeVisible = false;
      this.$refs.birdseyeContainer.style.display = "none";
      // this.toggleBirdseyeText = "鸟瞰图";
    },
    toggleBirdseye() {
      this.isBirdseyeVisible = !this.isBirdseyeVisible;
      if (this.isBirdseyeVisible) {
        const scaledWidth = this.img.width * this.scale;
        const scaledHeight = this.img.height * this.scale;
        if (
          scaledWidth > this.canvas.width ||
          scaledHeight > this.canvas.height
        ) {
          this.$refs.birdseyeContainer.style.display = "block";
          this.drawBirdseyeView();
          this.positionBirdseye();
          // this.toggleBirdseyeText = "鸟瞰图";
        } else {
          this.isBirdseyeVisible = false;
          this.$refs.birdseyeContainer.style.display = "none";
          // this.toggleBirdseyeText = "鸟瞰图";
        }
      } else {
        this.$refs.birdseyeContainer.style.display = "none";
        // this.toggleBirdseyeText = "鸟瞰图";
      }
    },
    deleteRectangle(index) {
      const removedRectangle = this.rectangles.splice(index, 1)[0];
      this.inputElements.splice(index, 1);
      this.updateIndices();
      this.redrawCanvas();
      this.$emit("rectangleRemoved", removedRectangle);
    },
    toggleFullscreen() {
      const targetDiv = this.$refs.fullDiv;
      const isFullscreenNow = document.fullscreenElement === targetDiv ||
        document.webkitFullscreenElement === targetDiv ||
        document.msFullscreenElement === targetDiv ||
        document.mozFullScreenElement === targetDiv;

      if (isFullscreenNow) {
        // 退出全屏
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        }
      } else {
        // 进入全屏
        const requestFullscreen = targetDiv.requestFullscreen ||
          targetDiv.webkitRequestFullScreen ||
          targetDiv.msRequestFullscreen ||
          targetDiv.mozRequestFullScreen;
        if (requestFullscreen) {
          requestFullscreen.call(targetDiv);
        }
      }
    },
    handleMouseMove(e) {
      const canvas = this.$refs.imageCanvas;
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const edgeThreshold = 40; // 边缘阈值
      this.isLeftArrowVisible = mouseX < edgeThreshold;
      this.isRightArrowVisible = mouseX > rect.width - edgeThreshold;
    },
    handleFullscreenChange() {
      const targetDiv = this.$refs.fullDiv;
      const isFullscreenNow = document.fullscreenElement === targetDiv ||
        document.webkitFullscreenElement === targetDiv ||
        document.msFullscreenElement === targetDiv ||
        document.mozFullScreenElement === targetDiv;

      if (isFullscreenNow) {
        this.isFullscreen = true;
        const parentWidth = targetDiv.offsetWidth;
        const parentHeight = targetDiv.offsetHeight;
        this.$refs.imageCanvas.style.width = `${parentWidth}px`;
        this.$refs.imageCanvas.style.height = `${parentHeight}px`;
        // 重新计算canvas的实际宽度和高度
        this.$nextTick(() => {
          this.canvas.width = this.$refs.imageCanvas.offsetWidth;
          this.canvas.height = this.$refs.imageCanvas.offsetHeight;
          this.entryLoadImg();
        });
      } else {
        this.isFullscreen = false;
        // 恢复canvas宽高为原来的计算属性值
        this.$refs.imageCanvas.style.width = this.computedWidth;
        this.$refs.imageCanvas.style.height = this.computedHeight;
        // 重新计算canvas的实际宽度和高度
        this.$nextTick(() => {
          this.canvas.width = this.$refs.imageCanvas.offsetWidth;
          this.canvas.height = this.$refs.imageCanvas.offsetHeight;
          this.entryLoadImg();
        });
      }
    },
    handleCtrlAndOne(e) {
      if (e.ctrlKey && e.key === '1') {
        this.toggleDrawing();
      }
    }
  },
};
</script>

<style scoped>
#ImageDrawing {
  display: flex;
  background-color: rgb(15, 26, 72)
}

.left {
  position: relative;
}

.fullscreen {
  width: 100% !important;
  height: 100% !important;
  margin: 0;
  padding: 0;
}

canvas {
  border: 1px solid black;
  display: block;
}

/* 设置按钮容器的样式 */
#button-container {
  position: absolute;
  background-color: transparent;
  /* 灰色背景 */
  width: 100%;
  height: 70px;
  /* 合适的高度 */
  display: flex;
  justify-content: flex-end;
  /* 按钮居右显示 */
  align-items: center;
  /* position: relative; */
}

#button-container button.active-button {
  background-color: rgba(38, 173, 187, 0.5);
}

/* 设置按钮的通用样式 */
#button-container button {
  height: 100%;
  background-color: transparent;
  border: none;
  margin-left: 10px;
  cursor: pointer;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#button-container button img {
  filter: grayscale(100%) brightness(1000%);
  height: 40%;
}

.slider-wrapper {
  position: absolute;
  width: 50%;
  ;
  top: -50px;
  /* 初始隐藏在上方 */
  left: 50%;
  /* 水平居中 */
  transform: translate(-50%, -50%);
  /* 精确居中 */
  color: white;
  background-color: rgba(128, 128, 128, 0.5);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: top 0.3s ease;
  /* margin-top: 100px; */
  z-index: 10;
  /* 确保滑动条显示在上方 */
}

.slide-in {
  top: 80px;
  /* 滑入显示 */
}

.slide-out {
  top: -50px;
  /* 滑出隐藏 */
}

.arrow {
  position: absolute;
  top: 50%;
  transform: scaleX(0.5) translateY(-50%);
  font-size: 50px;
  color: lightgray;
  background-color: transparent;
  cursor: pointer;
  opacity: 0;
  z-index: 10; 
}

/* 左箭头样式 */
.left-arrow {
  left: 5px;
}

/* 右箭头样式 */
.right-arrow {
  right: 5px;
}

/* 箭头显示时的样式 */
.arrow.show {
  opacity: 1;
}

/* .slider-wrapper label {
  margin-right: 10px;
  color: white;
} */

.slider-wrapper input {
  color: white;
}

/* 自定义滑动条轨道样式 */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: calc(100% - 80px);
  /* 滑动条长度 */
  height: 5px;
  /* 滑动条高度 */
  background: #d3d3d3;
  /* 轨道背景颜色 */
  outline: none;
  border-radius: 5px;
}

/* 自定义滑动条按钮样式 */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  /* 按钮宽度 */
  height: 20px;
  /* 按钮高度 */
  background: #007bff;
  /* 按钮背景颜色 */
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #007bff;
  border-radius: 50%;
  cursor: pointer;
}

.rect-button {
  position: absolute;
  z-index: 100;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.rect-cancel {
  background-color: rgba(255, 0, 0, 0.3);
}

.rect-confirm {
  background-color: rgba(0, 255, 0, 0.3);
  left: 25px;
}

.compare-original {
  position: absolute;
  width: 110px;
  height: 40px;
  left: 90%;
  top: 70%;
  color: white;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  border-radius: 25px;
  background-color: rgba(255, 255, 255, 0.3);
  z-index: 101;
}

.compare-original img {
  /* 让图片自适应按钮高度 */
  height: 80%;
  /* 为图片和文字之间添加间距 */
  margin-right: 5px;
  vertical-align: middle;
  /* 将图片的垂直对齐方式设置为中间 */
}

#slider-container {
  margin-top: 10px;
}

#slider-container label {
  display: block;
  margin-bottom: 5px;
}

#brightness-value,
#contrast-value,
#scale-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.7);
  padding: 5px;
  border-radius: 5px;
  display: none;
}

#birdseye-container {
  position: absolute;
  z-index: 10;
}

#birdseye-view {
  border: 1px solid black;
}

#close-birdseye {
  position: absolute;
  top: 5px;
  right: 5px;
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 2px 5px;
}

#imageCanvas {
  position: relative;
}
</style>