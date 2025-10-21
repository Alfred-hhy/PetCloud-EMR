<template>
  <div class="min-h-screen bg-slate-100 text-slate-800">
    <header class="bg-white shadow-sm">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <router-link to="/" class="text-xl font-semibold text-emerald-600">🐾 PetCloud EMR</router-link>
        <nav v-if="auth.isAuthenticated" class="flex items-center gap-4">
          <router-link to="/" class="hover:text-emerald-600">首页</router-link>
          <router-link to="/pets" class="hover:text-emerald-600">我的宠物</router-link>
          <button
            class="rounded bg-emerald-500 px-3 py-1 text-white hover:bg-emerald-600"
            @click="logout"
          >退出</button>
        </nav>
      </div>
    </header>
    <main class="mx-auto max-w-6xl px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

const auth = useAuthStore();

onMounted(async () => {
  if (auth.token && !auth.user) {
    try {
      await auth.fetchMe();
    } catch (error) {
      console.error('自动登录失败', error);
    }
  }
});

const logout = () => {
  auth.logout();
};
</script>
