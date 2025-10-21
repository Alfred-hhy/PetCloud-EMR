<template>
  <div class="space-y-8">
    <section class="rounded bg-white p-6 shadow">
      <h2 class="mb-4 text-lg font-semibold text-slate-700">新增宠物</h2>
      <form class="grid gap-4 md:grid-cols-2" @submit.prevent="savePet">
        <div class="md:col-span-1">
          <label class="mb-1 block text-sm text-slate-600">昵称 *</label>
          <input v-model="newPet.name" required class="w-full rounded border px-3 py-2" />
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">物种</label>
          <input v-model="newPet.species" class="w-full rounded border px-3 py-2" placeholder="如：猫、狗" />
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">品种</label>
          <input v-model="newPet.breed" class="w-full rounded border px-3 py-2" />
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">性别</label>
          <select v-model="newPet.sex" class="w-full rounded border px-3 py-2">
            <option value="">未选择</option>
            <option value="公">公</option>
            <option value="母">母</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">生日</label>
          <input v-model="newPet.birthday" type="date" class="w-full rounded border px-3 py-2" />
        </div>
        <div>
          <label class="mb-1 block text-sm text-slate-600">芯片号</label>
          <input v-model="newPet.chip_id" class="w-full rounded border px-3 py-2" />
        </div>
        <div class="md:col-span-2">
          <label class="mb-1 block text-sm text-slate-600">备注颜色/特征</label>
          <input v-model="newPet.color" class="w-full rounded border px-3 py-2" placeholder="如：橘色、短毛" />
        </div>
        <div class="md:col-span-2 text-right">
          <button type="submit" class="rounded bg-emerald-500 px-4 py-2 text-white hover:bg-emerald-600">保存宠物</button>
        </div>
      </form>
      <p v-if="message" class="mt-3 text-sm text-emerald-600">{{ message }}</p>
    </section>

    <section>
      <h2 class="mb-4 text-xl font-semibold text-slate-700">宠物列表</h2>
      <div v-if="petsStore.pets.length === 0" class="rounded bg-white p-6 text-slate-500 shadow">
        暂无宠物档案。
      </div>
      <div v-else class="grid gap-4 md:grid-cols-2">
        <div v-for="pet in petsStore.pets" :key="pet.id" class="flex flex-col justify-between rounded bg-white p-5 shadow">
          <div>
            <h3 class="text-lg font-semibold text-slate-700">{{ pet.name }}</h3>
            <p class="text-sm text-slate-500">物种：{{ pet.species || '未知' }} · 品种：{{ pet.breed || '未填写' }}</p>
            <p class="text-sm text-slate-500">生日：{{ pet.birthday || '未填写' }} · 性别：{{ pet.sex || '未填写' }}</p>
          </div>
          <div class="mt-3 flex items-center justify-between">
            <router-link :to="{ name: 'pet-detail', params: { id: pet.id } }" class="text-sm text-emerald-600">查看</router-link>
            <button
              v-if="pet.owner_id === auth.user?.id"
              class="text-sm text-red-500"
              @click="removePet(pet.id)"
            >删除</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue';
import { usePetsStore } from '../stores/pets';
import { useAuthStore } from '../stores/auth';

const petsStore = usePetsStore();
const auth = useAuthStore();

const newPet = reactive({
  name: '',
  species: '',
  breed: '',
  sex: '',
  birthday: '',
  chip_id: '',
  color: '',
});

const message = ref('');

onMounted(async () => {
  await petsStore.fetchPets();
});

const savePet = async () => {
  await petsStore.savePet(newPet);
  Object.assign(newPet, { name: '', species: '', breed: '', sex: '', birthday: '', chip_id: '', color: '' });
  message.value = '保存成功！';
  setTimeout(() => (message.value = ''), 2000);
};

const removePet = async (id: number) => {
  if (confirm('确定删除该宠物吗？删除后数据无法恢复。')) {
    await petsStore.deletePet(id);
  }
};
</script>
