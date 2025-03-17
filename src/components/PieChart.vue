<template>
  <div id="pieChart">
    <div id="PieChart" style="width: calc(100% - 40px); height: calc(100% - 40px)"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
export default {
  props: {
    titleText: {
      type: String,
      default: "饼状图示例",
    },
    // 接收父组件传递的数据
    chartData: {
      type: Array,
      default: () => [],
    },
    // 接收父组件传递的横坐标值
    names: {
      type: Array,
      default: () => [],
    },
    labelColor: {
      type: String,
      default: "#6E7079"
    },
    colorList: {
      type: Array,
      default: () => [
        "rgba(91, 142, 254,0.7)",
        "rgba(209, 215, 197,0.7)",
        "rgba(151, 122, 192,0.7)",
        "rgba(77, 185, 69,0.7)",
        "rgba(239, 186, 129,0.7)",
        "rgba(189, 85, 251,0.7)",
        "rgba(155, 187, 211,0.7)"
      ]
    },
    gradientColorList: {
      type: Array,
      default: () => [
        [
          { offset: 0, color: "rgba(91, 142, 254, 1)" },
          { offset: 1, color: "rgba(71, 122, 254, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(209, 215, 197, 1)" },
          { offset: 1, color: "rgba(189, 195, 177, 0)" },
        ],
        [
          { offset: 0, color: "rgba(151, 122, 192, 1)" },
          { offset: 1, color: "rgba(131, 102, 172, 0)" },
        ],
        [
          { offset: 0, color: "rgba(77, 185, 69, 1)" },
          { offset: 1, color: "rgba(77, 165, 69, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(239, 186, 129, 1)" },
          { offset: 1, color: "rgba(219, 166, 109, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(189, 85, 251, 1)" },
          { offset: 1, color: "rgba(169, 65, 231, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(155, 187, 211,1)" },
          { offset: 1, color: "rgba(135, 167, 191, 0.1)" },
        ],
      ],
    },
  },
  data() {
    return {
      myChart: null,
    };
  },
  mounted() {
    this.renderPieChart();
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
    if (this.myChart) {
      this.myChart.dispose();
    }
  },
  methods: {
    renderPieChart() {
      const chartDom = document.getElementById("PieChart");
      this.myChart = echarts.init(chartDom);

      const formattedData = this.names.map((name, index) => ({
        value: this.chartData[index],
        name: name,
      }));

      const option = {
        title: {
          text: this.titleText,
          left: "center",
          textStyle: {
            color: "rgb(145, 158, 182)",
          },
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: 'vertical', // 垂直布局
          left: 'right', // 位于图表右侧
          top: 'center', // 垂直居中
          textStyle: {
            color: 'rgb(145, 158, 182)' // 图例文字颜色
          }
        },
        series: [
          {
            name: "数据",
            type: "pie",
            radius: "70%",
            center: ['30%', '50%'], // 设置饼图中心位置，让饼图居左
            color: this.colorList,
            data: formattedData,
            label: {
              color: this.labelColor,
              show: false
            },
            labelLine: {
              show: false // 隐藏引导线
            },
            itemStyle: {
              borderColor: this.labelColor, // 边框颜色，这里设置为白色
              borderWidth: 2 // 边框宽度，单位为像素
            }
          },
        ],
      };

      this.myChart.setOption(option);
    },
    handleResize() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
  },
};
</script>

<style scoped>
#pieChart {
  width: 80%;
  height: 100%;
}

#PieChart {
  margin: 20px;
}
</style>