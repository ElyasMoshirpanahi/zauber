<template>
  <section class="container">
    <div class="card">
      <div class="card-body">
        
        <nuxt-link to="/textToimage" >
          <h2 class="emoji" role="img" aria-label="Text to Image">💬 ➡️ 🖼️</h2>
          <h5 class="card-title">Text to Image</h5>
        </nuxt-link>
      </div>
    </div>

    <div class="card">
      <div class="card-body">

        <nuxt-link to="/imageToimage">
          <h2 class="emoji" role="img" aria-label="Image to Image">🖼️ ➡️ 🖼️</h2>
          <h5 class="card-title">Image to Image</h5>
        </nuxt-link>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <nuxt-link to="/controlnetTextToimage">
        <h2 class="emoji" role="img" aria-label="Controlnet Text to Image">🤖 ➡️ 💬</h2>
        <h5 class="card-title">Controlnet Text to Image</h5>
        
        </nuxt-link>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <nuxt-link to="/controlnetImageToimage">
        <h2 class="emoji" role="img" aria-label="Controlnet Text to Image">🤖 ➡️ 💬</h2>
        <h5 class="card-title">Controlnet Text to Image</h5>
        

        </nuxt-link>
      </div>
    </div>
  </section>
</template>

<script>
export default {};
</script>

<style>
.cards-container {
  margin-top: 2rem;
}

.card {
  margin: 2% auto;
  text-align: center;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  width: 100%;
}

.card:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.1) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.1) 75%,
    transparent 75%,
    transparent 100%
  );
  background-size: 8px 8px;
  pointer-events: none;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow:0 8px 16px rgba(0, 0, 0, 0.2), 0px 7px 9px 0px rgb(244 75 255 / 60%);
}
</style>
