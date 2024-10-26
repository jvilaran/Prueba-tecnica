<template>
  <section>
    <div class="content">
      <div>
        <h1>Crear usuario</h1>
        <div class="usuario">
          <form @submit.prevent="handleCreate()">
            <div>
              <label for="nombre">Nombre completo:</label>
              <input
                type="nombre"
                id="nombre"
                v-model="nombre"
                required
                v-on:keypress="validarTexto"
              />
              <label for="correo">Correo Electrónico:</label>
              <input type="correo" id="corre" v-model="correo" required />
              <label for="telefono">Teléfono:</label>
              <input
                type="telefono"
                id="telefono"
                v-model="telefono"
                required
                v-on:keypress="validarNumero"
              />
            </div>
            <router-link to="/login" class="link"
              >Si tienes cuenta, inicia sesión aquí</router-link
            >
            <button type="submit">Registrarse</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import api from "../services/api";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      nombre: "",
      correo: "",
      telefono: "",
    };
  },
  methods: {
    handleCreate() {
      try {
        const payload = {
          nombre: this.nombre,
          correo: this.correo,
          telefono: this.telefono,
        };
        api.crearUsuario(payload);
        Swal.fire({
          title: "Aviso",
          text: "El usuario se ha registrado exitosamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        });
        this.navigateToLogin();
      } catch (error) {
        if (error.response) {
          alert("Error: " + error.response.data.detail);
        } else {
          console.error("Error:", error);
        }
      }
    },
    navigateToLogin() {
      this.$router.push("/login"); // Cambiar a la ruta de inicio de sesión
    },
    obtenerNombre() {
      api.getNombre().then((response) => {
        this.nombre = response.data;
      });
    },
    validarNumero(event) {
      const char = String.fromCharCode(event.keyCode);
      if (!/[0-9]/.test(char)) {
        event.preventDefault(); // Evita que se ingrese si no es número
      }
    },
    validarTexto(event) {
      const char = String.fromCharCode(event.keyCode);
      if (!/[a-zA-Z]/.test(char)) {
        event.preventDefault(); // Evita que se ingrese si no es letra
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
  min-height: 100vh;
}

section {
  background-image: url("../assets/board.jpg");
  background-size: cover;
  background-position: center;
  object-fit: cover;
  height: 100vh;
}
/* Contenedor principal */
.usuario {
  width: 500px;
  margin: auto;
  background-color: rgba(255, 255, 255);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  text-align: center;
  display: flex;
  justify-content: center; /* Centrar verticalmente */
  padding-top: 40px; /* Aumentar el padding superior */
  padding-bottom: 40px; /* Aumentar el padding inferior */
}

/* Encabezado */
h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 38px;
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
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
