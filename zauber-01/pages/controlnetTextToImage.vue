<template>
  <div class="container">
    <h1>Controlnet Text to Image</h1>
    <div v-if="isLoading" class="loading-overlay"></div>
    <form @submit="submitForm" class="my-4">
      <div class="row">
        <div class="form-group col-6">
          <label for="prompt">Prompt:</label>
          <textarea id="prompt" class="form-control" v-model="form.prompt" required></textarea>
        </div>



        <div class="form-group col-6">
          <label for="negativePrompt">Negative Prompt:</label>
          <textarea id="negativePrompt" class="form-control" v-model="form.negativePrompt"></textarea>
        </div>
        


        <div class="form-group col-6">
          <label for="width">Width:</label>
          <input id="width"  class="form-control small_ins" type="number" v-model.number="form.width" step="8"  min="200" max="2048">
        </div>

        <div class="form-group col-6">
          <label for="height">Height:</label>
          <input id="height" class="form-control small_ins" type="number" v-model.number="form.height" step="8" min="200" max="2048">
        </div>



        <div class="form-group col-6">
          <label for="guidanceScale">Guidance Scale:</label>
          <input id="guidanceScale" class="form-control" type="number"  step="0.5" min="0" max="10"  v-model.number="form.guidanceScale">
        </div>

        <div class="form-group col-6">
          <label for="controlnetConditioningScale">Controlnet Conditioning Scale:</label>
          <input id="controlnetConditioningScale" class="form-control" type="number" step="0.01" min="0.0" max="10.0"    v-model.number="form.controlnetConditioningScale" required>
        </div>

        <div class="form-group col-6">
          <label for="seed">Seed:</label>
          <input id="seed" class="form-control" type="text" v-model="form.seed">
        </div>


        <div class="form-group col-6" required>
          <label for="conditioningImage">Conditioning Image:</label>
          <input id="conditioningImage" class="form-control" type="file" accept="image/*" ref="conditioningImage" required>
        </div>
      </div>

      <div class="form-group col-12">
        <label for="preprocessor">Preprocessor:</label>
        <select id="preprocessor" class="form-control" v-model="form.preprocessor" required>
          <option value="null" selected>None</option>
          <option value="canny">Canny</option>
          <option value="scribble">Scribble</option>
        </select>
      </div>

      <div class="form-group" v-if="form.preprocessor === 'canny'">

        <div class="form-group">
          <label>Low Threshold</label>  
          <input class="form-control small_ins" v-model="form.cannyLow" step="1" min="0" max="10" type="number">
        </div>

        <div class="form-group">
          <label>High Threshold</label>
          <input class="form-control small_ins" v-model="form.cannyHigh" step="1" min="0" max="10"  type="number"> 
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
            <input
              v-model.number="form.applyGfpgan"
              onchange="this.form.applyGfpgan = document.getElementById('applyGfpganToggle').checked"
              type="checkbox"
              id="applyGfpganToggle"
              class="form-check-input"
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
        prompt: '',
        preprocessor: null,
        negativePrompt: '',
        width: null,
        height: null,
        numInferenceSteps: null,
        guidanceScale: null,
        controlnetConditioningScale: null,
        seed: '',
        applyGfpgan: null,
        cannyLow: null, // Add cannyLow and cannyHigh to the data object
        cannyHigh: null,
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
    

      // Validation before submitting the form
      const conditioningImage = this.$refs.conditioningImage.files[0];
      if (!conditioningImage) {
        this.errorMessage = 'Please select an conditioning Image.';
        return;
      }


      if (this.form.width && this.form.height && (this.form.width > 2048 || this.form.height > 2048)) {
        this.showMessage('Width and Height cannot exceed 2048.','danger')
        return;
      }

      if (this.form.width % 8 !==0  || this.form.height % 8 !==0) {
        this.showMessage('Width and Height must be diviable by 8 please try again.','danger')
        return;
      }
      if (this.controlnetConditioningScale % controlnetConditioningScale == 0){
        this.showMessage('controlnet Conditioning Scale must be a float number not a total integer, please try again.','danger')
        return;

      
      }
      if (this.controlnetConditioningScale == 0){
        this.showMessage('controlnet Conditioning Scale must be a float number not Zero, please try again.','danger')
        return;

      }


      // Prepare the data to be sent to the API


      let preprocessorProperties = null;


      if (this.form.preprocessor === 'canny') {
        preprocessorProperties = {
          type: 'canny',
          low_threshold:  this.form.cannyLow   ? parseInt(this.form.cannyLow) :0,
          high_threshold: this.form.cannyHigh  ? parseInt(this.form.cannyHigh):0,
        };
      } else if (this.form.preprocessor === 'scribble') {
        preprocessorProperties = {
          type: 'scribble',
        };
      }

      const data = {
        type                              : 'controlnet_text_to_image',
        prompt                            : this.form.prompt,
        preprocessor                      : preprocessorProperties,
        negative_prompt                   : this.form.negativePrompt,
        width                             : this.form.width,
        height                            : this.form.height,
        num_inference_steps               : this.form.numInferenceSteps,
        guidance_scale                    : this.form.guidanceScale ? parseFloat(this.form.guidanceScale) : null,
        controlnet_conditioning_scale     : this.form.controlnetConditioningScale ? parseFloat(this.form.controlnetConditioningScale): null,
        seed                              : this.form.seed ? this.form.seed.split(',').map(num => parseInt(num.trim())) : null,
        apply_gfpgan                      : this.form.applyGfpgan == true,
      };

      // TODO: Make API request with the data

      console.log(data);
      console.log(conditioningImage);

      //converting image to base64 String
      const base64_img = await this.getBase64(conditioningImage);
      this.base64 = base64_img;
      console.log(`Conditioning image convert to base64:   ${this.base64 }`)

      //Make API request with the data
      const formData = new FormData();
      formData.append('data', JSON.stringify(data));
      formData.append("input_image",'');
      formData.append("conditioning_image",this.base64);

      
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


<style scoped>
.form-card {
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.error-message {
  color: red;
  margin-top: 1rem;
}

/* Responsive styles */
@media (max-width: 600px) {
  .form-card {
    width: 100%;
  }
}
</style>
