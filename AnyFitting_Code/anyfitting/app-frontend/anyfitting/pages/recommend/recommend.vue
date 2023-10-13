<template>
	<view>
		<view class="recommend">

			<view class="search">
				<image src="../../static/search.png" mode=""></image><input type="text" value=""
					placeholder="Keyword" />
				<view class="search_btn">
					Search
				</view>
			</view>
			<view class="condition">
				<view :class="{active:conditionType==1}" @click="changeConditionType()">
					Hot
				</view>
				<view :class="{active:conditionType==2}" @click="changeConditionType()">
					Guess you like it
				</view>
			</view>
			<view class="list" v-for="(item,index) in recommendData" v-show="conditionType == 1">
				<view class="top">
					<text>Top {{item[0]}}</text>
				</view>
				<view class="hot">
					<text>{{item[3]}}</text>
				</view>
				<image :src="item[2]" mode="widthFix"></image>
			</view>
			<view class="list" v-for="(item,index) in guessData" v-show="conditionType == 2">
				<!-- 	<view class="top">
					<text>top {{item[0]}}</text>
				</view> -->
				<!-- 	<view class="hot">
					<text>{{item[3]}}</text>
				</view> -->
				<image :src="item" mode="widthFix"></image>
			</view>
			<!-- <view class="list">
				<view class="top">
					<text>top 1</text>
				</view>
				<view class="hot">
					<text>20000</text>
				</view>
				<image src="../../static/1.jpeg" mode="widthFix"></image>
			</view> -->
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 筛选类型值，改1或2变动样式
				conditionType: 1,
				recommendData: {},
				guessData: {}
			}
		},
		onLoad() {
			this.getData()
			this.getGuess()
		},
		methods: {
			changeConditionType() {
				if (this.conditionType == 1) {
					this.conditionType = 2
				} else {
					this.conditionType = 1
				}
			},
			getGuess() {
				uni.request({
					url: `/api/recommendation/recommendation`,
					method: 'GET',
					data: {
						uid: '23'
					},
					success: (res) => {
						console.log(res.data.cloth);
						this.guessData = res.data.cloth
						this.conditionType = 2
						console.log(this.guessData)
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			getData() {
				uni.request({
					url: `/api/recommendation/top`,
					method: 'GET',
					data: {
						uid: '23'
					},
					success: (res) => {
						console.log(res);
						this.recommendData = res.data.data
						this.conditionType = 1
					},
					fail(err) {
						console.log(err)
					}
				});
			}
		}
	}
</script>

<style lang="less">
	.recommend {
		background-color: #fff;
		margin-top: calc(var(--status-bar-height) + 156rpx);

		.search {
			display: flex;
			align-items: center;
			justify-content: space-between;
			background-color: #EEE;
			position: fixed;
			top: calc(var(--status-bar-height) + 84rpx);
			left: 0;
			width: 750rpx;
			z-index: 10;

			image {
				width: 44rpx;
				height: 44rpx;
				margin: 0 20rpx;
			}

			input {
				height: 80rpx;
				width: 500rpx;
			}

			.search_btn {
				display: flex;
				align-items: center;
				justify-content: center;
				width: 100rpx;
				height: 80rpx;
				padding: 0 30rpx;
				background-color: #DDD;
			}
		}

		.condition {
			display: flex;
			justify-content: space-between;
			background-color: #FFF;
			position: fixed;
			top: calc(var(--status-bar-height) + 163rpx);
			left: 0;
			width: 750rpx;
			z-index: 10;

			view {
				display: flex;
				justify-content: center;
				width: 50%;
				font-size: 30rpx;
				padding: 20rpx 0;
			}

			.active {
				color: #007AFF;
			}
		}

		.list {
			text-align: center;
			position: relative;
			padding-bottom: 10rpx;

			.top {
				position: absolute;
				width: 100rpx;
				height: 100rpx;
				top: 10rpx;
				left: 10rpx;
				// border: 2rpx solid rgba(39, 39, 39, .2);
				background-color: rgba(39, 39, 39, .2);
				color: #FFF;
				z-index: 1;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: 10rpx;
			}

			.hot {
				position: absolute;
				width: 100rpx;
				height: 100rpx;
				top: 10rpx;
				right: 10rpx;
				z-index: 1;
				// border: 2rpx solid rgba(39, 39, 39, .2);
				background-color: rgba(39, 39, 39, .2);
				color: #FFF;
				display: flex;
				justify-content: center;
				align-items: center;
				border-radius: 10rpx;
			}

			image {
				width: 750rpx;

				// border: 2rpx solid #CCC;
				border-radius: 10rpx;
			}
		}
	}
</style>
