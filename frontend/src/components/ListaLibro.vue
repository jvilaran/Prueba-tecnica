<template>
  <div class="lista-libros">
    <h1>Lista de libros</h1>
    <table>
      <thead>
        <tr>
          <th>Título</th>
          <th>Autor</th>
          <th>Cantidad</th>
          <th>Disponibilidad</th>
          <th>Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="libro in libros" :key="libro._id">
          <td>{{ libro.titulo }}</td>
          <td>{{ libro.autor }}</td>
          <td>{{ libro.cantidad }}</td>
          <td>{{ libro.cantidad != 0 ? "Sí" : "No" }}</td>
          <td>
            <button
              v-if="libro.cantidad != 0"
              @click="
                () => {
                  obtenerLibros(libro._id);
                  prestarLibro(libro);
                }
              "
            >
              Prestar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from "../services/api";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      libros: [],
      usuarioGuardado: JSON.parse(localStorage.getItem("usuario")), // Se asegura de que el usuario está cargado
    };
  },
  methods: {
    obtenerLibros() {
      api.getLibros().then((response) => {
        this.libros = response.data;
      });
    },
    prestarLibro(libro) {
      // Si la cantidad es mayor a cero, se intenta hacer el préstamo
      if (libro.cantidad > 0) {
        const prestamo = {
          libro_id: libro._id,
          usuario_id: this.usuarioGuardado._id,
        };
        // Llamada a la API para crear el préstamo
        api
          .crearPrestamo(prestamo)
          .then((response) => {
            // Reduce la cantidad del libro en la lista local
            libro.cantidad -= 1;
            if (libro.cantidad === 0) {
              libro.disponible = false; // Deshabilita el botón al llegar a 0
            }
            this.tituloLibro(response.data.prestamo_id);
          })
          .catch((error) => {
            console.error("Error al prestar el libro:", error);
          });
      }
    },
    tituloLibro(prestamoID) {
      // Mostrar ventana emergente
      Swal.fire({
        title: "Aviso para devolución",
        text: `Recuerda el ID del préstamo para realizar la devolución o puedes encontrarlo en la página 'Libros en préstamo'. ID: ${prestamoID}`,
        icon: "info",
        confirmButtonText: "Aceptar",
      }).then((result) => {
        if (result.isConfirmed) {
          // Ejecuta obtenerLibros cuando el usuario hace clic en "Aceptar"
          this.obtenerLibros();
        }
      });
    },
  },
  mounted() {
    this.obtenerLibros();
  },
};
</script>

<style scoped>
/* Contenedor principal */
.lista-libros {
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
