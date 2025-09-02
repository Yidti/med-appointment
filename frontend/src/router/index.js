import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import DoctorList from '../components/DoctorList.vue';
import { useAuthStore } from '../stores/auth';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/doctors',
    name: 'DoctorList',
    component: DoctorList,
    meta: { requiresAuth: true },
  },
  {
    path: '/doctors/:id',
    name: 'DoctorDetail',
    component: () => import('../views/DoctorDetail.vue'),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
