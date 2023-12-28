<template>
    <List :dataurl="$api.companys" :listType=2></List>
</template>
<script>
import List from '../utils/List.vue'
export default {

    name: 'Companys',
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