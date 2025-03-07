import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';//这是element-ui的样式，必须引入，否则会报错

// 全局注册ElementUI组件
Vue.use(ElementUI);
new Vue({
  // 使用render函数渲染根组件App
  render: h => h(App)
}).$mount('#app') // 挂载