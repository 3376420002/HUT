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
                    if (fieldName === 'eyeImage') return; // 跳过图片字段

                    try {
                        const field = form.getTextField(fieldName);
                        field.setText(formData[fieldName]);
                        field.updateAppearances(customFont);
                    } catch (error) {
                        console.warn(`未找到字段 ${fieldName} 或不是文本字段`);
                    }
                });

                // 处理图片字段
                if (formData.eyeImage) {
                    try {
                        // 获取图片域
                        const imageField = form.getButton('eyeImage_af_image');

                        const imageBytes = await this.readFileAsArrayBuffer(formData.eyeImage);
                        
                        // 通用图片处理（根据文件类型自动选择嵌入方式）
                        const imageType = formData.eyeImage.type;
                        let image;
                        if (imageType === 'image/jpeg') {
                            image = await pdfDoc.embedJpg(imageBytes);
                        } else if (imageType === 'image/png') {
                            image = await pdfDoc.embedPng(imageBytes);
                        } else {
                            throw new Error('不支持的图片格式，仅支持JPG/PNG');
                        }

                        // 获取图片字段的尺寸和位置
                        const widget = imageField.acroField.getWidgets()[0];
                        const rect = widget.getRectangle();

                        // 将图片设置到图片域中
                        imageField.setImage(image);
                    } catch (error) {
                        console.warn('图片字段处理失败:', error);
                    }
                }

                // 保存PDF
                const pdfBytes = await pdfDoc.save();
                const blob = new Blob([pdfBytes], { type: 'application/pdf' });
                saveAs(blob, `${this.formData.name}_病历报告.pdf`);

            } catch (error) {
                console.error('生成PDF失败:', error);
                this.$message.error('生成PDF失败，请稍后重试');
            }
        },
        async readFileAsArrayBuffer(file) {
            return new Promise((resolve, reject) => {
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
}

.export-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>