import { defineStore } from 'pinia';
import api from '../api/http';
import { useAuthStore } from './auth';

export interface PetItem {
  id: number;
  owner_id: number;
  name: string;
  species?: string | null;
  breed?: string | null;
  sex?: string | null;
  birthday?: string | null;
  color?: string | null;
  chip_id?: string | null;
  avatar_url?: string | null;
  created_at: string;
}

export interface AccessGrant {
  id: number;
  grantee_user_id: number;
  scope: 'read' | 'write' | 'all';
  expires_at?: string | null;
}

export interface WeightLog {
  id: number;
  logged_at: string;
  weight_kg: number;
}

export interface FeedingLog {
  id: number;
  logged_at: string;
  food: string;
  amount?: string | null;
  notes?: string | null;
}

export interface VaccineRecord {
  id: number;
  vaccine_name: string;
  batch_no?: string | null;
  dose_number?: number | null;
  injected_at: string;
  next_due?: string | null;
}

export interface DewormingRecord {
  id: number;
  drug_name: string;
  given_at: string;
  cycle_days: number;
}

export interface MedicalRecord {
  id: number;
  pet_id: number;
  vet_id?: number | null;
  clinic_id?: number | null;
  visit_date: string;
  chief_complaint?: string | null;
  diagnosis?: string | null;
  treatment?: string | null;
  notes?: string | null;
  attachments: string[];
}

export interface ReminderItem {
  pet_id: number;
  pet_name: string;
  type: string;
  title: string;
  due_date?: string | null;
  description?: string | null;
}

interface PetState {
  pets: PetItem[];
  loading: boolean;
  petDetail: (PetItem & {
    grants: AccessGrant[];
    weight_logs: WeightLog[];
    feeding_logs: FeedingLog[];
    vaccines: VaccineRecord[];
    dewormings: DewormingRecord[];
  }) | null;
  medicalRecords: MedicalRecord[];
  reminders: ReminderItem[];
}

export const usePetsStore = defineStore('pets', {
  state: (): PetState => ({
    pets: [],
    loading: false,
    petDetail: null,
    medicalRecords: [],
    reminders: [],
  }),
  actions: {
    async fetchPets() {
      this.loading = true;
      try {
        const { data } = await api.get<PetItem[]>('/api/pets');
        this.pets = data;
      } finally {
        this.loading = false;
      }
    },
    async fetchPetDetail(id: number) {
      const { data } = await api.get(`/api/pets/${id}`);
      this.petDetail = data;
    },
    async savePet(payload: Partial<PetItem> & { id?: number }) {
      if (payload.id) {
        const { data } = await api.put(`/api/pets/${payload.id}`, payload);
        await this.fetchPets();
        return data;
      }
      const auth = useAuthStore();
      const body = { ...payload } as any;
      if (!body.owner_id && auth.user) {
        body.owner_id = auth.user.id;
      }
      const { data } = await api.post('/api/pets', body);
      await this.fetchPets();
      return data;
    },
    async deletePet(id: number) {
      await api.delete(`/api/pets/${id}`);
      this.pets = this.pets.filter((p) => p.id !== id);
    },
    async fetchMedicalRecords(petId: number) {
      const { data } = await api.get<MedicalRecord[]>(`/api/pets/${petId}/records`);
      this.medicalRecords = data;
    },
    async addWeight(petId: number, payload: { logged_at: string; weight_kg: number }) {
      await api.post(`/api/pets/${petId}/weights`, payload);
      await this.fetchPetDetail(petId);
    },
    async addFeeding(petId: number, payload: { logged_at: string; food: string; amount?: string; notes?: string }) {
      await api.post(`/api/pets/${petId}/feedings`, payload);
      await this.fetchPetDetail(petId);
    },
    async addVaccine(petId: number, payload: any) {
      await api.post(`/api/pets/${petId}/vaccines`, payload);
      await this.fetchPetDetail(petId);
    },
    async addDeworming(petId: number, payload: any) {
      await api.post(`/api/pets/${petId}/dewormings`, payload);
      await this.fetchPetDetail(petId);
    },
    async createGrant(petId: number, payload: { grantee_user_id: number; scope: string; expires_at?: string | null }) {
      await api.post(`/api/pets/${petId}/grants`, payload);
      await this.fetchPetDetail(petId);
    },
    async fetchReminders(days = 30) {
      const { data } = await api.get<ReminderItem[]>(`/api/reminders/upcoming`, { params: { days } });
      this.reminders = data;
    },
    async createRecord(petId: number, payload: any) {
      const { data } = await api.post(`/api/pets/${petId}/records`, payload);
      await this.fetchMedicalRecords(petId);
      return data;
    },
    async uploadAttachments(recordId: number, files: FileList) {
      const form = new FormData();
      Array.from(files).forEach((file) => form.append('files', file));
      const { data } = await api.post(`/api/records/${recordId}/attachments`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return data.urls as string[];
    },
    async addPrescription(recordId: number, payload: { drug_name: string; dosage?: string; frequency?: string; days?: number }) {
      await api.post(`/api/records/${recordId}/prescriptions`, payload);
    },
  },
});
