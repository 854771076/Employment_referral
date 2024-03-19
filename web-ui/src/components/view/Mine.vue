<template>
    <div id="user">
        <div class="userdata">
            <div class="headerpic">
                <img :src="this.$ApiBaseUrl + userinfo.photo" class="rounded-circle" height="35" width="35">
            </div>
            <div class="accountinfo">
                <div id="m_username">
                    <span id="nikename" v-text="userinfo.name" @click="login"></span> <a href="/resume"><el-icon>
                            <EditPen />
                        </el-icon></a>
                </div>
                <div id="m_account">
                    <span id="m_phone">手机号：{{ userinfo.phone }} </span>
                    <span id="m_email">邮箱： {{ userinfo.email }} </span>
                </div>
            </div>
        </div>

        <div class="m_invitedinfo">
            <div>
                <span id="m_uid">{{ userinfo.username }}</span>
                <span>用户ID</span>
            </div>
            <div>
                <span id="m_sex">{{ userinfo.genderTranslation }}</span>
                <span>性别</span>
            </div>
            <div>
                <span id="m_user">{{ userinfo.currentIdentity }}</span>
                <span>身份</span>
            </div>
        </div>

        <div class="fun_card">
            <a href="/history">
                <el-icon>
                    <Clock />
                </el-icon>
                <span>我的足迹</span>
            </a>
            <a href="/star">
                <el-icon>
                    <Star />
                </el-icon>
                <span>我的收藏</span>
            </a>

        </div>

        <div class="setting">
            更多服务
            <a href="javascript:;" @click="changeresume">
                <span >
                    <el-icon style="margin-right: 10px;">
                        <Edit />
                    </el-icon>
                    <i>修改简历</i>
                </span>
                <i class="fa-solid fa-chevron-up fa-rotate-90"></i>
            </a>
            <a href="javascript:;" @click="changepwd">
                <span>
                    <el-icon style="margin-right: 10px;">
                        <User />
                    </el-icon>
                    <i>修改密码</i>
                </span>
                <i class="fa-solid fa-chevron-up fa-rotate-90"></i>

            </a>
            <a href="javascript:;" @click="bigdata">
                <span>
                    <el-icon style="margin-right: 10px;">
                        <User />
                    </el-icon>
                    <i>分析大屏</i>
                </span>
                <i class="fa-solid fa-data fa-rotate-90"></i>

            </a>
            <a href="#">
                <span>
                    <el-icon style="margin-right: 10px;"><Service /></el-icon>
                    <i>联系我们</i>

                </span>

                <i class="fa-solid fa-chevron-up fa-rotate-90"></i>
            </a>

        </div>

        
        <a id="logout" href="javascript:;" @click="logout" style="margin-bottom: 70px;">退出登录</a>
    </div>
</template>
<script>
export default {
    props: {
        userinfo: {
            type: Object,
            required: true
        }
    },
    name: 'Mine',

    methods: {
        bigdata(){
            this.$router.push({ path: '/bigview' })
        },
        logout() {
            sessionStorage.clear()
            localStorage.clear()
            this.$router.push('/login')
        },
        login() {
            if (!this.userinfo.is_login) {
                this.$router.push('/login')
            }
        },
        changeresume() {
            this.$router.push({ path: '/resume' })
        },
        changepwd() {
            this.$router.push({ path: '/login', query: { isForget: true, email: this.userinfo.email } })
        },
    }

};
</script>
<style  scoped>
#user {
    padding: 0 20px;
}
.setting span{
    display: flex;
    justify-content: center;
    align-items: center;

}

.userdata {
    width: 100%;
    display: flex;
    height: 70px;
    padding-top: 30px;
    padding-bottom: 10px;

    border-radius: 15px;
    box-sizing: content-box;
}

.mine {
    background-color: #ffffff7d;
    height: 90%;
}

.headerpic {
    width: 70px;
    height: 70px;
    border-radius: 35px;
    /* background-color: rgb(192, 79, 79); */
    border: 1px #80808029 solid;

}

.headerpic img {
    width: 100%;
    height: 100%;
    border-radius: 35px;
}

.accountinfo {
    flex: 1;
    padding: 0 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}

#m_account {
    color: gray;
    font-size: 12px;
    display: flex;
    flex-direction: column;
}

#m_username {
    color: #ff7e3e;
    font-size: 18px;
    cursor: pointer;
}

.m_invitedinfo {
    width: 100%;
    height: 60px;
    display: flex;
    padding: 15px 0;
}

.m_invitedinfo>div {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.m_invitedinfo>div>span:nth-child(2) {
    color: gray;
    font-size: 12px;
}

.m_invitedinfo>div:nth-child(2) {
    border-left: 1px #80808029 solid;
    border-right: 1px #80808029 solid;
}

.pxmu-toast {
    bottom: 80px !important;
}

.fun_card {
    width: 100%;

    padding: 10px 0px;
    background-color: #fff;
    border-radius: 15px;
    border-top: 1px solid #80808029;
    border-bottom: 1px solid #80808029;

}

.fun_card {
    display: flex;

}

.fun_card>a {
    display: flex;
    height: 100%;
    flex: 1;
    flex-direction: column;
    align-items: center;
}

.fun_card>a>span {
    font-size: 12px;
}

.fun_card>a>i {
    font-size: 25px;
    color: #e6a038;
    margin-bottom: 5px;
}

.footer {
    height: 1px;
    width: 100%;
    /* background: rgba(0,0,0,0.8); */
}

#pager {
    margin-top: 20px;
    display: flex;
    height: 45px;
    width: 100%;
    justify-content: center;
    align-items: center;
}

#pager a {
    display: block;
    padding: 0px 5px;

}

#curpage {
    background-color: orange;
    color: white;
}

.setting {
    margin-top: 20px;
    color: black;
    font-weight: 700;
    padding: 15px 20px;
    background-color: #fff;
    border-radius: 15px;
}

.setting>a {
    height: 55px;
    display: flex;

    font-size: 15px;
    align-items: center;
    justify-content: space-between;
}

.setting>div>span {
    width: 85px;
    display: flex;
    justify-content: space-between;
}

.setting * {
    color: #666;
}

#logout {
    margin-top: 20px;
    display: block;
    height: 40px;
    background-color: #fff;
    border-radius: 15px;
    line-height: 40px;
    text-align: center;
}</style>