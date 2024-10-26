import { createRouter, createWebHistory } from "vue-router";
import ListaLibro from "../components/ListaLibro.vue"; // Se importan las componentes
import UserLogin from "../components/UserLogin.vue";
import CrearLibro from "../components/CrearLibro.vue";
import CrearUsuario from "../components/CrearUsuario.vue"; 
import ListaUsuarios from "../components/ListaUsuarios.vue";
import DevolverLibro from "../components/DevolverLibro.vue";
import ListaPrestamos from "../components/ListaPrestamos.vue";

const routes = [
  {
    path: "/listalib",
    name: "ListaLibro",
    component: ListaLibro, // Asigna el componente a la nueva ruta
  },
  {
    path: "/login",
    name: "UserLogin",
    component: UserLogin,
  },
  {
    path: "/libros",
    name: "CrearLibro",
    component: CrearLibro,
  },
  {
    path: "/usuario",
    name: "CrearUsuario",
    component: CrearUsuario,
  },
  {
    path: "/usuarios",
    name: "ListaUsuarios",
    component: ListaUsuarios,
  },
  {
    path: "/devolver",
    name: "DevolverLibro",
    component: DevolverLibro,
  },
  {
    path: "/prestamos",
    name: "ListaPrestamos",
    component: ListaPrestamos,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || "/"),
  routes,
});

export default router;
