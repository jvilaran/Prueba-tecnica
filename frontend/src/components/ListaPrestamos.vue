<template>
  <div class="lista-prestamos">
    <h1>Lista de libros en prestamo</h1>
    <p>{{ usuarioJSON._id }}</p>
    <table class="user-table">
      <thead>
        <tr>
          <th>Prestamos ID</th>
          <th>Nombre Libro</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prestamo in prestamos" :key="prestamo._id">
          <td v-if="prestamo.usuario_id === usuario._id">
            {{ prestamo._id }}
          </td>
          <td v-if="prestamo.usuario_id === usuario._id">
            {{ prestamo.titulo_libro }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      prestamos: [],
      usuario: {},
      usuarioJSON: localStorage.getItem("usuario"),
    };
  },
  methods: {
    obtenerPrestamos() {
      api.getPrestamos().then((response) => {
        this.prestamos = response.data;
      });
    },
  },
  mounted() {
    // Obtener datos del local storage al montar el componente
    const usuarioJSON = localStorage.getItem("usuario");
    if (usuarioJSON) {
      this.usuario = JSON.parse(usuarioJSON); // Asigna el objeto de usuario
    }
    this.obtenerPrestamos();
  },
};
</script>

<style scoped>
/* Contenedor principal */
.lista-prestamos {
  font-family: "Arial", sans-serif;
  padding: 20px;
  border-radius: 10px;
  background-color: rgb(37, 37, 37);
  color: white;
}

/* Título */
h1 {
  text-align: center;
  margin-bottom: 20px;
}

/* Tabla */
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background-color: #928059;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center; /* Alineación central para toda la tabla */
}

/* Cabecera de la tabla */
thead {
  background-color: #928059;
  color: #ffffff;
}

th {
  padding: 12px 8px;
  font-weight: bold;
}

/* Filas de la tabla */
tbody tr {
  background-color: #f0ede6;
}

tbody tr:nth-child(even) {
  background-color: #cfc1a3;
}

td {
  padding: 12px 8px;
  color: #3e2723;
  vertical-align: middle; /* Centrado vertical */
}

/* Botón de acción */
button {
  background-color: #6d4c41;
  color: #fff;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #5d4037;
}
</style>
