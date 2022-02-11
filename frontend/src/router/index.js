import Vue from 'vue';
import VueRouter from 'vue-router';

import EstatesPanel from '../views/EstatesPanel.vue';
import OwnersPanel from '../views/OwnersPanel.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/estates'
  },
  {
    path: '/owners',
    name: 'Owners',
    component: OwnersPanel
  },
  {
    path: '/estates',
    name: 'Estates',
    component: EstatesPanel
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
