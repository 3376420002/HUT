<template>
  <div id="Login">
    <div class="login-form">
      <h2 class="login-title">{{ isRegistering ? '用户注册' : '用户登录' }}</h2>
      <el-form :model="loginForm" :rules="loginRules" ref="loginForm" @keyup.enter.native="handleSubmit">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="el-icon-user"
            :placeholder="isRegistering ? '请输入用户名' : '请输入用户名'"></el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" type="password" show-password
            :placeholder="isRegistering ? '请输入密码' : '请输入密码'"></el-input>
        </el-form-item>

        <!-- 注册专用字段 -->
        <template v-if="isRegistering">
          <div class="inline-form-items">
            <el-form-item label="邮箱" class="inline-form-item" prop="email">
              <el-input v-model="loginForm.email" prefix-icon="el-icon-message"></el-input>
            </el-form-item>
            <el-form-item label="手机号" class="inline-form-item" prop="phone">
              <el-input v-model="loginForm.phone" prefix-icon="el-icon-phone"></el-input>
            </el-form-item>
          </div>
        </template>

        <div class="login-options">
          <el-button type="text" @click="toggleForm" class="login-option">
            {{ isRegistering ? '已有账号？去登录' : '没有账号？立即注册' }}
          </el-button>
        </div>

        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleSubmit" :loading="loading">
            {{ isRegistering ? '立即注册' : '立即登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRegistering: false,
      loading: false,
      loginForm: {
        username: '',
        password: '',
        email: '',
        phone: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          setTimeout(() => {
            this.loading = false
            if (this.isRegistering) {
              this.$message.success('注册成功！')
              this.$refs.loginForm.resetFields()
              this.isRegistering = false
            } else {
              this.$router.push('/analyses')
            }
          }, 1000)
        }
      })
    },
    toggleForm() {
      this.isRegistering = !this.isRegistering
      this.$nextTick(() => {
        this.$refs.loginForm.clearValidate()
      })
    }
  }
}
</script>

<style scoped>
#Login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100% - 40px);
  width: calc(100% - 15px);
  background-image: url('@/assets/login-bg.png');
  background-size: cover;
  background-position: center;
  position: absolute;
}

.login-form {
  width: 400px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-title {
  margin-bottom: 30px;
  text-align: center;
  color: #ffffff;
}

.login-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.login-option {
  color: #ffffff;
  font-size: 13px;
}

.login-btn {
  width: 100%;
  height: 45px;
  padding: 0 20px;
  font-size: 16px;
  color: #ffffff;
  border-color: #ffffff;
  background-color: transparent;
}

.el-input :deep(.el-input__inner) {
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: transparent;
}

.el-input :deep(.el-input__inner)::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.el-input :deep(.el-input__inner):focus {
  box-shadow: 0 0 0 2px rgba(195, 102, 48, 0.2);
}

.inline-form-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.inline-form-item :deep(.el-form-item__content) {
  display: inline-block;
}

.inline-form-item :deep(.el-form-item__label) {
  float: none;
  display: inline-block;
  width: 60px;
  text-align: right;
  color: #ffffff;
  margin-right: 10px;
}

.inline-form-item :deep(.el-input) {
  width: 250px;
}
</style>