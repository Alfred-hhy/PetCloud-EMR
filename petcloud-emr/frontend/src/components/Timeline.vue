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
            v-for="attachment in formatAttachments(item.attachments)"
            :key="attachment.original"
            class="inline-flex items-center overflow-hidden rounded border border-emerald-200 text-xs text-emerald-600"
            :href="attachment.url"
            target="_blank"
            rel="noopener noreferrer"
          >
            <template v-if="attachment.isImage">
              <img :src="attachment.url" alt="附件预览" class="h-20 w-20 object-cover" />
            </template>
            <template v-else>
              <span class="px-2 py-1">查看附件</span>
            </template>
          </a>
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

const apiBase = (import.meta.env.VITE_API_BASE as string | undefined) || 'http://localhost:8000';

const resolveAttachmentUrl = (url: string) => {
  if (!url) return '';
  if (/^https?:\/\//i.test(url)) {
    return url;
  }
  const normalizedBase = apiBase.replace(/\/$/, '');
  const normalizedPath = url.startsWith('/') ? url : `/${url}`;
  return `${normalizedBase}${normalizedPath}`;
};

const isImageAttachment = (url: string) => {
  const cleanUrl = url.split('?')[0] || '';
  return /\.(png|jpe?g|gif|bmp|webp|svg)$/i.test(cleanUrl);
};

const formatAttachments = (attachments: string[] = []) =>
  attachments.map((url) => ({
    original: url,
    url: resolveAttachmentUrl(url),
    isImage: isImageAttachment(url),
  }));

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
