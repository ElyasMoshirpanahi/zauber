<template>
  <div class="container">
    <div v-if="isLoading" class="loading-overlay"></div>
    <h1>Image to Image</h1>
    <form @submit="submitForm" class="my-4" enctype="multipart/form-data">
      <div class="row">
        <div class="form-group col-6">
          <label for="prompt">Prompt:</label>
          <textarea id="prompt" class="form-control" type="text" v-model="form.prompt" required></textarea>
        </div>



        <div class="form-group col-6">
          <label for="negativePrompt">Negative Prompt:</label>
          <textarea id="negativePrompt" class="form-control" v-model="form.negativePrompt"></textarea>
        </div>


        <div class="form-group col-6">
          <label for="strength">Strength:</label>
          <input id="strength" class="form-control" type="number" v-model.number="form.strength" step="0.05" min="0" max="1" required>
        </div>

        <div class="form-group col-6">
          <label for="guidanceScale">Guidance Scale:</label>
          <input id="guidanceScale" class="form-control" type="number"  step="0.5" min="0" max="10"   v-model.number="form.guidanceScale">
        </div>

        <div class="form-group col-6">
          <label for="seed">Seed:</label>
          <input id="seed" class="form-control" type="text" v-model="form.seed">
        </div>
        
        <div class="form-group col-6">
          <label for="inputImage">Input Image:</label>
          <input id="inputImage" class="form-control" type="file" accept="image/*" ref="inputImage" required>
        </div>

      </div>

      <div class="form-group">
        <label for="numInferenceSteps">Number of Inference Steps: <span class="value">{{ form.numInferenceSteps }}</span></label>

        <div class="range-input">
          <input id="numInferenceSteps" class="form-range" v-model.number="form.numInferenceSteps" type="range" min="1" max="60">
        </div>

      </div>

      <div class="form-group">
        <label>Apply GFPGAN:</label>
        <div class="form-check form-switch">
          <input v-model.number="form.applyGfpgan" onchange="this.form.applyGfpgan = document.getElementById('applyGfpganToggle').checked" type="checkbox" id="applyGfpganToggle" class="form-check-input">
        </div>
      </div>

        <button type="submit" class="btn btn-primary">Submit</button>

    </form>

    <img 
      v-if="generatedImageBase64" 
      :src="generatedImageBase64"
      width="150"
      height="150"
      @click="showOverlay"

      style="border-radius: 25px;"
    >

    <div v-if="isOverlayVisible" class="overlay"  @click="closeOverlay">
      <img :src="generatedImageBase64">
    </div>
    <!-- <img v-for="file in imageFiles" :key="file" :src="'/output/' + file"> -->
    
    <div v-if="errorMessage" :class="['alert', 'alert-' + errorType]">
      {{ errorMessage }}
    </div>

    <div class="spinner-border" id="loading-spinner" role="status"></div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        prompt: '',
        strength: null,
        negativePrompt: '',
        numInferenceSteps: null,
        guidanceScale: null,
        seed: '',
        applyGfpgan: false,
      },      
      errorMessage: '',
      generatedImageBase64: null,
      isOverlayVisible: false,
      isLoading: false,
      imageFiles: [],
      base64:'',
    };
  },
  methods: {
    cleanFormData(data) {
      // Helper function to remove null, undefined, and empty string properties from an object
      return Object.fromEntries(Object.entries(data).filter(([_, v]) => v !== null && v !== undefined && v !== ''));
    },

    showMessage(message, type) {
      this.errorMessage = message;
      this.errorType = type;

      setTimeout(() => {
        this.errorMessage = '';
        this.errorType    = '';
      }, 3000); 
    },

    showOverlay() {
      this.isOverlayVisible = true;
    },
    closeOverlay() {
      this.isOverlayVisible = false;
    },

    showLoadingOverlay() {
      this.isLoading = true;
      document.getElementById("loading-spinner").style.display= "block";
    },
    closeLoadingOverlay() {
      this.isLoading = false;
      document.getElementById("loading-spinner").style.display= "none";
    },
    getBase64(file) {
      return new Promise(resolve => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          resolve(reader.result); 
        };
      })
    },

    async submitForm(event) {



      //loading  spinner
      this.showLoadingOverlay();
      
      event.preventDefault();
      const inputImage = this.$refs.inputImage.files[0];

      if (!inputImage) {
        this.showMessage( 'Please select an input image.','danger');
        return;
      }

      // Prepare the data to be sent to the API
      const cleanData = this.cleanFormData(this.form);
      const data = {
        type                : 'image_to_image',
        prompt              : this.form.prompt,
        strength            : this.form.strength ? parseFloat(this.form.strength) : null,
        negative_prompt     : this.form.negativePrompt,
        num_inference_steps : this.form.numInferenceSteps,
        guidance_scale      : this.form.guidanceScale ? parseFloat(this.form.guidanceScale) : null,
        seed                : this.form.seed ? this.form.seed.split(',').map(num => parseInt(num.trim())) : null,
        apply_gfpgan        : this.form.applyGfpgan == true,
      };



      // TODO: Make API request with the formData
      console.log(data);
      console.log(inputImage);

      //converting image to base64 String
      const base64_img = await this.getBase64(inputImage);
      this.base64 = base64_img;
      
      // console.log(`base64 image is :  ${this.base64}`)
      
      //Make API request with the data
      const formData = new FormData();
      formData.append('data', JSON.stringify(data));
      formData.append("input_image",this.base64);
      formData.append("conditioning_image",'');

      try {
        const response = await fetch('http://localhost:7071/api/Http_API_Trigger', {

          method: 'POST',
          body: formData,

          mode: 'cors'
        });

        const imageBase64 = await response.text();
        // Decode base64 data 
        const imageData = atob(imageBase64);

        // Convert to ArrayBuffer
        const arrayBuffer = Uint8Array.from(imageData, c => c.charCodeAt(0));

        // Create blob
        const blob = new Blob([arrayBuffer], {type: 'image/png'});

        // Generate filename
        const fileName = `${data.type}_${Date.now()}.png`;

        const outputFolder = 'output';
        // Get folder to save to in project
        const img_path = `${outputFolder}/${data.type}/${fileName}`; 

        
        
        console.log(`Image path is :${img_path}`);

        // Create URL for saving file
        const url = URL.createObjectURL(blob);

        // Create a link to click to save file
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName; 
        link.click(); 


        this.imageFiles.push(img_path);
        // Revoke object URL
        URL.revokeObjectURL(url);


        if (response.ok){
          // Handle the case where the API request was  successful
          this.showMessage('Success', 'success');
          this.generatedImageBase64 =  `data:image/png;base64, ${imageBase64}` ;
          //console.log(`Generated Base 64 image is : ${this.generatedImageBase64}`)

        } else if (!response.ok) {
          // Handle the case where the API request was not successful
          this.showMessage('Error occurred while processing the request.', 'danger'); 
          return;
        }

        // Handle the response data and display the generated image in your frontend
        // For example, you can store the image URL in your component's data and display it in your template
        // this.generatedImageUrl = responseData.imageUrl;
      } catch (error) {
        // Handle any errors that occurred during the API request
        error = 'An error occurred while communicating with the server.' + error;
        this.showMessage(error, 'danger');
      };


      //Hiding the spinner
      this.closeLoadingOverlay();




    },
  },
};
</script>
