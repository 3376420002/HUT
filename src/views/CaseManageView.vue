<template>
  <div id="case-manage">
    <div class="body">
      <!-- 引入对话框子组件 -->
      <div class="dialog-container">
        <AIDialog :shortcutButtons="shortcutButtons" :shortcutFunctions="shortcutFunctions" @CaseAnalysis="caseAnalysis"
          @open="open" @close="close" />
      </div>
      <div class="case-content" :class="{ 'shrink': isOpen }">
        <div class="page-content">
          <!-- 页面其他内容
          <h1>页面主要内容</h1>
          <p>这是页面的主要内容。</p> -->
          <el-form :model="form" ref="formRef">
            <el-row>
              <!-- 左半部分表单 -->
              <el-col :span="14">
                <h2 style="color: #d4c7e3;">病历信息</h2>
                <div class="personal-info-container">
                  <el-form-item label="姓名" prop="name" class="name-item">
                    <el-input v-model="form.name" />
                  </el-form-item>
                  <el-form-item label="年龄" prop="age" class="age-item">
                    <el-input v-model="form.age" @input="handleAgeInput" />
                  </el-form-item>
                  <el-form-item label="性别" prop="gender" class="gender-item">
                    <el-input v-model="form.gender" />
                  </el-form-item>
                  <el-form-item label="病历号" prop="caseID" class="caseID-item">
                    <el-input v-model="form.caseID" />
                  </el-form-item>
                </div>

                <div class="eye-data-container">
                  <el-form-item label="左眼视力" prop="leftEyeVision" class="LeftEyeVision-item">
                    <el-input v-model="form.leftEyeVision" />
                  </el-form-item>
                  <el-form-item label="右眼视力" prop="rightEyeVision" class="REyeVision-item">
                    <el-input v-model="form.rightEyeVision" />
                  </el-form-item>
                  <el-form-item label="左眼眼压" prop="leftEyePressure" class="LEyePressure-item">
                    <el-input v-model="form.leftEyePressure" />
                  </el-form-item>
                  <el-form-item label="右眼眼压" prop="rightEyePressure" class="REyePressure-item">
                    <el-input v-model="form.rightEyePressure" />
                  </el-form-item>
                </div>

                <div class="eye-status-container1">
                  <el-form-item label="眼轴长度" prop="eyeAxisLength" class="EyeAxisLength-item">
                    <el-input v-model="form.eyeAxisLength" />
                  </el-form-item>
                  <el-form-item label="角膜曲率" prop="cornealCurvature" class="CornealCurvature-item">
                    <el-input v-model="form.cornealCurvature" />
                  </el-form-item>
                  <el-form-item label="晶状体混浊程度" prop="lensClouding" class="LensClouding-item">
                    <el-input v-model="form.lensClouding" />
                  </el-form-item>
                  <el-form-item label="视网膜血管情况" prop="retinalVasculature" class="RetinalVasculature-item">
                    <el-input v-model="form.retinalVasculature" />
                  </el-form-item>
                </div>

                <div class="eye-status-container2">
                  <el-form-item label="黄斑状况" prop="macularCondition" class="MacularCondition-item">
                    <el-input v-model="form.macularCondition" />
                  </el-form-item>
                  <el-form-item label="高血压病史" prop="historyOfHypertension" class="HistoryOfHypertension-item">
                    <el-input v-model="form.historyOfHypertension" />
                  </el-form-item>
                  <el-form-item label="糖尿病病史" prop="historyOfDiabetes" class="HistoryOfDiabetes-item">
                    <el-input v-model="form.historyOfDiabetes" />
                  </el-form-item>
                </div>

                <div class="eye-status-container3">
                  <el-form-item label="眼底病史" prop="historyOfEyeDisease" class="HistoryOfEyeDisease-item">
                    <el-input v-model="form.historyOfEyeDisease" />
                  </el-form-item>
                  <el-form-item label="家族病史" prop="familyMedicalHistory" class="FamilyMedicalHistory-item">
                    <el-input v-model="form.familyMedicalHistory" />
                  </el-form-item>
                </div>

                <div class="clinicalDiagnosis-container">
                  <el-form-item label="临床诊断" prop="clinicalDiagnosis">
                    <el-input v-model="form.clinicalDiagnosis" />
                  </el-form-item>
                </div>

              </el-col>
              <!-- 右半部分图片和导出 -->
              <el-col :span="10">
                <div class="image-container">
                  <el-form-item label="左眼图片" class="eyeImageLabel">
                    <image-uploader :isUpload="true" :imageFile="this.form.leftEyeImageBase64"
                      @file-uploaded="LHandleUpload" />
                  </el-form-item>
                  <el-form-item label="右眼图片" class="eyeImageLabel">
                    <image-uploader :isUpload="true" :imageFile="this.form.rightEyeImageBase64"
                      @file-uploaded="RHandleUpload" />
                  </el-form-item>
                </div>
                <el-form-item label="医生建议">
                  <el-input v-model="form.advice" type="textarea" maxlength="300" resize="none"
                    :autosize="{ minRows: 4, maxRows: 8 }" />
                </el-form-item>
                <!-- 提交pdf按钮 -->
                <el-form-item>
                  <PdfExportButton :form-data="form" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageUploader from '@/components/ImageUploader.vue';
import AIDialog from '@/components/AIDialog.vue';
import PdfExportButton from '@/components/PdfExportButton.vue';
import axios from 'axios'
export default {
  components: {
    AIDialog, ImageUploader, PdfExportButton
  },
  data() {
    return {
      isOpen: false,
      shortcutButtons: ["病例综合分析", "左眼分析", "右眼分析"],
      shortcutFunctions: ["caseAnalysis"],//供AIDialog调用获得父组件的信息
      form: {
        name: '',
        age: '',
        gender: '',
        caseID: '',
        leftEyeVision: '',
        rightEyeVision: '',
        leftEyePressure: '',
        rightEyePressure: '',
        eyeAxisLength: '',
        cornealCurvature: '',
        lensClouding: '',
        retinalVasculature: '',
        macularCondition: '',
        historyOfHypertension: '',
        historyOfDiabetes: '',
        historyOfEyeDisease: '',
        familyMedicalHistory: '',
        advice: '',
        diagnoseDoctor: '',
        diagnoseDate: '',
        clinicalDiagnosis: '',
        // leftEyeImage: null,//file
        // rightEyeImage: null,
        leftEyeImageBase64: null,
        rightEyeImageBase64: null,
        // leftOctImage: null,
        // rightOctImage: null,
        leftOctImageBase64: null,
        rightOctImageBase64: null,
      }
    }
  },
  activated(){
    this.InitCase();
    this.InitAdvice();
  },
  // created() {
  //   this.InitCase();
  //   this.InitAdvice();
  // },
  mounted() {

  },
  methods: {
    InitCase() {
      if (this.$route.query && this.$route.query.imageChoice) {
        const choice = this.$route.query.imageChoice;
        const images = this.$route.query.images;
        console.log(images);
        if (choice === 1) {
          if (images.name == "left") {
            this.form.leftEyeImageBase64 = images.path;
            // this.form.leftEyeImage = this.base64ToFile(images.path, "leftEye");
          }
          else if (images.name == "right") {
            this.form.rightEyeImageBase64 = images.path;
            // this.form.rightEyeImage = this.base64ToFile(images.path, "rightEye");
          }
          else if (images.name == "left-oct") this.form.leftOctImageBase64 = images.path;
          else this.form.rightOctImageBase64 = images.path;
        } else {
          for (let image of images) {
            if (image.name == "left") this.form.leftEyeImageBase64 = image.path;
            else if (image.name == "right") this.form.rightEyeImageBase64 = image.path;
            else if (image.name == "left-oct") this.form.leftOctImageBase64 = image.path;
            else this.form.rightOctImageBase64 = image.path;
          }
        }
      }
    },
    InitAdvice() {
      if (this.$route.query && this.$route.query.inputs) {
        const inputElements = this.$route.query.inputs;
        const validInputElements = Array.isArray(inputElements) ? inputElements : [];
        const groupedData = {
          "左眼": [],
          "右眼": []
        };
        // 对 inputElements 进行分类
        validInputElements.forEach(item => {
          if (item.name === "left" || item.name === "left - oct") {
            groupedData["左眼"] = groupedData["左眼"].concat(item.inputs.map(input => input.value));
          } else if (item.name === "right" || item.name === "right - oct") {
            groupedData["右眼"] = groupedData["右眼"].concat(item.inputs.map(input => input.value));
          }
        });
        // 用于存储最终生成的字符串
        let result = "";
        // 遍历分类后的结果，拼接字符串
        for (const [key, values] of Object.entries(groupedData)) {
          if (values.length > 0) {
            result += `${key}：\n`;
            values.forEach((value, index) => {
              result += `${index + 1}.${value}\n`;
            });
          }
        }
        this.form.advice = result;
      }
    },
    async caseAnalysis() {
      console.log("测试输出")
      //获取该页面病例的信息并返回给对话框，这里返回1
      const response = await axios.get("http://192.168.1.136:8800");
      const data = String(response.data.message);
      console.log(data);
      return data;
      // return String("针对50岁男性患者晚期青光眼的情况，以下是针对性的诊断建议和治疗流程：\n\n### 1. 治疗建议\n- **眼内压控制**：在晚期青光眼患者中，眼内压的控制是防止进一步视神经损害的关键。可以考虑如下方式：\n  - **药物治疗**：根据患者的个体耐受性及以往用药记录，选择合适的降眼压药物组合。\n  - **激光治疗**：如需要可考虑进行处于相对安全的范围内的激光小梁成形术或激光周边虹膜切开术，以改善房水流出。\n  - **手术治疗**：对于需要手术干预的患者，可以考虑进行青光眼滤过手术（如小梁切除术）或管状阀植入手术。\n\n### 2. 检查计划\n- **眼压监测**：定期监测眼内压，评估治疗效果。\n- **视野检查**：使用电脑视野计定期进行视野检测，记录视野缺损的进展情况。\n- **视神经检查**：使用OCT（光学相干断层扫描）检查视网膜神经纤维层厚度，评估视神经的损伤程度。\n- **房角检查**：使用前房角镜检查房角的开放情况，如有必要进行房水动力学检查。\n\n### 3. 用药建议\n根据患者的具体情况，可以考虑以下几类降眼压药物：\n- **β-adrenergic拮抗剂**（如美托洛尔眼药水）\n- **前列腺素类**（如拉坦前列素眼药水）\n- **碳酸酐酶抑制剂**（如乙酰唑胺口服或磺酰胺眼药水）\n- **α2-adrenergic激动剂**（如布林佐胺眼药水）\n\n在实施药物治疗时，务必注意患者可能的副作用和合并症，同时对药物的相互作用进行评估。如果患者对某些药物有过敏或不良反应，需及时调整用药计划。\n\n### 总结\n鉴于患者已经处于青光眼的晚期阶段，治疗的重点在于降低眼内压，减缓视神经进一步损害的进展。通过综合的检查与个体化的用药计划，可以为患者提供最佳的管理方案。同时，患者的生活方式调整（如合理控制体重、避免剧烈运动等）也对病情有一定影响，建议进行相应的指导和提醒。");
    },
    // 打开操作，将 isOpen 设为 true
    open() {
      this.isOpen = true;
    },
    // 关闭操作，将 isOpen 设为 false
    close() {
      this.isOpen = false;
    },
    LHandleUpload({ file, base64 }) {  // 解构参数获取file和base64
      if (file instanceof File) {
        // this.form.leftEyeImage = file;
        this.form.leftEyeImageBase64 = base64;
      } else {
        this.$message.error('文件格式不正确，请上传图片文件');
      }
    },
    RHandleUpload({ file, base64 }) {
      if (file instanceof File) {
        // this.form.rightEyeImage = file;
        this.form.rightEyeImageBase64 = base64;
      } else {
        this.$message.error('文件格式不正确，请上传图片文件');
      }
    },
    // base64ToFile(base64, filename) {
    //   // 提取 MIME 类型
    //   const mimeType = base64.match(/^data:([^;]+);base64,/)[1];
    //   const sliceSize = 512;
    //   const byteCharacters = atob(base64.split(',')[1]);
    //   const byteArrays = [];
    //   for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    //     const slice = byteCharacters.slice(offset, offset + sliceSize);
    //     const byteNumbers = new Array(slice.length);
    //     for (let i = 0; i < slice.length; i++) {
    //       byteNumbers[i] = slice.charCodeAt(i);
    //     }
    //     const byteArray = new Uint8Array(byteNumbers);
    //     byteArrays.push(byteArray);
    //   }
    //   const blob = new Blob(byteArrays, { type: mimeType });
    //   return new File([blob], filename, { type: mimeType });
    // },
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
};
</script>

<style scoped>
#case-manage {
  width: 100%;
  height: 100%;
  /* 确保容器有足够的高度 */
}

.body {
  background-color: #1A1F28;
  display: flex;
  height: 100%;
  width: 100%;
  position: relative;
  /* 为父容器添加相对定位 */
}

.page-content {
  padding: 0 20px 0 20px;
}

.dialog-container {
  width: 400px;
  position: relative;
}

.case-content {
  position: absolute;
  /* 使用绝对定位 */
  top: 0;
  right: 0;
  left: 0;
  width: 100%;
  transition: width 0.3s ease, left 0.3s ease;
  /* 添加 left 属性的过渡效果 */
}

.case-content.shrink {
  left: 400px;
  width: calc(100% - 400px);
}

/* 每个信息容器独占一行 */
.personal-info-container {
  display: flex;
  width: 100%;
  gap: 20px;
  padding: 0;
  clear: both;
}

.personal-info-container .age-item {
  width: 60px;
}

.personal-info-container .gender-item {
  width: 75px;
}

.eye-data-container {
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;
}

.eye-data-container [class$="-item"] {
  width: 80px;
  margin: 0 8px 0 0;
}

.eye-status-container1 {
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;
}

.eye-status-container1 .EyeAxisLength-item {
  width: 70px;
}

.eye-status-container1 .CornealCurvature-item {
  width: 70px;
}

.eye-status-container1 .LensClouding-item {
  width: 150px;
}

.eye-status-container1 .RetinalVasculature-item {
  width: 150px;
}


.eye-status-container2 {
  display: flex;
  width: 100%;
  gap: 60px;
  padding: 0;
  clear: both;
}

.eye-status-container2 .MacularCondition-item {
  width: 160px;
}

.eye-status-container2 .HistoryOfHypertension-item {
  width: 160px;
}

.eye-status-container2 .HistoryOfDiabetes-item {
  width: 160px;
}

.eye-status-container3 {
  display: flex;
  width: 100%;
  gap: 100px;
  padding: 0;
}

.eye-status-container3 .HistoryOfEyeDisease-item {
  width: 200px;
}

.eye-status-container3 .FamilyMedicalHistory-item {
  width: 200px;
}

.clinicalDiagnosis-container {
  display: flex;
  padding: 0;
  width: 100%;
}

.image-container {
  display: flex;
  width: 100%;
  gap: 20px;
  padding: 0;
  clear: both;
}

.el-form-item:deep(.el-textarea__inner),
.el-form-item:deep(.el-input__inner) {
  background-color: #1A1F28;
  color: #d4c7e3;
}

.el-row {
  display: flex;
  gap: 20px;
}

.eyeImageLabel {
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* 全局表单标签左对齐 */
:deep(.el-form-item__label) {
  text-align: left;
  width: 100%;
  padding-left: 0;
  color: #d4c7e3;
}
</style>