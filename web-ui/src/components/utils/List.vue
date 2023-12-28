<template>
    <div class="query" v-if="listType != 0">
        <div class="search-input">

            <el-input placeholder="关键词" v-model="Q.keywords" clearable>
            </el-input>
            <el-button type="primary" @click="submit"><el-icon>
                    <search />
                </el-icon></el-button>

        </div>
        <div class="select-input">
            <div class="address">
                <el-form-item label="工作地址" v-if="listType!=2">
                    <el-select v-model="Q.city" class="m-2" placeholder="省" @change="clearaddress()">
                        <el-option label="不限" value="" />
                        <el-option v-for="item in this.$baseData.allCity" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                    <el-select v-model="Q.citydistrict" class="m-2" placeholder="市">
                        <el-option label="不限" value="" />
                        <el-option v-for="item in citysub" :key="item.name" :label="item.name" :value="item.code" />
                    </el-select>
                </el-form-item>

            </div>
            <div class="more"
                style="margin:15px 0;display:flex;flex-wrap: wrap;justify-content: flex-start;align-items: center;">

                <el-form-item label="工作经验" v-if="listType!=2">
                    <el-select v-model="Q.workingexpCode" class="m-2" placeholder="工作经验">
                        <el-option v-for="item in this.$baseData.workExpType" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                </el-form-item>
                <el-form-item label="企业类型">
                    <el-select v-model="Q.propertycode" class="m-2" placeholder="企业类型">
                        <el-option v-for="item in this.$baseData.companyType" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                </el-form-item>
                <el-form-item label="职位类型" v-if="listType!=2">

                    <el-tree-select placeholder="职位类型" v-model="Q.subjobtypelevel" :props="props"
                        :data="this.$baseData.jobType" filterable />
                </el-form-item>
                <el-form-item label="工作类型" v-if="listType!=2">
                    <el-select v-model="Q.worktypeCode" class="m-2" placeholder="工作类型">
                        <el-option v-for="item in this.$baseData.jobStatus" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                </el-form-item>

                <el-form-item label="薪资范围" v-if="listType!=2">
                    <el-select v-model="Q.salarytype" class="m-2" placeholder="薪资待遇">
                        <el-option v-for="item in this.$baseData.salaryType" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                </el-form-item>
                <el-form-item label="公司规模">
                    <el-select v-model="Q.companysize" class="m-2" placeholder="公司规模">
                        <el-option v-for="item in this.$baseData.companySize" :key="item.name" :label="item.name"
                            :value="item.name" />
                    </el-select>
                </el-form-item>
                <el-form-item label="学历" v-if="listType!=2">
                    <el-select v-model="Q.eduHighestLevel" class="m-2" placeholder="学历">
                        <el-option v-for="item in this.$baseData.educationType" :key="item.name" :label="item.name"
                            :value="item.code" />
                    </el-select>
                </el-form-item>
            </div>
        </div>

    </div>

    <div class="list">
        <template v-for="job in listData">
            <div class="list-items" v-if="listType!=2">
                <div class="list-items-body">
                    <div class="jobs">
                        <p>
                            <template v-if="job.type">
                                <el-badge :value="job.type" class="item">
                                <el-tooltip class="box-item" effect="light" :content="job.name" placement="bottom">
                                    <a :href="'/job/detail/' + job.number+'?page='+this.currentPage">{{ job.name.length <= 9 ? job.name :
                                        job.name.slice(0, 9) + '...' }} </a>

                                </el-tooltip>
                            </el-badge>
                            </template>
                            <template v-else>
                                <el-tooltip class="box-item" effect="light" :content="job.name" placement="bottom">
                                    <a :href="'/job/detail/' + job.number+'?page='+this.currentPage">{{ job.name.length <= 9 ? job.name :
                                        job.name.slice(0, 9) + '...' }} </a>

                                </el-tooltip>
                            </template>

                            <span v-if="job.workcity">
                                [{{ job.workcity }}
                                <span v-if="job.citydistrict">·{{ job.citydistrict }}</span>
                                <span v-if="job.streetname">·{{ job.streetname }}</span>]
                            </span>
                        </p>
                        <p style="margin-top: 15px;">
                            <span class="salary">
                                {{ job.salary60 }}
                            </span>
                            <el-tag class="ml-2" type="info" v-if="job.workingexp">{{ job.workingexp }}</el-tag>
                            <el-tag class="ml-2" type="info" v-if="job.education">{{ job.education }}</el-tag>

                        </p>
                    </div>
                    <div class="companys">
                        <div>
                            <el-image
                                style="width: 55px; height: 55px;display: flex;align-items: center;justify-content: center;border-radius: 15px;margin-right: 10px;"
                                :src="job.companylogo" alt="" />
                        </div>
                        <div>
                            <el-tooltip class="box-item" effect="dark" :content="job.companyname" placement="bottom">
                                <a :href="'/company/detail/' + job.companynumber+'?page='+this.currentPage">{{ job.companyname.length <= 9 ?
                                    job.companyname : job.companyname.slice(0, 7) + '...' }}</a>
                            </el-tooltip>

                            <p style="font-size: 15px">
                                <span v-if="job.companysize" style="margin-right: 15px;"><el-icon
                                        style="vertical-align: middle;">
                                        <UserFilled />
                                    </el-icon>{{ job.companysize }}</span>
                                <br>
                                <span v-if="job.industryname" style="margin-right: 15px;"><el-icon
                                        style="vertical-align: middle;">
                                        <OfficeBuilding />
                                    </el-icon> {{ job.industryname }}</span>


                            </p>

                        </div>
                    </div>
                </div>
                <div class="list-items-footer">
                    <span>{{ job.skilllabel.replace(/\//g, ' | ') }}</span>
                    <span class="welfaretaglist">{{ job.welfaretaglist.replace(/\//g, ' | ') }}</span>


                </div>
            </div>
            <div class="list-items" v-else>
                <div class="list-items-body">
                    
                    <div class="companys2" >
                        <div>
                            <el-image
                                style="width: 55px; height: 55px;display: flex;align-items: center;justify-content: center;border-radius: 15px;margin-right: 10px;"
                                :src="job.companylogo" alt="" />
                        </div>
                        <div>
                            <template v-if="job.companyscaletypetagsnew">
                                <el-badge :value="job.companyscaletypetagsnew" class="item">
                                <el-tooltip class="box-item" effect="dark" :content="job.companyname" placement="bottom">
                                <a :href="'/company/detail/' + job.companynumber+'?page='+this.currentPage">{{ job.companyname.length <= 9 ?
                                    job.companyname : job.companyname.slice(0, 7) + '...' }}</a>
                            </el-tooltip>
                            </el-badge>
                            </template>
                            <template v-else>
                                <el-tooltip class="box-item" effect="dark" :content="job.companyname" placement="bottom">
                                <a :href="'/company/detail/' + job.companynumber+'?page='+this.currentPage">{{ job.companyname.length <= 9 ?
                                    job.companyname : job.companyname.slice(0, 7) + '...' }}</a>
                            </el-tooltip>
                            </template>
                            

                            <p style="font-size: 15px">
                                <span v-if="job.companysize" style="margin-right: 15px;"><el-icon
                                        style="vertical-align: middle;">
                                        <UserFilled />
                                    </el-icon>{{ job.companysize }}</span>
                                <br>
                                <span v-if="job.industryname" style="margin-right: 15px;"><el-icon
                                        style="vertical-align: middle;">
                                        <OfficeBuilding />
                                    </el-icon> {{ job.industryname }}</span>


                            </p>

                        </div>
                        
                    </div>
                    <div class="job_num" style="color: orange;font-size: 20px;padding-right: 15px;">{{ job.job_num }}</div>
                </div>
                <div class="list-items-footer">
                    <span class="property">{{ job.property }}</span>


                </div>
            </div>
        </template>

    </div>
    <el-pagination v-model:current-page="currentPage" :page-size="pagesize" :small="small" :disabled="disabled"
        :background="background" layout="prev, pager, next" :total="count" @size-change="handleSizeChange"
        @current-change="handleCurrentChange" :hide-on-single-page="true" />
</template>
<script>
export default {

    name: 'List',

    props: {
        dataurl: {
            type: String,
            required: true
        },
        listType: {
            type: Number,
            required: true
        },
        pagesize: {
            type: Number,
            default: 20
        },


    },


    async created() {
        this.Q.keywords=this.$route.query.keywords?this.$route.query.keywords:''
        this.Q.subjobtypelevel=this.$route.query.subjobtypelevel?this.$route.query.subjobtypelevel:'-1'
        this.$nextTick(()=>{
            this.getListData(this.currentPage)
        })
        

        

    },
    data() {
        return {
            count: 0,
            // pagesize: 20,
            currentPage: Number(this.$route.query.page)  || 1,
            background: true,
            small: true,
            listData: [],
            citysub: [{ 'code': null, 'name': null }],
            props: {
                label: 'name',
                children: 'sublist',
                value: 'code'
            },
            disabled: false,
            Q: {
                keywords: '',
                city: '',
                citydistrict: '',
                workingexpCode: '-1',
                eduHighestLevel: '-1',
                propertycode: '0',
                subjobtypelevel: '-1',
                worktypeCode: '-1',
                salarytype: '0000,9999999',
                companysize: '不限'

            }
        };
    },
    computed: {
        params() {

            if (this.listType == 1) {
                let salaryrange = this.Q.salarytype.split(',')
                return `&companysize=${this.Q.companysize == '不限' ? '' : this.Q.companysize}&salary=${Number(salaryrange[0])}&salary2=${Number(salaryrange[1])}&search=${this.Q.keywords.trim()}&cityid=${this.Q.city}&citydistrict=${this.Q.citydistrict}&workingexpcode=${this.Q.workingexpCode == '-1' ? '' : this.Q.workingexpCode}&educationcode=${this.Q.eduHighestLevel == '-1' ? '' : this.Q.eduHighestLevel}&propertycode=${this.Q.propertycode == '0' ? '' : this.Q.propertycode}&subjobtypelevel=${this.Q.subjobtypelevel == '-1' ? '' : this.Q.subjobtypelevel}&worktypecode=${this.Q.worktypeCode == '-1' ? '' : this.Q.worktypeCode}`
            } else {
                return `&companysize=${this.Q.companysize == '不限' ? '' : this.Q.companysize}&search=${this.Q.keywords.trim()}&propertycode=${this.Q.propertycode == '0' ? '' : this.Q.propertycode}`
            }

        }
    },
    methods: {
        submit() {
            this.getListData(1)
        },
        clearaddress() {
            this.citysub = []
            this.$baseData.allCity.forEach(element => {
                if (element.code == this.Q.city) {
                    this.citysub = element.sublist
                }
            })
            this.Q.citydistrict = ''


        },
        async getListData(page) {
            const url = new URL(window.location.href);
            // 修改参数
            url.searchParams.set('page', page);
            this.currentPage=Number(page)
            // 修改 URL 不刷新页面
            window.history.pushState({}, '', url.href);
            let Loading = this.$Loading({ fullscreen: true })

            let response = await this.$http
                .get(this.dataurl + `?page=${page}${this.listType != 0 ? this.params : ''}`)
                .then(response => {
                    let resp = response.data
                    if (resp.results) {
                        this.listData = resp.results
                    } else if (resp.data) {
                        this.listData = resp.data
                    } else {
                        this.$Message({ type: 'warning', message: '未查询到数据' })
                    }
                    this.count = resp.count
                    Loading.close()
                })
                .catch(error => {
                    Loading.close()
                });
        },
        scrollToTop() {
            window.scrollTo(0, 0, 1000); // 将页面滚动到坐标(0, 0)，动画时长为500ms
        },
        handleSizeChange(val) {
            console.log(`${val} items per page`)
        },
        async handleCurrentChange(val) {
            this.getListData(val)
            this.scrollToTop()
        },

    },
}
</script>
<style scoped>
.salary-range {
    width: 250px;
    display: flex;
}

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
        background-color: #f6f6f8 !important;
    }


    :deep(.el-input__inner) {
        background-color: #f6f6f8 !important;
        border: none !important;
        box-shadow: none !important;
    }
}

:deep(.el-input__wrapper) {
    background-color: #f6f6f8 !important;
    box-shadow: none !important;
    border-radius: 10px;
}

.select-input>div>div {
    margin-right: 5px;
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

.search-input {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    margin-bottom: 15px;
    border: 1px var(--el-menu-border-color) solid;
    border-radius: 10px;

}

.el-pagination {
    justify-content: center;
    margin-top: 15px;
}

.jobs {
    width: 400px;
    padding: 16px 0 16px 24px;
}

.jobs * {
    font-size: 18px;
}

.jobs>p>* {
    margin-right: 15px;
}

.query {
    margin-bottom: 15px;
    background-color: white;
    padding: 20px 15px;
    border-radius: 15px;
}

.companys,.companys2 {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px 16px 10px;
    width: 250px;
}

.list-items-footer * {
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #666 !important;
    line-height: 18px !important;
    word-break: break-word !important;
    -ms-word-break: break-all !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap;
    /* 禁止文本换行 */
    overflow: hidden;
    /* 超出部分隐藏 */
    text-overflow: ellipsis;
}

.list-items-footer {
    -webkit-text-size-adjust: 100%;
    font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: #414a60;
    -webkit-font-smoothing: antialiased;
    list-style: none;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    margin: 0;
    padding: 15px 24px;
    background: linear-gradient(90deg, #f5fcfc, #fcfbfa);
    border-radius: 0 0 12px 12px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.list-items-body {
    display: flex;
    justify-content: space-between;
    align-items: center;
    -webkit-text-size-adjust: 100%;
    font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: #414a60;
    -webkit-font-smoothing: antialiased;
    list-style: none;
    cursor: pointer;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    margin: 0;
    padding: 0;
}

a:hover {
    color: orange;
}

.list-items:hover {
    box-shadow: 0 10px 10px 0 rgba(0, 0, 0, .12)
}

.list-items {
    margin-bottom: 15px;
    -webkit-text-size-adjust: 100%;
    font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: #414a60;
    -webkit-font-smoothing: antialiased;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    padding: 0;
    list-style: none;
    position: relative;
    width: 100%;
    background: #fff;
    border-radius: 12px;
    transition: all .2s linear;
    cursor: pointer;
}

@media screen and (max-width: 1000px) {

    .companys {
        display: none !important;
    }

    .welfaretaglist {
        display: none;
    }
}
</style>
