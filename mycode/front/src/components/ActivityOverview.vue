<template>
  <el-container>
    <el-header style="text-align: center; font-size: 12px;top: 30px">
        <h1>活动地图</h1>
      </el-header>
      <el-main direction="horizontal">
      
      <el-container class="container" style="width: 65vw; height: 90vh; left: 220px;">
        <!-- 创建一个容器，用来渲染地图 -->
        <div ref="mapContainer" style="width: 100%; height: 100%;"></div>
      </el-container>
      
      
      <el-container class="container" style="width: 18vw; height: 90vh; right: 10px">
        <el-header style="text-align: center; font-size: 12px">
          <h3>地点详情</h3>
        </el-header>
        <!-- 添加详情内容区域 -->
        <el-main v-if="selectedVenue">
          <el-descriptions :column="1" border  class="transparent-descriptions">
            <el-descriptions-item label="名称">{{ selectedVenue.name }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ selectedVenue.description }}</el-descriptions-item>
            <el-descriptions-item label="城市">{{ selectedVenue.city }}</el-descriptions-item>
            <el-descriptions-item label="区县">{{ selectedVenue.county }}</el-descriptions-item>
            <el-descriptions-item label="街道">{{ selectedVenue.street }}</el-descriptions-item>
            <el-descriptions-item label="电话">{{ selectedVenue.phone }}</el-descriptions-item>
            <el-descriptions-item label="经度">{{ selectedVenue.longitude }}</el-descriptions-item>
            <el-descriptions-item label="纬度">{{ selectedVenue.latitude }}</el-descriptions-item>
          </el-descriptions>
        </el-main>
        <el-main v-else>
          <el-empty description="请点击地图上的地点查看详情" />
        </el-main>
      </el-container>
      
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted, shallowRef,ref } from 'vue';
import {getVenues,getVenueDetail} from '../api/api'
import { ElMessage } from 'element-plus'
const mapContainer = shallowRef(null);
// 文娱活动场所和景区的坐标（假设你有这些数据）
const venues = ref([])
const selectedVenue = ref(null)
// 获取所有场所信息
const fetchVenues = async () => {
  try {
    const response = await getVenues()
    venues.value = response.data.data
    
  } catch (error) {
    console.error('获取场所列表失败:', error)
  }
}

// 获取特定场所详情
const fetchVenueDetail = async (venueId) => {
  try {
    const response = await getVenueDetail({
      venue_id: venueId  
    })
    
    if (response.data && response.data.data) {
      selectedVenue.value = response.data.data
      console.log('获取到的场所详情:', response.data.data)  // 调试信息
    } else {
      console.error('返回数据格式不正确:', response.data)
    }
  } catch (error) {
    console.error('获取场所详情失败:', error.response?.data || error.message)
    selectedVenue.value = null  // 清空当前选中的场所
  }
}

const handlePlaceClick = (place) => {
  ElMessage({message: '你点击了：'+place.name, type: 'success'})
  fetchVenueDetail(place.venue_id)
};
onMounted(async() => {
 await fetchVenues()
  // 确保在DOM挂载后加载高德地图API
  const script = document.createElement('script');
  script.src = `https://webapi.amap.com/maps?v=1.4.15&key=93ba1e6e2659c80338f8e8c4bbfd2354`;  // 替换成你的高德API Key
  script.onload = () => {
    // 初始化地图
    const map = new AMap.Map(mapContainer.value, {
      center: [121.4737, 31.2304],  // 上海的经纬度
      zoom: 17,  // 缩放级别
      pitch: 50,
      rotation: -15,
      viewMode: "3D", //是否为3D地图模式
    });
   // 在地图上添加所有文娱活动场所的标记点
    venues.value.forEach(place => {
      const marker = new AMap.Marker({
        position: new AMap.LngLat(place.longitude, place.latitude),  // 标记点的位置
        title: place.name,  // 提示文字
      });

      // 添加点击事件
      marker.on('click', () => handlePlaceClick(place));

      // 将标记点添加到地图
      marker.setMap(map);
    });
  };
  document.head.appendChild(script);
});
</script>

<style scoped>
.container {
position:fixed;
 
  top: 30px;
  padding: 10px;
  z-index: 2;
  margin: auto;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置边框 */
  border: 1px solid rgba(255, 255, 255, 0.6);
  /* 设置盒子阴影 */
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
  color: white;
    
    justify-content: center;
    gap: 20px;
    border-radius: 10px;
    backdrop-filter: blur(4px);
    background-color: rgba(174,0,255, 0.151);
    box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px;
    border: 4px rgba(255,255,255,0.4) solid;
    border-bottom: 4px rgba(40,40,40,0.35) solid;
    border-right: 4px rgba(40,40,40,0.35) solid;
}
.transparent-descriptions :deep(.el-descriptions__body) {
  background: transparent !important;
}

.transparent-descriptions :deep(.el-descriptions__cell) {
  background: transparent !important;
}

/* 可选：如果想要文字更清晰可见，可以添加文字阴影 */
.transparent-descriptions :deep(.el-descriptions__label),
.transparent-descriptions :deep(.el-descriptions__content) {
  color: rgba(230, 230, 230, 1);
  font-size: 14px;
}
</style>
