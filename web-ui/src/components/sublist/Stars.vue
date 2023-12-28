<template>
    <Snav>
        <template v-slot:name>我的收藏</template>
    </Snav>

    <el-main class="main">
        <List :dataurl="$api.collectjobs" :listType="0" ></List>
    </el-main>
    
</template>
<script>
import List from '../utils/List.vue'
import Snav from '../utils/Snav.vue'
export default {

    name: 'Stars',
    data() {
        return {
        
        };
    },
    
    methods: {
        

    },
    components:{
        List,
        Snav 
    }
}
</script>
<style>

</style>