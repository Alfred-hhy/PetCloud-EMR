<template>
  <div class="rounded bg-white p-4 shadow">
    <h3 class="mb-2 text-lg font-semibold text-slate-700">体重趋势 (kg)</h3>
    <div v-if="!points.length" class="text-sm text-slate-500">暂无体重记录。</div>
    <svg v-else viewBox="0 0 300 160" class="w-full">
      <polyline :points="points" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" />
      <g v-for="(item, index) in sorted" :key="item.id">
        <circle
          :cx="xPositions[index]"
          :cy="yPositions[index]"
          r="4"
          fill="#10b981"
        ></circle>
        <text
          :x="xPositions[index]"
          :y="yPositions[index] - 8"
          class="text-xs"
          text-anchor="middle"
          fill="#334155"
        >{{ item.weight_kg }}</text>
        <text
          :x="xPositions[index]"
          y="150"
          class="text-xs"
          text-anchor="middle"
          fill="#94a3b8"
        >{{ shortDate(item.logged_at) }}</text>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import dayjs from 'dayjs';
import type { WeightLog } from '../stores/pets';

const props = defineProps<{ data: WeightLog[] }>();

const sorted = computed(() => [...props.data].sort((a, b) => dayjs(a.logged_at).valueOf() - dayjs(b.logged_at).valueOf()));

const xPositions = computed(() => {
  const count = sorted.value.length;
  if (!count) return [] as number[];
  const step = count === 1 ? 0 : 280 / (count - 1);
  return sorted.value.map((_, index) => 10 + step * index);
});

const yPositions = computed(() => {
  if (!sorted.value.length) return [] as number[];
  const weights = sorted.value.map((item) => item.weight_kg);
  const max = Math.max(...weights);
  const min = Math.min(...weights);
  const range = max === min ? 1 : max - min;
  return sorted.value.map((item) => 130 - ((item.weight_kg - min) / range) * 100);
});

const points = computed(() => xPositions.value.map((x, index) => `${x},${yPositions.value[index]}`).join(' '));

const shortDate = (value: string) => dayjs(value).format('MM/DD');
</script>
