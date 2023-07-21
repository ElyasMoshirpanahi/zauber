<template>
  <div>
    <Header />
    <nuxt/>
  </div>
</template>

<script>
import Header from '@/components/Header'

export default {
  components: {
    Header
  }
}
</script>


<style>
body {
  background: linear-gradient(261deg, #0064cf, rgb(74 74 255 / 85%), rgba(225,32,32,0.81961));
  color: #fff;
  font-family: 'Arial', sans-serif;
  }
</style>
