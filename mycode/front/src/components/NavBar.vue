<template>
	<el-container class="nav-container" direction="vertical">
        <el-row style="padding: 30px 0px 20px 0px; ">
            <el-col :span="6">
            </el-col>
            <el-col :span="12" 
                style="display: flex; align-items: center; justify-content: center; cursor: pointer;">
                
                    <el-avatar :size="60" :src="avatarImg" />
                
            </el-col>
            <el-col :span="6">
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="12" style="text-align: center; margin: auto 0px">
                <p style="font-size:18px ; margin: 0px;"> 
                    身份 
                </p>
                <p style="font-size:14px;margin: 0px; margin-top: 10px;"> 
                    &emsp;{{user.role}}
                </p >
            </el-col>
            <el-col :span="12" style="text-align: left; margin: auto 0px">
                <p style="font-size:18px ; margin: 0px;"> 
                    用户名 
                </p>
                <p style="font-size:14px;margin: 0px; margin-top: 10px;"> 
                    &emsp;{{user.name}}
                </p >
            </el-col>
        </el-row>
        <el-row>
            <p style="font-size:18px ; margin: 0px;"> 
                    &emsp;邮箱 
                </p>
                <p style="font-size:14px;margin: 0px; margin-top: 10px;"> 
                    &emsp;{{user.email}}
                </p >
        </el-row>
        <el-row v-if="user.role === 'visitor'">
            <p style="font-size:18px ; margin: 0px;"> 
                    &emsp;喜爱类型 
                </p>
                <p style="font-size:14px;margin: 0px; margin-top: 10px;"> 
                    &emsp;{{user.like}}
                </p >
        </el-row>
        <el-row v-if="user.role === 'organizer'">
            <p style="font-size:18px ; margin: 0px;"> 
                    &emsp;合规性 
                </p>
                <p style="font-size:14px;margin: 0px; margin-top: 10px;"> 
                    &emsp;{{user.compliance_status?'合规':'不合规'}}
                </p >
        </el-row>
        <div style="flex:65%">
            <el-menu :default-active="activeIndex" @select="handleSelect" router>
                <el-menu-item
                  v-for="(item, index) in NavList" :key="index" :index="item.url"
                  style="font-size: 16px; padding: 0px 10px; background-color: #E1B6F4;"
                >
                    <div style="padding: 0px 25px;">
                        <el-icon >
                            <component :is="item.icon" />
                        </el-icon>
                        <span>{{ item.title }}</span>
                    </div>
                </el-menu-item>
            </el-menu>
        </div>          
    </el-container>
</template>



<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserFilled , Files , MapLocation } from '@element-plus/icons-vue'  // 导入图标
import avatarImg from '@/assets/images/en.jpg'  // 添加图片导入

// 添加用户数据
const user = reactive({
    name: localStorage.getItem('username'),
    id: localStorage.getItem('userId'),
    role: localStorage.getItem('role'),
    email: localStorage.getItem('email'),
    like: localStorage.getItem('favorite_activity_type'),
    compliance_status: localStorage.getItem('compliance_status')
})

const NavList = reactive([
	{
		title: "我的",
		url: "/DashBoard/SelfPage",
		icon: UserFilled 
    },
	{
		title: "活动地图",
		url: "/DashBoard/ActivityOverview",
		icon: MapLocation 
	},
	{
		title: "活动列表",
		url: "/DashBoard/ActivityList",
		icon: Files 
	},
	
])
const activeIndex = ref('/DashBoard/ActivityOverview')  // 默认选中的菜单项路径
const router = useRouter()  // 获取路由对象
function handleSelect(key) {
    activeIndex.value = key
    router.push(key)  // 跳转到选中的路由路径
}

</script>

<style scoped>
.nav-container {
  height: 700px;
  width: 200px;
  left: 10px;
  top: 10px;
  position: fixed;
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

.el-menu-item.is-active {
    background-color: #E39AC5 !important;
    color: #ffffff !important; 
    font-weight: bold; 
    
}

.el-menu-item.is-active  div{
    border-left:5px #fff solid !important;
}

.el-menu-item:hover {
  background-color:  #E39AC5 !important; 
  color: #ffffff !important; 
}


  
</style>

