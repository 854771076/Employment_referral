<template>
    <div class="comment-section">


        <!-- 添加评论表单 -->
        <div class="comment-form">
            <el-form ref="commentForm" :model="newComment">
                <el-form-item label="评论内容">
                    <el-input type="textarea" v-model="newComment.content" resize="none" maxlength="50"
                        show-word-limit></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitComment">发表评论</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 评论列表 -->
        <ul v-infinite-scroll="getcomment" class="infinite-list" style="overflow: auto" ref="comment">
            <li v-for="comment in comments" :key="comment.number " class="comment-item infinite-list-item">
                <div class="comment-info">
                    <span class="username">{{ comment.username }}</span>
                    <span class="timestamp">{{ new Date(comment.create_time).toLocaleString() }}</span>
                </div>
                <p class="comment-content">{{ comment.content }}</p>
            </li>
        </ul>
    </div>
</template>
  
<script>

export default {
    name: 'Comment',
    props: {
        number : {
            type: Number,
            required: true,
        },

    },
    created() {
        this.getcomment()
    }
    ,
    data() {

        return {
            comments: [

            ],
            maxpage: 1,
            page:1,
            newComment: {
                number :this.number ,
                content: ''
            },
            isloading:false,
            isloading2:false
        };
    },
    methods: {
        async getcomment() {
            // console.log(this.page ,this.maxpage ,this.number )
            if (this.page <= this.maxpage && this.number &&!this.isloading) {
                this.isloading=true
                let Loading = this.$Loading({ fullscreen: true })
                let response = await this.$http
                    .get(this.$api.commentjobs + `?number =${this.number }&page=${this.page}`)
                    .then(response => {
                        this.comments = [...this.comments, ...response.data.data]
                        this.maxpage = Math.ceil(response.data.count / 10)
                        
                        this.page += 1
                        console.log(this.page ,this.maxpage ,this.number )
                        Loading.close()
                        this.isloading=false
                    })
                    .catch(error => {
                        Loading.close()
                        this.isloading=false
                        this.$Message.error('未查询到数据')
                    });
                    if (this.page> this.maxpage && this.maxpage != 0 && this.maxpage != 1) {
                this.$Message({ type: 'success', message: '到底啦！' })
            }
            }
        },
        async refrashcomment() {

        if ((this.page <= this.maxpage && this.number &&!this.isloading2) || this.maxpage == 0) {
            this.isloading2=true
            let Loading = this.$Loading({ fullscreen: true })
            let response = await this.$http
                .get(this.$api.commentjobs + `?number =${this.number }&page=${this.page}`)
                .then(response => {
                    this.comments = response.data.data
                    this.maxpage = Math.ceil(response.data.count / 10)

                    this.page = 2
                    this.$refs.comment.scrollTo(0, 0, 1000)
                    Loading.close()
                    this.isloading2=false
                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error('未查询到数据')
                    this.isloading2=false
                });
        }
        

        },
        async submitComment() {
            let Loading = this.$Loading({ fullscreen: true })
            if(this.newComment.content!=''){
                console.log(this.newComment)
                let response = await this.$http

                .post(this.$api.comment ,this.newComment)
                .then(response => {
                    if(response.data.code=="200"){
                        this.page=1
                    this.refrashcomment()
                    Loading.close()
                    this.$Message({ type: 'success', message: '评论成功' })
                    }
                    else{
                        this.$Message.error(response.data.msg,response.data.data)
                        Loading.close()
                    }

                })
                .catch(error => {
                    Loading.close()
                    this.$Message.error(error)
                });
            }else{
                this.$Message.error('评论不能为空')
                Loading.close()
            }
            

            // 清空表单
            this.newComment.username = '';
            this.newComment.content = '';
        }
    }
};
</script>
  
<style scoped>
.infinite-list {
  max-height: 500px;
  padding: 15px 0;
  margin: 0;
  list-style: none;
}

.infinite-list .infinite-list-item {
  /* display: flex;
  align-items: center;
  justify-content: center; */
  height: 70px;
} 
.infinite-list .infinite-list-item + .list-item {
  margin-top: 10px;
}
.comment-section {
    width: 100%;
    margin: 0 auto;
}

.comment-item {
    margin-bottom: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}

.comment-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.username {
    font-weight: bold;
}

.comment-content {
    margin: 0;
}

.comment-form {
    margin-top: 20px;
}
</style>