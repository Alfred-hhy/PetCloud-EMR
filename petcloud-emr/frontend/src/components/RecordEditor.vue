<template>
  <form class="space-y-4" @submit.prevent="submit">
    <div class="grid gap-4 md:grid-cols-2">
      <div>
        <label class="mb-1 block text-sm text-slate-600">就诊日期 *</label>
        <input v-model="recordForm.visit_date" type="date" required class="w-full rounded border px-3 py-2" />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">就诊诊所 ID (可选)</label>
        <input v-model="recordForm.clinic_id" type="number" min="1" class="w-full rounded border px-3 py-2" />
      </div>
    </div>
    <div class="grid gap-4 md:grid-cols-2">
      <div>
        <label class="mb-1 block text-sm text-slate-600">主诉</label>
        <textarea v-model="recordForm.chief_complaint" rows="3" class="w-full rounded border px-3 py-2"></textarea>
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600">诊断</label>
        <textarea v-model="recordForm.diagnosis" rows="3" class="w-full rounded border px-3 py-2"></textarea>
      </div>
    </div>
    <div>
      <label class="mb-1 block text-sm text-slate-600">治疗/处置方案</label>
      <textarea v-model="recordForm.treatment" rows="3" class="w-full rounded border px-3 py-2"></textarea>
    </div>
    <div>
      <label class="mb-1 block text-sm text-slate-600">备注</label>
      <textarea v-model="recordForm.notes" rows="3" class="w-full rounded border px-3 py-2"></textarea>
    </div>
    <div>
      <label class="mb-1 block text-sm text-slate-600">上传病历图片</label>
      <input ref="fileInput" type="file" multiple accept="image/*" class="w-full rounded border px-3 py-2" />
      <p class="mt-1 text-xs text-slate-400">支持多张图片，文件会保存在后端 uploads/ 目录</p>
    </div>

    <div>
      <h3 class="mb-2 text-lg font-semibold text-slate-700">处方列表</h3>
      <div v-for="(pres, index) in prescriptions" :key="index" class="grid gap-3 md:grid-cols-4">
        <input v-model="pres.drug_name" placeholder="药品名称" class="rounded border px-3 py-2" />
        <input v-model="pres.dosage" placeholder="剂量" class="rounded border px-3 py-2" />
        <input v-model="pres.frequency" placeholder="频次" class="rounded border px-3 py-2" />
        <input v-model.number="pres.days" type="number" min="1" placeholder="天数" class="rounded border px-3 py-2" />
      </div>
      <button type="button" class="mt-2 text-sm text-emerald-600" @click="addPrescription">+ 添加处方</button>
    </div>

    <p v-if="message" class="text-sm text-emerald-600">{{ message }}</p>
    <p v-if="error" class="text-sm text-red-500">{{ error }}</p>

    <div class="text-right">
      <button type="submit" class="rounded bg-emerald-500 px-4 py-2 text-white hover:bg-emerald-600" :disabled="submitting">
        {{ submitting ? '保存中...' : '保存病历' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { usePetsStore } from '../stores/pets';

const props = defineProps<{ petId: number }>();
const emit = defineEmits<{ (e: 'saved'): void }>();

const petsStore = usePetsStore();

const recordForm = reactive({
  visit_date: new Date().toISOString().slice(0, 10),
  chief_complaint: '',
  diagnosis: '',
  treatment: '',
  notes: '',
  clinic_id: '' as string | number | '',
});

const prescriptions = reactive([
  { drug_name: '', dosage: '', frequency: '', days: undefined as number | undefined },
]);

const fileInput = ref<HTMLInputElement | null>(null);
const message = ref('');
const error = ref('');
const submitting = ref(false);

const addPrescription = () => {
  prescriptions.push({ drug_name: '', dosage: '', frequency: '', days: undefined });
};

const submit = async () => {
  submitting.value = true;
  message.value = '';
  error.value = '';
  try {
    const payload: any = {
      visit_date: recordForm.visit_date,
      chief_complaint: recordForm.chief_complaint,
      diagnosis: recordForm.diagnosis,
      treatment: recordForm.treatment,
      notes: recordForm.notes,
      clinic_id: recordForm.clinic_id ? Number(recordForm.clinic_id) : undefined,
      attachments: [],
    };
    const record = await petsStore.createRecord(props.petId, payload);
    if (fileInput.value?.files?.length) {
      await petsStore.uploadAttachments(record.id, fileInput.value.files);
    }
    for (const pres of prescriptions) {
      if (!pres.drug_name) continue;
      await petsStore.addPrescription(record.id, {
        drug_name: pres.drug_name,
        dosage: pres.dosage,
        frequency: pres.frequency,
        days: pres.days,
      });
    }
    message.value = '病历已保存';
    emit('saved');
    if (fileInput.value) fileInput.value.value = '';
  } catch (err: any) {
    error.value = err?.response?.data?.detail || '保存失败，请稍后再试';
  } finally {
    submitting.value = false;
  }
};
</script>
