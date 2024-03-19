<template>
    <header>
      <h1 class="title" >JobFree数字化分析大屏</h1>
      <div style="display: flex;justify-content: space-between;">
        <div class="filter">
          <!-- <div class="filter_active" @click="Filter">本月</div>
          <div @click="Filter">本年</div> -->
        </div>
        <div ref="timer" class="timer"></div>
  
      </div>
  
    </header>
    <!-- 页面主体 -->
    <section class="mainbox" style="flex-direction: column;">
      <div class="column centerchart">
        <!-- 头部 no模块 -->
        <div class="no">
          <div class="no-hd">
            <ul>
            <li>{{ info.count[0] ? info.count[0] : 0 }}</li>
              <li>{{ info.total[0] ? info.total[0] : 0 }}</li>
             
            </ul>
          </div>
          <div class="no-bd">
            <ul>
              
              <li>企业数</li>
              <li>岗位数</li>
            </ul>
          </div>
        </div>
        <!-- map模块 -->
        <!-- <div class="map">
          <div class="map1"></div>
          <div class="map2"></div>
          <div class="map3"></div>
          <div class="chart" ref="mapchart"></div>
        </div> -->
      </div>
      <div class="charts">
        <!-- 左侧盒子 -->
        <div class="column leftchart">
          <div class="panel ">
            <h2>柱形图-各企业类型平均工资排行</h2>
            <!-- 图表放置盒子 -->
            <div class="chart" ref="left1"></div>
            <!-- 伪元素绘制盒子下边角 -->
            <div class="panel-footer"></div>
          </div>
          <!-- <div class="panel">
            <h2>折线图-利润涨幅</h2>
            <div class="chart" ref="left2"></div>
            <div class="panel-footer"></div>
          </div> -->
          <div class="panel pie">
            <h2>饼形图-类型分布</h2>
            <div class="chart" ref="left3"></div>
            <div class="panel-footer"></div>
          </div>
        </div>
        <!-- 中间盒子 -->
  
        <!-- 右侧盒子 -->
        <div class="column rightchart">
          <div class="panel bar2">
            <h2>柱形图-各学历平均工资排行</h2>
            <!-- 大社的总收款排行情况 -->
            <div class="chart" ref="right1"></div>
            <div class="panel-footer"></div>
          </div>
          <!-- <div class="panel line2">
            <h2>折线图-各月/天收款情况</h2>
            <div class="chart" ref="right2"></div>
            <div class="panel-footer"></div>
          </div> -->
          <div class="panel pie2">
            <h2>饼形图-各地点岗位数量占比</h2>
            <div class="chart" ref="right3"></div>
            <div class="panel-footer"></div>
          </div>
        </div>
      </div>
  
    </section>
    <!-- <div ref="chart" style="height: 300px;"></div>
    <div ref="chart2" style="height: 300px;"></div> -->
  </template>
  <script setup>
  import { markRaw } from 'vue'
  </script>
  <script >
  
  
  export default {
    name: 'BigView',
    created() {
      let script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = '/assets/js/flexible.js';
      document.body.appendChild(script);
      let link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/assets/css/charts.css';
      document.body.appendChild(link);
      this.getinfo()
      window.setInterval(this.getinfo, 60000)
  
    },
    mounted() {
      this.charts()
    },
  
    data() {
      return {
        methods:false,
        t: null,
        resize: null,
        mapchart: null,
        left1: null,
        left2: null,
        left3: null,
        right1: null,
        right2: null,
        right3: null,
        info:{
          total:[0],
          count:[0],
          uncollected:[0]
        }
      }
    },
  
    methods: {
      getinfo() {
  
        this.$http.get(this.$api.jobs+'bigdata_info/', {
          
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => {
            this.info = response.data.data
  
          })
          .catch(error => {
            console.error(error)
            this.$message({ type: 'error', text: '加载失败' })
          });
  
  
      },
      async charts() {
        this.$nextTick(() => {
  
          this.left1 = markRaw(this.$echarts.init(this.$refs.left1));
          this.right1 = markRaw(this.$echarts.init(this.$refs.right1));
          // this.left2 = markRaw(this.$echarts.init(this.$refs.left2));
          // this.right2 = markRaw(this.$echarts.init(this.$refs.right2));
          this.left3 = markRaw(this.$echarts.init(this.$refs.left3));
  
  
  
          this.right3 = markRaw(this.$echarts.init(this.$refs.right3));
  
          //地图
          // this.mapchart = markRaw(this.$echarts.init(this.$refs.mapchart));
          this.Left1()
          this.Right1()
          // this.Left2()
          // this.Right2()
          this.Left3()
  
          this.Right3()
          // this.Map()
          //时间
          this.t = window.setInterval(this.time, 1000)
          this.resize = window.setInterval(this.ReSize)
        })
      },
      ReSize() {
        // 获取当前屏幕分辨率
  
        this.left1.resize()
        this.right1.resize()

        this.left3.resize()
  
  
        this.right3.resize()
        // this.mapchart.resize()
  
      },
      Filter(e) {
        if (!e.target.classList.contains('filter_active')) {
          if (e.target.previousElementSibling) {
            e.target.previousElementSibling.classList.remove('filter_active')
            e.target.classList.add('filter_active')
          } else {
            e.target.nextElementSibling.classList.remove('filter_active')
            e.target.classList.add('filter_active')
          }
          this.methods=!this.methods
          this.getinfo()
          this.Left1()
          this.Right1()
          this.Left2()
          this.Right2()
          this.Left3()
          //查询数据
        }
      },
      time() {
        var dt = new Date();
        var y = dt.getFullYear();
        var mt = dt.getMonth() + 1;
        var day = dt.getDate();
        var h = dt.getHours(); //获取时
        var m = dt.getMinutes(); //获取分
        var s = dt.getSeconds(); //获取秒
        this.$refs.timer.innerHTML =
  
          y +
          "年" +
          mt +
          "月" +
          day +
          "日-" +
          h +
          "时" +
          m +
          "分" +
          s +
          "秒";
      },
      async Right3() {
        await this.$http.get(this.$api.jobs+'workcity_info/', {
          
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => {
            this.right3_info = response.data.data
  
          })
          .catch(error => {
            console.error(error)
          });
  
        var option = {
          color: ['#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'],
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
            bottom: 0,
            itemWidth: 10,
            itemHeight: 10,
            textStyle: {
              color: "rgba(255,255,255,.5)",
              fontSize: 10
            }
          },
          series: [{
            name: '地点分布',
            type: 'pie',
            radius: ["10%", "60%"],
            center: ['50%', '40%'],
            // 半径模式  area面积模式
            roseType: 'radius',
            // 图形的文字标签
            label: {
              fontsize: 10
            },
            // 引导线调整
            labelLine: {
              // 连接扇形图线长(斜线)
              length: 8,
              // 连接文字线长(横线)
              length2: 10
            },
            data: this.right3_info
          }]
        };
        this.right3.setOption(option)
  
      },
      async Left3() {
        await this.$http.get(this.$api.jobs+'worktype_info/', {
          
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => {
            this.left3_info = response.data.data
  
          })
          .catch(error => {
            console.error(error)
          });
        var option = {
          // color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"],
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            // 垂直居中,默认水平居中
            // orient: 'vertical',
  
            bottom: 0,
            left: 10,
            // 小图标的宽度和高度
            itemWidth: 10,
            itemHeight: 10,
            // 修改图例组件的文字为 12px
            textStyle: {
              color: "rgba(255,255,255,.5)",
              fontSize: "10"
            }
          },
          series: [{
            name: '类型分布',
            type: 'pie',
            // 设置饼形图在容器中的位置
            center: ["50%", "42%"],
            // 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
            radius: ['40%', '60%'],
            avoidLabelOverlap: false,
            // 图形上的文字
            label: {
              show: false,
              position: 'center'
            },
            // 链接文字和图形的线
            labelLine: {
              show: false
            },
            data: this.left3_info 
          }]
        }
        this.left3.setOption(option)
  
      },
    //   async Left2() {
    //     // 年份对应数据
    //     await this.$http.get(this.$api.jobs+'increment_info/', {
    //       params:{
    //         methods:this.methods
    //       },
    //       headers: {
    //         'Content-Type': 'application/json',
    //       }
    //     })
    //       .then(response => {
    //         this.left2_info = response.data.data
  
    //       })
    //       .catch(error => {
    //         console.error(error)
    //       });
    //     let type
    //     let type1
    //     if (this.methods){
    //       type='本年'
    //       type1='去年'
    //     }else{
    //       type='本月'
    //       type1='上月'
    //     }
        
    //     var option = {
    //       // 修改两条线的颜色
    //       color: ['#00f2f1', '#ed3f35'],
    //       tooltip: {
    //         trigger: 'axis'
    //       },
    //       // 图例组件
    //       legend: {
    //         // 当serise 有name值时， legend 不需要写data
    //         // 修改图例组件文字颜色
    //         textStyle: {
    //           color: '#4c9bfd'
    //         },
    //         right: '10%',
    //       },
    //       grid: {
    //         top: "20%",
    //         left: '3%',
    //         right: '4%',
    //         bottom: '3%',
    //         containLabel: true,
    //         show: true, // 显示边框
    //         borderColor: '#012f4a' // 边框颜色
    //       },
    //       xAxis: {
    //         type: 'category',
    //         boundaryGap: false, // 去除轴间距
    //         data: this.left2_info[0][0],
    //         // 去除刻度线
    //         axisTick: {
    //           show: false
    //         },
    //         axisLabel: {
    //           color: "#4c9bfb" // x轴文本颜色
    //         },
    //         axisLine: {
    //           show: false // 去除轴线
    //         }
    //       },
    //       yAxis: {
    //         type: 'value',
    //         // 去除刻度线
    //         axisTick: {
    //           show: false
    //         },
    //         axisLabel: {
    //           color: "#4c9bfb" // x轴文本颜色
    //         },
    //         axisLine: {
    //           show: false // 去除轴线
    //         },
    //         splitLine: {
    //           lineStyle: {
    //             color: "#012f4a"
    //           }
    //         }
    //       },
    //       series: [{
    //         type: 'line',
    //         smooth: true, // 圆滑的线
    //         name: type,
    //         data: this.left2_info[0][1].map((x)=>{
    //           return x?x:0
    //         })
    //       },
    //       {
    //         type: 'line',
    //         smooth: true, // 圆滑的线
    //         name: type1,
    //         data: this.left2_info[1][1].map((x)=>{
    //           return x?x:0
    //         })
    //       }
    //       ]
    //     }
    //     this.left2.setOption(option)
  
    //   },
    //   async Right2() {
        
    //     await this.$http.get(this.$api.jobs+'money_info/', {
    //       params:{
    //         methods:this.methods
    //       },
    //       headers: {
    //         'Content-Type': 'application/json',
    //       }
    //     })
    //       .then(response => {
    //         this.right2_info = response.data.data
  
    //       })
    //       .catch(error => {
    //         console.error(error)
    //       });
    //     let type
    //     let type1
    //     if (this.methods){
    //       type='本年'
    //       type1='去年'
    //     }else{
    //       type='本月'
    //       type1='上月'
    //     }
    //     var option = {
    //       tooltip: {
    //         trigger: 'axis',
    //       },
    //       legend: {
    //         top: "0%",
    //         textStyle: {
    //           color: "rgba(255,255,255,.5)",
    //           fontSize: "12"
    //         }
    //       },
    //       grid: {
    //         top: '30',
    //         left: '10',
    //         right: '30',
    //         bottom: '10',
    //         containLabel: true
    //       },
    //       xAxis: [{
    //         type: 'category',
    //         boundaryGap: false,
    //         // 文本颜色为rgba(255,255,255,.6)  文字大小为 12
    //         axisLabel: {
    //           textStyle: {
    //             color: "rgba(255,255,255,.6)",
    //             fontSize: 12
    //           }
    //         },
    //         // x轴线的颜色为   rgba(255,255,255,.2)
    //         axisLine: {
    //           lineStyle: {
    //             color: "rgba(255,255,255,.2)"
    //           }
    //         },
    //         data: this.right2_info[0][0]
    //       }],
    //       yAxis: [{
    //         type: 'value',
    //         axisTick: {
    //           // 不显示刻度线
    //           show: false
    //         },
    //         axisLine: {
    //           lineStyle: {
    //             color: "rgba(255,255,255,.1)"
    //           }
    //         },
    //         axisLabel: {
    //           textStyle: {
    //             color: "rgba(255,255,255,.6)",
    //             fontSize: 12
    //           }
    //         },
    //         // 修改分割线的颜色
    //         splitLine: {
    //           lineStyle: {
    //             color: "rgba(255,255,255,.1)"
    //           }
    //         }
    //       }],
    //       series: [{
    //         name: type,
    //         type: 'line',
    //         smooth: true, // 圆滑的线
    //         // 单独修改当前线条的样式
    //         lineStyle: {
    //           color: "#0184d5",
    //           width: 2
    //         },
    //         // 填充区域渐变透明颜色
    //         areaStyle: {
    //           color: new this.$echarts.graphic.LinearGradient(
    //             0,
    //             0,
    //             0,
    //             1,
    //             [{
    //               offset: 0,
    //               color: "rgba(1, 132, 213, 0.4)" // 渐变色的起始颜色
    //             },
    //             {
    //               offset: 0.8,
    //               color: "rgba(1, 132, 213, 0.1)" // 渐变线的结束颜色
    //             }
    //             ],
    //             false
    //           ),
    //           shadowColor: "rgba(0, 0, 0, 0.1)"
    //         },
    //         // 拐点设置为小圆点
    //         symbol: 'circle',
    //         // 设置拐点大小
    //         symbolSize: 5,
    //         // 开始不显示拐点， 鼠标经过显示
    //         showSymbol: false,
    //         // 设置拐点颜色以及边框
    //         itemStyle: {
    //           color: "#0184d5",
    //           borderColor: "rgba(221, 220, 107, .1)",
    //           borderWidth: 12
    //         },
    //         data: this.right2_info[0][1].map((x)=>{
    //           return x?x:0
    //         })
    //       },
    //       {
    //         name: type1,
    //         type: "line",
    //         smooth: true,
    //         lineStyle: {
    //           normal: {
    //             color: "#00d887",
    //             width: 2
    //           }
    //         },
    //         areaStyle: {
    //           normal: {
    //             color: new this.$echarts.graphic.LinearGradient(
    //               0,
    //               0,
    //               0,
    //               1,
    //               [{
    //                 offset: 0,
    //                 color: "rgba(0, 216, 135, 0.4)"
    //               },
    //               {
    //                 offset: 0.8,
    //                 color: "rgba(0, 216, 135, 0.1)"
    //               }
    //               ],
    //               false
    //             ),
    //             shadowColor: "rgba(0, 0, 0, 0.1)"
    //           }
    //         },
    //         // 设置拐点 小圆点
    //         symbol: "circle",
    //         // 拐点大小
    //         symbolSize: 5,
    //         // 设置拐点颜色以及边框
    //         itemStyle: {
    //           color: "#00d887",
    //           borderColor: "rgba(221, 220, 107, .1)",
    //           borderWidth: 12
    //         },
    //         // 开始不显示拐点， 鼠标经过显示
    //         showSymbol: false,
    //         data: this.right2_info[1][1].map((x)=>{
    //           return x?x:0
    //         })
    //       }
    //       ]
    //     }
    //     this.right2.setOption(option)
  
    //   },
      async Right1() {
        await this.$http.get(this.$api.jobs+'education_info/', {
          
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => {
            this.right1_info = response.data.data
            this.right1.total=response.data.total[0]
          })
          .catch(error => {
            console.error(error)
          });
        // 声明颜色数组
        var myColor = ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"];
        // 2.指定配置项和数据
        var option = {
          grid: {
            top: "10%",
            left: '22%',
            bottom: '10%',
            // containLabel: true
          },
          xAxis: {
            // 不显示x轴相关信息
            show: false
          },
          yAxis: [{
            type: 'category',
            // y轴数据反转，与数组的顺序一致
            inverse: true,
            // 不显示y轴线和刻度
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            // 将刻度标签文字设置为白色
            axisLabel: {
              color: "#fff"
            },
            data: this.right1_info.map((x)=>{
              return x.name
            })
          }, {
            // y轴数据反转，与数组的顺序一致
            inverse: true,
            show: true,
            // 不显示y轴线和刻度
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            // 将刻度标签文字设置为白色
            axisLabel: {
              color: "#fff"
            },
            data: this.right1_info.map((x)=>{
              return x.sum
            })
          }],
          series: [{
            // 第一组柱子（条状）
            name: '条',
            type: 'bar',
            // 柱子之间的距离
            barCategoryGap: 50,
            // 柱子的宽度
            barWidth: 10,
            // 层级 相当于z-index
            yAxisIndex: 0,
            // 柱子更改样式
            itemStyle: {
              barBorderRadius: 20,
              // 此时的color可以修改柱子的颜色
              color: function (params) {
                // params 传进来的是柱子的对象
                // dataIndex 是当前柱子的索引号
                // console.log(params);
                return myColor[params.dataIndex];
              }
            },
            data: this.right1_info.map((x)=>{
              return (Number(x.sum)/Number(this.right1.total)*100).toFixed(2)
            }),
            // 显示柱子内的百分比文字
            label: {
              show: true,
              position: "inside",
              // {c} 会自动解析为数据（data内的数据）
              formatter: "{c}%"
            }
          },
          {
            // 第二组柱子（框状 border）
            name: '框',
            type: 'bar',
            // 柱子之间的距离
            barCategoryGap: 50,
            // 柱子的宽度
            barWidth: 14,
            // 层级 相当于z-index
            yAxisIndex: 1,
            // 柱子修改样式
            itemStyle: {
              color: "none",
              borderColor: "#00c1de",
              borderWidth: 2,
              barBorderRadius: 15,
            },
            data: this.right1_info.map((x)=>{
              return (Number(x.sum)/Number(this.right1.total)*100).toFixed(2)
            })
          }
          ]
        };
        this.right1.setOption(option)
      },
      async Left1() {
        await this.$http.get(this.$api.jobs+'property_info/', {
          
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => {
            this.left1_info = response.data.data
  
          })
          .catch(error => {
            console.error(error)
          });
        this.left1.setOption({
          color: ['#2f89cf'],
          // 提示框组件
          tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          // 修改图表位置大小
          grid: {
            left: '0%',
            top: '10px',
            right: '0%',
            bottom: '4%',
            containLabel: true
          },
          // x轴相关配置
          xAxis: [{
            type: 'category',
            data: this.left1_info.map((x)=>{
              return x.name
            }),
            axisTick: {
              alignWithLabel: true
            },
            // 修改刻度标签，相关样式
            axisLabel: {
              color: "rgba(255,255,255,0.8)",
              fontSize: 10
            },
            // x轴样式不显示
            axisLine: {
              show: false
            }
          }],
          // y轴相关配置
          yAxis: [{
            type: 'value',
            // 修改刻度标签，相关样式
            axisLabel: {
              color: "rgba(255,255,255,0.6)",
              fontSize: 12
            },
            // y轴样式修改
            axisLine: {
              lineStyle: {
                color: "rgba(255,255,255,0.6)",
                width: 2
              }
            },
            // y轴分割线的颜色
            splitLine: {
              lineStyle: {
                color: "rgba(255,255,255,0.1)"
              }
            }
          }],
          // 系列列表配置
          series: [{
            name: '类型',
            type: 'bar',
            barWidth: '35%',
            // ajax传动态数据
            data: this.left1_info.map((x)=>{
              return x.sum
            }),
            itemStyle: {
              // 修改柱子圆角
              barBorderRadius: 5
            }
          }]
        });
      },
     
    },
  
  
  
  }
  </script>
  
  <style lang="less" scoped>
  .filter {
    display: flex;
    flex-direction: row;
    color: white;
    width: 70px;
    font-size: 15px;
    justify-content: space-between;
  }
  
  .filter_active {
    border-bottom: 1.5px gray solid;
  
  }
  
  .filter>div {
    cursor: pointer;
  }
  
  header {
    padding: 20px 15px;
    height: 120px;
  }
  
  .map {
    flex: 1;
  }
  
  .title {
    text-align: center;
    font-size: 40px;
    margin: 0;
    line-height: 40px;
  }
  
  .timer {
  
    font-size: 15px;
    text-align: right;
    color: rgba(255, 255, 255, 0.87);
  }
  
  .no ul {
    margin: 0;
    padding: 0;
  }
  
  .column {
    display: flex;
    flex-direction: column;
  
  }
  
  
  .mainbox .panel{
    height: 400px;
  }
  .mainbox .panel .chart{
    height: 80%;
  }
  .no {
    flex: unset;
  }
  
  .leftchart,
  .rightchart {
    width: 50%;
  }
  
  .centerchart {
    flex: unset
  }
  
  .chart {
    margin-bottom: 20px;
  }
  
  .charts {
    display: flex;
    flex-direction: row;
    flex: 1
  }
  
  @media only screen and (max-width: 990px) {
    .mainbox .panel{
    height: 300px;
  }
    .mainbox {
      width: 100%;
      height: 100%;
    }
  
    .mainbox .panel h2 {
      margin-top: 15px;
    }
  
    .map {
      display: none;
    }
  
    .chart {
      height: 250px !important;
      width: 95%;
    }
  
    .leftchart,
    .rightchart {
      width: 100%;
    }
  
    .timer {
      text-align: center;
    }
  
    header {
      padding: 15px 15px;
      height: 100px;
  
    }
  
    .title {
      text-align: center;
      font-size: 25px;
      margin-bottom: 15px;
      line-height: 20px;
    }
  
    .charts {
      flex-direction: column;
    }
  
  
  }
  </style>