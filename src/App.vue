<template>
  <div id="app">
    <test-form />
  </div>
</template>

<script>
import TestForm from './components/TestForm.vue';

export default {
  name: 'App',
  components: {
    TestForm
  },
};
</script>

<style>
#app {
  padding: 20px;        
  max-width: 800px;     
  margin: 0 auto;       
  box-sizing: border-box;
}
</style> 