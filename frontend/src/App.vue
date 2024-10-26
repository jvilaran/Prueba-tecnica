<template>
  <div style="margin: 0px; background-color: rgb(37, 37, 37); color: white">
    <nav v-if="mostrarNav">
      <router-link to="/listalib" class="link">Libros disponibles</router-link>
      <router-link to="/libros" class="link">Almacenar libros</router-link>
      <router-link to="/usuarios" class="link">Lista de usuarios</router-link>
      <router-link to="/devolver" class="link">Devolver libro</router-link>
      <router-link to="/prestamos" class="link">Libros en prestamo</router-link>
      <router-link to="/" class="link" @click="limpiarLocalStorage"
        >Cerrar Sesión</router-link
      >
    </nav>
    <router-view></router-view>
    <!-- Renderiza el componente de la ruta actual -->
  </div>
</template>

<script>
export default {
  methods: {
    limpiarLocalStorage() {
      localStorage.clear(); // Limpiar todo el local storage
    },
  },
  computed: {
    mostrarNav() {
      // Retorna true si la ruta actual no es /login
      return (this.$route.path !== "/" && this.$route.path !== "/usuario");
    },
  },
};
</script>

<style scoped>
/* Contenedor principal */
div {
  font-family: "Arial", sans-serif;
  min-height: 100vh;
  margin: 0;
}

/* Estilos de navegación */
nav {
  background-color: #928059;
  padding: 15px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.link {
  text-decoration: none;
  color: white;
}

.link:hover {
  color: #d6cccc;
}

router-link.router-link-active {
  background-color: #4e342e;
  color: #fff;
}
</style>
