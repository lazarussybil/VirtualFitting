<template>
	<view class="tabbar">
		<view v-if="active==1" class="item" @click="jump('/pages/businessData/businessData')">
			<image style="width: 50rpx;margin-top: 3rpx;" src="../../static/tabbar5_active.png" mode="widthFix"></image>
			<text>Data</text>
		</view>
		<view v-if="active!=1" class="item" @click="jump('/pages/businessData/businessData')">
			<image style="width: 50rpx;margin-top: 3rpx;" src="../../static/tabbar5.png" mode="widthFix"></image>
			<text>Data</text>
		</view>
<!-- 		<view v-if="active==2" class="item" @click="jump('/pages/businessWarehousing/businessWarehousing')">
			<image src="../../static/tabbar1_active.png" mode="widthFix"></image>
			<text>入库</text>
		</view>
		<view v-if="active!=2" class="item" @click="jump('/pages/businessWarehousing/businessWarehousing')">
			<image src="../../static/tabbar1.png" mode="widthFix"></image>
			<text>入库</text>
		</view> -->
		<view v-if="active==3" class="item" @click="jumpTabbar('/pages/user/user')">
			<image src="../../static/tabbar4_active.png" mode="widthFix"></image>
			<text>Business</text>
		</view>
		<view v-if="active!=3" class="item" @click="jumpTabbar('/pages/user/user')">
			<image src="../../static/tabbar4.png" mode="widthFix"></image>
			<text>Business</text>
		</view>



	</view>
</template>

<script>
	export default {
		name: "businessTabbar",
		data() {
			return {

			};
		},
		props: {
			active: {
				default: 1
			}
		},
		methods: {
			jump(url) {
				console.log(url)
				uni.navigateTo({
					url: url
				});
			},
			jumpTabbar(url) {
				uni.switchTab({
					url: url
				});
			}
		}
	}
</script>

<style lang="less">
	.tabbar {
		background-color: #FFF;
		border-top: 1rpx solid #CCC;
		// height: 100rpx;
		z-index: 10;
		position: fixed;
		bottom: 0;
		left: 0;
		width: 750rpx;
		display: flex;
		justify-content: space-around;

		.item {
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: space-between;
			width: 33%;

			image {
				width: 50rpx;
				margin-top: 3rpx;
			}

			text {
				font-size: 30rpx;
			}
		}
	}
</style>
