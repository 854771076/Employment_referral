<template>
    <div class="search-input" >
        <el-select v-model="query.type" class="m-2">
            <el-option v-for="item in [{ code: '0', name: '职位' }, { code: '1', name: '企业' }]" :key="item.name"
                :label="item.name" :value="item.code" />
        </el-select>
        <el-input placeholder="关键词" v-model="query.keywords" clearable>
        </el-input>
        <el-button type="primary" @click="search"><el-icon>
                <search />
            </el-icon></el-button>
    </div>
    <div class="block text-center " m="t-4">
        <div class="job m-hide">
            <div class="bg">
                <el-carousel trigger="click" height="400px">
                    <el-carousel-item v-for="item in imgs" :key="item">

                        <a :href="item.href" target="_blank">
                            <el-image style="width: 100%; height: 100%" :src="item.url" />
                        </a>
                    </el-carousel-item>
                </el-carousel>
            </div>
            <div class="jobType">
                <template v-for="item in $baseData.jobType.slice(1, 9)">
                    <div class="jobtype-item">
                        <a href="#"> {{ item.name }}</a>
                        <div class="sub-items">
                            <h3>{{ item.name }}</h3>
                            <div class="sub-items-content">
                                <template v-for="sub in item.sublist">
                                    <div>
                                        <h4 >{{ sub.name }}</h4>
                                        <template v-for="sub in sub.sublist">
                                        <a :href="`/job?subjobtypelevel=${sub.code}`">{{ sub.name }}</a>
                                        </template>
                                    </div>
                                    

                                </template>
                            </div>

                        </div>
                    </div>
                </template>
                <div class="jobtype-item">
                    <a href="#">更多类型</a>

                </div>
            </div>
        </div>
        <div class="main-carousel">
            <el-carousel trigger="click" height="400px" width="700px">
                <el-carousel-item v-for="item in imgs" :key="item">

                    <a :href="item.href">
                        <el-image style="width: 100%; height: 100%" :src="item.url" />
                    </a>
                </el-carousel-item>
            </el-carousel>

        </div>

    </div>
    <div class="hotjob" style="margin-top: 50px;margin-bottom: 40px;">
        <h1>热招岗位</h1>
        <el-menu :default-active="jobtypeinit" class="el-menu-hotjob" mode="horizontal" :ellipsis="true" @select="getHotJob"
            style="height: 45px">
            <div class="flex-grow" />
            <!-- <template v-for="item in $baseData.jobType[3].sublist[0].sublist.slice(0, 10)">
                <el-menu-item :index="item.code">{{ item.name.split('/')[0] }}</el-menu-item>
            </template> -->
            <template v-for="item in $baseData.jobType.slice(1,)">
                <el-sub-menu :index="item.code">
                    <template #title>{{ item.name }}</template>
                    <template v-for="item2 in item.sublist">
                        <el-sub-menu :index="item2.code">
                            <template #title>{{ item2.name }}</template>
                            <template v-for="item3 in item2.sublist">
                                <el-menu-item :index="item3.code">
                                    {{ item3.name }}

                                </el-menu-item>
                            </template>
                        </el-sub-menu>

                    </template>
                </el-sub-menu>


            </template>
        </el-menu>
        <div class="hotjob-items">
            <template v-for="i in 9">
                <div class="hotjob-item-bg" v-show="!hotjobstatus">
                    <el-skeleton :rows="1" />
                    <br />
                    <el-skeleton style="--el-skeleton-circle-size: 24px">
                        <template #template>
                            <el-skeleton-item variant="circle" />
                        </template>
                    </el-skeleton>
                </div>

            </template>
            <template v-for="job in HotJob.slice(0, 9)">
                <div class="hotjob-item" v-show="hotjobstatus">
                    <div class="card-header">
                        <el-badge value="Hot" class="item">
                            <div class="card-title">
                                <el-tooltip class="box-item" effect="dark" :content="job.name" placement="bottom">
                                    <a :href="'/job/detail/'+job.number">{{ job.name.slice(0, 10) }}...</a>
                                </el-tooltip>
                                
                            </div>
                        </el-badge>

                        <div class="salary">{{ job.salary60 }}</div>
                    </div>
                    <div class="card-body">
                        <div class="card-info">
                            <span v-if="job.workcity">
                            {{ job.workcity }}&nbsp;
                            <span v-if="job.citydistrict">-&nbsp;{{job.citydistrict }}</span>
                            <span v-if="job.streetname">-&nbsp;{{job.streetname }}</span>
                            </span><span v-if="job.workingexp">&nbsp;|&nbsp;{{
        job.workingexp }}</span><span v-if="job.education">&nbsp;|&nbsp;{{ job.education }}</span>
                        </div>
                        <div class="tags">
                            <template v-for="tag1 in job.skilllabel.split('/').slice(0, 2)" v-if="job.skilllabel">
                                <el-tag class="ml-2" type="info">{{ tag1 }}</el-tag>
                            </template>
                            <template v-for="tag2 in job.welfaretaglist.split('/').slice(0, 2)" v-if="job.welfaretaglist">
                                <el-tag class="ml-2" type="info">{{ tag2 }}</el-tag>
                            </template>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div>
                            <el-avatar :size="24" :src="job.companylogo" alt="" v-if="job.companylogo"
                                style="margin-right:15px" />
                            <el-tooltip class="box-item" effect="dark" :content="job.companyname" placement="bottom">
                                <a :href="'/company/detail/'+job.companynumber">{{ job.companyname.slice(0, 4) }}...</a>
                            </el-tooltip>

                        </div>
                        <div>
                            <span v-if="job.industryname">{{ job.industryname }}</span><span
                                v-if="job.companysize">&nbsp;|&nbsp;{{ job.companysize }}</span>
                            <span v-if="job.property">&nbsp;|&nbsp;{{ job.property }}</span>
                        </div>
                    </div>
                </div>

            </template>
        </div>
    </div>
    <div class="hotcompany">
        <h1>热门企业</h1>
        <div class="hotcompany-items" >
            <template v-for="i in 9">
                <div class="hotcompany-item-bg" v-show="!hotcompanystatus">
                    <el-skeleton :rows="1"  />
                    <br />
                    <el-skeleton style="--el-skeleton-circle-size: 24px" >
                        <template #template>
                            <el-skeleton-item variant="circle" />
                        </template>
                    </el-skeleton>
                </div>

            </template>
            <template v-for="company in HotCompany.slice(0, 9)">
                <div class="hotcompany-item" v-show="hotcompanystatus">
                    <div class="card-header">
                        <el-badge value="Hot" class="item">
                            <div class="card-title">
                                <el-tooltip class="box-item" effect="dark" :content="company.companyname" placement="bottom">
                                    <a :href="'/company/detail/'+company.companynumber" >{{ company.companyname.slice(0, 10) }}...</a>
                                </el-tooltip>
                                
                            </div>
                        </el-badge>

                        <div class="salary">{{ company.job_num }}</div>
                    </div>
                    <div class="card-body">

                        <div class="tags">
                            <template v-for="tag1 in company.industryname.split('/').slice(0, 4)"
                                v-if="company.industryname">
                                <el-tag class="ml-2" type="info">{{ tag1 }}</el-tag>
                            </template>
                            <template v-for="tag2 in company.companyscaletypetagsnew.split('/')"
                                v-if="company.companyscaletypetagsnew">
                                <el-tag class="ml-2" type="info">{{ tag2 }}</el-tag>
                            </template>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div>
                            <el-avatar :size="24" :src="company.companylogo" alt="" v-if="company.companylogo"
                                style="margin-right:15px" />


                        </div>
                        <div>
                            <span v-if="company.companysize">{{ company.companysize }}</span>
                            <span v-if="company.property">&nbsp;|&nbsp;{{ company.property }}</span>
                        </div>
                    </div>
                </div>

            </template>
        </div>
    </div>
</template>
  
<script>
import img1 from '../../assets/imgs/1.jpg'
import img2 from '../../assets/imgs/2.jpg'
import img3 from '../../assets/imgs/3.jpg'
export default {
    name: 'Main',
    async created() {
        this.getHotJob(this.jobtypeinit)
        this.getHotCompany()

    },
    props: {
        userinfo: {
            type: Object,
            required: true,
        },

    },
    data() {
        return {
            query: {
                type: '0',
                keywords: ''
            },

            imgs: [
                { url: img1, href: 'https://edu.51testing.net/htm/51PC/zlzs.html' },
                { url: img2, href: 'http://zhaopin.chinatowercom.cn/campus' },
                { url: img3, href: 'https://xiaoyuan.zhaopin.com/company/KA0133889514D90000001000' }],
            HotJob: [],
            hotjobstatus: false,
            HotCompany: [],
            hotcompanystatus: false,
            jobtypeinit: '19000200100000'

        };
    },
    methods: {
        
        search(){
            if(this.query.type=='0'){
                window.location.href='/job'+`?keywords=${this.query.keywords}`
            }else{
                window.location.href='/company'+`?keywords=${this.query.keywords}`

            }
        },
        async clickjob(number){
            let response = await this.$http
                .post(this.$api.clickjob ,{number:number})
                .then(response => {
                })
                .catch(error => {
                    debagger;
                });
        },
        async getHotJob(code) {
            // let Loading = this.$Loading({ fullscreen: true })
            this.hotjobstatus = false
            let response = await this.$http
                .get(this.$api.jobs + `?subjobtypelevel=${code}&ordering=-publishtime`)
                .then(response => {
                    if (response.data.results.length == 0) {
                        this.$Message({ type: 'warning', message: '未查询到数据' })
                    }
                    this.HotJob = response.data.results
                    this.hotjobstatus = true
                })
                .catch(error => {
                    // Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });

        },
        async getHotCompany() {
            // let Loading = this.$Loading({ fullscreen: true })
            this.hotcompanystatus = false
            let response = await this.$http
                .get(this.$api.companys + `?ordering=-job_num`)
                .then(response => {
                    if (response.data.results.length == 0) {
                        this.$Message({ type: 'warning', message: '未查询到数据' })
                    }
                    this.HotCompany = response.data.results
                    this.hotcompanystatus = true
                })
                .catch(error => {
                    // Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });
        },

    },
    components: {

    }
};
</script>
  
<style scoped>

.el-select {
    width: 100px;

}

.el-input__wrapper>* {
    height: 100% !important;
}

.el-input {
    :deep(.el-input__wrapper) {
        border: none !important;
        box-shadow: none !important;
    }

    :deep(.el-input__inner) {
        border: none !important;
        box-shadow: none !important;
    }
}

:deep(.el-input__wrapper) {
    box-shadow: none !important;
    border-radius: 10px;
}

.el-select {
    min-width: 75px !important;

}

.el-button {
    width: 75px;
    border: 0 !important;
    box-shadow: none !important;
    border-radius: 0 10px 10px 0;
    color: none;
}

.el-input__inner {
    border: 0 !important;
    box-shadow: none;
    background-color: none;
}

.jobType {
    height: 400px;
    width: 250px;
    background: rgba(79, 90, 102, .6);
    -webkit-backdrop-filter: blur(35px);
    backdrop-filter: blur(35px);
    z-index: 100;
    position: relative;
    top: -400px;
    padding: 10px 0;
}

.jobtype-item {
    height: 42px;
    padding-left: 24px;
    padding-right: 16px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    cursor: pointer;


}

.jobtype-item a {
    line-height: 42px;
    color: white;
    font-size: 14px;
    font-family: PingFangSC-Medium, PingFang SC;
    font-weight: 500;
    text-decoration: none;
}

.search-input {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    margin-bottom: 15px;
    border: 1px var(--el-menu-border-color) solid;
    border-radius: 10px;
    background-color: white;
}

.jobtype-item:hover {
    background-color: rgba(0, 0, 0, 0.3);
}

.jobtype-item:hover .sub-items {
    display: block;
}

.sub-items-content {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;

}

.sub-items-content a {
    color: gray !important;
}

.sub-items h3 {
    margin-bottom: 15px;
}

.sub-items-content a {
    margin-right: 15px;
}

.text-center {
    display: flex;
    flex-direction: row;
}

.main-carousel {
    /* width: 900px; */
    flex: 1;
    position: relative;
}

.bg {
    width: 100%;
    height: 100%;
}

.el-input__wrapper {
    padding: 0 !important;

}

.el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
    text-align: center;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}
</style>
  