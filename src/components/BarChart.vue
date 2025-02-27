<template>
  <div id="chart-container">
    <div id="BarChart" style="flex: 1;"></div>
    <div id="statistics" v-if="statistics" style="flex: 0 0 30%; margin: 20px;">
      <!-- 这里可以添加统计信息 -->
      <h3>统计信息</h3>
      <p>总计: </p>
      <ul>
        <li v-for="(item, index) in seriesNames" :key="index">
          {{ item }}: {{ seriesData[index] ? seriesData[index].reduce((sum, val) => sum + val, 0) : 0 }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
} from "echarts/components";
import { LabelLayout, UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  BarChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer,
  LegendComponent,
]);

export default {
  props: {
    titleText: {
      type: String,
      default: "柱状图示例",
    },
    chartData: {
      type: Array,
      default: () => [],
    },
    xAxisValues: {
      type: Array,
      default: () => [],
    },
    axisTextColor: {
      type: String,
      default: "#6E7079"
    },
    seriesNames: {
      type: Array,
      default: () => [],
    },
    seriesData: {
      type: Array,
      default: () => [],
    },
    gradientColorList: {
      type: Array,
      default: () => [
        [
          { offset: 0, color: "rgba(91, 142, 254, 0.8)" },
          { offset: 1, color: "rgba(71, 122, 254, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(209, 215, 197, 0.8)" },
          { offset: 1, color: "rgba(189, 195, 177, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(151, 122, 192, 0.8)" },
          { offset: 1, color: "rgba(131, 102, 172, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(77, 185, 69, 0.8)" },
          { offset: 1, color: "rgba(77, 165, 69, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(239, 186, 129, 0.8)" },
          { offset: 1, color: "rgba(219, 166, 109, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(189, 85, 251, 0.8)" },
          { offset: 1, color: "rgba(169, 65, 231, 0.1)" },
        ],
        [
          { offset: 0, color: "rgba(155, 187, 211, 0.8)" },
          { offset: 1, color: "rgba(135, 167, 191, 0.1)" },
        ],
      ],
    },
    gradientDirection: {
      type: Object,
      default: () => ({ x: 0, y: 0, x2: 0, y2: 1 }),
    },
    statistics: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      myChart: null,
    };
  },
  mounted() {
    // 初始化 echarts 实例
    this.myChart = echarts.init(document.getElementById("BarChart"));
    // 动态生成 series 配置
    const series = this.seriesNames.map((name, index) => {
      const colorStops =
        this.gradientColorList[index % this.gradientColorList.length];
      return {
        name,
        type: "bar",
        data: this.seriesData[index] || [],
        itemStyle: {
          color: {
            type: "linear",
            ...this.gradientDirection,
            colorStops,
          },
        },
      };
    });
    // 设置图表配置项
    const option = {
      title: {
        text: this.titleText,
        textStyle: {
          color: "rgb(145, 158, 182)",
        },
      },
      tooltip: {},
      legend: {
        data: this.seriesNames,
        bottom: "10px",
        textStyle: {
          color: "rgb(38, 173, 187)",
        },
      },
      xAxis: {
        data: this.xAxisValues,
        axisLabel: {
          color: this.axisTextColor,
        },
      },
      yAxis: {
        axisLabel: {
          color: this.axisTextColor,
        },
        splitLine: {
          lineStyle: {
            color: "rgb(41, 52, 98)",
          },
        },
      },
      series,
    };
    // 应用配置项到图表
    this.myChart.setOption(option);
    // 监听窗口大小变化事件
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    // 组件销毁前移除事件监听
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      if (this.myChart) {
        // 窗口大小改变时，重新调整图表大小
        this.myChart.resize();
      }
    },
  },
};
</script>

<style scoped>
#chart-container {
  display: flex;
  width: 100%;
  height: 100%;
}

#BarChart {
  margin: 20px;
}

#statistics {
  color: rgb(38, 173, 187);
}
</style>