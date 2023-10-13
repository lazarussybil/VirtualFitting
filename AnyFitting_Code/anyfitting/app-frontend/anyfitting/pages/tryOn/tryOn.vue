<template>
	<view class="container">
		<view class="top">
			<image @click="uploadCloth()" v-if="isShowDefaultImg" src="../../static/1.jpeg" mode="widthFix"
				></image>
		<!-- 	<image @click="uploadCloth()" v-if="isShowDefaultImg" :src="human_url" mode="widthFix"
				style="width: 500rpx;padding: 180rpx 0;"></image> -->
			<!-- <image @click="uploadCloth()" v-if="!isShowDefaultImg" :src="tryonImg" mode="widthFix"></image> -->
			<image @click="previewImg(tryonImg)" v-if="!isShowDefaultImg" :src="tryonImg" mode="widthFix"></image>
			<view class="btn_box">
				<view class="bth" @click="tryon2()">
					<image src="../../static/tryon3.png" mode="widthFix"></image>
				</view>
				<view class="bth" @click="likeImg()">
					<image :src="isLikeActive ? '../../static/love_active.png' : '../../static/love.png'"
						mode="widthFix"></image>
				</view>
			</view>
		</view>
		<!-- 		<view class="clothes">
			<view class="clothes_item" :class="{actice_border: currentHuman == 0}">
				<image :src="getHumanUrlData" mode="aspectFill"></image>
			</view>
			<view class="clothes_item">
				<image src="../../static/1.jpeg" mode="aspectFill"></image>
			</view>
		</view> -->
		<view class="clothes recommend_clothes">
			<view class="clothes_item recommend_clothes_item" :class="{active_border:isUploadImageActive}">
				<image :src="uploadImage" mode="widthFix" @click="uploadCloth()"></image>
			</view>
			<view class="clothes_item recommend_clothes_item" :class="{active_border: currentLike == index}"
				v-for="(item,index) in likeData" @click="changeCurrentLike(index)">
				<image :src="item[3]" mode="aspectFill"></image>
			</view>
			<!-- <view class="clothes_item recommend_clothes_item">
				<image src="../../static/1.jpeg" mode="aspectFill"></image>
			</view> -->
		</view>
		<view class="" style="text-align: center;margin-top: 20rpx;">
			Discover More
		</view>
		<view class="clothes recommend_clothes">
			<view class="clothes_item" style="width: 150rpx;margin-right: 20rpx;text-align: center;">
				<!-- <text style="width: 150rpx;display: block;">More</text> -->
			</view>
			<view class="clothes_item recommend_clothes_item" :class="{active_border: currentRecommend == index}"
				v-for="(item,index) in recommendData" @click="changeCurrentRecommend(index)">
				<image :src="item[2]" mode="aspectFill"></image>
			</view>
			<!-- <view class="clothes_item recommend_clothes_item">
				<image src="../../static/1.jpeg" mode="aspectFill"></image>
			</view> -->
		</view>
		<view class="bottom_btn">
			<!-- 	<button type="default" @click="uploadCloth()">上传衣服图片</button>
			<button type="default" @click="uploadHuman()">上传个人图片</button> -->
			<!-- <button type="default" class="max_btn" @click="tryon2()">试穿</button> -->
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				isShowDefaultImg: true,
				cloth_url: '',
				human_url: '',
				tryonImg: '',

				// 接口获取的humanurl
				getHumanUrlData: '',
				// 当前选中humanurl
				currentHuman: -1,

				isLogin: false,
				recommendData: {},
				currentRecommend: -1,
				likeData: {},
				currentLike: -1,
				uploadImage: '../../static/regiter.png',
				isUploadImageActive: false,
				isLikeActive: false
			}
		},
		onLoad() {
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					console.log(res.data);
					this.getHumanUrl()
					this.isLogin = true
				}
			});
			this.getRecommend()
			this.getLike()
		},
		methods: {
			likeImg() {
				this.isLikeActive = !this.isLikeActive
				// uni.request({
				// 	url: `/api/user/likelist`,
				// 	method: 'GET',
				// 	data: {
				// 		id: uni.getStorageSync('user_id'),
				// 		cloth_url:this.tryonImg
				// 	},
				// 	success: (res) => {
				// 		console.log(res)
				// 	},
				// 	fail(err) {
				// 		console.log(err)
				// 	}
				// });
			},
			uploadCloth() {
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
								_this.uploadImage = data.data.cloth_url
								_this.isUploadImageActive = true
								_this.currentRecommend = -1
								_this.currentLike = -1
								console.log(_this.uploadImage)
								console.log(uploadFileRes);
							}
						});
					}
				});
			},
			uploadHuman() {

			},
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
			},
			getLike() {
				uni.request({
					url: `/api/user/likelist`,
					method: 'GET',
					data: {
						userid: '21'
					},
					success: (res) => {
						console.log('like', res);
						this.likeData = res.data.data
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			changeCurrentLike(index) {
				this.currentLike = index
				this.currentRecommend = -1
				this.isUploadImageActive = false
			},
			changeCurrentRecommend(index) {
				this.currentRecommend = index
				this.currentLike = -1
				this.isUploadImageActive = false
			},
			getRecommend() {
				uni.request({
					url: `/api/recommendation/top`,
					method: 'GET',
					data: {
						uid: '21'
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

			getHumanUrl() {
				
				uni.request({
					url: `/api/user/info/image`,
					method: 'GET',
					data: {
						uid: uni.getStorageSync('user_id'),
					},
					success: (res) => {
						// uni.showToast({
						// 	title: res.message,
						// 	duration: 2000
						// });
						console.log('getHumanUrl',res);
						this.getHumanUrlData = res.data.data.human_url
						this.human_url = res.data.data.human_url
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			uploadImg() {
				let _this = this
				if (this.cloth_url == '') {
					uni.showToast({
						title: 'Please choose a picture of clothes',
						duration: 3000
					});
				} else if (_this.isLogin == false) {
					uni.showToast({
						title: 'Please choose a personal picture',
						duration: 3000
					});
				}
				if (this.cloth_url == '') {
					this.selectImg()
				} else if (this.isLogin) {
					// this.tryon()
				} else {
					this.selectImg()
				}

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
								if (_this.cloth_url == '') {
									let data = JSON.parse(uploadFileRes.data)
									_this.cloth_url = data.data.cloth_url
									console.log(_this.cloth_url)
									// 上传衣服图片后判断是否已经登陆,登陆了直接试穿
									if (_this.isLogin) {
										_this.tryon()
									}
								} else {

									console.log('上传个人图片')
									let data = JSON.parse(uploadFileRes.data)
									_this.human_url = data.data.cloth_url
									console.log(_this.human_url)
									_this.tryon()
								}
								console.log(uploadFileRes);
							}
						});
					}
				});
			},
			tryon() {
				console.log('tryon')
				uni.showLoading()
				uni.request({
					// url: `/api/tryon/tryon`,
					url: `http://csc4001.hugoycj.club/tryon/tryon`,
					method: 'GET',
					data: {
						cloth_url: this.cloth_url,
						human_url: this.human_url,
					},
					success: (res) => {
						uni.showToast({
							title: res.message,
							duration: 2000
						});
						console.log(res);
						this.isShowDefaultImg = false
						this.tryonImg = res.data.data.tryon_url
						this.cloth_url = ''
						this.human_url = ''
						uni.hideLoading()
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			tryon2() {
				this.isLikeActive = false
				console.log('tryon2')
				uni.showLoading()
				let cloth_url = ''
				if (this.currentLike != -1) {
					cloth_url = this.likeData[this.currentLike]
				}
				if (this.currentRecommend != -1) {
					cloth_url = this.recommendData[this.currentRecommend][2]
				}
				if (this.isUploadImageActive) {
					cloth_url = this.uploadImage
				}
				uni.request({
					// url: `/api/tryon/tryon`,
					url: `http://csc4001.hugoycj.club/tryon/tryon`,
					method: 'GET',
					data: {
						cloth_url: cloth_url,
						human_url: this.getHumanUrlData,
					},
					success: (res) => {
						uni.showToast({
							title: res.message,
							duration: 2000
						});
						console.log(res);
						this.isShowDefaultImg = false
						this.tryonImg = res.data.data.tryon_url
						this.cloth_url = ''
						this.human_url = ''
						uni.hideLoading()
					},
					fail(err) {
						console.log(err)
					}
				});
			},
		}
	}
</script>

<style lang="less">
	@media screen and (max-width: 300px) {
		.container {
			background-color: pink;
		}
	}

	.active_border {
		border: 7rpx solid red;
	}

	.container {

		.top {
			position: relative;
			display: flex;
			justify-content: center;
			align-items: center;
			background-color: rgb(245, 245, 245);

			image {
				width: 750rpx;
			}

			.btn_box {
				.bth {
					position: absolute;
					width: 120rpx;
					height: 120rpx;
					display: flex;
					justify-content: center;
					align-items: center;
					background-color: rgba(100, 100, 100, .2);
					border-radius: 50%;

					&:nth-child(1) {
						bottom: 30rpx;
						left: 30rpx;
					}

					&:nth-child(2) {
						bottom: 30rpx;
						right: 30rpx;
					}

					image {
						width: 80rpx;
						height: 80rpx;
					}
				}
			}
		}

		.clothes {
			padding: 10rpx 20rpx;
			margin-top: 10rpx;
			display: flex;
			align-items: center;
			overflow: scroll;

			.active_clothes {
				border: 2rpx solid #CCC;
			}

			// border-radius: 20rpx;
			.clothes_item {
				display: flex;
				justify-content: center;
				align-items: center;
				border-radius: 20rpx;
				width: 150rpx;
				margin-right: 20rpx;
				padding: 0rpx 0;

				image {
					width: 150rpx;
					height: 200rpx;
					border-radius: 20rpx;
					// margin-right: 20rpx;
				}
			}
		}

		.bottom_btn {
			display: flex;
			justify-content: space-between;
			flex-wrap: wrap;

			button {
				width: 300rpx;
			}

			.max_btn {
				width: 680rpx;
				margin-top: 30rpx;
				margin-bottom: 30rpx;
			}
		}
	}
</style>
