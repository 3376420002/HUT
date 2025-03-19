<template>
    <el-button type="primary" @click="generatePDF" class="export-button" icon="el-icon-document-checked">
        导出PDF
    </el-button>
</template>

<script>
import { PDFDocument } from 'pdf-lib';
import fontkit from '@pdf-lib/fontkit';
import { saveAs } from 'file-saver';

export default {
    props: {
        formData: {
            type: Object,
            required: true
        }
    },
    methods: {
        async generatePDF() {
            try {
                // 加载PDF模板
                const templateUrl = '/template.pdf';
                //链式调用，将模板转为字节流
                const existingPdfBytes = await fetch(templateUrl).then(res => res.arrayBuffer());
                // 创建PDF文档并注册字体
                const pdfDoc = await PDFDocument.load(existingPdfBytes);
                pdfDoc.registerFontkit(fontkit);

                // 嵌入中文字体(PDF默认winansi，不支持中文字符)
                // 当使用embedFont嵌入字体时，pdf-lib会：
                // 解析字体文件的字符映射表（CMAP）
                // 将Unicode字符转换为字体内部的字形索引
                // 生成新的字体描述符覆盖WinAnsi编码
                // 在PDF中嵌入字体子集（仅包含实际使用的字符）
                const fontBytes = await fetch('/fzsongti.ttf').then(res => res.arrayBuffer());
                const customFont = await pdfDoc.embedFont(fontBytes);

                // 获取表单字段并自动匹配
                const form = pdfDoc.getForm();
                const formData = this.formData;

                // 自动填充文本字段
                Object.keys(formData).forEach(fieldName => {
                    if (fieldName.includes('Image')) return; // 跳过所有图片字段

                    try {
                        const field = form.getTextField(fieldName);
                        field.setText(formData[fieldName]);
                        field.updateAppearances(customFont);
                    } catch (error) {
                        console.warn(`未找到字段 ${fieldName} 或不是文本字段`);
                    }
                });

                // 处理左右眼图片字段
                const handleImageField = async (formFieldName, pdfFieldName) => {
                    if (formData[formFieldName]) {
                        try {
                            const imageField = form.getButton(pdfFieldName);
                            const imageBytes = await this.readFileAsArrayBuffer(formData[formFieldName]);
                            
                            // 通用图片处理（根据文件类型自动选择嵌入方式）
                            const imageType = formData[formFieldName].type;
                            let image;
                            if (imageType === 'image/jpeg') {
                                image = await pdfDoc.embedJpg(imageBytes);
                            } else if (imageType === 'image/png') {
                                image = await pdfDoc.embedPng(imageBytes);
                            } else {
                                throw new Error('不支持的图片格式，仅支持JPG/PNG');
                            }
                            imageField.setImage(image);
                        } catch (error) {
                            console.warn(`图片字段 ${formFieldName} 处理失败:`, error);
                        }
                    }
                };

                await handleImageField('leftEyeImage', 'leftEyeImage_af_image');
                await handleImageField('rightEyeImage', 'rightEyeImage_af_image');

                // 保存PDF
                const pdfBytes = await pdfDoc.save();
                const blob = new Blob([pdfBytes], { type: 'application/pdf' });
                saveAs(blob, `${this.formData.name}_检查报告.pdf`);

            } catch (error) {
                this.$message.error('生成PDF失败，请稍后重试');
            }
        },
        async readFileAsArrayBuffer(file) {
            return new Promise((resolve, reject) => {
                // 确保传入的是有效的File对象
                if (!(file instanceof Blob)) {
                    reject(new Error('无效的文件类型，请确保上传的是有效的文件对象'));
                    return;
                }

                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsArrayBuffer(file);
            });
        }
    }
}
</script>

<style scoped>
.export-button {
    padding: 10px 20px;
    transition: all 0.3s;
    background-color: #BAE67E;
    border-color: #67606F;
}

.export-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>