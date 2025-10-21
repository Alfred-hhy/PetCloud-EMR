<template>
  <div class="space-y-8">
    <section>
      <h2 class="mb-4 text-xl font-semibold text-slate-700">未来提醒</h2>
      <div v-if="petsStore.reminders.length === 0" class="rounded bg-white p-4 text-slate-500 shadow">
        暂无未来提醒，记录疫苗或驱虫计划后即可看到。
      </div>
      <div v-else class="grid gap-4 md:grid-cols-2">
        <div v-for="item in petsStore.reminders" :key="item.title + item.pet_id" class="rounded border-l-4 border-emerald-400 bg-white p-4 shadow">
          <h3 class="text-lg font-semibold text-emerald-600">{{ item.title }}</h3>
          <p class="text-sm text-slate-500">宠物：{{ item.pet_name }}</p>
          <p class="text-sm text-slate-500">到期日：{{ formatDate(item.due_date) }}</p>
          <p class="mt-2 text-sm text-slate-600">{{ item.description }}</p>
        </div>
      </div>
    </section>

    <section>
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-xl font-semibold text-slate-700">我管理的宠物</h2>
        <router-link to="/pets" class="text-sm text-emerald-600">全部管理 &rarr;</router-link>
      </div>
      <div v-if="petsStore.pets.length === 0" class="rounded bg-white p-4 text-slate-500 shadow">
        暂无宠物，前往“我的宠物”页面创建档案。
      </div>
      <div v-else class="grid gap-4 md:grid-cols-2">
        <PetCard
          v-for="pet in petsStore.pets"
          :key="pet.id"
          :pet="pet"
          :reminder="petReminders.get(pet.id)"
        />
      </div>
    </section>

    <section>
      <h2 class="mb-4 text-xl font-semibold text-slate-700">最新病历</h2>
      <div v-if="recentRecords.length === 0" class="rounded bg-white p-4 text-slate-500 shadow">
        暂无病历，兽医记录后会显示最近 5 条。
      </div>
      <div v-else class="space-y-3">
        <div v-for="record in recentRecords" :key="record.id" class="rounded bg-white p-4 shadow">
          <p class="text-sm text-slate-500">宠物：{{ petName(record.pet_id) }} · 就诊日：{{ formatDate(record.visit_date) }}</p>
          <h3 class="mt-1 font-medium text-slate-700">主诉：{{ record.chief_complaint || '未填写' }}</h3>
          <p class="text-sm text-slate-600">诊断：{{ record.diagnosis || '未填写' }}</p>
          <router-link
            class="mt-2 inline-block text-sm text-emerald-600"
            :to="{ name: 'pet-detail', params: { id: record.pet_id } }"
          >查看详情</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import dayjs from 'dayjs';
import PetCard from '../components/PetCard.vue';
import api from '../api/http';
import { usePetsStore, type MedicalRecord } from '../stores/pets';

const petsStore = usePetsStore();
const recentRecords = ref<MedicalRecord[]>([]);

const formatDate = (value?: string | null) => {
  if (!value) return '未设定';
  return dayjs(value).format('YYYY-MM-DD');
};

const loadRecentRecords = async () => {
  const records: MedicalRecord[] = [];
  for (const pet of petsStore.pets) {
    const { data } = await api.get<MedicalRecord[]>(`/api/pets/${pet.id}/records`);
    records.push(...data);
  }
  recentRecords.value = records
    .sort((a, b) => dayjs(b.visit_date).valueOf() - dayjs(a.visit_date).valueOf())
    .slice(0, 5);
};

onMounted(async () => {
  await petsStore.fetchPets();
  await petsStore.fetchReminders();
  await loadRecentRecords();
});

const petReminders = computed(() => {
  const map = new Map<number, string>();
  petsStore.reminders.forEach((item) => {
    if (!map.has(item.pet_id)) {
      map.set(item.pet_id, `${item.title} · ${formatDate(item.due_date)}`);
    }
  });
  return map;
});

const petName = (id: number) => petsStore.pets.find((p) => p.id === id)?.name || '未知宠物';
</script>
