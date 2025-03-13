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
  max-width: 100%;     
}
</style> 