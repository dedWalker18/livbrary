import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "about",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignUp.vue"),
  },
  {
    path: "/dashboard",
    name: "dadhboard",
    component: () => import("../views/UserDash.vue"),
  },
  {
    path: "/news",
    name: "news",
    component: () => import("../views/NewsVue.vue"),
  },
  {
    path: "/genres",
    name: "genres",
    component: () => import("../views/GenreDash.vue"),
  },
  {
    path: "/dashboard/admin",
    name: "Control",
    component: () => import("../views/AdminDash.vue"),
  },
  {
    path: "/dashboard/admin/update/:bookId",
    name: "updatebooks",
    component: () => import("../views/UpdateBooks.vue"),
    props: true,
  },
  {
    path: "/dashboard/admin/add/book",
    name: "addooks",
    component: () => import("../views/AddBooks.vue"),
    props: true,
  },
  {
    path: "/dashboard/admin/duebooks",
    name: "duebooks",
    component: () => import("../views/DueBooks.vue"),
  },
  {
    path: "/dashboard/admin/requests",
    name: "Requests",
    component: () => import("../views/AdminRequests.vue"),
  },
  {
    path: "/dashboard/books/:bookId",
    name: "BookComponent",
    component: () => import("../views/GetBook.vue"),
    props: true,
  },
  {
    path: "/user/read/:bookId",
    name: "ReadBook",
    component: () => import("../views/ReadBook.vue"),
    props: true,
  },
  {
    path: "/dashboard/user/settings",
    name: "userSettings",
    component: () => import("../views/UserSettings.vue"),
  },
  {
    path: "/dashboard/admin/add/genre",
    name: "addGenre",
    component: () => import("../views/AddGenre.vue"),
  },
  {
    path: "/user/books",
    name: "ViewBook",
    component: () => import("../views/ViewBook.vue"),
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
