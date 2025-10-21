<template>
  <div class="mx-auto max-w-md rounded-lg bg-white p-8 shadow">
    <h1 class="mb-6 text-2xl font-semibold text-slate-700">登录 PetCloud</h1>
    <form class="space-y-4" @submit.prevent="submit">
      <div>
        <label class="mb-1 block text-sm text-slate-600">邮箱</label>
        <input v-model="form.email" type="email" required class="w-full rounded border px-3 py-2" />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">密码</label>
        <input v-model="form.password" type="password" required class="w-full rounded border px-3 py-2" />
      </div>
      <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
      <button
        type="submit"
        class="w-full rounded bg-emerald-500 py-2 text-white hover:bg-emerald-600"
        :disabled="auth.loading"
      >
        {{ auth.loading ? '登录中...' : '登录' }}
      </button>
    </form>
    <p class="mt-4 text-sm text-slate-500">
      还没有账号？
      <router-link class="text-emerald-600" to="/register">立即注册</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const form = reactive({
  email: '',
  password: '',
});

const error = ref('');

const submit = async () => {
  error.value = '';
  try {
    await auth.login(form);
    const redirect = (route.query.redirect as string) || '/';
    router.push(redirect);
  } catch (err: any) {
    error.value = err?.response?.data?.detail || '登录失败，请稍后重试';
  }
};
</script>
