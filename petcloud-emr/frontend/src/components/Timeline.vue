<template>
  <div class="space-y-4">
    <div v-for="item in items" :key="item.id" class="flex gap-3">
      <div class="flex flex-col items-center">
        <div class="h-2 w-2 rounded-full bg-emerald-500"></div>
        <div class="min-h-full w-px flex-1 bg-emerald-100"></div>
      </div>
      <div class="flex-1 rounded bg-white p-4 shadow">
        <p class="text-xs uppercase tracking-wide text-slate-400">{{ formatType(item.type) }} · {{ item.date }}</p>
        <h3 class="text-lg font-semibold text-slate-700">{{ item.title }}</h3>
        <p v-if="item.subtitle" class="text-sm text-slate-500">{{ item.subtitle }}</p>
        <p v-if="item.description" class="mt-2 text-sm text-slate-600 whitespace-pre-line">{{ item.description }}</p>
        <div v-if="item.attachments && item.attachments.length" class="mt-3 flex flex-wrap gap-2">
          <a
            v-for="url in item.attachments"
            :key="url"
            class="inline-flex items-center rounded border border-emerald-200 px-2 py-1 text-xs text-emerald-600"
            :href="url"
            target="_blank"
          >查看附件</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';

export interface TimelineItem {
  id: string | number;
  type: string;
  date: string;
  title: string;
  subtitle?: string;
  description?: string;
  attachments?: string[];
}

defineProps({
  items: {
    type: Array as PropType<TimelineItem[]>,
    default: () => [],
  },
});

const formatType = (type: string) => {
  const map: Record<string, string> = {
    record: '病历',
    vaccine: '疫苗',
    deworming: '驱虫',
    weight: '体重',
    feeding: '喂养',
  };
  return map[type] || type;
};
</script>
