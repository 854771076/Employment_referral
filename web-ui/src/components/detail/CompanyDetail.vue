<template>
    <Snav>
        <template v-slot:name>企业详细</template>
    </Snav>
    <div
        style="width:100%;background-color:rgba(255, 255, 255, 0.726);box-shadow:0 3px 10px 0 rgba(0,0,0,.12);margin-bottom: 20px;padding-top: 45px;">
        <div class="info">
            <div class="baseinfo">
                <div style="    display: flex;align-items: center;">
                    <div>
                        <el-image
                            style="width: 70px; height: 70px;display: flex;align-items: center;justify-content: center;border-radius: 15px;margin-right: 10px;"
                            :src="companyinfo.companylogo" alt="" />
                    </div>
                    <div style="">
                        <el-tooltip class="box-item" effect="dark" :content="companyinfo.companyname" placement="bottom">
                            <h1 class="name">{{ companyinfo.companyname.length <= 9 ? companyinfo.companyname :
                                companyinfo.companyname.slice(0, 7) + '...' }} </h1>
                        </el-tooltip>

                        <p style="font-size: 15px">
                            <span v-if="companyinfo.companysize" style="margin-right: 15px;"><el-icon
                                    style="vertical-align: middle;">
                                    <UserFilled />
                                </el-icon>{{ companyinfo.companysize }}</span>
                            <span v-if="companyinfo.industryName" style="margin-right: 15px;"><el-icon
                                    style="vertical-align: middle;">
                                    <OfficeBuilding />
                                </el-icon> {{ companyinfo.industryName }}</span>


                        </p>

                    </div>
                </div>

            </div>
            <div class="tag">

                <div><strong style="color:orange;font-size: 20px;">{{ companyinfo.job_num }}</strong>在招职位</div>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="company-detail">
            <div class="company-detail-section">
                <h2>在招职位</h2>
                <ul v-infinite-scroll="getjobs" class="infinite-list" style="overflow: auto">
                    <li v-for="i,index in jobs" :key="i.number" class="infinite-list-item">
                        <div class="jobinfo">
                            <div class="index" style="margin-right: 15px;">{{ index+1 }}</div>
                            <el-tooltip class="box-item" effect="dark" :content="i.name" placement="bottom">
                                <a :href="'/job/detail/' + i.number" style="display: flex;justify-content: space-between;align-items: center;flex:1">

                                    {{ i.name.length <= 9 ? i.name : i.name.slice(0, 9) + '...' }} 
                                    <div class="salary" >
                                {{ i.salary60 }}
                            </div>
                                </a>
                            </el-tooltip>
                            
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <div class="sider">
            <div>
                <p class="title">其他信息</p>
                <p style="padding: 0 24px;">
                    <template v-for="tag1 in companyinfo.companyscaletypetagsnew.split('/')"
                        v-if="companyinfo.companyscaletypetagsnew">
                        <el-tag class="ml-2" size="large" style="margin-right: 15px;margin-top: 15px;">{{ tag1 }}</el-tag>
                    </template>
                    <el-tag class="ml-2" size="large" style="margin-right: 15px;margin-top: 15px;"
                        v-if="companyinfo.property">{{ companyinfo.property }}</el-tag>
                </p>

            </div>
        </div>
    </div>
</template>
<script>
import Snav from '../utils/Snav.vue'
export default {

    name: 'companyDetail',
    created() {
        const number = this.$route.params.number;
        this.getcompanyInfo(number)

    },
    data() {
        return {
            companyinfo: {
                companyname: ''
            },
            jobs: [],
            maxpage: 1,
            page:1
        };
    },

    methods: {

        async getcompanyInfo(number) {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .get(this.$api.companys + number + '/')
                .then(response => {
                    this.companyinfo = response.data
                    Loading.close()
                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('未查询到数据')
                });

        }
        ,
        async getjobs() {

            if (this.page <= this.maxpage && this.companyinfo.companynumber) {
                let Loading = this.$Loading({ fullscreen: true })
                let response = await this.$http
                    .get(this.$api.jobs+`?companynumber=${this.companyinfo.companynumber}&ordering=-publishtime&page=${this.page}`)
                    .then(response => {
                        this.jobs=[...this.jobs, ...response.data.results]
                        this.maxpage =Math.ceil(response.data.count / 20)

                        this.page+=1
                        Loading.close()
                    })
                    .catch(error => {
                        Loading.close()
                        this.$Message.error('未查询到数据')
                    });
            }
            
        }

    },
    components: {
        Snav
    }
}
</script>
<style scoped>
.infinite-list {
    max-height: 600px;
    min-height: 100px;
    padding: 0;
    margin: 0;
    list-style: none;
}

.infinite-list .infinite-list-item {

    height: 50px;
    margin: 10px;
}

.infinite-list .infinite-list-item+.list-item {
    margin-top: 10px;
}

.jobinfo {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.jobinfo a {
    font-size: 18px;
}

.jobinfo:hover a {
    color: orange;
}

.jobinfo {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    line-height: 24px;
}

.jobinfo>div {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    line-height: 24px;
}

.jobinfo:hover a {
    color: orange;
}

.job:hover {
    background: rgba(0, 0, 0, 0.1);
}

.job {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    line-height: 26px;
    color: #414a60;
    font-size: 14px;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    list-style: none;
    border-radius: 8px;
    padding: 12px 16px;
    transition: all .2s linear;
}

.company-detail-company-logo_custompage {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    font-size: 16px;
    font-weight: 500;
    line-height: 22px;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    color: #414a60;
    float: left;
    width: 48px;
    height: 48px;
    margin-right: 16px;
    border: 1px solid #f3f5fb;
    border-radius: 8px;
}

.company-detail-company_custompage {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    font-size: 16px;
    font-weight: 500;
    line-height: 22px;
    padding: 0;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    text-decoration: none;
    color: #414a60;
}

.company-info {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    overflow: hidden;
    display: flex;
    align-items: center;
    padding: 16px 24px;
    margin-bottom: 4px;
    font-size: 16px;
    font-weight: 500;
    color: #222;
    line-height: 22px;
}

.main {
    display: flex;
    flex-direction: row;
}

.name {
    text-align: left;
}

.title {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    display: flex;
    align-items: center;
    font-size: 16px;
    font-weight: 500;
    color: #222;
    line-height: 22px;
    padding: 12px 24px;
    background: linear-gradient(90deg, #f5fcfc 0, #fcfbfa 100%);
    margin-bottom: 0;
    border-radius: 12px 12px 0 0;
}

.sider>div {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    line-height: 26px;
    color: #414a60;
    font-size: 14px;
    padding: 0;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    border-radius: 12px;
    padding-bottom: 20px;
    background: #fff;
    margin-bottom: 16px;
}

.company-detail-tags {
    margin-top: 15px;

}

.company-detail-tags>* {
    margin-right: 15px;
    margin-top: 15px;
}

.company-detail-section {
    font-family: arial, verdana, helvetica, 'PingFang SC', 'HanHei SC', STHeitiSC-Light, Microsoft Yahei, sans-serif;
    -webkit-font-smoothing: antialiased;
    line-height: 26px;
    color: #414a60;
    font-size: 14px;
    margin: 0;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    background: #fff;
    border-radius: 12px;
    padding: 20px 30px;
}

.info {
    padding: 20px 10px;
    height: 140px;
    top: 0;
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    display: flex;
    justify-content: space-between
}

.salary {
    font-size: 20px;
    padding: 10px 0;
}

.baseinfo {
    min-width: 300px;
}

.baseinfo>div {
    width: 100%;
}

.tag {
    line-height: 100px;
    width: 300px;
    position: relative;
    padding-bottom: 20px;
    white-space: nowrap;
    /* 禁止文本换行 */
    overflow: hidden;
    /* 超出部分隐藏 */
    text-overflow: ellipsis;

}

.tag>* {
    margin-right: 15px;
}

.btn {
    position: absolute;
    bottom: 15px;
    left: 0
}

.company-detail {
    flex: 1;
    margin: 0 10px;
}

.sider {
    width: 280px;
    margin: 0 10px !important;
}

@media screen and (max-width: 568px) {
    .info {
        flex-direction: column;
        padding: 0 15px;
    }

    .tag {
        flex: 1;
        line-height: 60px;
    }

    .name {
        text-align: center !important;
    }

    .main {
        flex-direction: column;
    }

    .sider {
        flex: 1;
        width: unset;
    }


}</style>