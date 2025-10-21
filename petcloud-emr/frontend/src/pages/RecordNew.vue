<template>
  <div class="space-y-6">
    <div class="rounded bg-white p-6 shadow">
      <h1 class="text-2xl font-semibold text-slate-700">新增病历</h1>
      <p class="mt-2 text-sm text-slate-500">
        当前宠物：<strong>{{ pet?.name || '加载中' }}</strong>。仅兽医或被授权用户可创建病历。
      </p>
    </div>
    <div class="rounded bg-white p-6 shadow">
      <RecordEditor :pet-id="petId" @saved="goBack" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import RecordEditor from '../components/RecordEditor.vue';
import { usePetsStore } from '../stores/pets';

const route = useRoute();
const router = useRouter();
const petId = Number(route.params.id);
const petsStore = usePetsStore();
const pet = ref<any>(null);

onMounted(async () => {
  await petsStore.fetchPetDetail(petId);
  pet.value = petsStore.petDetail;
});

const goBack = () => {
  router.push({ name: 'pet-detail', params: { id: petId } });
};
</script>
