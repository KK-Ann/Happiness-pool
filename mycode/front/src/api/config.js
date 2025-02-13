import axios from 'axios'
// import { ElMessage } from 'element-plus'
// //配置相关信息，将前端获取的信息传给后端
// //创建axios实例
// const Service = axios.create({
//     baseURL: 'http://localhost:5000',
//     timeout: 5000, 
//     withCredentials: false
//   });
  
// Service.interceptors.request.use(
//     config=>{
//         const token = localStorage.getItem('token');
//         // 请求头加上token
//         if(token)
//             config.headers.authorization = `Bearer ${token}`
//         return config
//     },err=>{
//         return Promise.reject(err);
//     }
// ) 
//export default Service//导出,以便其他文件import

axios.defaults.baseURL = "http://localhost:5000";
export const getAction = (url,params) => {
    return axios({
        url:url,
        method:"get",
        params
    })
}
export const postAction = (url, parameter) => {
  console.log('Request URL:', url)
  console.log('Request Data:', parameter)
  return axios({
    url:  url,
    method: 'post',
    data: parameter,
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => {
    console.log('Response:', response)
    return response
  }).catch(error => {
    console.log('Error:', error.response)
    throw error
  })
}
export const putAction = (url,data) => {
    return axios({
        url:url,
        method:"put",
        data
    })
}