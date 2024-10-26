<template>
  <div class="content">
    <div>
      <h2>Devolver libro</h2>
      <div class="devolver">
        <form @submit.prevent="handleReturn()">
          <label for="libroid">Ingrese el ID del préstamo:</label>
          <input type="libroid" id="libroid" v-model="libroid" required />
          <button type="submit">Confirmar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      libroid: "",
    };
  },
  methods: {
    handleReturn() {
      api
        .devolverPrestamo(this.libroid)
        .then(() => {
          // Mostrar ventana emergente
          Swal.fire({
            title: "¡Excelente!",
            text: "El libro se ha devuelto exitosamente",
            icon: "info",
            confirmButtonText: "Aceptar",
          });
          this.libroid = "";
        })
        .catch((error) => {
          if (error.response && error.response.status === 400) {
            this.error = error.response.data.detail; // Manejar error 400
            Swal.fire({
              title: "Alerta de error",
              text: "El libro ya ha sido devuelto",
              icon: "error",
              confirmButtonText: "Aceptar",
            });
            this.libroid = "";
          } else {
            console.error("Error al devolver el libro:", error);
          }
        });
    },
  },
};
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
/* Contenedor principal */
.devolver {
  max-width: 500px;
  margin: auto;
  background-color: #e9e8e7;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  display: flex;
  justify-content: center; /* Centrar verticalmente */
  padding-top: 40px; /* Aumentar el padding superior */
  padding-bottom: 40px; /* Aumentar el padding inferior */
}

/* Encabezado */
h2 {
  text-align: center;
  margin-bottom: 20px;
}

/* Estilos de los labels */
label {
  font-weight: bold;
  color: #3e2723;
  display: block;
  margin-top: 10px;
  text-align: center;
}

/* Estilos de los inputs */
input {
  width: 92%;
  padding: 10px;
  margin: 5px auto;
}

/* Input Focus */
input:focus {
  outline: none;
  border-color: #795548;
}

/* Botón de guardar */
button {
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #6d4c41;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-items: center;
  text-align: center;
}

button:hover {
  background-color: #5d4037;
}
</style>
