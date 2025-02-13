<template>
<div class="background--custom">
    <canvas id="canvas" />
  </div>
  <el-container direction="horizontal" style="width: 100%; height: 100%;">
    <NavBar></NavBar>
    <router-view></router-view>
    
  </el-container>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue"
import { onMounted } from 'vue'

onMounted(() => {
  const loadGradient = () => {
    try {
      const gradient = new Gradient()
      gradient.initGradient("#canvas")
    } catch (error) {
      console.error('Gradient initialization failed:', error)
    }
  }

  if (window.Gradient) {
    loadGradient()
    return
  }

  const script = document.createElement('script')
  script.src = "https://cdn.jsdelivr.net/gh/greentfrapp/pocoloco@minigl/minigl.js"
  script.onload = loadGradient
  document.body.appendChild(script)
})
</script>

<style scoped>
.page-body {
  display: flex;
}
.background--custom {
  background-color: #FFFFFF;
  width: 100vw;
  height: 100vh;
  position: fixed;

  z-index: -2;
  top: 0;
  left: 0;
}

canvas#canvas {
  z-index: -1;
  position: fixed;
  width: 100%;
  height: 100%;
  transform: rotate(0deg) scale(2) translateY(0%);
  --gradient-color-1: #E39AC5;
  --gradient-color-2: #6ec3f4;
  --gradient-color-3: #875EF0;
  --gradient-color-4: #EAD781;
  --gradient-speed: 0.000006;
}
</style>
