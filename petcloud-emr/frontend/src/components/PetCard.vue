<template>
  <div class="flex h-full flex-col justify-between rounded bg-white p-5 shadow">
    <div>
      <h3 class="text-lg font-semibold text-slate-700">{{ pet.name }}</h3>
      <p class="text-sm text-slate-500">物种：{{ pet.species || '未知' }} · 品种：{{ pet.breed || '未填写' }}</p>
      <p class="text-sm text-slate-500">生日：{{ pet.birthday || '未填写' }}</p>
      <p v-if="reminder" class="mt-2 text-sm text-emerald-600">{{ reminder }}</p>
    </div>
    <router-link
      :to="{ name: 'pet-detail', params: { id: pet.id } }"
      class="mt-4 inline-flex items-center justify-center rounded bg-emerald-500 px-3 py-1 text-sm text-white hover:bg-emerald-600"
    >
      查看详情
    </router-link>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';
import type { PetItem } from '../stores/pets';

defineProps({
  pet: {
    type: Object as PropType<PetItem>,
    required: true,
  },
  reminder: {
    type: String,
    default: '',
  },
});
</script>
