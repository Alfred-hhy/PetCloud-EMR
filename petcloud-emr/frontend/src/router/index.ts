import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../pages/Login.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../pages/Register.vue'),
  },
  {
    path: '/',
    name: 'dashboard',
    component: () => import('../pages/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/pets',
    name: 'pets',
    component: () => import('../pages/Pets.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/pets/:id',
    name: 'pet-detail',
    component: () => import('../pages/PetDetail.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/pets/:id/records/new',
    name: 'record-new',
    component: () => import('../pages/RecordNew.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/pets/:id/sharing',
    name: 'sharing',
    component: () => import('../pages/Sharing.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'login' || to.name === 'register') && auth.isAuthenticated) {
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router;
