<template>
    <div class="upload-wrapper">
        <div class="upload-container">
            <img :src="resultImage" class="preview-image">
        </div>
    </div>
</template>

<script>
export default {
    props: {
        resultImage: {
            type: String,
            required: true
        }
    }
}
</script>

<style scoped>
.upload-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
}

.upload-container {
    width: 250px;
    height: 250px;
    border: 2px dashed #dcdfe6;
    border-radius: 8px;
    background: #fafafa;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    transition: border-color 0.3s;
}

.preview-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
</style>