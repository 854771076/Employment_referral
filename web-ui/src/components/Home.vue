<template>
    <div class="common-layout">
        <el-container>
            <el-header class="navbar-wrapper">
                <el-menu :default-active="activeIndex" class="el-menu" mode="horizontal" :ellipsis="false" :router="true">
                    <!-- <el-menu-item>
                        <img style="width: 100px" src="/src/assets/imgs/logo.png" alt="logo" />
                    </el-menu-item> -->
                    <div class="flex-grow" />
                    <el-menu-item index="/" class="min_hide">首页</el-menu-item>
                    <el-menu-item index="/recommend" class="min_hide">推荐职位</el-menu-item>
                    <el-menu-item index="/job" class="min_hide">找工作</el-menu-item>
                    <el-menu-item index="/company" class="min_hide">找公司</el-menu-item>
                    <el-menu-item index="/mine" class="min_hide" @click="gomine">我的</el-menu-item>
                    <el-menu-item index="/login" v-if="!Islogin"><el-button round>登录/注册</el-button></el-menu-item>
                    <el-menu-item v-if="Islogin" class="min_hide"><el-dropdown>
                            <span class="el-dropdown-link">
                                <el-avatar :size="32" class="mr-3" :src="this.$ApiBaseUrl + userinfo.photo"
                                    style="border: 1px solid gray;" />
                                <span id="username">{{ userinfo.username }}</span>
                                <el-icon class="el-icon--right">
                                    <ArrowDown />
                                </el-icon>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item disabled>用户信息</el-dropdown-item>
                                    <el-dropdown-item divided><strong>手机号:</strong>{{ userinfo.phone }}</el-dropdown-item>
                                    <el-dropdown-item><strong>邮&nbsp;&nbsp;&nbsp;箱:</strong>{{ userinfo.email
                                    }}</el-dropdown-item>
                                    <el-dropdown-item divided disabled>功能</el-dropdown-item>
                                    <el-dropdown-item divided @click="changepwd">修改密码</el-dropdown-item>
                                    <el-dropdown-item @click="changeresume">修改简历</el-dropdown-item>
                                    <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </el-menu-item>


                </el-menu>
            </el-header>
            <el-main class="main">
                <component :is="view" style="margin-top: 15px;" :userinfo="userinfo" ></component>
            </el-main>

            <el-footer>
                
            </el-footer>
            <div class="phone-tabbar">
                <el-menu :default-active="activeIndex" class="el-menu" mode="horizontal" :ellipsis="false" :router="true">
                    
                    <el-menu-item index="/" ><div class="phone-tabbar-item"><el-icon><House /></el-icon><div>首页</div></div></el-menu-item>
                    <el-menu-item index="/recommend" ><div class="phone-tabbar-item"><el-icon><MostlyCloudy /></el-icon><div>推荐</div></div></el-menu-item>
                    <el-menu-item index="/job"><div class="phone-tabbar-item"><el-icon><Suitcase /></el-icon><div>找工作</div> </div></el-menu-item>
                    <el-menu-item index="/company" ><div class="phone-tabbar-item"><el-icon><OfficeBuilding /></el-icon><div>找公司</div></div></el-menu-item>
                    <el-menu-item index="/mine" @click="gomine"><div class="phone-tabbar-item"><el-icon><User /></el-icon><div>我的</div></div></el-menu-item>
                    


                </el-menu>
            </div>
        </el-container>
    </div>
</template>

<script>
import Main from './view/Main.vue'
import Recommend from './view/Recommend.vue'
import Jobs from './view/Jobs.vue'
import Companys from './view/Companys.vue'
import Mine from './view/Mine.vue'
export default {
    created() {
        this.getUserinfo()



    },

    data() {
        return {
            userinfo: {
                id: "-",
                date_joined: "-",
                email: "-",
                is_active: false,
                is_staff: false,
                is_superuser: false,
                last_login: "-",
                last_update: "-",
                phone: "-",
                photo: "/media/default/user.jpg",
                has_resume: true,
                username: "-",
                genderTranslation:'-'
            },
            router: {
                '/': 'Main',
                '/recommend': 'Recommend',
                '/job': 'Jobs',
                '/company': 'Companys',
                '/mine':'Mine'
            },
            view: "",
            activeIndex: '',
            Islogin: false
        }
    },

    watch: {
        $route:{

            handler(newValue, oldValue) {

                this.activeIndex = newValue.path
                this.view = this.router[newValue.path]

            },
            deep: true,
                immediate: true

        }
    },
    methods: {
        gomine(){
            if(!this.Islogin){
            this.$router.push({ path: '/login' })
        }
        },
        logout() {
            // 清除存储的访问令牌和刷新令牌
            localStorage.clear()
            sessionStorage.clear()
            this.$router.push({ path: '/login' })

        },
        changeresume() {
            this.$router.push({ path: '/resume' })
        },
        changepwd() {
            this.$router.push({ path: '/login', query: { isForget: true, email: this.userinfo.email } })
        },

        async getUserinfo() {


            this.$http.get(this.$api.userinfo, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                this.userinfo = response.data.data
                this.Islogin = true
            })

        },
        
    },
    components: {
        Main,
        Recommend,
        Jobs,
        Companys,
        Mine
    }
}
</script>
<style scoped>
.phone-tabbar{
    width: 100%;
    display: none;
    position: fixed;
    bottom: 0;
    height: 60px;
    z-index: 100;

}
.phone-tabbar .el-menu{
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
}
.phone-tabbar-item{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.phone-tabbar-item .el-icon{
    margin: 0;
}
.phone-tabbar-item>div{
    
    line-height: 20px;
    height: auto;
}
/* .el-menu-item [class^=el-icon] {
    height: 100%;
} */

#username {
    line-height: 32px;
    padding: 0 5px;
}

:focus-visible:focus-visible {
    outline: 0;
}

.el-menu--horizontal>.el-menu-item {
    border: 0 !important;
}

.example-showcase .el-dropdown-link {
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
}

.flex-grow {
    flex-grow: 1;
}

.el-menu {
    margin: 0 auto;
    max-width: 1200px;
    border: 0;
    height: 45px;
}

.main {
    margin: 0 auto;
    max-width: 1200px;
    width: 100%;
}

.navbar-wrapper {
    border-bottom: solid 1px var(--el-menu-border-color);
    height: 45px;
}

@media screen and (max-width: 568px) {
    .min_hide {
        display: none !important;
    }

    .main {
        width: 100%;
    }
    .phone-tabbar{
        display: block;
    }
}
</style>