<template>
    <List :dataurl="$api.jobs" :listType=1></List>
</template>
<script>
import List from '../utils/List.vue'
export default {

    name: 'Jobs',
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