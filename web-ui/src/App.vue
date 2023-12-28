<template>
  <router-view></router-view>
</template>

<style scoped></style>

<script>

export default {
  name: 'App',
  data() {
    return {
      refreshTokenInterval: null, // 定时器变量
      refreshTokenExpirationTime: 1000 * 60 * this.$refreshTime, // 刷新令牌的过期时间，替换为实际的值
    };
  },

  created() {
    this.startTokenRefresh();
  },
  methods: {
    //基本信息
    
    async refreshAccessToken() {

      if (localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')) {
        let refresh = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')
        await this.$http.post(this.$api.refresh, { 'refresh': refresh })
          .then(response => {
            const { access } = response.data;
            // 将新的访问令牌存储在本地（例如使用localStorage）
            localStorage.setItem('accessToken', access);
            
          })
          .catch(error => {
            console.error(error)
            localStorage.clear()
            // window.location.href = '/login'

          });
      }

    },
    // 开始定时刷新令牌
    startTokenRefresh() {
      // 每隔一定时间调用refreshAccessToken函数
      this.refreshTokenInterval = setInterval(() => { this.refreshAccessToken() }, this.refreshTokenExpirationTime);
    },


  },
}
</script>