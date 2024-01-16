import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import { ElMessage } from 'element-plus'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { ElLoading } from 'element-plus'
import * as Elicons from "@element-plus/icons-vue";
const app = createApp(App)
const method='dev'
if(method=='dev'){
    const com = '127.0.0.1:8000'
    axios.defaults.baseURL = '//127.0.0.1:8000'
    app.config.globalProperties.$ApiBaseUrl='//127.0.0.1:8000'
}else{
    const com = ''
    axios.defaults.baseURL = ''
    app.config.globalProperties.$ApiBaseUrl=''
}
app.use(ElementPlus)

app.config.globalProperties.$Message=ElMessage
app.config.globalProperties.$Loading=ElLoading.service
for (const name in Elicons) {
    app.component(name, Elicons[name]);
}

axios.defaults.withCredentials = true
axios.defaults.timeout = 50000
//1.请求拦截器
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('accessToken');

        if (token && config.url != '/login' && config.url != '/api/token/refresh/') {
            // 在请求头中添加新令牌
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

window.isRefeshing = false
axios.interceptors.response.use(
    (response) => {
        // 在这里可以处理响应数据
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // 处理401 Unauthorized错误，刷新令牌并重试原始请求
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                if (!window.isRefeshing) {
                    await getToken();
                }
                // 刷新令牌
                return axios(originalRequest); // 重新发送原始请求
            } catch (refreshError) {
                // 刷新令牌失败，执行适当的操作，例如跳转到登录页面或清除用户数据
                console.error('刷新令牌失败', refreshError);
                localStorage.clear()
                window.location.href = '/login'
            }
        }

        return Promise.reject(error);
    }
);
app.config.globalProperties.$http = axios
async function getToken() {
    if (localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')) {
        window.isRefeshing = true
        let refresh = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')
        await app.config.globalProperties.$http.post('/api/token/refresh/', { 'refresh': refresh })
            .then(response => {
                const { access } = response.data;
                // 将新的访问令牌存储在本地（例如使用localStorage）
                localStorage.setItem('accessToken', access);
                
                window.isRefeshing = false
                window.location.reload()
                return;
            }).catch(error => {
                console.error(error)
                localStorage.clear()
                // window.location.href = '/login'
                return;
            });

    } else {
        localStorage.clear()
        // window.location.href = '/login'
        return;
    }
}


app.config.globalProperties.$refreshTime = 5
app.config.globalProperties.$api = {
    login: '/api/auth/login/',
    refresh: '/api/token/refresh/',
    emailcode: '/api/code/emailcode',
    imgcode: '/api/code/imgcode',
    signup: '/api/auth/signup/',
    userinfo: '/api/auth/userinfo/',
    foreget: '/api/auth/foreget/',
    announcements: '/api/announcement/getannouncementlist',
    uploadphoto:'/api/data/resume/uploadPhoto/',
    resumeinfo:'/api/data/resume/resumeinfo/',
    basedata:'/api/data/baseData',
    changebaseinfo:'/api/data/resume/changebaseinfo/',
    changeresumeinfo:'/api/data/resume/changeresumeinfo/',
    changereadme:'/api/data/resume/changereadme/',
    jobs:'/api/data/jobs/',
    companys:'/api/data/company/',
    similarjobs:'/api/data/similar-jobs/',
    clickjob:'/api/data/jobs/click/',
    collect:'/api/data/jobs/collect/',
    iscollected:'/api/data/jobs/iscollected/',
    removecollect:'/api/data/jobs/removecollect/',
    recommend:'/api/data/jobs/recommend/',
    collectjobs:'/api/data/jobs/collectjobs/',
    clickjobs:'/api/data/jobs/clickjobs/',
    comment:'/api/data/jobs/comment/',
    commentjobs:'/api/data/jobs/commentJobs/',

}
async function getbaseData(){
    return axios.get('/api/data/baseData')
    
}
app.use(router)
getbaseData().then((response)=>{
    app.config.globalProperties.$baseData = response.data;  
    app.mount('#app')
}).catch(error => {
    console.error('初始化失败',error)

  });

