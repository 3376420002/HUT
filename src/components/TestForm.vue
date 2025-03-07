<template>
  <el-form :model="form" ref="formRef" label-width="100px" class="demo-form">
    <div>
      <h2>病历信息</h2>
    </div>
    <el-form-item label="姓名" prop="name" class="name-item">
      <el-input v-model="form.name" placeholder="请输入姓名" />
    </el-form-item>

    <el-form-item label="性别" prop="gender" class="gender-item">
      <el-select v-model="form.gender" placeholder="请选择">
        <el-option label="男" value="男" />
        <el-option label="女" value="女" />
      </el-select>
    </el-form-item>

    <el-form-item label="年龄" prop="age" class="age-item">
      <el-input v-model="form.age" @input="handleAgeInput" />
    </el-form-item>

    <el-form-item label="医生建议" prop="advice" class="advice-item">
      <el-input v-model="form.advice" type="textarea" maxlength=300 />
    </el-form-item>

    <el-form-item label="上传图片">
      <image-uploader @file-uploaded="handleUpload" />
    </el-form-item>

    <el-form-item>
      <pdf-export-button :form-data="form" />
    </el-form-item>

  </el-form>
</template>

<script>
import PdfExportButton from './PdfExportButton.vue'
import ImageUploader from './ImageUploader.vue';

export default {
  components: {
    PdfExportButton,
    ImageUploader
  },
  data() {
    return {
      form: {
        name: '',
        gender: '',
        age: '',
        advice: '',
        eyeImage: null
      }
    }
  },
  methods: {
    handleUpload(uploadEvent) {
      const file = uploadEvent?.file || uploadEvent;
      if (file instanceof File) {
        this.form.eyeImage = file;
      } else {
        console.error('无效的文件类型:', file);
        this.$message.error('文件格式不正确，请上传图片文件');
      }
    },
    handleAgeInput(value) {//浏览器所有输入的返回都是字符串
      if (!/^(1[0-1][0-9]|120|[1-9][0-9]?)$/.test(value)) {
        this.form.age = value.replace(/[^\d]/g, '')
          .replace(/^0+/, '') 
          .slice(0, 3);

        if (this.form.age !== '') {
          this.$nextTick(() => {
            this.$message.warning('请输入1-120之间的有效年龄');
          });
        }
      }
    }
  }
}
</script>

<style scoped>
.demo-form {
  max-width: 600px;
  margin: 20px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.name-item :deep(.el-input) {
  /*:deep()选择器穿透element-ui组件样式*/
  width: 120px;
}

.gender-item :deep(.el-select) {
  width: 100px;
}

.age-item :deep(.el-input) {
  width: 60px;
}

.advice-item :deep(.el-textarea) {
  width: 400px;
  min-height: 80px;
}
</style>