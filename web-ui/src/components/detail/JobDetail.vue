<template>
    <Snav>
        <template v-slot:name>岗位详细</template>
    </Snav>
    <div
        style="width:100%;background-color:rgba(255, 255, 255, 0.726);box-shadow:0 3px 10px 0 rgba(0,0,0,.12);margin-bottom: 20px;padding-top: 45px;">
        <div class="info">
            <div class="baseinfo">
                <el-tooltip class="box-item" effect="dark" :content="jobinfo.name" placement="bottom">
                    <h1 class="name">{{ jobinfo.name.length <= 9 ? jobinfo.name : jobinfo.name.slice(0, 9) + '...' }} </h1>
                </el-tooltip>

                <p style="font-size: 15px">
                    <span v-if="jobinfo.workcity" style="margin-right: 15px;"><el-icon style="vertical-align: middle;">
                            <Location />
                        </el-icon>{{ jobinfo.workcity }}</span>
                    <span v-if="jobinfo.workingexp" style="margin-right: 15px;"><el-icon style="vertical-align: middle;">
                            <Suitcase />
                        </el-icon> {{ jobinfo.workingexp }}</span>
                    <span v-if="jobinfo.education"><el-icon style="vertical-align: middle;">
                            <Reading />
                        </el-icon>{{ jobinfo.education }}</span>

                </p>
                <p class="salary">{{ jobinfo.salary60 }}</p>

            </div>
            <div class="tag">

                <el-tag class="ml-2" size="large">{{ jobinfo.worktype }}</el-tag>
                <div class="btn">

                    <el-button type="info" disabled><el-icon>

                            <View />
                        </el-icon>{{ viewer }}浏览</el-button>
                    <el-button type="success"><a :href="jobinfo.positionurl" style="color: white;">申请职位</a></el-button>
                    <el-button type="warning" v-if="!iscollected" @click="Collected(jobinfo.number)"><el-icon style="vertical-align: middle;"
                            >
                            <StarFilled />
                        </el-icon>收藏</el-button>
                    <el-button type="warning" v-if="iscollected" @click="removeCollected(jobinfo.number)"><el-icon style="color: yellow;vertical-align: middle;"
                            >
                            <StarFilled />
                        </el-icon> 已收藏</el-button>

                </div>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="job-detail">
            <div class="job-detail-section">
                <h2>职位描述</h2>
                <div class="job-detail-tags">
                    <template v-for="tag3 in jobinfo.industryname.split('/')" v-if="jobinfo.industryname">
                        <el-tag class="ml-2" size="large">{{ tag3 }}</el-tag>
                    </template>
                    <el-tag class="ml-2" size="large"
                        v-if="jobinfo.workingexpcode == 0 || jobinfo.workingexpcode == -1">无经验要求</el-tag>
                    <el-tag class="ml-2" size="large" v-if="jobinfo.educationcode == -1">无学历要求</el-tag>
                    <el-tag class="ml-2" size="large" v-if="jobinfo.property">{{ jobinfo.property }}</el-tag>
                    <template v-for="tag4 in jobinfo.subjobtypelevelname.split('/')" v-if="jobinfo.subjobtypelevelname">
                        <el-tag class="ml-2" size="large">{{ tag4 }}</el-tag>
                    </template>
                </div>
                <div class="summary" style="margin-top: 50px;">
                    {{ jobinfo.jobsummary }}
                </div>
                <h2 style="margin-top: 50px;">薪资情况</h2>
                <div style="margin-top: 20px;">

                    <strong>薪资范围：</strong>{{ jobinfo.salaryreal }}
                    <br>
                    <template v-for="tag2 in jobinfo.welfaretaglist.split('/')" v-if="jobinfo.welfaretaglist">
                        <el-tag class="ml-2" size="large" style="margin-right: 15px;margin-top: 15px;">{{ tag2 }}</el-tag>
                    </template>
                </div>
                <h2 style="margin-top: 30px;" v-if="jobinfo.skilllabel">技能要求</h2>
                <div style="margin-top: 20px;">
                    <template v-for="tag1 in jobinfo.skilllabel.split('/')" v-if="jobinfo.skilllabel">
                        <el-tag class="ml-2" size="large" style="margin-right: 15px;margin-top: 15px;">{{ tag1 }}</el-tag>
                    </template>
                </div>
                <h2 style="margin-top: 30px;" v-if="jobinfo.skilllabel">地址</h2>
                <div style="margin-top: 20px;" v-if="jobinfo.workcity">
                    <span>
                        {{ jobinfo.workcity }}&nbsp;
                        <span v-if="jobinfo.citydistrict">-&nbsp;{{ jobinfo.citydistrict }}</span>
                        <span v-if="jobinfo.streetname">-&nbsp;{{ jobinfo.streetname }}</span>
                    </span>
                </div>
                <Comment :number="number"></Comment>
            </div>
        </div>
        <div class="sider">
            <div>

                <p class="title">公司基本信息</p>
                <div class="company-info">
                    <a class="job-detail-company-logo_custompage" :href="'/company/detail/' + jobinfo.companynumber">
                        <el-image
                            style="width: 48px; height: 48px;display: flex;align-items: center;justify-content: center;border-radius: 15px;"
                            :src="jobinfo.companylogo" alt="" />
                    </a>
                    <el-tooltip class="box-item" effect="dark" :content="jobinfo.companyname" placement="bottom">
                        <a class="job-detail-company_custompage" :href="'/company/detail/' + jobinfo.companynumber">

                            {{ jobinfo.companyname.length <= 9 ? jobinfo.companyname : jobinfo.companyname.slice(0, 9)
                                + '...' }} </a>
                    </el-tooltip>

                </div>
                <p style="padding: 0 24px;" v-if="jobinfo.companysize">
                    <el-icon style="margin-right: 20px;">
                        <UserFilled />
                    </el-icon>
                    {{ jobinfo.companysize }}
                </p>
                <p style="padding: 0 24px;" v-if="jobinfo.industryname">
                    <el-icon style="margin-right: 20px;">
                        <OfficeBuilding />
                    </el-icon>
                    {{ jobinfo.industryname }}
                </p>

            </div>
            <div>
                <p class="title">相似职位</p>
                <template v-for="job in similarjobs" v-if="similarjobs.length!=0">
                    <div class="simlaryjob">
                        <div class="simlaryjobinfo">
                            <el-tooltip class="box-item" effect="dark" :content="job.name" placement="bottom">
                                <a :href="'/job/detail/' + job.number">

                                    {{ job.name.length <= 9 ? job.name : job.name.slice(0, 9) + '...' }} </a>
                            </el-tooltip>
                            <div class="salary">
                                {{ job.salary60 }}
                            </div>
                        </div>
                        <div class="simlarycompanyinfo">
                            <div>
                                <el-image
                                    style="width: 24px; height: 24px;display: flex;align-items: center;justify-content: center;border-radius: 24px;margin-right: 15px;"
                                    :src="job.companylogo" alt="" />
                                <el-tooltip class="box-item" effect="dark" :content="job.companyname" placement="bottom">
                                    <a :href="'/company/detail/' + job.companynumber">
                                        {{ job.companyname.length <= 9 ? job.companyname : job.companyname.slice(0, 9)
                                            + '...' }} </a>
                                </el-tooltip>

                            </div>
                            {{ job.workcity }}
                        </div>
                    </div>
                </template>
                <template v-else>
                    <div class="simlaryjob">
                        <div class="simlaryjobinfo">
                             <el-empty description="description" style="width: 100%;" />
                        </div>
                        
                    </div>
                </template>

            </div>
        </div>
    </div>
</template>
<script>
import Snav from '../utils/Snav.vue'
import Comment from '../detail/Comment.vue'
export default {

    name: 'JobDetail',
    created() {
        const number = this.$route.params.number;
        this.number =number 
        this.getJobInfo(number)
        this.getsimilarjobs(number)
        this.clickjob(number)
        this.isCollected(number)
    },
    data() {
        return {
            jobinfo: {
                name: '',
                companyname: ''
            },
            similarjobs: [],
            iscollected: false,
            viewer: 0
        };
    },

    methods: {
        async removeCollected(number) {
            let response = await this.$http
                .post(this.$api.removecollect, { number: number })
                .then(response => {
                    if(response.data.code==200){
                        this.iscollected = false
                    }else{
                        this.$Message({type:'warning',message:response.data.msg})
                    }
                    
                })
                .catch(error => {
                    this.$Message({type:'warning',message:'系统异常'})
                });
        },
        async Collected(number) {
            let response = await this.$http
                .post(this.$api.collect, { number: number })
                .then(response => {
                    if(response.data.code==200){
                        this.iscollected = true
                    }else{
                        this.$Message({type:'warning',message:response.data.msg})
                    }
                })
                .catch(error => {
                });
        },
        async isCollected(number) {
            let response = await this.$http
                .post(this.$api.iscollected, { number: number })
                .then(response => {
                    this.iscollected = response.data.data
                    
                })
                .catch(error => {
                });
        },
        async clickjob(number) {
            let response = await this.$http
                .post(this.$api.clickjob, { number: number })
                .then(response => {
                    this.viewer = response.data.data.sum?response.data.data.sum:0
                })
                .catch(error => {
                });
        },
        async getJobInfo(number) {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .get(this.$api.jobs + number + '/')
                .then(response => {
                    this.jobinfo = response.data
                    console.log(response.data)
                    Loading.close()
                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('未查询到数据')
                });

        }
        ,
        async getsimilarjobs(number) {
            let response = await this.$http
                .get(this.$api.similarjobs + number + '/')
                .then(response => {
                    this.similarjobs = response.data.results
                })
                .catch(error => {
                    // this.$Message.error('未查询到数据')
                });

        }
    },
    components: {
        Snav,
        Comment
    }
}
</script>
<style scoped>
.simlaryjobinfo {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.simlaryjobinfo a {
    font-size: 18px;
}

.simlaryjobinfo:hover a {
    color: orange;
}

.simlarycompanyinfo {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    line-height: 24px;
}

.simlarycompanyinfo>div {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    line-height: 24px;
}

.simlarycompanyinfo:hover a {
    color: orange;
}

.simlaryjob:hover {
    background: rgba(0, 0, 0, 0.1);
}

.simlaryjob {
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

.job-detail-company-logo_custompage {
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

.job-detail-company_custompage {
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

.job-detail-tags {
    margin-top: 15px;

}

.job-detail-tags>* {
    margin-right: 15px;
    margin-top: 15px;
}

.job-detail-section {
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
    height: 215px;
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

.tag {
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

.job-detail {
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
        flex: 1
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

    .sider div {
        /* width: 100%; */
    }
}
</style>