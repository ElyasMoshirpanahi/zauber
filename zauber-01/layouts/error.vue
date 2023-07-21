<template>

<div  style="text-align: center;">
    <NuxtLogo/>
    <div class="error-page">
      
      <div class="message">
        <h1>404</h1>
        <h3>Dang it ! Some error happend !</h3>  
        <p>The page you are looking for could not be found.</p>
        
        <h2><NuxtLink to="/" style="color:deeppink;">🏠🚶🏻‍♂️Go Home</NuxtLink></h2>
      </div>
  
      <div class="image">
        <img src="~/assets/images/404.png" /> 
      </div>

  
    </div>


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