<template>
  <div id="statistic">
    <div class="top">
      <div class="line">
        <LineChart
          :titleText="LineChartTitle"
          :chartData="LineChartData"
          :xAxisValues="LineXAxisValues"
          :isGradient="isGradient"
          :colors="LineGradientColors"
          :axisTextColor="axisTextColor"
        />
      </div>
      <div class="pie">
        <PieChart
          :titleText="PieChartTitle"
          :chartData="PieChartData"
          :names="BarSeriesNames"
          :labelColor="axisTextColor"
        />
      </div>
    </div>
    <div class="bottom">
      <BarChart
        :titleText="BarChartTitle"
        :seriesNames="BarSeriesNames"
        :seriesData="BarSeriesData"
        :xAxisValues="BarXAxisValues"
        :axisTextColor="axisTextColor"
      ></BarChart>
    </div>
  </div>
</template>

<script>
import BarChart from "@/components/BarChart.vue";
import LineChart from "@/components/LineChart.vue";
import PieChart from "@/components/PieChart.vue";
export default {
  components: {
    BarChart,
    LineChart,
    PieChart,
  },
  data() {
    return {
      LineChartTitle: "不同月份的患者数量",
      LineChartData: [
        450, 250, 155, 348, 192, 687, 485, 665, 985, 475, 342, 258,
      ],
      isGradient: true,
      LineGradientColors: ["rgb(30, 114, 119)", "rgba(0, 123, 255,0.1)"],
      LineXAxisValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      PieChartTitle:"不同疾病占比情况",
      PieChartData:[485,159,644,542,387,194,674],
      BarChartTitle: "不同年龄段的患病情况",
      BarSeriesNames: [
        "糖尿病",
        "青光眼",
        "白内障",
        "AMD",
        "高血压",
        "近视",
        "其他疾病或异常",
      ],
      BarSeriesData: [
        [12, 25, 30, 18, 22, 28],
        [8, 15, 20, 12, 16, 22],
        [2, 10, 22, 37, 18, 32],
        [15, 27, 44, 25, 25, 44],
        [26, 36, 47, 29, 14, 17],
        [9, 18, 18, 18, 29, 9],
        [44, 15, 9, 37, 36, 23],
      ],
      BarXAxisValues: [
        "0~9岁",
        "10~19岁",
        "20~34岁",
        "35~49岁",
        "50~64岁",
        "65岁及以上",
      ],
      axisTextColor: "rgb(38, 173, 187)",
    };
  },
  mounted() {},
  methods: {},
};
</script>

<style scoped>
#statistic {
  height: 100%;
  background-color: rgb(26, 43, 90);
}

.top {
  height: 50%;
  display: flex;
}

.line {
  width: 55%;
  margin: 15px 15px 0px 15px;
  border: 2px solid rgb(25, 55, 95);
  background-color: rgb(1, 20, 97);
}

.pie {
  width: 45%;
  margin: 15px 15px 0px 0px;
  border: 2px solid rgb(25, 55, 95);
  background-color: rgb(1, 20, 97);
  display:flex;
  align-items:center;
  justify-content: center;
}

.bottom {
  margin: 15px;
  border: 2px solid rgb(25, 55, 95);
  height: 45%;
  background-color: rgb(1, 20, 97);
}
</style>