<template>
	<view>
		<view class="list">

	<!-- 		<view class="img_box" v-for="(item,index) in list">
				<image class="main_img" @click="previewImg(item.imgUrl)" :src="item.imgUrl" mode="widthFix"></image>
				<image class="guanbi" @click="list[index].isActive = !list[index].isActive"
					:src="item.isActive ? '../../static/sc_active.png' :'../../static/sc.png'" mode=""></image>
			</view> -->
			<view class="img_box" v-for="(item,index) in likeData">
				<image class="main_img" @click="previewImg(item[3])" :src="item[3]" mode="aspectFill"></image>
			<!-- 	<image class="guanbi" @click="list[index].isActive = !list[index].isActive"
					:src="item.isActive ? '../../static/sc_active.png' :'../../static/sc.png'" mode=""></image> -->
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 页面模式是tryon就是试穿列表,根据这个判断请求是试穿还是收藏列表
				pageMode: '',
				list: [{
					imgUrl: '../../static/1.jpeg',
					isActive: false
				}, {
					imgUrl: '../../static/1.jpeg',
					isActive: true
				}, {
					imgUrl: '../../static/1.jpeg',
					isActive: false
				}, ],
				likeData: {}
			}
		},
		onLoad(options) {
			console.log(options)
			if (options.mode == 'tryon') {
				this.pageMode = 'tryon'
				uni.setNavigationBarTitle({
					title: "Try on list"
				})
			}
			this.getLike()
		},
		methods: {
			getLike() {
				uni.request({
					url: `/api/user/likelist`,
					method: 'GET',
					data: {
						userid: '21'
					},
					success: (res) => {
						console.log(res);
						this.likeData = res.data.data
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
		},

	}
</script>

<style lang="less">
	.list {
		display: flex;
		// justify-content: space-around;
		flex-wrap: wrap;
		padding: 20rpx;
		padding-left: 0;

		.img_box {
			position: relative;
			width: 223rpx;
			margin-left: 20rpx;
			margin-top: 20rpx;

			.main_img {
				width: 100%;
				box-sizing: border-box;
				border-radius: 20rpx;
				height: 250rpx;
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
	}
</style>
