<template>
  <el-container>
    <el-header style="text-align: center; font-size: 12px">
      <h1>个人主页</h1>
    </el-header>
    <el-main>
      <el-container class="container" style="top: 40px; left: 250px; width: 80vw; height: 70vh;">
        <el-scrollbar>
          <!-- Visitor 的搭子请求表格 -->
          <el-table v-if="userType === 'visitor'" 
          :data="visitorData"           
          style="width: 75vw; background-color: rgba(255, 255, 255, 0.2) !important;" 
            :header-cell-style="{ 'text-align': 'center' }" 
            :cell-style="{ 'text-align': 'center' }"
            :header-row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.2)' }"
            :row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }"
            >
            <el-table-column prop="activity_name" label="活动名称"  />
            <el-table-column prop="buddy_requirement" label="搭子要求"  />
            <el-table-column prop="request_time" label="发布时间"  />
            <el-table-column  label="操作" width="180">
              <template #default="scope">
                <el-switch v-model="scope.row.is_found" 
                class="ml-2"
                size="large"
                @change="handleBuddyFound(scope.row)"
                inline-prompt
                style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                active-text="已找到" inactive-text="寻找中" />
              
                <el-button type="danger" 
                @click="handleBuddyDelete(scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Organizer 的活动表格 -->
          <el-table v-if="userType === 'organizer'" 
          :data="organizerData" 
          style="width: 75vw; background-color: rgba(255, 255, 255, 0.2) !important;" 
            :header-cell-style="{ 'text-align': 'center' }" 
            :cell-style="{ 'text-align': 'center' }"
            :header-row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.2)' }"
            :row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }"
            >
            <el-table-column prop="name" label="活动名称" width="180" />
            <el-table-column prop="type" label="活动类型" width="120" />
            <el-table-column prop="start_time" label="开始时间" width="180" />
            <el-table-column prop="end_time" label="结束时间" width="180" />
            <el-table-column prop="flow" label="预计人流量" width="100" />
            <el-table-column prop="venue" label="场所" width="180" />
            <el-table-column >
              <template #header>
                <el-button size="small" type="success" @click="handleAddActivity()">增加活动</el-button>
              </template>
              <template #default="scope">
                <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Manager 的组织者管理表格 -->
          <el-table v-if="userType === 'manager'" 
          :data="managerData" 
          style="width: 75vw; background-color: rgba(255, 255, 255, 0.2) !important;" 
            :header-cell-style="{ 'text-align': 'center' }" 
            :cell-style="{ 'text-align': 'center' }"
            :header-row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.2)' }"
            :row-style="{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }"
            >
            <el-table-column prop="name" label="组织者名称" width="180" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="compliance_status" label="合规状态">
              <template #default="scope">
                <el-tag :type="scope.row.compliance_status ? 'success' : 'danger'">
                  {{ scope.row.compliance_status ? '合规' : '不合规' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="small" 
                  :type="scope.row.compliance_status ? 'danger' : 'success'"
                  @click="handleComplianceChange(scope.row)"
                >
                  {{ scope.row.compliance_status ? '设为不合规' : '设为合规' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
      </el-container>
    </el-main>
  </el-container>

  <!-- 编辑活动对话框 -->
  <el-dialog
    v-model="editDialogVisible"
    title="编辑活动"
    width="50%"
    :close-on-click-modal="false"
  >
    <el-form :model="editForm" label-width="120px">
      <el-form-item label="活动名称">
        <el-input v-model="editForm.name" />
      </el-form-item>
      <el-form-item label="活动类型">
        <el-select v-model="editForm.type" placeholder="请选择活动类型">
          <el-option label="文化类" value="文化类" />
          <el-option label="体育类" value="体育类" />
          <el-option label="娱乐类" value="娱乐类" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始时间">
        <el-date-picker
          v-model="editForm.start_time"
          type="datetime"
          placeholder="选择开始时间"
          format="YYYY-MM-DD HH:mm:ss"
        />
      </el-form-item>
      <el-form-item label="结束时间">
        <el-date-picker
          v-model="editForm.end_time"
          type="datetime"
          placeholder="选择结束时间"
          format="YYYY-MM-DD HH:mm:ss"
        />
      </el-form-item>
      <el-form-item label="预计人流量">
        <el-input-number v-model="editForm.flow" :min="0" />
      </el-form-item>
      <el-form-item label="活动描述">
        <el-input
          v-model="editForm.description"
          type="textarea"
          :rows="3"
        />
      </el-form-item>
      <el-form-item label="场地">
        <el-select v-model="editForm.venue_id" placeholder="请选择场地">
          <el-option
            v-for="venue in venues"
            :key="venue.venue_id"
            :label="venue.name"
            :value="venue.venue_id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEditSubmit">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getVenues,getPartners, changePartnerStatus, deletePartner, 
getOrganizerActivities,editActivity,addActivity,deleteActivity,
getOrganizers,changeOrganizerStatus} from '../api/api'

const userType = ref()  // 用户类型：'visitor', 'organizer', 'manager'
const visitorData = ref([])
const organizerData = ref([])
const managerData = ref([])

const editDialogVisible = ref(false)
const editForm = ref({
  organizer_id: localStorage.getItem('userId'),
  activity_id: '',
  name: '',
  type: '',
  start_time: '',
  end_time: '',
  flow: 0,
  description: '',
  venue_id: '',
  
})
const venues = ref([])

// 获取用户类型和对应数据
const initializeData = async () => {
  try {
    // 从localStorage获取用户类型
    userType.value = localStorage.getItem('role')
    console.log(userType.value)
    // 根据用户类型获取对应数据
    switch (userType.value) {
      case 'visitor':
        await fetchVisitorData()
        break
      case 'organizer':
        await fetchOrganizerData()
        break
      case 'manager':
        await fetchManagerData()
        break
    }
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

// 获取访客的搭子请求数据
const fetchVisitorData = async () => {
  try {
    const response = await getPartners({visitor_id: localStorage.getItem('userId')})
    if (response.data && response.data.data) {
      visitorData.value = response.data.data
    }
  } catch (error) {
    console.error('获取搭子请求失败:', error)
    ElMessage.error('获取搭子请求失败')
  }
}

// 获取组织者的活动数据
const fetchOrganizerData = async () => {
   try {
    const response = await getOrganizerActivities({
      organizer_id: localStorage.getItem('userId')
    })
    if (response.data && response.data.data) {
      organizerData.value = response.data.data
    }
  } catch (error) {
    console.error('获取活动列表失败:', error)
    ElMessage.error('获取发布活动列表失败')
  }
}

// 获取管理员管理的组织者数据
const fetchManagerData = async () => {
  try {
    const response = await getOrganizers()
    if (response.data && response.data.data) {
      managerData.value = response.data.data
    }
  } catch (error) {
    console.error('获取组织者列表失败:', error)
    ElMessage.error('获取组织者列表失败')
  }
}
// 更改搭子是否找到
const handleBuddyFound = async (row) => {
  try {
    const response = await changePartnerStatus(
      { activity_id: row.activity_id, 
        visitor_id: localStorage.getItem('userId'),
        is_found: row.is_found })
    if (response.data && response.data.data) {
      ElMessage.success('更改搭子是否找到成功')
    }
  } catch (error) {
    console.error('更改搭子是否找到失败:', error)
    ElMessage.error('更改搭子是否找到失败')
  }
}
const handleBuddyDelete = async (row) => {
  try {
    const response = await deletePartner(
      { activity_id: row.activity_id, 
      visitor_id: localStorage.getItem('userId') })
    if (response.data && response.data.data) {
      ElMessage.success('删除搭子请求成功')
      await fetchVisitorData()
    }
  } catch (error) {
    console.error('删除搭子请求失败:', error)
    ElMessage.error('删除搭子请求失败')
  }
}
// 获取场地列表
const fetchVenues = async () => {
  try {
    const response = await getVenues()
    venues.value = response.data.data
  } catch (error) {
    console.error('获取场地列表失败:', error)
  }
}

// 打开编辑对话框
const handleEdit = async (row) => {
  editForm.value = {
    organizer_id: localStorage.getItem('userId'),
    activity_id: row.activity_id,
    name: row.name,
    type: row.type,
    start_time: row.start_time,
    end_time: row.end_time,
    flow: row.flow,
    description: row.description,
    venue_id: row.venue_id,    
  }
  await fetchVenues() // 获取场地列表
  editDialogVisible.value = true
}

// 提交编辑
const handleEditSubmit = async () => {
  //console.log(editForm.value)
  //非空判断
  if (!editForm.value.name || !editForm.value.type ) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (editForm.value.activity_id) {
  try {
    await editActivity(editForm.value)
    ElMessage.success('活动更新成功')
    editDialogVisible.value = false
    await fetchOrganizerData() // 刷新活动列表
  } catch (error) {
    console.error('更新活动失败:', error)
    ElMessage.error('更新活动失败')
  }
} else {
  try {

    await addActivity(editForm.value)
    ElMessage.success('活动增加成功')
    editDialogVisible.value = false
    await fetchOrganizerData() // 刷新活动列表
  } catch (error) {
    console.error('增加活动失败:', error)
    ElMessage.error('增加活动失败')
  }
}
}
// 增加活动
const handleAddActivity = async () => {
  editForm.value = {
    organizer_id: localStorage.getItem('userId'),
    activity_id: null,
    name: '',
    type: '',
    start_time: '',
    end_time: '',
    flow: 0,
    description: '',
    venue_id: null
  }
  await fetchVenues() // 获取场地列表
  editDialogVisible.value = true
}
// 处理删除活动
const handleDelete = async (row) => {
  try {
    // TODO: 添加删除活动的 API
    await ElMessageBox.confirm('确定要删除这个活动吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 调用删除 API
    await deleteActivity({activity_id: row.activity_id})
    ElMessage.success('删除成功')
    await fetchOrganizerData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除活动失败:', error)
      ElMessage.error('删除活动失败')
    }
  }
}

// 处理合规状态变更
const handleComplianceChange = async (row) => {
  try {
    await changeOrganizerStatus(
      {organizer_id: row.organizer_id, 
      status: !row.compliance_status})
    ElMessage.success('合规状态变更成功')
    await fetchManagerData()
  } catch (error) {
    console.error('合规状态变更失败:', error)
    ElMessage.error('合规状态变更失败')
  }
}

// 组件挂载时初始化数据
onMounted(() => {
  initializeData()
})
</script>

<style scoped>
.container {
position:fixed;
  padding: 10px;
  justify-content: center;
  z-index: 2;
  margin: auto;
  border-radius: 8px;
  backdrop-filter: blur(4px);
  background-color: rgba(174,0,255, 0.151);
  box-shadow: rgba(0, 0, 0, 0.3) 2px 8px 8px;
  border: 4px rgba(255,255,255,0.4) solid;
  border-bottom: 4px rgba(40,40,40,0.35) solid;
  border-right: 4px rgba(40,40,40,0.35) solid;
}

.dialog-footer {
  padding: 20px 0;
  text-align: right;
}

:deep(.el-dialog) {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 15px;
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

:deep(.el-form-item__label) {
  font-weight: bold;
}

:deep(.el-input__wrapper),
:deep(.el-textarea__wrapper) {
  background-color: rgba(255, 255, 255, 0.8);
}
</style>
