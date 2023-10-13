<template>
	<view class="container">
		<view class="" style="text-align: center;width: 100%;">
			Popularity Trend
		</view>
		<image src="../../static/data3.jpeg" mode="widthFix"></image>
		<view class="" style="text-align: center;width: 100%;margin-top: 50rpx;">
			Color Distribution
		</view>
		<image src="../../static/data2.jpg" mode="widthFix"></image>
		<view class="" style="display: flex;width: 100%;text-align: center;">
			<text style="width:50%">Female Most Liked</text>
			<text style="width:50%">Male Most Liked</text>
		</view>
		<image class="smallImg" src="../../static/data4.png" mode="widthFix"></image>
		<image class="smallImg" src="../../static/data5.png" mode="widthFix"></image>
		<businessTabbar active="1"></businessTabbar>
	</view>
</template>

<script>
	export default {
		data() {
			return {

			}
		},
		methods: {

		}
	}
</script>

<style lang="less">
	.container {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		padding: 20rpx;
		padding-bottom: 200rpx;
		text-align: center;

		image {
			width: 710rpx;
			margin: 0 auto;
			border-radius: 20rpx;
		}

		.smallImg {
			width: 340rpx;
			margin-top: 20rpx;
		}
	}
</style>
