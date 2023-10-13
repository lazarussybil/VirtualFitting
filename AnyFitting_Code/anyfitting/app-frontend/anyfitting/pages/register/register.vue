<template>
	<view class="container">
	<!-- 	<view class="header" v-show="pageMode=='update'">
			<text>Profile Photo</text>
			<image @click="selectImg()" src="../../static/regiter.png" mode="widthFix"></image>
		</view> -->
		<input type="text" v-model="nickname" placeholder="Nickname" v-show="pageMode=='update'" />
		<input type="text" v-model="accountNum" placeholder="Account number" />
		<input type="password" v-model="password" placeholder="Password" />
		<view class="date" v-show="pageMode=='update'">
			<view class="uni-list-cell-left">
				Birthday
			</view>
			<view class="uni-list-cell-db">
				<picker mode="date" :value="date" :start="startDate" :end="endDate" @change="bindDateChange">
					<view class="uni-input">{{date}}</view>
				</picker>
			</view>
		</view>

		<radio-group @change="radioChange" class="radio_box" v-show="pageMode=='update'">
			<label class="radio_item" v-for="(item, index) in items" :key="item.value">
				<view>
					<radio :value="item.value" :checked="index === current" />
				</view>
				<view>{{item.name}}</view>
			</label>
		</radio-group>
		<radio-group @change="typeRadioChange" class="radio_box" v-show="pageMode!='update'">
			<label class="radio_item" v-for="(item, index) in typeItems" :key="item.value">
				<view>
					<radio :value="item.value" :checked="index === current" />
				</view>
				<view>{{item.name}}</view>
			</label>
		</radio-group>
		<view class="header" v-show="pageMode=='update'">
			<text>Personal Portrait</text>
			<image @click="selectImg()" :src="picture == '' ? '../../static/regiter.png' : picture" mode="widthFix"></image>
		</view>
		<button class="btn" type="primary" v-if="pageMode != 'update'" @click="register()">register</button>
		<button class="btn" type="primary" v-if="pageMode == 'update'" @click="updateUserInfo()">Update
			information</button>
	</view>
</template>

<script>
	export default {
		data() {
			const currentDate = this.getDate({
				format: true
			})
			return {
				date: currentDate,
				items: [{
						value: 'male',
						name: 'Male',
						checked: true
					},
					{
						value: 'female',
						name: 'Female',
						checked: false
					}
				],
				typeItems: [{
						value: '1',
						name: 'Personal',
						checked: true
					},
					{
						value: '2',
						name: 'Business',
						checked: false
					}
				],
				// 用户类型
				userType:'',
				// 用户账号
				accountNum: '',
				password: '',
				// 昵称
				nickname: '',
				birthday: '',
				sex: '',
				// 个人图像
				picture:'',
				// 单选值的当前checked
				current: 0,

				// 页面模式是update就是更新信息,根据这个判断请求是注册还是更新
				pageMode: '',
				
				// 用户信息，自动填写之前的信息在页面上用
				userInfo: {},
				
				// // 好像没用了，暂时留着
				// personalmage:''
			}
		},
		computed: {
			startDate() {
				return this.getDate('start');
			},
			endDate() {
				return this.getDate('end');
			}
		},
		onLoad(options) {
			console.log(options)
			if (options.mode == "update") {
				this.pageMode = "update"
				uni.setNavigationBarTitle({
					title: "Update information"
				})
				this.getUserInfo()
			}
		},
		methods: {
			register() {
				uni.request({
					url: `/api/user/register`,
					method: 'GET',
					data: {
						type: 1,
						mailbox: this.accountNum,
						password: this.password,
					},
					success: (res) => {
						console.log(res);
						uni.showToast({
							title: res.data.message,
							duration: 2000
						});
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			updateUserInfo() {
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
					// header: {
					// 	"Content-Type": "application/x-www-form-urlencoded"
					// }, // 请求头
					url: `/api/user/info/update`,
					method: 'GET',
					data: {
						id: id,
						mailbox: this.accountNum,
						password: this.password,
						nickname: this.nickname,
						birthday: this.date,
						sex: this.sex,
						picture:this.picture
					},
					success: (res) => {
						console.log(res);
						uni.switchTab({
							url:'../user/user'
						})
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			// 获取用户信息
			getUserInfo() {
				console.log('getuserinfo')
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
						this.accountNum = res.data.data.mailbox
						this.nickname = res.data.data.nickname
						this.picture = res.data.data.figure
						if(res.data.data.sex == 'male'){
							this.items[0].checked = true
							this.items[1].checked = false
							this.sex = 'male'
							this.current = 0
						}else{
							console.log('female')
							this.items[1].checked = true
							this.items[0].checked = false
							this.sex = 'female'
							this.current = 1
						}
						
					},
					fail(err) {
						console.log(err)
					}
				});
			},
			selectImg() {
				let _this = this
				uni.chooseImage({
					count: 6, //默认9
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
								console.log(uploadFileRes);
								let data = JSON.parse(uploadFileRes.data)
								_this.picture = data.data.cloth_url
								console.log(_this.picture)
							}
						});
					}
				});

			},
			typeRadioChange(evt){
				console.log(evt.detail.value)
				this.userType = evt.detail.value
				for (let i = 0; i < this.items.length; i++) {
					if (this.items[i].value === evt.target.value) {
						this.current = i;
						break;
					}
				}
			},
			radioChange: function(evt) {
				console.log(evt.detail.value)
				this.sex = evt.detail.value
				for (let i = 0; i < this.items.length; i++) {
					if (this.items[i].value === evt.target.value) {
						this.current = i;
						break;
					}
				}
			},
			bindPickerChange: function(e) {
				console.log('picker发送选择改变，携带值为', e.target.value)
				this.index = e.target.value
			},
			bindDateChange: function(e) {
				console.log(e)
				this.date = e.target.value
			},
			bindTimeChange: function(e) {
				this.time = e.target.value
			},
			getDate(type) {
				const date = new Date();
				let year = date.getFullYear();
				let month = date.getMonth() + 1;
				let day = date.getDate();

				if (type === 'start') {
					year = year - 60;
				} else if (type === 'end') {
					year = year + 2;
				}
				month = month > 9 ? month : '0' + month;;
				day = day > 9 ? day : '0' + day;
				return `${year}-${month}-${day}`;
			}
		}
	}
</script>

<style lang="less">
	.container {
		padding: 20rpx;
		height: 100vh;
		width: 750rpx;
		background-color: rgb(248, 248, 248);

		input {
			width: 710rpx;
			height: 100rpx;
			box-sizing: border-box;
			padding-left: 20rpx;
			border-radius: 20rpx;
			margin-bottom: 20rpx;
			background-color: #FFF;
		}
	}

	.header {
		width: 710rpx;
		height: 150rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
		background-color: #FFF;
		padding: 20rpx;
		border-radius: 20rpx;
		box-sizing: border-box;
		margin-bottom: 20rpx;

		image {
			width: 100rpx;
			height: 100rpx;
		}
	}

	.date {
		display: flex;
		width: 710rpx;
		background-color: #FFF;
		height: 100rpx;
		align-items: center;
		padding-left: 20rpx;
		box-sizing: border-box;
		border-radius: 20rpx;
		margin-bottom: 20rpx;

		.uni-list-cell-db {
			margin-left: 20rpx;
		}
	}

	.radio_box {
		display: flex;
		width: 710rpx;
		background-color: #FFF;
		height: 100rpx;
		align-items: center;
		border-radius: 20rpx;
		padding-left: 20rpx;
		box-sizing: border-box;
		margin-bottom: 20rpx;
	}

	.radio_item {
		display: flex;
		align-items: center;
		margin-right: 20rpx;
	}

	.btn {
		width: 710rpx;
		margin: 0;
	}
</style>
