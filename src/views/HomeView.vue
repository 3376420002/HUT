<template>
  <div id="Home">
    <div class="header">
      <span class="logo-text">这里是logo</span>
      <!-- <img src="@/assets/generalIcons/visitor.png" alt="Logo" class="logo"> -->
      <img src="@/assets/generalIcons/visitor.png" alt="User" class="user-icon" @click="goToPersonalInfo">
    </div>
    <div class="toolbar">
      <ul>
        <!-- 使用 v-for 动态生成 li 元素 -->
        <li v-for="(item, index) in toolbarItems" :key="index" :class="{ 'active': $route.path === item.path }">
          <router-link :to="item.path">{{ item.label }}</router-link>
        </li>
      </ul>
    </div>
    <div class="main">
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      // 存储 toolbar 菜单项信息的数组
      toolbarItems: [
        { path: '/analyses', label: 'AI分析' },
        { path: '/case', label: '病例管理' },
        { path: '/dataCharts', label: '病理数据可视化统计' },
        { path: '/userInform', label: '个人信息' }
      ]
    };
  },
  mounted() { },
  methods: {
    goToPersonalInfo() {
      if (this.$route.path !== '/userInform') {
        this.$router.push('/userInform')
      }
    }
  }
};
</script>

<style scoped>
#Home {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 50px);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #1A1F28;
  color: #BAE67E;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 添加阴影，增加立体感 */
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  /* 加粗logo文字 */
  margin-right: 10px;
}

.logo {
  height: 40px;
}

.user-icon {
  height: 30px;
  cursor: pointer;
}

.toolbar {
  height: 40px;
  /* 增加toolbar高度，使内容更舒展 */
  background-color: #212733;
  /* 淡蓝色背景 */
  padding: 0 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #67606F;
  /* 添加底部边框，区分内容区域 */
}

.toolbar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  /* 允许列表项换行 */
}

.toolbar li {
  margin: 0 10px;
}

.toolbar li a {
  text-decoration: none;
  padding: 5px;
  border-radius:5px;
  color: #CCCCCC;
  font-size: 14px;
  font-weight: 500;
  /* 适当加粗文字 */
  transition: color 0.2s ease, background-color 0.2s ease;
  /* 添加过渡效果 */
}

.toolbar li a:hover {
  color: #BAE67E;
  /* 鼠标悬浮时文字变色 */
  background-color: #212733;
  /* 鼠标悬浮时背景色变化 */
}

/* 为选中状态的li设置文字加粗样式 */
.toolbar li.active a {
  color: #BAE67E;
  font-weight: bold;
}

.main {
  flex: 1;
  overflow: auto;
  /* 允许内容滚动 */
  height: calc(100vh - 80px);
  width: 100%;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  /* 添加底部阴影，增加立体感 */
}
</style>