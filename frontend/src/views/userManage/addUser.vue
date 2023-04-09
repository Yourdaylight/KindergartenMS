<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { register, updateUser, searchClass } from '../../api/api'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'

const route = useRoute()

const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive({
  username: route.query.username ?? '',
  user_id: route.query.user_id ?? '',
  password: route.query.password ?? '',
  role: route.query.role ?? null,
  class_no: route.query.class_no ?? ''
})

const rules = reactive<FormRules>({
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: 'change'
    }
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'change'
    }
  ],
  role: [
    {
      required: true,
      message: '请选择用户角色',
      trigger: 'change'
    }
  ],
  class_no: [
    {
      required: true,
      message: '请选择班级',
      trigger: 'change'
    }
  ]
})

const classList = ref([])
const getUser = () => {
  try {
    let params = {
      class_no: '',
      class_name: '',
      teacher_id: null
    }
    searchClass(params).then((res) => {
      const { data: Data } = res
      // 单独获取班级列表
      Data.forEach((el) => {
        classList.value.push({ label: el.class_name, value: el.class_no })
      })
    })
  } catch (err) {}
}
getUser()

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      try {
        let params = { ...ruleForm }
        if (route.query.username) {
          updateUser(params).then((res) => {
            if (res.code == 200) {
              ElMessage({
                message: '更新成功！',
                type: 'success'
              })
              ruleFormRef.value.resetFields()
            } else {
              ElMessage.error(res.msg)
            }
          })
        } else {
          register(params).then((res) => {
            if (res.code == 200) {
              ElMessage({
                message: '新增成功！',
                type: 'success'
              })
              ruleFormRef.value.resetFields()
            } else {
              ElMessage.error(res.msg)
            }
          })
        }
      } catch (err) {}
    } else {
      console.log('error submit!', fields)
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
<template>
  <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    :rules="rules"
    label-width="120px"
    class="demo-ruleForm"
    :size="formSize"
    status-icon
    label-position="top"
  >
    <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username" placeholder="请输入用户名" />
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="ruleForm.password" type="password" placeholder="请输入密码" />
    </el-form-item>
    <el-form-item label="角色" prop="role">
      <el-select v-model="ruleForm.role" placeholder="请选择用户角色">
        <el-option label="系统管理员" value="1" />
        <el-option label="教师" value="2" />
        <el-option label="家长" value="3" />
      </el-select>
    </el-form-item>
    <el-form-item v-if="ruleForm.role == '3'" label="班级" prop="class_no">
      <el-select v-model="ruleForm.class_no" placeholder="请选择班级" size="large">
        <el-option
          :label="item.label"
          :value="item.value"
          v-for="(item, index) in classList"
          :key="index"
        />
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)"> 创建/更新 </el-button>
      <el-button @click="resetForm(ruleFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<style lang="less" scoped>
.demo-ruleForm {
  width: 50%;
}
</style>
