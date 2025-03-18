<template>
  <div id="chart-container">
    <div id="BarChart"></div>
    <div id="statistics" v-if="statistics" style="flex: 0 0 30%; margin: 20px 20px 0 0;">
      <!-- <h3>统计信息</h3> -->
      <div class="button-group">
        <button v-for="(button, index) in statisticButtons" :key="index"
          :class="{ active: currentStatistics === button.type }" @click="showStatistics(button.type)"
          @mouseenter="showTooltip(button.label, $event)" @mouseleave="hideTooltip" @mousemove="moveTooltip($event)">
          {{ button.label }}
        </button>
        <div v-if="isTooltipVisible" class="tooltip" :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }">
          {{ tooltipContent }}
        </div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th v-if="currentStatistics === 'diseaseTotal' || currentStatistics === 'diseasePercentage'">疾病</th>
              <th v-if="currentStatistics === 'ageGroupTotal'">年龄段</th>
              <th
                v-if="currentStatistics === 'diseaseTotal' || currentStatistics === 'ageGroupTotal' || currentStatistics === 'totalCount'">
                数量（例）</th>
              <th v-if="currentStatistics === 'diseasePercentage'">占比（%）</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="currentStatistics === 'diseaseTotal' || currentStatistics === 'diseasePercentage'">
              <tr v-for="(item, index) in seriesNames" :key="index">
                <td>{{ item }}</td>
                <td v-if="currentStatistics === 'diseaseTotal'">{{seriesData[index] ? seriesData[index].reduce((sum,
                  val) => sum + val, 0) : 0}}</td>
                <td v-if="currentStatistics === 'diseasePercentage'">{{ getDiseasePercentage(index) }}</td>
              </tr>
            </template>
            <template v-if="currentStatistics === 'ageGroupTotal'">
              <tr v-for="(ageGroup, index) in xAxisValues" :key="index">
                <td>{{ ageGroup }}</td>
                <td>{{ getAgeGroupTotal(index) }}</td>
              </tr>
            </template>
            <tr v-if="currentStatistics === 'totalCount'">
              <td>所有疾病总患病数</td>
              <td>{{ getTotalCount() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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
      currentStatistics: 'diseaseTotal',
      statisticButtons: [
        { type: 'diseaseTotal', label: '各疾病总计' },
        { type: 'ageGroupTotal', label: '年龄段总患病数' },
        { type: 'totalCount', label: '总患病数' },
        { type: 'diseasePercentage', label: '占比' }
      ],
      isTooltipVisible: false,
      tooltipContent: '',
      tooltipX: 0,
      tooltipY: 0
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
    getAgeGroupTotal(index) {
      let total = 0;
      this.seriesData.forEach((data) => {
        if (data[index]) {
          total += data[index];
        }
      });
      return total;
    },
    getTotalCount() {
      let total = 0;
      this.seriesData.forEach((data) => {
        total += data.reduce((sum, val) => sum + val, 0);
      });
      return total;
    },
    getDiseasePercentage(index) {
      const diseaseTotal = this.seriesData[index]
        ? this.seriesData[index].reduce((sum, val) => sum + val, 0)
        : 0;
      const totalCount = this.getTotalCount();
      return totalCount > 0 ? ((diseaseTotal / totalCount) * 100).toFixed(2) : 0;
    },
    showStatistics(type) {
      this.currentStatistics = type;
    },
    showTooltip(content, event) {
      this.isTooltipVisible = true;
      this.tooltipContent = content;
      this.moveTooltip(event);
    },
    hideTooltip() {
      this.isTooltipVisible = false;
    },
    moveTooltip(event) {
      this.tooltipX = event.pageX + 10;
      this.tooltipY = event.pageY + 10;
    }
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
  width: 80%;
  margin: 20px 0 10px 20px;
  overflow: hidden;
}

#statistics {
  width: 20%;
  color: rgb(38, 173, 187);
}

.button-group {
  width: 100%;
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top:20px;
  margin-bottom: 10px;
}

.button-group button {
  padding: 5px 10px;
  background-color: #e0ecff;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  white-space: nowrap;
  /* 禁止文字换行 */
  overflow: hidden;
  /* 隐藏超出部分 */
  text-overflow: ellipsis;
}

.button-group button.active {
  background-color: #0056b3;
  color: white;
}

.tooltip {
  position: absolute;
  background-color: rgba(255, 255, 255);
  border: 1px solid #ccc;
  color:black;
  border-radius: 4px;
  font-size:12px;
  padding: 5px;
  z-index: 100;
  pointer-events: none;
}

.table-container {
  height: calc(100% - 20px);
  width: 100%;
  /* 固定表格区域高度 */
  overflow-y: auto;
  /* 超出高度显示滚动条 */
}

table {
  border-collapse: collapse;
  table-layout: fixed;
  /* 固定表格布局，便于控制宽度 */
}

table th,
table td {
  border: 1px solid #ccc;
  padding: 2px 4px;
  /* 进一步减少单元格内边距，使表格更紧凑 */
  text-align: center;
  white-space: nowrap;
  /* 防止文本换行 */
  font-size: 13px;
  /* 减小字体大小 */
  overflow: hidden;
  text-overflow: ellipsis;
  /* 超出内容显示省略号 */
}

table th {
  width: auto;
  /* 自动调整表头宽度 */
}

/* 可以根据需要调整表格整体宽度 */
.table-container table {
  width: 90%;
  /* 让表格宽度变小 */
  margin: 0 auto;
  /* 居中显示 */
}
</style>