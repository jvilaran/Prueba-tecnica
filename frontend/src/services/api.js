import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    Accept: "application/json",
    "Content-type": "application/json",
  },
});

export default {
  getLibros() {
    return apiClient.get("/libros/");
  },
  crearLibro(data) {
    return apiClient.post("/libros/", data);
  },
  crearUsuario(data) {
    return apiClient.post("/usuarios/", data);
  },
  crearPrestamo(data) {
    return apiClient.post("/prestamos/", data);
  },
  devolverPrestamo(prestamoId) {
    return apiClient.put(`/prestamos/${prestamoId}`);
  },
  verificarCorreo(correo) {
    return apiClient.get(`/usuarios/${correo}`);
  },
  getNombre(nombre) {
    return apiClient.get(`/usuarios/${nombre}`);
  },
  getUsuarios() {
    return apiClient.get("/usuarios/");
  },
  getPrestamos() {
    return apiClient.get("/prestamos/");
  },
};
