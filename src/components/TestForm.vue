<template>
  <el-form :model="form" ref="formRef">
    <el-row>
      <!-- 左半部分表单 -->
      <el-col :span="14">
        <h2>病历信息</h2>

        <div class="personal-info-container">
          <el-form-item label="姓名" prop="name" class="name-item">
            <el-input v-model="form.name" placeholder="请输入姓名" />
          </el-form-item>

          <el-form-item label="年龄" prop="age" class="age-item">
            <el-input v-model="form.age" @input="handleAgeInput" />
          </el-form-item>

          <el-form-item label="性别" prop="gender" class="gender-item">
            <el-select v-model="form.gender" placeholder="">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>

          <el-form-item label="病历号" prop="caseID" class="caseID-item">
            <el-input v-model="form.caseID" placeholder="请输入病历号" />
          </el-form-item>
        </div>



        <div class="eye-data-container">
          <el-form-item label="左眼视力" prop="left_eye_vision" class="Leyevision-item">
            <el-input v-model="form.left_eye_vision" />
          </el-form-item>

          <el-form-item label="右眼视力" prop="right_eye_vision" class="Reyevision-item">
            <el-input v-model="form.right_eye_vision" />
          </el-form-item>

          <el-form-item label="左眼眼压" prop="left_eye_pressure" class="Leyepressure-item">
            <el-input v-model="form.left_eye_pressure" />
          </el-form-item>

          <el-form-item label="右眼眼压" prop="right_eye_pressure" class="Reyepressure-item">
            <el-input v-model="form.right_eye_pressure" />
          </el-form-item>
        </div>




        <div class="eye-status-container1">
          <el-form-item label="眼轴长度" prop="eye_axis_length" class="Eyeaxislength-item">
            <el-input v-model="form.eye_axis_length" />
          </el-form-item>

          <el-form-item label="角膜曲率" prop="corneal_curvature" class="Cornealcurvature-item">
            <el-input v-model="form.corneal_curvature" />
          </el-form-item>

          <el-form-item label="晶状体混浊程度" prop="lens_clouding" class="Lensclouding-item">
            <el-input v-model="form.lens_clouding" />
          </el-form-item>

          <el-form-item label="视网膜血管情况" prop="retinal_vascularization" class="Retinalvascularization-item">
            <el-input v-model="form.retinal_vascularization" />
          </el-form-item>
        </div>


        <div class="eye-status-container2">
          <el-form-item label="黄斑状况" prop="macular_condition" class="Macularcondition-item">
            <el-input v-model="form.macular_condition" />
          </el-form-item>

          <el-form-item label="高血压病史" prop="history_of_hypertension" class="Historyofhypertension-item">
            <el-input v-model="form.history_of_hypertension" />
          </el-form-item>

          <el-form-item label="糖尿病病史" prop="history_of_diabetes" class="Historyofdiabetes-item">
            <el-input v-model="form.history_of_diabetes" />
          </el-form-item>
        </div>



        <div class="eye-status-container3">
          <el-form-item label="眼底病史" prop="history_of_eye_disease" class="Historyofeyedisease-item">
            <el-input v-model="form.history_of_eye_disease" />
          </el-form-item>

          <el-form-item label="家族病史" prop="family_medical_history" class="Amilymedicalhistory-item">
            <el-input v-model="form.family_medical_history" />
          </el-form-item>
        </div>
      </el-col>

      <!-- 右半部分图片和导出 -->
      <el-col :span="10">
        <div class="image-container">
          <el-form-item label="左眼图片" class="top-label-item">
            <image-uploader @file-uploaded="LhandleUpload" />
          </el-form-item>

          <el-form-item label="右眼图片" class="top-label-item">
            <image-uploader @file-uploaded="RhandleUpload" />
          </el-form-item> 
        </div>

        <el-form-item label="医生建议">
          <el-input v-model="form.advice" type="textarea" maxlength=300 :autosize="{ minRows: 2, maxRows: 4 }" />
        </el-form-item>
        <el-form-item>
          <pdf-export-button :form-data="form" />
        </el-form-item>

      </el-col>

    </el-row>
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
        age: '',
        gender: '',
        caseID: '',
        left_eye_vision: '',
        right_eye_vision: '',
        left_eye_pressure: '',
        right_eye_pressure: '',
        eye_axis_length: '',
        corneal_curvature: '',
        lens_clouding: '',
        retinal_vascularization: '',
        macular_condition: '',
        history_of_hypertension: '',
        history_of_diabetes: '',
        history_of_eye_disease: '',
        family_medical_history: '',
        advice: '',
        left_eye_image: null,
        right_eye_image: null
      }
    }
  },
  methods: {
    LhandleUpload(uploadEvent) {
      const file = uploadEvent?.file || uploadEvent;
      if (file instanceof File) {
        this.form.left_eye_image = file;
      } else {
        this.$message.error('文件格式不正确，请上传图片文件');
      }
    },
    RhandleUpload(uploadEvent) {
      const file = uploadEvent?.file || uploadEvent;
      if (file instanceof File) {
        this.form.right_eye_image = file;
      } else {
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
            this.form.age = '';
          });
        }
      }
    }
  }
}
</script>

<style scoped>
/* 每个信息容器独占一行 */
.personal-info-container {
  display: flex;
  width: 100%;
  gap: 20px;
  padding: 0;
  clear: both;

  .age-item {
    width: 60px;
  }

  .gender-item {
    width: 75px;
  }
}

.eye-data-container {
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;

  [class$="-item"] {
    /* 匹配所有以 -item 结尾的类 */
    width: 80px;
    margin: 0 8px;
  }
}

.eye-status-container1 {
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;

  .Eyeaxislength-item {
    width: 70px;
  }

  .Cornealcurvature-item {
    width: 70px;
  }

  .Lensclouding-item {
    width: 150px;
  }

  .Retinalvascularization-item {
    width: 150px;
  }
}

.eye-status-container2{
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;  

  .Macularcondition-item{
    width: 160px;
  }

  .Historyofhypertension-item{
    width: 160px;
  }

  .Historyofdiabetes-item{
    width: 160px;
  }
  
}

.eye-status-container3{
  display: flex;
  width: 100%;
  gap: 100px;
  padding: 0;

  .Historyofeyedisease-item{
    width: 200px;
  }

  .Amilymedicalhistory-item{
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

/* 通用顶部标签样式 */
.top-label-item {
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* 全局表单标签左对齐 */
:deep(.el-form-item__label) {
  text-align: left;
  width: 100%;
  padding-left: 0;
}
</style>