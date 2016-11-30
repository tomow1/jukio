<template>
  <button :class="values[value].state ? '' : 'toggle-button-off'" @click="toggle">
    <slot>hello</slot>
  </button>
</template>

<script>
export default {
  data () {
    return {}
  },
  props: ['value', 'values'],
  methods: {
    toggle () {
      var val = this.value + 1
      if (val === this.values.length) val = 0
      this.$emit('input', val)
    }
  }
}
</script>

<style lang="styl">
.toggle-button-off
  opacity 0.5
  color $dark !important

</style>
