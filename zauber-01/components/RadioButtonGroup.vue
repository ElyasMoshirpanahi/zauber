<template>
 <v-radio-group
    v-model="value"
    :label="label"
    :options="options"
  ></v-radio-group>  
</template>

<script>
export default {
  props: ['value', 'label', 'options']
};
</script>