<template>
  <div class="background--custom">
    <canvas id="canvas" />
  </div>
  <!-- 最外层的大盒子 -->
  <div class="bigBox">    
    <div class="box" ref="box">
      <!-- 滑动盒子 -->
      <div class="pre-box">
        <h1>欢迎来到快乐搜集池</h1>
        <p>一个文娱活动查询系统</p>
        <div class="img-box">
          <img src="@/assets/images/hi.jpg" alt="" id="avatar" />
        </div>
      </div>
      <!-- 注册盒子 -->
      <div class="register-form">
        <!-- 标题盒子 -->
        <div class="title-box">
          <h1>注册</h1>
        </div>
        <!-- 输入框盒子 使用el-form -->
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="rules"
          label-width="5px"
        > 
          <el-form-item prop="username" >
            <el-input
              type="text"
              placeholder="请输入用户名"
              :suffix-icon="User"
              v-model="registerForm.username"
            />
          </el-form-item>
          
          <el-form-item prop="password" show-password>
            <el-input
              type="password"
              placeholder="请输入密码"
              show-password
              v-model="registerForm.password"
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword" >
            <el-input
              type="password"
              placeholder="请再次输入密码"
              show-password
              v-model="registerForm.confirmPassword"
            />
          </el-form-item>
          <el-form-item prop="email" >
            <el-input
              type="text"
              placeholder="请输入邮箱"
              :suffix-icon="Message"
              v-model="registerForm.email"
            />
          </el-form-item>
          <el-form-item label="身份">
            <el-radio-group v-model="registerForm.role">
              <el-radio value="visitor">普通游玩者</el-radio>
              <el-radio value="organizer">活动发布者</el-radio>
              <el-radio value="manager">城市管理者</el-radio>
            </el-radio-group>
          </el-form-item>

        </el-form>

        <!-- 按钮盒子 -->
        <div class="btn-box">
          <button @click="register">注册</button>
          <!-- 绑定点击事件 -->
          <p @click="mySwitch_left">已有账号?去登录</p>
        </div>
      </div>
      <!-- 登录盒子 -->
      <div class="login-form">
        <!-- 标题盒子 -->
        <div class="title-box">
          <h1>登录</h1>
        </div>
        <!-- 输入框盒子 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="rules"
          label-with="5px"
        >
          <el-form-item prop="username" label=" ">
            <el-input
              type="text"
              placeholder="用户名"
              :suffix-icon="User"
              v-model="loginForm.username"
            />
          </el-form-item>
          <el-form-item prop="password" label=" " >
            <el-input
              type="password"
              show-password
              placeholder="密码"
              v-model="loginForm.password"
            />
          </el-form-item>
          <el-form-item label="身份">
            <el-radio-group v-model="loginForm.role">
              <el-radio value="visitor">普通游玩者</el-radio>
              <el-radio value="organizer">活动发布者</el-radio>
              <el-radio value="manager">城市管理者</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <!-- 按钮盒子 -->
        <div class="btn-box">
          <button @click="login">登录</button>
          <!-- 绑定点击事件 -->
          <p @click="mySwitch_right">没有账号?去注册</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
//import { onMounted } from 'vue';
import { Lock, User,Message } from '@element-plus/icons-vue'
//import mySwitch from '@/utils/mySwitch'
import { reactive, ref } from 'vue'
//import { Service } from '@/api/config.js'
import{ visitorLogin,organizerLogin,managerLogin,visitorRegister,organizerRegister,managerRegister} from '@/api/api.js'
import { ElMessage,ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { onMounted } from '@vue/runtime-core'
onMounted(() => {//背景动态
  const script = document.createElement('script');
  script.src = "https://cdn.jsdelivr.net/gh/greentfrapp/pocoloco@minigl/minigl.js";
  script.onload = () => {
    const gradient = new Gradient();
    gradient.initGradient("#canvas");
  };
  document.body.appendChild(script);
});
const loginForm = reactive({//reactive：用于创建响应式的对象，变化能够自动触发视图的更新
  username: '',
  password: '',
  role: ''
})
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  role: '',
})
//验证相关
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
};
const validatePassword = (rule, value, callback) => {
  //  密码只能由大小写英文字母或数字开头，且由大小写英文字母_.组成
      const reg = /^[A-Za-z0-9]{6,15}$/
      console.log('reg', value.match(reg))
      if (!value.match(reg)) {
        callback(new Error('密码由字母或数字开头，且只能为字母,数字,下划线及（.）'))
      } else {
        callback()
      }
};
// 邮箱校验
const validateEmail = (rule, value, callback) => {
  const Reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
  const Reg1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
  if (!value.match(Reg)||!value.match(Reg1)) {
    callback(new Error('请输入有效邮箱格式！'));
  } else {
    callback();
  }
};
const loginFormRef = ref('')
//ref：用于创建单一响应式数据，通常用于保存基本类型的数据
//使用：<el-form
//          ref="registerFormRef"
//         :model="registerForm"
const registerFormRef = ref('')
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min:2 , message: '长度至少2个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 15,message: '位数只能在6~15之间', trigger: 'blur' },
    { validator: validatePassword, message:'密码只能为字母,数字',trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请输入确认密码', trigger: 'blur' },
    { min: 6, message: '长度应该大于6', trigger: 'blur' },
   { validator: validateConfirmPassword, message:'两次输入的密码不一致',trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { validator: validateEmail, message:'请输入有效邮箱格式',trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'blur' },
  ]
})


const router = useRouter()
//将loginForm传给loginApi
const login = () => {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      console.log('Form Data:', loginForm)
      if(loginForm.role === 'visitor'){
        visitorLogin({
          name: loginForm.username,
          password: loginForm.password
        }).then(response => {
          console.log('Login Success:', response)
          localStorage.setItem('userId', response.data.data.id)
          localStorage.setItem('email', response.data.data.email)
          localStorage.setItem('favorite_activity_type', response.data.data.favorite_activity_type)
          localStorage.setItem('role', 'visitor')
          localStorage.setItem('username', loginForm.username)
          ElMessage({message: '登录成功！', type: 'success'})
          router.push('/Dashboard')
        })
        .catch(error => {
          console.log('Login Error:', error.response?.data)
          ElMessage({
            message: error.response?.data?.message || '登录失败，请检查用户名和密码', 
            type: 'error'
          })
        });
      }
      else if(loginForm.role === 'organizer'){
        organizerLogin({
          name: loginForm.username,
          password: loginForm.password,
        }).then(response => {
          localStorage.setItem('userId', response.data.data.id)
          localStorage.setItem('email', response.data.data.email)
          localStorage.setItem('compliance_status', response.data.data.compliance_status)
          localStorage.setItem('role', 'organizer')
          localStorage.setItem('username', loginForm.username)
          ElMessage({message: '登录成功！', type: 'success'})
          router.push('/Dashboard')
        })
        .catch(error => {
          ElMessage({message: '登录失败，请检查用户名和密码', type: 'error'})
        });
      }
      else if(loginForm.role === 'manager'){
        managerLogin({
          name: loginForm.username,
          password: loginForm.password,
        }).then(response => {
          localStorage.setItem('userId', response.data.data.id)
          localStorage.setItem('email', response.data.data.email)
          localStorage.setItem('role', 'manager')
          localStorage.setItem('username', loginForm.username)
          ElMessage({message: '登录成功！', type: 'success'})
          router.push('/Dashboard')
        })
        .catch(error => {
          ElMessage({message: '登录失败，请检查用户名和密码', type: 'error'})
        });
      }
    }
  })
}

const register = () => {
  registerFormRef.value.validate((valid) => {
    if (valid) {
      if(registerForm.role === 'visitor'){
        visitorRegister({
          name: registerForm.username,
          password: registerForm.password,
          email: registerForm.email,
          favorite_activity_type: "文化类"
        }).then(response => {
          ElMessage({message: '注册成功！', type: 'success'})
          mySwitch_left() // 切换到登录界面
        })
        .catch(error => {
          ElMessage({message: '注册失败，该用户名可能已存在', type: 'error'})
        });
      }
      else if(registerForm.role === 'organizer'){
        organizerRegister({
          name: registerForm.username,
          password: registerForm.password,
          email: registerForm.email
        }).then(response => {
          ElMessage({message: '注册成功！', type: 'success'})
          mySwitch_left()
        })
        .catch(error => {
          ElMessage({message: '注册失败，该用户名可能已存在', type: 'error'})
        });
      }
      else if(registerForm.role === 'manager'){
        managerRegister({
          name: registerForm.username,
          password: registerForm.password,
          email: registerForm.email
        }).then(response => {
          ElMessage({message: '注册成功！', type: 'success'})
          mySwitch_left()
        })
        .catch(error => {
          ElMessage({message: '注册失败，该用户名可能已存在', type: 'error'})
        });
      }
    }
  })
}

//let flag = ref(true)
const mySwitch_right = () => {
  const pre_box = document.querySelector('.pre-box')
  const img = document.querySelector("#avatar")    
  pre_box.style.transform = "translateX(100%)"
  pre_box.style.backgroundColor = " #875EF0"
  //img.src = url("@/assets/images/wuwu.jpeg")  
  
}
const mySwitch_left = () => {
  const pre_box = document.querySelector('.pre-box')
  const img = document.querySelector("#avatar")    
  pre_box.style.transform = "translateX(0%)"
  pre_box.style.backgroundColor = "#E39AC5"
  //img.src = url("@/assets/images/waoku.jpg")
}
</script>

<style scoped>
/* 去除input的轮廓 */
input {
  outline: none;
}

.bigBox {
  /* 溢出隐藏 */
 height: 100vh;
  overflow-x: hidden;
  display: flex;
  /* background-image: url("@/assets/images/background.png");
  background-size: 100%;
  /* 渐变方向从左到右 */
 /* background: linear-gradient(to right, rgb(247, 209, 215), rgb(191, 227, 241));*/
      /*background: linear-gradient(90deg, #AC74E3, #E9A2ED, #EAE88A);
      
      animation: gradient 1s alternate infinite;
      */
      
}

/* 最外层的大盒子 */
.box {
  width: 1050px;
  height: 600px;
  display: flex;
  /* 相对定位 */
  position: relative;
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

/* 滑动的盒子 */
.pre-box {
  /* 宽度为大盒子的一半 */
  width: 50%;
  height: 100%;
  /* 绝对定位 */
  position: absolute;
  /* 距离大盒子左侧为0 */
  left: 0;
  /* 距离大盒子顶部为0 */
  top: 0;
  z-index: 99;
  border-radius: 4px;
  background-color: #E39AC5;
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
  /* 动画过渡，先加速再减速 */
  transition: 0.5s ease-in-out;
}

/* 滑动盒子的标题 */
.pre-box h1 {
  margin-top: 150px;
  text-align: center;
  /* 文字间距 */
  letter-spacing: 5px;
  color: white;
  /* 禁止选中 */
  user-select: none;
  /* 文字阴影 */
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 滑动盒子的文字 */
.pre-box p {
  height: 30px;
  line-height: 30px;
  text-align: center;
  margin: 20px 0;
  /* 禁止选中 */
  user-select: none;
  font-weight: bold;
  color: white;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片盒子 */
.img-box {
  width: 200px;
  height: 200px;
  margin: 20px auto;
  /* 设置为圆形 */
  border-radius: 50%;
  /* 设置用户禁止选中 */
  user-select: none;
  overflow: hidden;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片 */
.img-box img {
  width: 100%;
  transition: 0.5s;
}

/* 登录和注册盒子 */
.login-form,
.register-form {
  flex: 1;
  height: 100%;
}

/* 标题盒子 */
.title-box {
  height: 300px;
  line-height: 300px;
}

/* 标题 */
.title-box h1 {
  text-align: center;
  color: white;
  /* 禁止选中 */
  user-select: none;
  letter-spacing: 5px;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 输入框盒子 */
.el-form {
  display: flex;
  /* 纵向布局 */
  flex-direction: column;
  position: relative;
  top: -90px; /* 向上移动 20px */
  /* 水平居中 */
  align-items: center;
}
.el-form-item {
  width: 65%;
}
/* 输入框 */
input {
  /* width: 60%; */
  height: 40px;
  margin-bottom: 20px;
  text-indent: 10px;
  border: 1px solid #fff;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 120px;
  /* 增加磨砂质感 */
  backdrop-filter: blur(10px);
}

input:focus {
  /* 光标颜色 */
  color: #b0cfe9;
}

/* 聚焦时隐藏文字 */
input:focus::placeholder {
  opacity: 0;
}

/* 按钮盒子 */
.btn-box {
  display: flex;
  justify-content: center;
  position: relative;
  top: -50px; /* 向上移动 20px */
}

/* 按钮 */
button {
  width: 100px;
  height: 30px;
  margin: 0 7px;
  line-height: 30px;
  border: none;
  border-radius: 4px;
  background-color: #EAD781;
  color: white;
}

/* 按钮悬停时 */
button:hover {
  /* 鼠标小手 */
  cursor: pointer;
  /* 透明度 */
  opacity: 0.8;
}

/* 按钮文字 */
.btn-box p {
  height: 30px;
  line-height: 30px;
  /* 禁止选中 */
  user-select: none;
  font-size: 14px;
  color: white;
}

.btn-box p:hover {
  cursor: pointer;
  border-bottom: 1px solid white;
}
.background--custom {
  background-color: #FFFFFF;
  width: 100vw;
  height: 100vh;
  position: absolute;
  overflow: hidden;
  z-index: -2;
  top: 0;
  left: 0;
}

canvas#canvas {
  z-index: -1;
  position: absolute;
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