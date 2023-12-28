<template>
    <!-- <div class="login-wrapper"> -->
    <Snav>
        <template v-slot:name>{{ title }}</template>
    </Snav>

    <div class="container">
        <section id="formHolder">

            <div class="row">

                <!-- Brand Box -->
                <div class="col-sm-6 brand">
                    <a href="#" class="logo">JobFree <span>.</span></a>

                    <div class="heading">
                        <h2>选择</h2>
                        <p>最合适的工作</p>
                    </div>

                    <!-- <div class="success-msg">
                        <p>Great! You are one of our members now</p>
                        <a href="#" class="profile">Your Profile</a>
                    </div> -->
                </div>


                <!-- Form Box -->
                <div class="col-sm-6 form">

                    <!-- Login Form -->
                    <div :class="{ 'login form-peice switched': IsActive, 'login form-peice': !IsActive }">
                        <el-form ref="LoginruleFormRef" :model="LoginruleForm" :rules="Loginrules" label-width="70px "
                            :size="formSize" status-icon :label-position="labelPosition" v-if="!isForget">
                            <el-form-item label="用户名" prop="account" >
                                <el-input v-model="LoginruleForm.account" autocomplete clearable />
                            </el-form-item>

                            <el-form-item label="密码" prop="pwd" type="password" >
                                <el-input v-model="LoginruleForm.pwd" autocomplete type="password" clearable />
                            </el-form-item>

                            <el-form-item label="验证码" prop="code" class="code">
                                <el-input v-model="LoginruleForm.code" clearable />
                                <img style="height: 30px;width: 80px;" :src="imgurl" alt="加载中..." @click="resetcode">
                            </el-form-item>
                            <div class="fun">
                                <el-checkbox v-model="isRemember" label="记住密码" />
                                <a href="javascript:;" class="forget" @click="changeforget">忘记密码</a>
                            </div>
                            

                            <div class="CTA">
                                <el-button type="submit" class="submit" @click="LoginsubmitForm()">登录
                                </el-button>
                                <a href="javascript:;" class="switch" @click="change">没有账户？</a>
                            </div>
                        </el-form>
                        <el-form ref="ForegetruleFormRef" :model="ForegetruleForm" :rules="Foregetrules" label-width="80px "
                            :size="formSize" status-icon :label-position="labelPosition" v-if="isForget">
                            <el-form-item label="邮箱" prop="email"  >
                                <el-input v-model="ForegetruleForm.email" autocomplete type="email" clearable />
                            </el-form-item>

                            <el-form-item label="密码" prop="password" >
                                <el-input v-model="ForegetruleForm.password" autocomplete type="password" clearable />
                            </el-form-item>
                            <el-form-item label="重复密码" prop="checkpassword" >
                                <el-input v-model="ForegetruleForm.checkpassword" autocomplete type="password" clearable />
                            </el-form-item>
                            <el-form-item label="验证码" prop="code" class="code" >
                                <el-input v-model="ForegetruleForm.code" clearable />
                                <el-button style="margin-left: 20px; "  @click="sendcode(ForegetruleForm.email)">{{
                                    code_status }}</el-button>
                            </el-form-item>
                            

                            <div class="CTA">
                                <el-button type="submit" class="submit" @click="ForegetsubmitForm()">修改密码
                                </el-button>
                                <el-button class="changeforget " @click="changeforget" type="primary">返回登录</el-button>
                            </div>
                        </el-form>
                    </div><!-- End Login Form -->


                    <!-- Signup Form -->
                    <div :class="{ 'signup form-peice switched': !IsActive, 'signup form-peice': IsActive }">
                        <el-form ref="SignupruleFormRef" :model="SignupruleForm" :rules="Signuprules" label-width="80px "
                            :size="formSize" status-icon :label-position="labelPosition">
                            <el-form-item label="邮箱" prop="email"  >
                                <el-input v-model="SignupruleForm.email" autocomplete type="email" clearable />
                            </el-form-item>

                            <el-form-item label="密码" prop="password" clearable >
                                <el-input v-model="SignupruleForm.password" autocomplete type="password" clearable />
                            </el-form-item>
                            <el-form-item label="重复密码" prop="checkpassword" >
                                <el-input v-model="SignupruleForm.checkpassword" autocomplete type="password" clearable />
                            </el-form-item>
                            <el-form-item label="手机号" prop="phone"  >
                                <el-input v-model="SignupruleForm.phone" autocomplete type="phone" clearable />
                            </el-form-item>
                            <el-form-item label="验证码" prop="code" class="code">
                                <el-input v-model="SignupruleForm.code" clearable />
                                <el-button style="margin-left: 20px; width: 80px !important;"  @click="sendcode(SignupruleForm.email)">{{
                                    code_status }}</el-button>
                            </el-form-item>
                            <el-checkbox v-model="isRemember" label="记住密码" />

                            <div class="CTA">
                                <el-button type="submit" class="submit" @click="SignupsubmitForm()">注册
                                </el-button>
                                <a href="javascript:;" class="switch" @click="change">已有账户？</a>
                            </div>
                        </el-form>
                    </div><!-- End Signup Form -->
                </div>
            </div>

        </section>




    </div>

    <!-- </div> -->
</template>

<script lang="ts">
import Snav from '../utils/Snav.vue'
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules, FormProps } from 'element-plus'



export default {

    name: 'Login',
    created(){
        if(this.$route['query']['isForget']){
        this.changeforget()
        }
        this.ForegetruleForm.email=this.$route['query']['email']
    },
    data() {
        return {
            title:'登录',
            imgurl: this.$ApiBaseUrl + this.$api["imgcode"] + '?random=' + Math.random(),
            IsActive: true,
            LoginruleForm: {
                account: '',
                pwd: '',
                code: '',
            },
            Loginrules: {
                account: [
                    { required: true, message: '请输入账户', trigger: 'blur' },
                    { min: 3, max: 50, message: '长度应该在 3 - 50', trigger: 'blur' },
                ],
                pwd: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                code: [
                    { required: true, message: '请输入验证码', trigger: 'blur' },
                    { min: 4, max: 4, message: '长度应该在 4', trigger: 'blur' },
                ],
            },
            SignupruleForm: {
                email: '',
                password: '',
                checkpassword: '',
                phone: '',
                code: ''
            },
            Signuprules: {
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    { min: 3, max: 50, message: '长度应该在 3 - 50', trigger: 'blur' },
                    {type:'email',message: '邮箱格式不正确', trigger:['blur', 'change']}
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                checkpassword: [
                    { required: true, message: '请输入重复密码', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                phone: [
                    { required: true, message: '请输入手机号', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                code: [
                    { required: true, message: '请输入邮箱验证码', trigger: 'blur' },
                    { min: 4, max: 6, message: '长度应该在  6', trigger: 'blur' },
                ],
            },
            ForegetruleForm: {
                email: '',
                password: '',
                checkpassword: '',
                code: ''
            },
            Foregetrules: {
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' },
                    { min: 3, max: 50, message: '长度应该在 3 - 50', trigger: 'blur' },
                    {type:'email',message: '邮箱格式不正确', trigger:['blur', 'change']}
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                checkpassword: [
                    { required: true, message: '请输入重复密码', trigger: 'blur' },
                    { min: 8, max: 16, message: '长度应该在 8 - 16', trigger: 'blur' },
                ],
                code: [
                    { required: true, message: '请输入邮箱验证码', trigger: 'blur' },
                    { min: 4, max: 6, message: '长度应该在  6', trigger: 'blur' },
                ],
            },
            code_status: '发送验证码',
            issend: 0,
            Interval: '',
            action: '注册验证',
            formSize: 'default',
            labelPosition: ref<FormProps['labelPosition']>('left'),
            isRemember: true,
            isForget:false
        };
    },

    methods: {
        changeforget(){
            
            this.isForget=!this.isForget
            this.title=this.isForget?'忘记密码':'登录'
        },
        async sendcode(email) {
            
            if (this.issend == 0 && email != '') {
                let Loading = this.$Loading({ fullscreen: true })
                await this.$http.post(
                    this.$api.emailcode,
                    {
                        'email': email,
                        'action': this.action
                    }
                )
                    .then(response => {

                        this.issend = 1
                        this.code_status = 60
                        this.Interval = setInterval(this.countdown, 1000)
                        this.$Message({
                            type: 'success',
                            message: '发送成功'
                        })
                        Loading.close()
                    })
                    .catch(error => {
                        this.$Message.error('请求频繁')
                        Loading.close()
                    })

            }
            else if (this.SignupruleForm.email == '') {
                this.$Message({
                    type: 'warning',
                    message: '请填写邮箱'
                })

            }
        },
        countdown() {
            if (this.code_status != 0) {
                this.code_status--
            } else {
                this.code_status = '邮箱验证码'
                clearInterval(this.Interval)
                this.issend = 0
            }
        },
        change() {
            this.IsActive = !this.IsActive
            this.title=this.IsActive ? '登录':'注册'
        },
        resetcode() {
            this.imgurl = this.$ApiBaseUrl + this.$api["imgcode"] + '?random=' + Math.random()
        },
        async LoginsubmitForm() {
            this.$refs.LoginruleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.login()

            })

        },
        async SignupsubmitForm() {
            this.$refs.SignupruleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.signup()

            })

        },
        async ForegetsubmitForm() {
            this.$refs.ForegetruleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.foreget()

            })

        },
        async login() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.login, this.LoginruleForm)
                .then(response => {
                    // 登录成功，获取访问令牌和刷新令牌并保存到本地（例如使用localStorage）
                    if (response.data.code === 200) {
                        const { access_token, refresh_token } = response.data.tokens;
                        if (this.isRemember) {
                            localStorage.setItem('accessToken', access_token);
                            localStorage.setItem('refreshToken', refresh_token)
                        } else {
                            localStorage.setItem('accessToken', access_token);
                            sessionStorage.setItem('refreshToken', refresh_token)
                        }
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "登录成功"
                        })
                        this.$router.push('/');
                    } else {
                        this.$Message.error(response.data.error)
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });

            this.resetcode()


        },
        async signup() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.signup, this.SignupruleForm)
                .then(response => {
                    if (response.data.code === 200) {
                        
                        
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "注册成功"
                        })
                        this.IsActive=true
                    } else {
                        this.$Message.error(response.data.error)
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });

        },
        async foreget() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.foreget, this.ForegetruleForm)
                .then(response => {
                    if (response.data.code === 200) {
                        
                        
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "修改成功"
                        })
                        this.changeforget()
                    } else {
                        this.$Message.error(response.data.error)
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });

        },

    },
    components: {
        Snav
    }
}
</script>
<style scoped>
body {
    font-family: "Montserrat", sans-serif;
    background: #f7edd5;
}
.forget{
    font-size: 14px;
    font-weight: 400;
    font-family: "Montserrat", sans-serif;
    color: black;
}
.fun{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.form form {
    left: 50% !important;
}

.code>div>* {
    flex: 1 !important;
}

.CTA {
    display: flex;
    justify-content: space-around;
}

.container {
    max-width: 500px;
    position: relative;
    top: calc(50% - 320px);
    left: calc(50% - 500px);
}

a {
    display: inline-block;
    text-decoration: none;
}

input {
    outline: none !important;
}

h1 {
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 40px;
    font-weight: 700;
}

section#formHolder {
    padding: 50px 0;
}

.brand {
    padding: 20px;
    background-size: cover;
    background-position: center center;
    color: #fff;
    min-height: 540px;
    position: relative;
    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.6s cubic-bezier(1, -0.375, 0.285, 0.995);
    z-index: 1;
}

.brand.active {
    width: 100%;
}

.brand::before {
    content: "";
    display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.85);
    z-index: -1;
}

.brand a.logo {
    color: #f95959;
    font-size: 20px;
    font-weight: 700;
    text-decoration: none;
    line-height: 1em;
}

.brand a.logo span {
    font-size: 30px;
    color: #fff;
    transform: translateX(-5px);
    display: inline-block;
}

.brand .heading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    transition: all 0.6s;
}

.brand .heading.active {
    top: 100px;
    left: 100px;
    transform: translate(0);
}

.brand .heading h2 {
    font-size: 70px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 0;
}

.brand .heading p {
    font-size: 15px;
    font-weight: 300;
    text-transform: uppercase;
    letter-spacing: 2px;
    white-space: 4px;
    font-family: "Raleway", sans-serif;
}

.brand .success-msg {
    width: 100%;
    text-align: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-top: 60px;
}

.brand .success-msg p {
    font-size: 25px;
    font-weight: 400;
    font-family: "Raleway", sans-serif;
}

.brand .success-msg a {
    font-size: 12px;
    text-transform: uppercase;
    padding: 8px 30px;
    background: #f95959;
    text-decoration: none;
    color: #fff;
    border-radius: 30px;
}

.brand .success-msg p,
.brand .success-msg a {
    transition: all 0.9s;
    transform: translateY(20px);
    opacity: 0;
}

.brand .success-msg p.active,
.brand .success-msg a.active {
    transform: translateY(0);
    opacity: 1;
}

.form {
    position: relative;
}

.form .form-peice {
    background: #fff;
    min-height: 480px;
    margin-top: 30px;
    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
    color: #bbbbbb;
    padding: 30px 0 60px;
    transition: all 0.9s cubic-bezier(1, -0.375, 0.285, 0.995);
    position: absolute;
    top: -510px;
    left: 0;
    width: 100%;
    overflow: hidden;
}

.form .form-peice.switched {
    transform: translateX(-100%);
    width: 100%;
    left: 200%;
}

.form form {
    padding: 0 40px;
    margin: 0;
    width: 70%;
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
}

.form form .form-group {
    margin-bottom: 5px;
    position: relative;
}

.form form .form-group.hasError input {
    border-color: #f95959 !important;
}

.form form .form-group.hasError label {
    color: #f95959 !important;
}

.form form label {
    font-size: 12px;
    font-weight: 400;
    text-transform: uppercase;
    font-family: "Montserrat", sans-serif;
    /* transform: translateY(40px); */
    transition: all 0.4s;
    cursor: text;
    /* z-index: -1; */
}

.form form label.active {
    transform: translateY(10px);
    font-size: 10px;
}

.form form label.fontSwitch {
    font-family: "Raleway", sans-serif !important;
    font-weight: 600;
}

.form form input:not([type=submit]) {
    background: none !important;
    outline: none !important;
    border: none !important;
    display: block !important;
    padding: 10px 0 !important;
    width: 100% !important;
    border-bottom: 1px solid #eee !important;
    color: #444 !important;
    font-size: 15px !important;
    font-family: "Montserrat", sans-serif !important;
    z-index: 1 !important;
}

.form form input:not([type=submit]).hasError {
    border-color: #f95959;
}

.form form span.error {
    color: #f95959;
    font-family: "Montserrat", sans-serif;
    font-size: 12px;
    position: absolute;
    bottom: -20px;
    right: 0;
    display: none;
}

.form form input[type=password] {
    color: #f95959;
}

.form form .CTA {
    margin-top: 30px;
}

.form form .CTA * {
    line-height: 32px;
}

.form form .CTA input,
.form form .CTA button {
    font-size: 12px;
    text-transform: uppercase;
    padding: 5px 30px;
    background: #f95959;
    color: #fff;
    border-radius: 30px;
    /* margin-right: 20px; */
    border: none;
    font-family: "Montserrat", sans-serif;
}

.form form .CTA a.switch {
    font-size: 13px;
    font-weight: 400;
    font-family: "Montserrat", sans-serif;
    color: #bbbbbb;
    text-decoration: underline;
    transition: all 0.3s;
}

.form form .CTA a.switch:hover {
    color: #f95959;
}

footer {
    text-align: center;
}

footer p {
    color: #777;
}

footer p a,
footer p a:focus {
    color: #b8b09f;
    transition: all 0.3s;
    text-decoration: none !important;
}

footer p a:hover,
footer p a:focus:hover {
    color: #f95959;
}

@media (max-width: 768px) {
    .container {
        overflow: hidden;
        max-width: 100%;
        position: unset;
    }

    section#formHolder {
        padding: 0;
    }

    section#formHolder div.brand {
        min-height: 200px !important;
    }

    section#formHolder div.brand.active {
        min-height: 100vh !important;
    }

    section#formHolder div.brand .heading.active {
        top: 200px;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    section#formHolder div.brand .success-msg p {
        font-size: 16px;
    }

    section#formHolder div.brand .success-msg a {
        padding: 5px 30px;
        font-size: 10px;
    }

    section#formHolder .form {
        width: 80vw;
        min-height: 500px;
        margin-left: 10vw;
    }

    section#formHolder .form .form-peice {
        margin: 0;
        left: 0;
        width: 100% !important;
        transition: all 0.5s ease-in-out;
        /* transform: translateY(-100%); */
    }

    section#formHolder .form .form-peice.switched {
        transform: translateY(100%);
        width: 100%;

        left: 0;
    }

    section#formHolder .form .form-peice>form {
        width: 100% !important;
        padding: 60px;
        left: 50%;
    }
}

@media (max-width: 480px) {
    section#formHolder .form {
        width: 100vw;
        margin-left: 0;
    }

    h2 {
        font-size: 50px !important;
    }
}
</style>
  
