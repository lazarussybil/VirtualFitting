<template>
	<view class="bg">
		<!-- 信息反馈 -->
		<textarea v-model="msg" placeholder="Please input the information you want to feedback" maxlength="-1" auto-height/>
		<button type="primary" @click="sendMsg">Submit</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				msg:''
			}
		},
		methods: {
			sendMsg(){
				
				uni.showToast({
				    title: 'Submission Successful',
				    duration: 2000
				});
			}
		}
	}
</script>

<style lang="less">
	.bg{
		height: 100vh;
		background-color: rgb(248,248,248);
		textarea{
			width: 650rpx;
			margin: 0 auto;
			background-color: #FFF;
			border-radius: 20rpx;
			padding: 20rpx;
			box-sizing: border-box;
			min-height: 300rpx;
		}
		button{
			margin-top: 20rpx;
			width: 690rpx;
			border-radius: 20rpx;
		}
	}
</style>
