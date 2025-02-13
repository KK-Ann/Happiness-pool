<template>
  <el-container>
    <el-header style="text-align: center; font-size: 12px">
      <h1>活动列表</h1>
    </el-header>
    <el-main>
      <el-container class="container" style="top: 30px; left: 220px; width: 85vw; height: 230px;">
        

        <el-scrollbar>
          <el-table 
            :data="filteredActivityList" 
            style="width: 75vw; background-color: rgba(255, 255, 255, 0.2) !important;" 
            :header-cell-style="{ 'text-align': 'center' }" 
            :cell-style="{ 'text-align': 'center' }"
            :header-row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.2)' }"
            :row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }"
            @row-click="handleActivityClick">
            <el-table-column prop="name" label="活动名称"  />
            <el-table-column prop="start_time" label="开始时间" sortable />
            <el-table-column prop="end_time" label="结束时间" sortable />
            <el-table-column prop="venue_name" label="活动地点"  />
            <el-table-column prop="registration_channel" label="报名渠道"  />
            <el-table-column prop="type" align="right" width="300">
              <template #header>
                <div class="search-container">
                  <el-input
                    v-model="searchQuery"
                    placeholder="搜索活动名称"
                    class="search-input"
                    clearable
                    @input="handleSearch"
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>                  
                  </el-input>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
      </el-container>
      
      <el-row>
        <el-container class="container" direction="vertical" style="top: 300px; left: 220px; width: 40vw; height: 400px;">
          <el-row style="display: flex; align-items: center; justify-content: center;">
            <h3>{{ currentActivity?.name  || '请选择活动'}}</h3>
          </el-row>
          <el-collapse class="transparent-collapse">
            <el-collapse-item title="活动详情" name="1">
              <el-scrollbar max-height="50px">
                <div>{{currentActivity?.description || '请选择活动查看详情'}}</div>         
              </el-scrollbar>         
            </el-collapse-item>
            <el-collapse-item title="评论" name="2">                  
              <el-scrollbar max-height="120px">
                <div v-for="(comment, index) in comments" :key="index" class="comment-item">
                  <el-row>
                    <el-col :span="4" class="user-col">
                      <div>
                        <p class="user-name">{{ comment.visitor_name }}</p>
                      </div>
                    </el-col>

                    <el-col :span="20" class="comment-col">
                      <p class="comment-content">{{ comment.content }}</p>
                      <p class="comment-time">发布时间：{{ comment.comment_time }}</p>
                    </el-col>
                  </el-row>
                </div>
              </el-scrollbar>
            </el-collapse-item>
          </el-collapse>
          
          <div style="padding: 0px 20px;">
            <el-row>
              <el-col :span="3" style="display: flex; align-items: center; justify-content: center;">
                <p style="color:white; font-size:0.9em; font-weight: bold;">新增评论:</p>
              </el-col>

              <el-col :span="18">
                <el-input v-model="newComment" placeholder="输入评论内容" type="textarea" :autosize="{ minRows: 2, maxRows: 3 }"/>
              </el-col>

              <el-col :span="3" style="display: flex; align-items: center; justify-content: center;">
                <el-button class="btn3" @click="handleAddComment">发布</el-button>
              </el-col>
            </el-row>
          </div>
        </el-container>

        <el-container class="container" direction="vertical" style="top: 300px; right: 2vw; width: 40vw; height: 400px;">
          <el-row style="display: flex; align-items: center; justify-content: center;">
            <h3>{{ currentActivity?.name  || '请选择活动'}}</h3>
          </el-row>
          <el-scrollbar height="300px">
            <div v-for="(partner, index) in partners" :key="index" class="partner-item">
              <el-row>
                <el-col :span="4" class="user-col">
                  <div>
                    <h3>{{ partner.visitor_name }}</h3>
                     <p style="font-size: 0.6em;">{{ partner.email }}</p>
                  </div>
                </el-col>

                <el-col :span="19" class="partner-col">
                  <p class="partner-content">{{ partner.requirement }}</p>
                  <p class="partner-time">发布时间：{{ partner.request_time }}</p>
                </el-col>
                <el-col :span="1" class="user-col">
                  <p class="user-name">{{ partner.is_found? '已找到' : '未找到' }}</p>
                </el-col>
              </el-row>
            </div>
          </el-scrollbar>
          
          <div style="padding: 0px 20px;">
            <el-row>
              <el-col :span="3" style="display: flex; align-items: center; justify-content: center;">
                <p style="color:white; font-size:0.9em; font-weight: bold;">新增搭子请求:</p>
              </el-col>

              <el-col :span="18">
                <el-input v-model="newPartnerRequest" placeholder="输入搭子要求" type="textarea" :autosize="{ minRows: 2, maxRows: 3 }"/>
              </el-col>

              <el-col :span="3" style="display: flex; align-items: center; justify-content: center;">
                <el-button class="btn3" @click="handleAddPartner">发布</el-button>
              </el-col>
            </el-row>
          </div>
        </el-container>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getActivities, getActivityDetail, addComment, addPartner } from '@/api/api'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const activityList = ref([])
const currentActivity = ref(null)
const comments = ref([])
const partners = ref([])
const newComment = ref('')
const newPartnerRequest = ref('')
const searchQuery = ref('')

// 获取活动列表
const fetchActivities = async () => {
  try {
    const response = await getActivities()
    activityList.value = response.data.data
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取活动列表失败')
  }
}

// 获取活动详情
const handleActivityClick = async (row) => {
  
  try {
    const response = await getActivityDetail({
      activity_id: row.activity_id
    })
    currentActivity.value = response.data.data.activity
    comments.value = response.data.data.comments
    partners.value = response.data.data.partners
    console.log(partners.value)
  } catch (error) {
    console.error('获取活动详情失败:', error)
    ElMessage.error('获取活动详情失败')
  }
  ElMessage.success(row.name+'的信息已加载在下方')
}

// 添加评论
const handleAddComment = async () => {
  if (localStorage.getItem('role') !== 'visitor') {
    ElMessage.warning('只有游客可以发布搭子请求')
    return
  }
  if (!currentActivity.value) {
    ElMessage.warning('请先选择活动')
    return
  }
  
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  try {
    console.log(localStorage.getItem('userId'))
    await addComment({
      activity_id: currentActivity.value.activity_id,
      visitor_id: localStorage.getItem('userId'), // 确保已存储用户ID
      content: newComment.value
    })
    
    ElMessage.success('评论发布成功')
    newComment.value = ''
    // 刷新评论列表
    await handleActivityClick(currentActivity.value)
  } catch (error) {
    console.error('发布评论失败:', error)
    ElMessage.error('发布评论失败')
  }
}

// 添加搭子请求
const handleAddPartner = async () => {
  if (localStorage.getItem('role') !== 'visitor') {
    ElMessage.warning('只有游客可以发布搭子请求')
    return
  }
  if (!currentActivity.value) {
    ElMessage.warning('请先选择活动')
    return
  }
  
  if (!newPartnerRequest.value.trim()) {
    ElMessage.warning('请输入搭子要求')
    return
  }

  try {
    const response = await addPartner({
      activity_id: currentActivity.value.activity_id,
      visitor_id: localStorage.getItem('userId'), // 确保已存储用户ID
      content: newPartnerRequest.value
    })
    if(response.data.status === 'success'){
    ElMessage.success('搭子请求发布成功')
    newPartnerRequest.value = ''
    // 刷新搭子请求列表
    await handleActivityClick(currentActivity.value)
    }
    else{
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('发布搭子请求失败:', error)
    ElMessage.error('发布搭子请求失败')
  }
}

// 根据搜索关键词过滤活动列表
const filteredActivityList = computed(() => {
  if (!searchQuery.value) {
    return activityList.value
  }
  return activityList.value.filter(activity => 
    activity.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 处理搜索输入
const handleSearch = () => {
  // 可以在这里添加额外的搜索逻辑
  console.log('搜索关键词:', searchQuery.value)
}

onMounted(() => {
  fetchActivities()
})
</script>

<style scoped>
.container {
position:fixed;
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

.transparent-collapse {
  background: transparent !important;
}

.transparent-collapse :deep(.el-collapse-item__header) {
  background: rgba(255, 255, 255, 0.2) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.transparent-collapse :deep(.el-collapse-item__wrap) {
  background: transparent !important;
  border-bottom: none;
}

.transparent-collapse :deep(.el-collapse-item__content) {
  background: transparent !important;
  padding: 10px;
}

.comment-item, .partner-item {
  margin-bottom: 10px;
  border: 1px solid rgba(189, 200, 162, 0.3);
  border-radius: 4px;
}

.user-col {
  background-color: rgba(227, 153, 253, 0.6);
  padding: 20px 0px;
  display: flex;

}

.comment-col, .partner-col {
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  padding: 10px 20px;
  flex-direction: column;
  justify-content: space-between;
}

.user-name {
  margin: 10px 0 0 0;
  text-align: center;
  font-size: 1em;
}

.comment-content, .partner-content {
  font-size: 0.9em;
  text-align: left;
  margin: 5px 0 10px 0;
  color: #7f9b7e;
}

.comment-time, .partner-time {
  font-size: 0.8em;
  text-align: right;
  color: darkgray;
  margin: 0;
  margin-top: auto;
}

.btn3 {
  background-color: rgba(227, 153, 253, 0.6);
  color: white;
}

.search-container {
  
  width: 15vw;
  display: flex;
  justify-content: flex-start;
}

.search-input {
  width: 300px;
  margin-bottom: 10px;
}

.search-input :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
}

.search-input :deep(.el-input__inner) {
  color: #333;
}

.search-input :deep(.el-input__prefix) {
  color: #666;
}
</style>
