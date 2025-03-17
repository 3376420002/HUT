<template>
  <div style="height: 100%;background-color: #1A1F28;">
    <el-form :model="form">
      <el-row>
        <!-- 左半部分表单 -->
        <el-col :span="14" class="{display: 'flex', flexDirection: 'column'}">
          <div class="personal-info-container">
            <el-form-item label="姓名" prop="name" class="name-item">
              <el-input v-model="form.name" :disabled="!isEditing" />
            </el-form-item>

            <el-form-item label="年龄" prop="age" class="age-item">
              <el-input v-model="form.age" @input="handleAgeInput" :disabled="!isEditing" />
            </el-form-item>

            <el-form-item label="性别" prop="gender" class="gender-item">
              <el-input v-model="form.gender" :disabled="!isEditing" />
            </el-form-item>

            <el-form-item label="医生工号" prop="doctorID" class="doctorID-item">
              <el-input v-model="form.doctorID" :disabled="!isEditing" />
            </el-form-item>
          </div>

          <div class="personal-info-container">
            <el-form-item label="科室" prop="department" class="department-item">
              <el-input v-model="form.department" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email" class="email-item">
              <el-input v-model="form.email" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone" class="phone-item">
              <el-input v-model="form.phone" :disabled="!isEditing" />
            </el-form-item>
          </div>
        </el-col>
        <!-- 右半部分图片-->
        <el-col :span="10">
          <div class="image-container">
            <el-form-item label="个人照片">
              <ImageUploader @file-uploaded="imageUpload" :disabled="!isEditing" />
            </el-form-item>
          </div>
        </el-col>

      </el-row>
    </el-form>

    <div class="button-group">
      <el-button v-if="!isEditing" type="primary" @click="enableEditing">修改</el-button>
      <el-button v-else type="success" @click="submitForm">提交</el-button>
    </div>
  </div>
</template>

<script>
import ImageUploader from '@/components/ImageUploader.vue';

export default {
  components: {
    ImageUploader
  },
  data() {
    return {
      isEditing: false,
      form: {
        name: '',
        age: '',
        gender: '',
        doctorID: '',
        department: '',
        email: '',
        phone: '',
        image: ''
      }
    }
  },
  computed: {
    cssVars() {
      return {
        '--bg-color': this.isEditing ? '#fff' : '#f5f7fa',
        '--cursor-type': this.isEditing ? 'text' : 'not-allowed'
      }
    }
  },
  methods: {
    enableEditing() {
      this.isEditing = true
    },
    submitForm() {
      // 这里添加提交逻辑
      console.log('提交表单:', this.form)
      this.isEditing = false
    },
    imageUpload({ file, base64 }) {
      this.form.image = base64;
      this.file = file;
    }
  }
}
</script>

<style scoped>
/* 每个信息容器独占一行 */
.personal-info-container {
  display: flex;
  flex-direction: pow;
  width: 100%;
  gap: 20px;
  padding: 0;
  clear: both;

  .name-item {
    width: 150px;
  }

  .age-item {
    width: 60px;
  }

  .gender-item {
    width: 75px;
  }

  .doctorID-item {
    width: 200px;
  }

  .department-item {
    width: 200px;
  }
}

.image-container {
  display: flex;
  width: 100%;
  gap: 20px;
  padding: 0;
  clear: both;
}

/* 表单项垂直布局 */
.el-form-item {
  margin: 20px 0;
}

.el-row {
  display: flex;
  gap: 20px;
}

.el-textarea {
  width: 100%;
}

.button-group {
  margin-top: 20px;
  text-align: center;
}

.el-input :deep(.el-input__inner),
.el-select :deep(.el-select__wrapper) {
  background-color: var(--bg-color);
  cursor: var(--cursor-type);
}

/* 添加图片上传组件禁用样式 */
.el-form-item.is-disabled .image-uploader-container {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* 修改表单容器背景 */
.el-form {
  background-color: #1A1F28;
  /* 与header背景一致 */
  padding: 20px;
  border-radius: 8px;
}

/* 标签文字颜色 */
.el-form-item :deep(.el-form-item__label) {
  color: #CCCCCC !important;
  /* 浅灰色 */
}

/* 输入框文字颜色 */
.el-input :deep(.el-input__inner) {
  color: #BAE67E;
  /* 主题绿色 */
  background-color: #212733;
  /* 工具栏背景色 */
}

/* 按钮颜色 */
.el-button--primary {
  background-color: #67606F !important;
  /* 边框色 */
  border-color: #67606F !important;
}

.el-button--success {
  background-color: #BAE67E !important;
  /* 主题绿色 */
  border-color: #BAE67E !important;
  color: #1A1F28 !important;
  /* 深色文字 */
}

/* 禁用状态样式 */
.el-input.is-disabled :deep(.el-input__inner) {
  background-color: #1A1F28 !important;
  /* 头部背景色 */
  color: #67606F !important;
  /* 边框色 */
}
</style>