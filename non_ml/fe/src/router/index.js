import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import CustomerView from '@/views/customer/CustomerView.vue';
import MerchantView from '@/views/merchant/MerchantView.vue';
import AddTransactionView from '@/views/AddTransactionView.vue';
import ExportDataView from '@/views/ExportDataView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/customers',
      name: 'customers',
      component: CustomerView,
    },
    {
      path: '/merchants',
      name: 'merchants',
      component: MerchantView,
    },
    {
      path: '/transaction/add',
      name: 'add-transaction',
      component: AddTransactionView,
    },
    {
      path: '/export-data',
      name: 'export-data',
      component: ExportDataView
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
});

export default router;
