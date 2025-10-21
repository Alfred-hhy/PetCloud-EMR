<template>
  <div class="mx-auto max-w-md rounded-lg bg-white p-8 shadow">
    <h1 class="mb-6 text-2xl font-semibold text-slate-700">注册账号</h1>
    <form class="space-y-4" @submit.prevent="submit">
      <div>
        <label class="mb-1 block text-sm text-slate-600">姓名</label>
        <input v-model="form.full_name" required class="w-full rounded border px-3 py-2" />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">邮箱</label>
        <input v-model="form.email" type="email" required class="w-full rounded border px-3 py-2" />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">密码</label>
        <input v-model="form.password" type="password" required minlength="6" class="w-full rounded border px-3 py-2" />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">角色</label>
        <select v-model="form.role" class="w-full rounded border px-3 py-2">
          <option value="OWNER">宠主</option>
          <option value="VET">兽医</option>
          <option value="CLINIC_ADMIN">诊所管理员</option>
        </select>
      </div>
      <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
      <button type="submit" class="w-full rounded bg-emerald-500 py-2 text-white hover:bg-emerald-600">注册</button>
    </form>
    <p class="mt-4 text-sm text-slate-500">
      已有账号？
      <router-link class="text-emerald-600" to="/login">直接登录</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore, type UserRole } from '../stores/auth';

const auth = useAuthStore();
const router = useRouter();

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  role: 'OWNER' as UserRole,
});

const error = ref('');

const submit = async () => {
  error.value = '';
  try {
    await auth.register(form);
    await auth.login({ email: form.email, password: form.password });
    router.push('/');
  } catch (err: any) {
    error.value = err?.response?.data?.detail || '注册失败，请稍后再试';
  }
};
</script>
