<template>
 <v-textarea
   v-model="value"
   :label="label"
   :rows="5"
   :counter="200"
 ></v-textarea>
</template>

<script>
export default {
  props: ['value', 'label']  
}
</script>