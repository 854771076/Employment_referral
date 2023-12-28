<template>
    <el-container>
        <el-header>
            <Snav>
                <template v-slot:name>简历信息</template>
            </Snav>
        </el-header>
        <el-main class="main">
            <el-card :class="{ 'folded': !card1, '': card1 }">
                <template #header>
                    <div class="card-header ">
                        <span>基本信息</span>
                        <div class="button">
                            <el-button class="button" text>
                                <el-icon class="el-icon--right" @click="openCard(1)">
                                    <ArrowUp v-if="!card1Ico" />
                                    <ArrowDown v-if="card1Ico" />
                                </el-icon></el-button>
                        </div>
                    </div>

                </template>
                <el-form ref="UserinforuleFormRef" :model="UserinforuleForm" :rules="Userinforules" label-width="90px "
                    :size="formSize" status-icon :label-position="labelPosition">

                    <el-form-item label="证件照" prop="photo">
                        <el-upload class="avatar-uploader" :show-file-list="false" :on-success="handleAvatarSuccess"
                            :before-upload="beforeAvatarUpload" action="Jump" :on-error="retryupdate">
                            <img v-if="resumeinfo.photo" :src="this.$ApiBaseUrl + resumeinfo.photo" class="avatar" />
                            <el-icon v-else class="avatar-uploader-icon">
                                <Plus />
                            </el-icon>
                        </el-upload>
                    </el-form-item>
                    <el-form-item label="姓名" prop="name">
                        <el-input v-model="UserinforuleForm.name" />
                    </el-form-item>

                    <el-form-item label="生日" prop="birth">
                        <el-date-picker v-model="UserinforuleForm.birth" type="date" placeholder="生日" format="YYYY-MM-DD"
                            value-format="YYYY-MM-DD" />
                    </el-form-item>
                    <el-form-item label="邮箱" class="readonly">
                        <el-input v-model="resumeinfo.email" readonly />
                    </el-form-item>
                    <el-form-item label="手机号" class="readonly">
                        <el-input v-model="resumeinfo.phone" readonly />
                    </el-form-item>
                    <el-form-item label="性别">
                        <el-select v-model="UserinforuleForm.genderCode" class="m-2" placeholder="性别">
                            <el-option v-for="key, value in this.$baseData.genderObject" :key="value" :label="key"
                                :value="value" />
                        </el-select>
                    </el-form-item>

                    <el-form-item label="求职者身份">
                        <el-select v-model="UserinforuleForm.currentIdentity" class="m-2" placeholder="求职者身份">
                            <el-option v-for="key, value in this.$baseData.currentIdentityObject" :key="key" :label="key"
                                :value="key" />
                        </el-select>

                    </el-form-item>
                    <el-form-item label="政治面貌">
                        <el-select v-model="UserinforuleForm.politicalAffiliation" class="m-2" placeholder="政治面貌">
                            <el-option v-for="key, value in this.$baseData.politicalAffiliationObject" :key="key"
                                :label="key" :value="key" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="居住地" class="address">
                        <el-select v-model="UserinforuleForm.currentProvince" class="m-2" placeholder="省"
                            @change="clearaddress(0)">
                            <el-option v-for="item in this.$baseData.allCity" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                        <el-select v-model="UserinforuleForm.currentCity" class="m-2" placeholder="市"
                            @change="clearaddress(1)">
                            <el-option v-for="item in citysub" :key="item.name" :label="item.name" :value="item.code" />
                        </el-select>
                        <el-select v-model="UserinforuleForm.currentCityDistrictId" class="m-2" placeholder="区">
                            <el-option v-for="item in Districtsub" :key="item.name" :label="item.name" :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-button type="danger" plain @click="UserinfosubmitForm()">保存</el-button>

                </el-form>
            </el-card>
            <el-card :class="{ 'folded': !card2, '': card2 }" style="margin-top: 15px;">
                <template #header>
                    <div class="card-header ">
                        <span>求职期望</span>
                        <div class="button">
                            <el-button class="button" text>
                                <el-icon class="el-icon--right" @click="openCard(2)">
                                    <ArrowUp v-if="!card2Ico" />
                                    <ArrowDown v-if="card2Ico" />
                                </el-icon></el-button>
                        </div>
                    </div>
                </template>
                <el-form ref="UserresumeruleFormRef" :model="UserresumeruleForm" label-width="90px " :size="formSize"
                    status-icon :label-position="labelPosition">
                    <el-form-item label="工作类型">
                        <el-select v-model="UserresumeruleForm.worktypeCode" class="m-2" placeholder="工作类型">
                            <el-option v-for="item in this.$baseData.jobStatus" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="工作城市" class="address">
                        <el-select v-model="UserresumeruleForm.workcity" class="m-2" placeholder="城市1">
                            <el-option v-for="item in this.$baseData.allCity" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                        <el-select v-model="UserresumeruleForm.workcity2" class="m-2" placeholder="城市2">
                            <el-option v-for="item in this.$baseData.allCity" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                        <el-select v-model="UserresumeruleForm.workcity3" class="m-2" placeholder="城市3">
                            <el-option v-for="item in this.$baseData.allCity" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="职位类型">
                        <el-select v-model="UserresumeruleForm.subjobtypelevel" class="m-2" placeholder="职位类型">
                            <el-option v-for="item in this.$baseData.jobType" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="企业类型">
                        <el-select v-model="UserresumeruleForm.propertycode" class="m-2" placeholder="企业类型">
                            <el-option v-for="item in this.$baseData.companyType" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="薪资范围" class="salary">
                        <el-input v-model="UserresumeruleForm.preferredSalaryMin" type="number" /> - <el-input
                            v-model="UserresumeruleForm.preferredSalaryMax" type="number" />
                    </el-form-item>
                    <el-button type="primary" plain @click="UserResumesubmitForm()">保存</el-button>
                </el-form>
            </el-card>
            <el-card :class="{ 'folded': !card3, '': card3 }" style="margin-top: 15px;">
                <template #header>
                    <div class="card-header ">
                        <span>自我评估</span>
                        <div class="button">
                            <el-button class="button" text>
                                <el-icon class="el-icon--right" @click="openCard(3)">
                                    <ArrowUp v-if="!card3Ico" />
                                    <ArrowDown v-if="card3Ico" />
                                </el-icon></el-button>
                        </div>
                    </div>
                </template>
                <el-form ref="UserReadmeruleFormRef" :model="UserReadmeruleForm" label-width="90px " :size="formSize"
                    status-icon :label-position="labelPosition">
                    <el-form-item label="学历">
                        <el-select v-model="UserReadmeruleForm.eduHighestLevel" class="m-2" placeholder="学历">
                            <el-option v-for="item in this.$baseData.educationType" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="工作经验">
                        <el-select v-model="UserReadmeruleForm.workingexpCode" class="m-2" placeholder="工作经验">
                            <el-option v-for="item in this.$baseData.workExpType" :key="item.name" :label="item.name"
                                :value="item.code" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="技能标签" class="skill">
                        <div>
                            <el-tag v-for="tag in UserReadmeruleForm.skilllabel2" :key="tag" class="mx-1" closable
                                :disable-transitions="false" @close="handleClose(tag)" style="margin-right: 15px;">
                                {{ tag }}
                            </el-tag>
                            <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="ml-1 w-20" size="small"
                                @keyup.enter="handleInputConfirm" @blur="handleInputConfirm" />
                            <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">
                                + 添加
                            </el-button>
                        </div>
                    </el-form-item>
                    <el-form-item label="自我介绍">
                        <el-input v-model="UserReadmeruleForm.SelfEvaluate" maxlength="200" placeholder="自我介绍"
                            show-word-limit resize="none" rows="10" type="textarea" />
                    </el-form-item>
                    <el-button type="primary" plain @click="UserReadmesubmitForm()">保存</el-button>
                </el-form>
            </el-card>
        </el-main>
    </el-container>
</template>
  
<script lang="ts">

import { ref } from 'vue'
import type { FormProps } from 'element-plus'
export default {

    name: 'Resume',
    created() {
        this.getResumeinfo()

    },


    data() {

        return {
            UserReadmeruleForm: {
                eduHighestLevel: '',
                eduHighestLevelTranslation: '',
                workingexpCode: '',
                workingexp: '',
                skilllabel: '',
                skilllabel2: [],
                SelfEvaluate: ''
            },
            UserresumeruleForm: {
                worktypeCode: '',
                worktype: '',
                workcity: '',
                workcityTranslation: '',
                workcity2: '',
                workcity2Translation: '',
                workcity3: '',
                workcity3Translation: '',
                subjobtypelevel: '',
                subjobtypelevelname: '',
                propertycode: '',
                property: '',
                preferredSalaryMin: 0,
                preferredSalaryMax: 3000
            },
            Userinforules: {
                photo: [
                    { required: false, message: '请上传证件照', trigger: 'blur' },
                ],
                name: [
                    { required: true, message: '请输入姓名', trigger: 'blur' },
                    { min: 2, max: 50, message: '长度应该在 3 - 50', trigger: 'blur' },
                ],
                birth: [
                    { required: true, message: '请选择生日', trigger: 'blur' },
                ],

            },

            UserinforuleForm: {
                name: '',
                birth: '',
                genderCode: '1',
                genderTranslation: '',
                currentIdentity: '社会求职者',
                currentCity: '',
                currentCityTranslation: '',
                currentCityDistrictId: '',
                currentCityDistrictIdTranslation: '',
                currentProvince: '',
                currentProvinceTranslation: '',
                politicalAffiliation: '群众',



            },
            card1: true,
            card1Ico: true,
            card2: true,
            card2Ico: true,
            card3: true,
            card3Ico: true,
            // imageUrl: '',
            formSize: 'default',
            labelPosition: ref<FormProps['labelPosition']>('left'),
            action: this.$ApiBaseUrl + this.$api['uploadphoto'],
            resumeinfo: {
                email: '',
                phone: '',
                photo: "",
                genderCode: null,
            },
            citysub: [{ 'code': null, 'name': null }],
            Districtsub: [{ 'code': null, 'name': null }],
            inputValue: '',
            inputVisible: false,

        };
    },

    watch: {
        UserinforuleForm: {
            // 此处监听obj属性a值变量
            handler(item1, item2) {

                this['UserinforuleForm']['subjobtypelevelname'] = this.$baseData['jobType'][item1['subjobtypelevel']]
                this['UserinforuleForm']['genderTranslation'] = this.$baseData['genderObject'][item1['genderCode']]
                this['UserinforuleForm']['currentProvinceTranslation'] = this.getname(this.$baseData['allCity'], item1['currentProvince'])
                this['UserinforuleForm']['currentCityTranslation'] = this.getname(this['citysub'], item1['currentCity'])
                this['UserinforuleForm']['currentCityDistrictIdTranslation'] = this.getname(this['Districtsub'], item1['currentCityDistrictId'])
                this.$baseData['allCity'].forEach(element => {
                    if (element['code'] == item1['currentProvince']) {
                        this['citysub'] = element['sublist']
                    }
                })
                this['citysub'].forEach(element => {
                    if (element['code'] == item1['currentCity']) {
                        this['Districtsub'] = element['sublist']
                    }
                });

            },
            deep: true,
            immediate: true
        },
        UserresumeruleForm: {
            handler(item1, item2) {
                this['UserresumeruleForm']['worktype'] = this.getname(this.$baseData['jobStatus'], item1['worktypeCode'])
                this['UserresumeruleForm']['worktypeTranslation'] = this.$baseData['jobStatus'][item1['worktype']]
                this['UserresumeruleForm']['workcityTranslation'] = this.getname(this.$baseData['allCity'], item1['workcity'])
                this['UserresumeruleForm']['workcity2Translation'] = this.getname(this.$baseData['allCity'], item1['workcity2'])
                this['UserresumeruleForm']['workcity3Translation'] = this.getname(this.$baseData['allCity'], item1['workcity3'])
                this['UserresumeruleForm']['subjobtypelevelname'] = this.getname(this.$baseData['jobType'], item1['subjobtypelevel'])
                this['UserresumeruleForm']['property'] = this.getname(this.$baseData['companyType'], item1['propertycode'])
                if (item1['preferredSalaryMin'] < 0) {
                    this['UserresumeruleForm']['preferredSalaryMin'] = 0
                }
                if (item1['preferredSalaryMax'] < item1['preferredSalaryMin']) {
                    this['UserresumeruleForm']['preferredSalaryMax'] = item1['preferredSalaryMin']
                }
            },
            deep: true,
            immediate: true
        },
        resumeinfo: {
            // 此处监听obj属性a值变量
            handler(item1, item2) {
                // item1为新值，item2为旧值
                this['UserinforuleForm']['name'] = item1['name']
                this['UserinforuleForm']['birth'] = item1['birth']
                this['UserinforuleForm']['genderCode'] = item1['genderCode']
                this['UserinforuleForm']['currentIdentity'] = item1['currentIdentity']
                this['UserinforuleForm']['currentCity'] = item1['currentCity']
                this['UserinforuleForm']['currentCityDistrictId'] = item1['currentCityDistrictId']
                this['UserinforuleForm']['currentProvince'] = item1['currentProvince']
                this['UserinforuleForm']['politicalAffiliation'] = item1['politicalAffiliation']

                this['UserresumeruleForm']['worktypeCode'] = item1['worktypeCode']
                this['UserresumeruleForm']['worktype'] = item1['worktype']
                this['UserresumeruleForm']['workcity'] = !item1['workcity'] ? null : item1['workcity']
                this['UserresumeruleForm']['workcityTranslation'] = item1['workcityTranslation']
                this['UserresumeruleForm']['workcity2'] = !item1['workcity2'] ? null : item1['workcity2']
                this['UserresumeruleForm']['workcity2Translation'] = item1['workcity2Translation']
                this['UserresumeruleForm']['workcity3'] = !item1['workcity3'] ? null : item1['workcity3']
                this['UserresumeruleForm']['workcity3Translation'] = item1['workcity3Translation']
                this['UserresumeruleForm']['subjobtypelevel'] = item1['subjobtypelevel']
                this['UserresumeruleForm']['subjobtypelevelname'] = item1['subjobtypelevelname']
                this['UserresumeruleForm']['propertycode'] = item1['propertycode']
                this['UserresumeruleForm']['property'] = item1['property']
                this['UserresumeruleForm']['preferredSalaryMin'] = item1['preferredSalaryMin']
                this['UserresumeruleForm']['preferredSalaryMax'] = item1['preferredSalaryMax']

                this['UserReadmeruleForm']['eduHighestLevel'] = item1['eduHighestLevel']
                this['UserReadmeruleForm']['eduHighestLevelTranslation'] = item1['eduHighestLevelTranslation']
                this['UserReadmeruleForm']['workingexpCode'] = item1['workingexpCode']
                this['UserReadmeruleForm']['workingexp'] = item1['workingexp']
                try {
                    this['UserReadmeruleForm']['skilllabel2'] = item1['skilllabel'].split('/')
                }
                catch {
                }
                this['UserReadmeruleForm']['SelfEvaluate'] = item1['SelfEvaluate']
            },
            deep: true,
            immediate: true
        },
        UserReadmeruleForm: {
            // 此处监听obj属性a值变量
            handler(item1, item2) {

                // item1为新值，item2为旧值
                this['UserReadmeruleForm']['skilllabel'] = item1['skilllabel2'].join('/')
                this['UserReadmeruleForm']['eduHighestLevelTranslation'] = this.getname(this.$baseData['educationType'], item1['eduHighestLevel'])
                this['UserReadmeruleForm']['workingexp'] = this.getname(this.$baseData['workExpType'], item1['workingexp'])

            },
            deep: true,
            immediate: true
        }

    },

    methods: {

        handleClose(tag: string) {
            this.UserReadmeruleForm.skilllabel2.splice(this.UserReadmeruleForm.skilllabel2.indexOf(tag), 1)
        },
        showInput() {
            this.inputVisible = true
            this.$nextTick(() => {
                this.$refs.InputRef.focus()
            })
        },
        handleInputConfirm() {
            if (this.inputValue) {
                this.UserReadmeruleForm.skilllabel2.push(this.inputValue)
            }
            this.inputVisible = false
            this.inputValue = ''
        },
        clearaddress(methods) {
            if (methods == 0) {
                this['UserinforuleForm']['currentCity'] = ''
                this['UserinforuleForm']['currentCityDistrictId'] = ''
            } else {
                this['UserinforuleForm']['currentCityDistrictId'] = ''
            }

        },
        getname(arr, code) {
            let res = ''
            try {
                arr.forEach(element => {
                    if (element['code'] == code) {
                        res = element['name']
                    }
                });
            } catch {

            }

            return res
        },
        retryupdate(response, uploadFile) {
            const headers = {
                'Content-Type': 'multipart/form-data', // 设置请求头为文件上传类型
            }
            const formData = new FormData();
            formData.append('file', uploadFile.raw!);
            // 使用 axios 发送请求，并添加新的 key 到请求参数中
            this.$http.post(this.$api['uploadphoto'], formData, { headers }).then(res => {
                this.getResumeinfo()
            }).catch(err => {
                this.$Message.error(`${err}`)
            });
        },
        async getResumeinfo() {

            this.$http.get(this.$api.resumeinfo, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                this.resumeinfo = response.data.data

            })

        },
        openCard(num) {
            if (num == 1) {
                this.card1 = !this.card1
                this.card1Ico = !this.card1Ico
            } else if (num == 2) {
                this.card2 = !this.card2
                this.card2Ico = !this.card2Ico
            } else if (num == 3) {
                this.card3 = !this.card3
                this.card3Ico = !this.card3Ico
            }
        },
        async UserinfosubmitForm() {
            this.$refs.UserinforuleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.changebaseinfo()

            })

        },
        async UserResumesubmitForm() {
            this.$refs.UserresumeruleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.changeresumeinfo()

            })
        },
        UserReadmesubmitForm() {
            this.$refs.UserReadmeruleFormRef.validate((valid) => {
                if (!valid) {

                    return false
                }
                this.changeReadme()

            })
        },
        async changeReadme() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.changereadme, this.UserReadmeruleForm)
                .then(response => {
                    // 登录成功，获取访问令牌和刷新令牌并保存到本地（例如使用localStorage）
                    if (response['data']['code'] == 200) {
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "保存成功"
                        })
                        this.getResumeinfo()
                    } else {
                        this.$Message.error(response['data']['msg'])
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });
        },
        async changeresumeinfo() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.changeresumeinfo, this.UserresumeruleForm)
                .then(response => {
                    // 登录成功，获取访问令牌和刷新令牌并保存到本地（例如使用localStorage）
                    if (response['data']['code'] == 200) {
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "保存成功"
                        })
                        this.getResumeinfo()
                    } else {
                        this.$Message.error(response['data']['msg'])
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });
        },
        async changebaseinfo() {
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .post(this.$api.changebaseinfo, {
                    name: this['UserinforuleForm']['name'] ? this['UserinforuleForm']['name'] : '',
                    birth: this['UserinforuleForm']['birth'] ? this['UserinforuleForm']['birth'] : null,
                    genderCode: this['UserinforuleForm']['genderCode'] ? this['UserinforuleForm']['genderCode'] : 1,
                    genderTranslation: this['UserinforuleForm']['genderTranslation'] ? this['UserinforuleForm']['genderTranslation'] : '男',
                    currentIdentity: this['UserinforuleForm']['currentIdentity'] ? this['UserinforuleForm']['currentIdentity'] : '社会求职者',
                    currentCity: this['UserinforuleForm']['currentCity'] ? this['UserinforuleForm']['currentCity'] : null,
                    currentCityTranslation: this['UserinforuleForm']['currentCityTranslation'] ? this['UserinforuleForm']['currentCityTranslation'] : '',
                    currentCityDistrictId: this['UserinforuleForm']['currentCityDistrictId'] ? this['UserinforuleForm']['currentCityDistrictId'] : null,
                    currentCityDistrictIdTranslation: this['UserinforuleForm']['currentCityDistrictIdTranslation'] ? this['UserinforuleForm']['currentCityDistrictIdTranslation'] : '',
                    currentProvince: this['UserinforuleForm']['currentProvince'] ? this['UserinforuleForm']['currentProvince'] : null,
                    currentProvinceTranslation: this['UserinforuleForm']['currentProvinceTranslation'] ? this['UserinforuleForm']['currentProvinceTranslation'] : '',
                    politicalAffiliation: this['UserinforuleForm']['politicalAffiliation'] ? this['UserinforuleForm']['politicalAffiliation'] : '群众',
                })
                .then(response => {
                    // 登录成功，获取访问令牌和刷新令牌并保存到本地（例如使用localStorage）
                    if (response['data']['code'] == 200) {
                        Loading.close()
                        this.$Message({
                            type: 'success',
                            message: "保存成功"
                        })
                        this.getResumeinfo()
                    } else {
                        this.$Message.error(response['data']['msg'])
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('系统异常,请联系管理员')
                });

        },
        handleAvatarSuccess(
            response,
            uploadFile
        ) {
            // this.imageUrl = URL.createObjectURL(uploadFile.raw!)
            this.getResumeinfo()


        },
        beforeAvatarUpload(rawFile) {
            console.log(rawFile.type)
            if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png' && rawFile.type !== 'image/jpg') {
                this.$Message.error('Avatar picture must be JPG/PNG format!')
                return false
            } else if (rawFile.size / 1024 / 1024 > 2) {
                this.$Message.error('Avatar picture size can not exceed 2MB!')
                return false
            }
            return true
        }

    }
}
</script>

<style>
.address>div,
.salary>div {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
}

.skill>div {
    flex-direction: row !important;
    flex-wrap: nowrap !important;

}

.skill .el-input {
    width: 200px !important;
}

.salary>div {
    max-width: 300px !important;
    justify-content: space-between !important;
}

.address .el-input__wrapper {
    margin-right: 5px !important;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.folded .el-card__body {
    display: none !important;
}

.avatar {
    width: 120px;
    height: 120px;
}

.readonly .el-input__wrapper {
    background-color: rgba(85, 84, 84, 0.1) !important;
}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>
  