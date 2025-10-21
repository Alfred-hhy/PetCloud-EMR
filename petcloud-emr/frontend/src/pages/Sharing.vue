<template>
  <div class="space-y-6">
    <div class="rounded bg-white p-6 shadow">
      <h1 class="text-2xl font-semibold text-slate-700">共享访问</h1>
      <p class="mt-2 text-sm text-slate-500">为兽医或家人授予查看/编辑权限。</p>
      <div v-if="pet" class="mt-4">
        <p class="text-sm text-slate-600">宠物：{{ pet.name }}</p>
        <p class="text-sm text-slate-600">当前授权：{{ pet.grants.length }} 条</p>
      </div>
    </div>

    <div class="rounded bg-white p-6 shadow">
      <h2 class="mb-3 text-lg font-semibold text-slate-700">新增授权</h2>
      <form class="grid gap-4 md:grid-cols-3" @submit.prevent="submit">
        <div>
          <label class="mb-1 block text-sm text-slate-600">用户 ID *</label>
          <input v-model.number="grant.grantee_user_id" type="number" min="1" required class="w-full rounded border px-3 py-2" />
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">权限范围 *</label>
          <select v-model="grant.scope" class="w-full rounded border px-3 py-2">
            <option value="read">只读</option>
            <option value="write">读写</option>
            <option value="all">全部</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">过期日期</label>
          <input v-model="grant.expires_at" type="date" class="w-full rounded border px-3 py-2" />
        </div>
        <div class="md:col-span-3 text-right">
          <button type="submit" class="rounded bg-emerald-500 px-4 py-2 text-white hover:bg-emerald-600">保存授权</button>
        </div>
      </form>
      <p v-if="message" class="mt-2 text-sm text-emerald-600">{{ message }}</p>
      <p v-if="error" class="mt-2 text-sm text-red-500">{{ error }}</p>
    </div>

    <div class="rounded bg-white p-6 shadow">
      <h2 class="mb-3 text-lg font-semibold text-slate-700">授权列表</h2>
      <table class="w-full table-auto text-left text-sm">
        <thead class="bg-slate-50 text-slate-500">
          <tr>
            <th class="px-3 py-2">用户 ID</th>
            <th class="px-3 py-2">权限</th>
            <th class="px-3 py-2">到期时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pet?.grants" :key="item.id" class="border-b">
            <td class="px-3 py-2">{{ item.grantee_user_id }}</td>
            <td class="px-3 py-2">{{ scopeText(item.scope) }}</td>
            <td class="px-3 py-2">{{ item.expires_at || '不限期' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { usePetsStore } from '../stores/pets';

const route = useRoute();
const petsStore = usePetsStore();
const petId = Number(route.params.id);
const pet = ref<any>(null);

const grant = reactive({
  grantee_user_id: 0,
  scope: 'read',
  expires_at: '',
});

const message = ref('');
const error = ref('');

onMounted(async () => {
  await petsStore.fetchPetDetail(petId);
  pet.value = petsStore.petDetail;
});

const submit = async () => {
  try {
    await petsStore.createGrant(petId, {
      grantee_user_id: grant.grantee_user_id,
      scope: grant.scope,
      expires_at: grant.expires_at || undefined,
    });
    message.value = '授权已保存';
    error.value = '';
    await petsStore.fetchPetDetail(petId);
    pet.value = petsStore.petDetail;
  } catch (err: any) {
    error.value = err?.response?.data?.detail || '保存失败';
  }
};

const scopeText = (scope: string) => ({ read: '只读', write: '读写', all: '全部' }[scope] || scope);
</script>
