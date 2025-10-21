<template>
  <div v-if="pet" class="space-y-8">
    <section class="rounded bg-white p-6 shadow">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 class="text-2xl font-semibold text-slate-700">{{ pet.name }}</h1>
          <p class="text-sm text-slate-500">物种：{{ pet.species || '未知' }} · 品种：{{ pet.breed || '未填写' }}</p>
          <p class="text-sm text-slate-500">生日：{{ pet.birthday || '未填写' }} · 性别：{{ pet.sex || '未填写' }}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <router-link
            :to="{ name: 'sharing', params: { id: pet.id } }"
            class="rounded border border-emerald-500 px-3 py-1 text-sm text-emerald-600"
          >共享管理</router-link>
          <router-link
            :to="{ name: 'record-new', params: { id: pet.id } }"
            class="rounded bg-emerald-500 px-3 py-1 text-sm text-white"
          >新增病历</router-link>
        </div>
      </div>
    </section>

    <section class="grid gap-6 md:grid-cols-2">
      <div class="rounded bg-white p-6 shadow">
        <h2 class="mb-3 text-lg font-semibold text-slate-700">记录体重</h2>
        <form class="grid gap-3" @submit.prevent="addWeight">
          <div>
            <label class="mb-1 block text-sm text-slate-600">日期</label>
            <input v-model="weightForm.logged_at" type="date" class="w-full rounded border px-3 py-2" />
          </div>
          <div>
            <label class="mb-1 block text-sm text-slate-600">体重(kg)</label>
            <input v-model.number="weightForm.weight_kg" type="number" step="0.1" min="0" class="w-full rounded border px-3 py-2" />
          </div>
          <button type="submit" class="rounded bg-emerald-500 px-3 py-2 text-white">保存体重</button>
        </form>
      </div>
      <div class="rounded bg-white p-6 shadow">
        <h2 class="mb-3 text-lg font-semibold text-slate-700">喂养记录</h2>
        <form class="grid gap-3" @submit.prevent="addFeeding">
          <div>
            <label class="mb-1 block text-sm text-slate-600">日期</label>
            <input v-model="feedingForm.logged_at" type="date" class="w-full rounded border px-3 py-2" />
          </div>
          <div>
            <label class="mb-1 block text-sm text-slate-600">食物与份量</label>
            <input v-model="feedingForm.food" placeholder="如：主粮 80g" class="w-full rounded border px-3 py-2" />
          </div>
          <div>
            <label class="mb-1 block text-sm text-slate-600">备注</label>
            <input v-model="feedingForm.notes" class="w-full rounded border px-3 py-2" />
          </div>
          <button type="submit" class="rounded bg-emerald-500 px-3 py-2 text-white">保存喂养</button>
        </form>
      </div>
    </section>

    <section class="grid gap-6 md:grid-cols-2">
      <div class="rounded bg-white p-6 shadow">
        <h2 class="mb-3 text-lg font-semibold text-slate-700">疫苗记录</h2>
        <form class="grid gap-3" @submit.prevent="addVaccine">
          <input v-model="vaccineForm.vaccine_name" placeholder="疫苗名称" class="w-full rounded border px-3 py-2" />
          <input v-model="vaccineForm.batch_no" placeholder="批号" class="w-full rounded border px-3 py-2" />
          <input v-model.number="vaccineForm.dose_number" type="number" min="1" placeholder="第几针" class="w-full rounded border px-3 py-2" />
          <input v-model="vaccineForm.injected_at" type="date" class="w-full rounded border px-3 py-2" />
          <input v-model="vaccineForm.next_due" type="date" class="w-full rounded border px-3 py-2" placeholder="下次时间" />
          <button type="submit" class="rounded bg-emerald-500 px-3 py-2 text-white">保存疫苗</button>
        </form>
      </div>
      <div class="rounded bg-white p-6 shadow">
        <h2 class="mb-3 text-lg font-semibold text-slate-700">驱虫记录</h2>
        <form class="grid gap-3" @submit.prevent="addDeworming">
          <input v-model="dewormForm.drug_name" placeholder="药品名称" class="w-full rounded border px-3 py-2" />
          <input v-model="dewormForm.given_at" type="date" class="w-full rounded border px-3 py-2" />
          <input v-model.number="dewormForm.cycle_days" type="number" min="1" placeholder="周期天数" class="w-full rounded border px-3 py-2" />
          <button type="submit" class="rounded bg-emerald-500 px-3 py-2 text-white">保存驱虫</button>
        </form>
      </div>
    </section>

    <WeightChart :data="pet.weight_logs" />

    <section>
      <h2 class="mb-4 text-xl font-semibold text-slate-700">时间线</h2>
      <Timeline :items="timeline" />
    </section>
  </div>
  <div v-else class="rounded bg-white p-6 text-center text-slate-500 shadow">正在加载宠物信息...</div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import dayjs from 'dayjs';
import { useRoute } from 'vue-router';
import Timeline, { type TimelineItem } from '../components/Timeline.vue';
import WeightChart from '../components/WeightChart.vue';
import { usePetsStore } from '../stores/pets';

const route = useRoute();
const petId = Number(route.params.id);
const petsStore = usePetsStore();
const pet = ref<any>(null);

const weightForm = reactive({
  logged_at: new Date().toISOString().slice(0, 10),
  weight_kg: 0,
});

const feedingForm = reactive({
  logged_at: new Date().toISOString().slice(0, 10),
  food: '',
  notes: '',
});

const vaccineForm = reactive({
  vaccine_name: '',
  batch_no: '',
  dose_number: undefined as number | undefined,
  injected_at: new Date().toISOString().slice(0, 10),
  next_due: '',
});

const dewormForm = reactive({
  drug_name: '',
  given_at: new Date().toISOString().slice(0, 10),
  cycle_days: 90,
});

onMounted(async () => {
  await petsStore.fetchPetDetail(petId);
  await petsStore.fetchMedicalRecords(petId);
  pet.value = petsStore.petDetail;
});

const addWeight = async () => {
  await petsStore.addWeight(petId, {
    logged_at: weightForm.logged_at,
    weight_kg: weightForm.weight_kg,
  });
  pet.value = petsStore.petDetail;
};

const addFeeding = async () => {
  await petsStore.addFeeding(petId, {
    logged_at: feedingForm.logged_at,
    food: feedingForm.food,
    notes: feedingForm.notes,
  });
  pet.value = petsStore.petDetail;
};

const addVaccine = async () => {
  await petsStore.addVaccine(petId, vaccineForm);
  pet.value = petsStore.petDetail;
};

const addDeworming = async () => {
  await petsStore.addDeworming(petId, dewormForm);
  pet.value = petsStore.petDetail;
};

const timeline = computed<TimelineItem[]>(() => {
  if (!pet.value) return [];
  const items: TimelineItem[] = [];
  pet.value.weight_logs.forEach((log: any) => {
    items.push({
      id: `weight-${log.id}`,
      type: 'weight',
      date: log.logged_at,
      title: `体重 ${log.weight_kg} kg`,
    });
  });
  pet.value.feeding_logs.forEach((log: any) => {
    items.push({
      id: `feeding-${log.id}`,
      type: 'feeding',
      date: log.logged_at,
      title: log.food,
      description: log.notes,
    });
  });
  pet.value.vaccines.forEach((record: any) => {
    items.push({
      id: `vaccine-${record.id}`,
      type: 'vaccine',
      date: record.injected_at,
      title: record.vaccine_name,
      description: record.next_due ? `下次：${record.next_due}` : undefined,
    });
  });
  pet.value.dewormings.forEach((record: any) => {
    items.push({
      id: `deworm-${record.id}`,
      type: 'deworming',
      date: record.given_at,
      title: record.drug_name,
      description: `周期 ${record.cycle_days} 天`,
    });
  });
  petsStore.medicalRecords.forEach((record) => {
    items.push({
      id: `record-${record.id}`,
      type: 'record',
      date: record.visit_date,
      title: record.chief_complaint || '病历记录',
      description: `${record.diagnosis || ''}\n${record.treatment || ''}\n${record.notes || ''}`.trim(),
      attachments: record.attachments,
    });
  });
  return items.sort((a, b) => dayjs(b.date).valueOf() - dayjs(a.date).valueOf());
});
</script>
