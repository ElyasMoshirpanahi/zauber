<template>
  <header class="header">
    <ul class="nav-items">
      <li>
        <nuxt-link to="/">Home</nuxt-link>
      </li>
      <li>
        <nuxt-link to="/textToimage">Text to Image</nuxt-link>
      </li>
      <li>
        <nuxt-link to="/imageToimage">Image to Image</nuxt-link>
      </li>
      <li>
        <nuxt-link to="/controlnetTextToimage">Controlnet Text to Image</nuxt-link>
      </li>
      <li>
        <nuxt-link to="/controlnetImageToimage">Controlnet Image to Image</nuxt-link>
      </li>
    </ul>
  </header>
</template>

<style scoped>
  .header {
    width: 100%;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;  
    background: linear-gradient(90deg, #0064cf, rgb(74 74 255 / 85%), rgba(225,32,32,0.81961));
    box-shadow: 0px 5px 10px #aaa; 
  }

  .nav-items {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80%;
  }



.nav-items li {
  margin: 0 10px;
}

.nav-items a {
  text-decoration: none;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  box-shadow: 0 0 10px #7bff00;
  transition: 0.2s box-shadow;
}

.nav-items a:hover {
  box-shadow: inset 0 0 10px #aaa;
}

  .nav-items a {
    text-decoration: none;
    color: white;
  }

  .nav-items a:hover,
  .nav-items a:active {
    color: hotpink;
  }
</style>

