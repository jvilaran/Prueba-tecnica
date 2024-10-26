<template>
  <section>
    <div>
      <h1>Iniciar Sesión</h1>
      <div class="login">
        <form @submit.prevent="handleLogin()">
          <div>
            <label for="email">Correo Electrónico:</label>
            <input class="input" type="email" id="email" v-model="email" required />
          </div>
          <router-link to="/usuario" class="link"
            >Si no tienes cuenta, regístrate aquí</router-link>
          <button type="submit">Ingresar</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import api from "../services/api";
export default {
  data() {
    return {
      email: "test@mail.com",
      // Recuperar el objeto del localStorage
      nombreGuardado: JSON.parse(localStorage.getItem("usuario")),
    };
  },
  methods: {
    handleLogin() {
      api.verificarCorreo(this.email).then((response) => {
        // Guardar el objeto en localStorage
        localStorage.setItem("usuario", JSON.stringify(response.data));
        this.navigateToLibrary();
      });
    },
    navigateToLibrary() {
      this.$router.push("/listalib"); // Cambiar a la ruta de inicio de sesión
    },
  },
};
</script>

<style scoped>
html,
section {
  box-sizing: border-box;
  margin: 0 !important;
  padding: 0 !important;
  font-family: "Poppins", sans-serif;
  font-weight: 300;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
/* Estilo general del section */
section {
  background-image: url("../assets/Lib_login.png");
  background-size: cover;
  background-position: center;
  object-fit: cover;
  height: 100vh;
}

/* Estilo del contenedor del formulario de inicio de sesión */
.login {
  background-color: rgba(255, 255, 255);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 500px;
  text-align: center; /* Centrar el texto */
  display: flex;
  margin: auto;
  justify-content: center;
  padding-top: 40px; /* Aumentar el padding superior */
  padding-bottom: 40px; /* Aumentar el padding inferior */
}

/* Título del formulario */
h1 {
  color: #ffffff;
  text-align: center;
  font-size: 38px;
}

form {
  display: flex;
  flex-direction: column;
}
.link {
  margin-bottom: 1.5rem;
}

/* Estilo para las etiquetas del formulario */
.login label {
  display: block;
  color: #555;
  font-weight: 600;
}

/* Estilo para los campos de entrada */
.input{
  width: 343px;
  padding: 10px;
  margin: 1rem 0 0.5rem 0; /* Espaciado entre los campos */
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

/* Estilo para el botón de inicio de sesión */
.login button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login button:hover {
  background-color: #0056b3;
}
</style>
