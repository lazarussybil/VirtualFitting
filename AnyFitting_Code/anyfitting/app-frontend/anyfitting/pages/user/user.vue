<template>
	<view class="bg">
		<businessTabbar v-show="type == 2" active="3"></businessTabbar>
		<!-- 登陆弹窗 -->
		<view class="login_popup" @click="isShowLogin=false" v-show="isShowLogin">
			<view class="login" @click.stop="">
				<text class="title">Login account</text>
				<input type="text" v-model="loginMail" placeholder="Account number" />
				<input type="password" v-model="loginPwd" placeholder="Password" />
				<button type="primary" @click="login">Login</button>
				<view class="forgetpwd">
					<text @click="jump(`/pages/register/register`)">Register</text>
					<!-- <text>Forget the password</text> -->
				</view>
			</view>
		</view>
		<view class="user_info">
			<view class="info">
				<image :src="(userInfo.figure == 'None' || null) ? '../../static/user.png' : userInfo.figure" mode="widthFix">
				</image>
				<view class="text">
					<text>{{userInfo.nickname}}</text>
					<!-- <text>用户信息</text> -->
				</view>
			</view>
		</view>
		<!-- 菜单列表 -->
		<view class="menu">
			<view class="list" @click="jump(`/pages/register/register?mode=update`)">
				<image src="../../static/user6.png" mode="widthFix"></image>
				<text>Update Information</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" @click="jump(`/pages/register/register`)">
				<image src="../../static/user1.png" mode="widthFix"></image>
				<text>Register</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" @click="isShowLogin = true" v-show="!isLogin">
				<image src="../../static/user2.png" mode="widthFix"></image>
				<text>Login</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" v-show="type!=2" @click="jump(`/pages/collectionList/collectionList`)">
				<image src="../../static/user3.png" mode="widthFix"></image>
				<text>Collection List</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" v-show="type!=2" @click="jump(`/pages/collectionList/collectionList?mode=tryon`)">
				<image src="../../static/user4.png" mode="widthFix"></image>
				<text>Try on list</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" v-show="type==2" @click="jump(`/pages/businessWarehousing/businessWarehousing`)">
				<image src="../../static/user4.png" mode="widthFix"></image>
				<text>BusinessWarehousing</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" @click="jump(`/pages/feedback/feedback`)">
				<image src="../../static/user5.png" mode="widthFix"></image>
				<text>Feedback</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
			<view class="list" @click="LogOut">
				<image src="../../static/user7.png" mode="widthFix"></image>
				<text>LogOut</text>
				<image class="right_icon" src="../../static/user_right.png" mode="widthFix"></image>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 登陆弹窗控制
				isShowLogin: true,
				// 是否已经登陆
				isLogin: false,
				// 商家类型type2
				type: 1,
				loginMail: '',
				loginPwd: '',
				userInfo: {
					figure: 'None'
				}
			}
		},
		onLoad() {
			let _this = this
			//仅作为演示隐藏系统默认tabbar，type2的时候显示商家的tabbar
			if (false) {
				uni.hideTabBar()
			}

		},
		onShow() {
			let _this = this
			uni.getStorage({
				key: 'user_id',
				success: function(res) {
					console.log('user_id', res.data);
					if(res.data == 24){
						_this.type = 2
						uni.hideTabBar()
					}
					_this.isShowLogin = false
					_this.isLogin = true
					_this.getUserInfo()
				}
			});
		},
		methods: {
			// 获取用户信息
			getUserInfo() {
				let id
				try {
					id = uni.getStorageSync('user_id');
					if (value) {
						console.log(value);
					}
				} catch (e) {
					// error
				}
				uni.request({
					url: `/api/user/info/display`,
					method: 'GET',
					data: {
						id: id
					},
					success: (res) => {
						console.log(res.data);
						this.userInfo = res.data.data
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			// 退出登陆
			LogOut() {
				let _this = this
				uni.removeStorage({
					key: 'user_id',
					success: function(res) {
						console.log('success');
						uni.showToast({
							title: 'LogOut',
							duration: 2000
						});
						_this.isLogin = false
						_this.type = 1
						uni.switchTab({
							url:'/pages/user/user'
						})
					}
				});
			},
			jump(url) {
				console.log(url)
				uni.navigateTo({
					url: url
				});
			},
			login() {
				uni.request({
					url: `/api/user/login`,
					method: 'GET',
					data: {
						mailbox: this.loginMail,
						password: this.loginPwd
					},
					success: (res) => {
						uni.showToast({
							title: res.data.message,
							duration: 2000
						});
						uni.setStorage({
							key: 'user_id',
							data: res.data.data.ID,
							success: function() {
								console.log('success');
							}
						});
						console.log(res.data);
						if (res.data.code == 200) {
							this.isShowLogin = false
							this.isLogin = true
							this.getUserInfo()
						}
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			register() {
				uni.request({
					url: `/api/user/register`,
					method: 'POST',
					data: {
						id: '123456',
						password: '123456'
					},
					success: (res) => {
						console.log(res.data);
						uni.setStorage({
							key: 'user_id',
							data: res.data.id,
							success: function() {
								console.log('success');
							}
						});
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
	.bg {
		height: 100vh;
		background-color: rgb(248, 248, 248);
		padding-top: 20rpx;
	}

	.login_popup {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, .7);
		z-index: 1;
		display: flex;
		align-items: center;
		justify-content: center;

		.login {
			background-color: #FFF;
			width: 550rpx;
			padding: 30rpx;
			border-radius: 20rpx;
			text-align: center;

			.title {
				font-size: 45rpx;

			}

			input {
				text-align: left;
				height: 100rpx;
				padding: 10rpx 30rpx;
				box-sizing: border-box;
				border: 1rpx solid #CCC;
				border-radius: 20rpx;
				margin-top: 30rpx;

			}

			button {
				border-radius: 20rpx;
				margin-top: 20rpx;
			}

			.forgetpwd {
				text-align: right;
				color: #007AFF;
				font-size: 30rpx;
				margin-top: 15rpx;
				margin-right: 5rpx;
				display: flex;
				justify-content: space-between;
			}
		}
	}

	.user_info {
		margin: 0 20rpx;
		padding: 20rpx;
		background-color: #FFF;
		border-radius: 20rpx;

		.info {
			display: flex;
			align-items: center;

			image {
				margin-left: 30rpx;
				border-radius: 10rpx;
				height: 100rpx;
				width: 100rpx;
			}

			.text {
				display: flex;
				flex-direction: column;

				margin-left: 30rpx;
			}

		}
	}

	.menu {
		margin-top: 30rpx;
		background-color: #FFF;
		margin: 20rpx;
		margin-top: 30rpx;
		border-radius: 20rpx;

		.list {
			display: flex;
			align-items: center;
			padding: 30rpx 30rpx;
			border-bottom: 1rpx solid #f1eef3;

			position: relative;

			image {
				width: 40rpx;
				height: 40rpx;

			}

			text {
				margin-left: 20rpx;
			}

			.right_icon {
				width: 30rpx;
				height: 30rpx;
				position: absolute;
				right: 20px;
			}
		}
	}
</style>
