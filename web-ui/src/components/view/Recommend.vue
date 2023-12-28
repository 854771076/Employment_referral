<template>
    <List :dataurl="$api.recommend" :listType="0"></List>
</template>
<script>
import List from '../utils/List.vue'
export default {

    name: 'Recommend',
    data() {
        return {
        
        };
    },
    props:{
        userinfo: {
            type: Object,
            required: true,
        },
    },
    methods: {
        

    },
    components:{
        List
    }
}
</script>
<style>

</style>