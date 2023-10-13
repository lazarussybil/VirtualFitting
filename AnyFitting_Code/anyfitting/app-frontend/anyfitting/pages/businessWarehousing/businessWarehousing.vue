<template>
	<view class="container">
		<!-- <businessTabbar active="2"></businessTabbar> -->
		<!-- <image @click="selectImg()" src="../../static/regiter.png" mode="widthFix"></image> -->
		<view class="img_box">
			<image class="main_img" @click="selectImg()" src="../../static/regiter.png" mode="widthFix"></image>
		</view>
		<view class="img_box" v-for="(item,index) in uploadImage">
			<image class="main_img" @click="previewImg(item)" :src="item" mode="aspectFill"></image>
			<image class="guanbi" src="../../static/guanbi.png" mode=""></image>
		</view>
		<view class="img_box" v-for="(item,index) in recommendData">
			<image class="main_img" @click="previewImg(item[2])" :src="item[2]" mode="aspectFill"></image>
			<image class="guanbi" src="../../static/guanbi.png" mode=""></image>
		</view>
<!-- 		<view class="img_box">
			<image class="main_img" @click="previewImg('../../static/1.jpeg')" src="../../static/1.jpeg"
				mode="widthFix"></image>
			<image class="guanbi" src="../../static/guanbi.png" mode=""></image>
		</view> -->
		<button type="primary" @click="upload()">Upload All</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				uploadImage: [],
				recommendData: {}
			}
		},
		onLoad() {
			this.getData()
		},
		methods: {
			upload(){
				
				uni.showToast({
					title:'Upload complete'
				})
			},
			selectImg() {
				let _this = this
				uni.chooseImage({
					count: 1, //默认9
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: function(res) {
						console.log(res)
						console.log(JSON.stringify(res.tempFilePaths));
						const tempFilePaths = res.tempFilePaths[0];
						uni.uploadFile({
							url: 'api/user/upload/pictures',
							filePath: tempFilePaths,
							name: 'image',
							success: (uploadFileRes) => {
								let data = JSON.parse(uploadFileRes.data)
								_this.uploadImage = [data.data.cloth_url,..._this.uploadImage,] 
								console.log(_this.uploadImage)
								console.log(uploadFileRes);
							}
						});
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
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			// 传图片路径进来全屏预览
			previewImg(url) {
				console.log(url)
				uni.previewImage({
					urls: [url],
					longPressActions: {
						itemList: ['发送给朋友', '保存图片', '收藏'],
						success: function(data) {
							console.log('选中了第' + (data.tapIndex + 1) + '个按钮,第' + (data.index + 1) + '张图片');
						},
						fail: function(err) {
							console.log(err.errMsg);
						}
					}
				});
			}
		}
	}
</script>

<style lang="less">
	.container {
		padding: 30rpx;
		display: flex;
		flex-wrap: wrap;

		.img_box {
			position: relative;
			width: 30%;
			margin-left: 20rpx;
			margin-top: 20rpx;

			.main_img {
				width: 100%;
				height: 250rpx;
				box-sizing: border-box;
				border-radius: 20rpx;
			}

			.guanbi {
				position: absolute;
				width: 30rpx;
				height: 30rpx;
				background-color: rgba(228, 132, 135, 0.2);
				border-radius: 50%;
				border: 1rpx solid rgba(228, 132, 135, 0.2);
				z-index: 10;
				right: -7rpx;
				top: -7px;
				padding: 3rpx;
			}
		}

		button {
			border-radius: 20rpx;
			position: fixed;
			bottom: 20rpx;
			width: 690rpx;
		}
	}
</style>
