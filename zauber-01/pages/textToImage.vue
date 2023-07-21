<template>
  <div class="container">
    
    <div v-if="isLoading" class="loading-overlay"></div>
    <h1>Text to Image</h1>

    <form @submit="submitForm" class="my-4">

      <div class="row">

        <div class="col-6">
          <div class="form-group">
            <label for="prompt">Prompt:</label>
            <textarea id="prompt" class="form-control" v-model="form.prompt" required></textarea>
          </div>
        </div>  
        <div class="col-6">
          <div class="form-group">
            <label for="negativePrompt">Negative Prompt:</label>
            <textarea id="negativePrompt" class="form-control" v-model="form.negativePrompt"></textarea>
          </div>
        </div>  
      
      

        <div class="col-6">
          <div class="form-group">
            <label for="width">Width:</label>
            <input id="width" class="form-control small_ins" type="number" v-model.number="form.width" step="8" min="200" max="2048">
          </div>
        </div>

        <div class="col-6">
          <div class="form-group">
            <label for="height">Height:</label>
            <input id="height" class="form-control small_ins" type="number" v-model.number="form.height" step="8" min="200" max="2048">
          </div>
        </div>
      


      

        <div class="col-6">
          <div class="form-group">
            <label for="guidanceScale">Guidance Scale:</label>
            <input id="guidanceScale" class="form-control" type="number"  step="0.5" min="0" max="10"   v-model.number="form.guidanceScale">
          </div>
        </div>
        <div class="col-6">
          <div class="form-group">
            <label for="seed">Seed:</label>
            <input id="seed" class="form-control" type="text" v-model="form.seed">
          </div>
        </div>
      </div> 



       <div class="form-group">
        <label for="numInferenceSteps">Number of Inference Steps: <span class="value">{{ form.numInferenceSteps }}</span></label>

        <div class="range-input">
          <input id="numInferenceSteps" class="form-range" v-model.number="form.numInferenceSteps" type="range" min="1" max="60">
        </div>

      </div>

      <div class="form-group">
        <label>Apply GFPGAN</label>
        <div class="form-check form-switch">
          <input
            v-model.number="form.applyGfpgan"
            onchange="this.form.applyGfpgan =document.getElementById('applyGfpganToggle').checked;"
            type="checkbox"
            id="applyGfpganToggle"
            class="form-check-input"
            data-toggle="toggle"
          >
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
        "prompt": '',
        "negativePrompt": '',
        "width": null,
        "height": null,
        "numInferenceSteps": null,
        "guidanceScale": null,
        "seed": '',
        "applyGfpgan": false,
      },
      errorMessage: '',
      generatedImageBase64: null,
      isOverlayVisible: false,
      isLoading: false,
      imageFiles: []
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

    async submitForm(event) {
      

      //loading  spinner
      this.showLoadingOverlay();
      

      event.preventDefault();

      // Validation before submitting the form
      if (this.form.width && this.form.height && (this.form.width > 2048 || this.form.height > 2048)) {
        this.showMessage('Width and Height cannot exceed 2048.','danger')
        return;
      }

      if (this.form.width % 8 !==0  || this.form.height % 8 !==0) {
        this.showMessage('Width and Height must be diviable by 8 please try again.','danger')
        return;
      }


      // Prepare the data to be sent to the API
      const cleanData = this.cleanFormData(this.form);
      const data = {
        type                : 'text_to_image',
        prompt              : this.form.prompt,
        negative_prompt     : this.form.negativePrompt,
        width               : this.form.width,
        height              : this.form.height,
        num_inference_steps : this.form.numInferenceSteps,
        guidance_scale      : this.form.guidanceScale ? parseFloat(this.form.guidanceScale) : null,
        seed                : this.form.seed ? this.form.seed.split(',').map(num => parseInt(num.trim())) : null,
        apply_gfpgan        : this.form.applyGfpgan == true,
      };
      

      
      //Make API request with the data
      const formData = new FormData();
      formData.append('data', JSON.stringify(data));
      formData.append("input_image",'');
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

<style>
  

  a {
  text-decoration: none;
  color: #ff45d5;
  transition: 0.3s;
}

a:hover {
  color: #fff;
}

#loading-spinner {
  display: none; 
  position: absolute; 
  width:  8rem;
  height: 8rem;
  color: #ff45d5;
  border-bottom: 2px solid darkblue;
  border-radius: 50%;
  top: 45%; left: 45%; 
  box-shadow: 0 0 20px 1px #ff45d5, 0 0 20px 1px #002bff; 
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
  .form-group{
    margin:1% auto;
  }
  .container {
      border-radius: 30px;
      max-width: 30%;
      margin: 4% auto;
      padding: 20px;
      box-shadow: 0px 0px 17px 2px #34a2c3;
  }

  .range-input {
    position: relative;
  }

  .range-input .value {
    position: absolute;
    top: -2rem;
  }

  .range-input:hover .value {
    display: inline-block;
  }

  .range-input .value {
    display: none;
  }

  .small_ins{
    width: 30%;
  }
  .error-message {
    color: red;
    margin-top: 1rem;
  }


  .overlay {
  position: fixed;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 15, 38, 0.8);

  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay img {
  max-width: 80%;
  max-height: 80%;
}


.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 15, 38, 0.8);
  
  display: flex;
  align-items: center;
  justify-content: center; 
}
</style>
