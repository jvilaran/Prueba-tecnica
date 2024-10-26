<template>
  <div class="content">
    <div>
      <h2>Almacenar libro/s</h2>
      <div class="libro">
        <form @submit.prevent="handleLogin()">
          <label for="titulo">Título del libro:</label>
          <input type="titulo" id="titulo" v-model="titulo" required />
          <label for="autor">Autor:</label>
          <input type="autor" id="autor" v-model="autor" required />
          <label for="cantidad">Cantidad:</label>
          <input
            type="number"
            id="cantidad"
            v-model="cantidad"
            required
            v-on:keypress="validarNumero"
          />
          <button type="submit">Guardar</button>
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
      titulo: "",
      autor: "",
      cantidad: "",
    };
  },
  methods: {
    handleLogin() {
      try {
        const payload = {
          titulo: this.titulo,
          autor: this.autor,
          cantidad: this.cantidad,
        };

        const response = api.crearLibro(payload);

        alert(response.data.mensaje);
      } catch (error) {
        if (error.response) {
          alert("Error: " + error.response.data.detail);
        } else {
          console.error("Error:", error);
        }
      }
      // Mostrar alerta de éxito
      Swal.fire({
        icon: "success",
        title: "¡Éxito!",
        text: "El libro se almacenó exitosamente.",
      });
      this.titulo = "";
      this.autor = "";
      this.cantidad = "";
    },
    validarNumero(event) {
      const char = String.fromCharCode(event.keyCode);
      if (!/[0-9]/.test(char)) {
        event.preventDefault(); // Evita que se ingrese si no es número
      }
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
.libro {
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
