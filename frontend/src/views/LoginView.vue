<template>
  <div class="homepage">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img
            src="@/assets/logo_livbrary.png"
            alt="Logo"
            width="100"
            height="15%"
            class="d-inline-block align-top"
          />
        </a>
        <ul class="nav justify-content-end">
          <li class="nav-item active">
            <a class="nav-link text-white" href="#">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/signup">Signup</a>
          </li>
        </ul>
      </div>
    </nav>
    <div
      class="hero text-white align-items-center justify-content-center text-center"
    >
      <br />
      <br />
      <br />
      <form
        @submit.prevent="handleSubmit"
        class="d-flex flex-column justify-content-center align-items-center"
      >
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Username</label>
          <br />
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
            placeholder="Enter Username"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter Password"
            required
          />
        </div>
        <button type="submit" class="btn btn-dark">Login</button>
      </form>

      <div
        v-if="errors.length > 0"
        class="alert d-flex flex-column justify-content-center align-items-center"
      >
        <ul class="list-unstyled">
          <li v-for="error in errors" :key="error">
            <pre class="justify-content-center align-items-center">
            #######################################
                {{ error }}
            #######################################
            </pre>
          </li>
        </ul>
      </div>
    </div>
    <footer class="footer bg-dark text-white text-center py-3">
      <img
        src="/iitm_logo.png"
        class="img-thumbnail rounded-circle mr-2"
        style="width: 45px; height: 45px"
      />
      2024 LivBrary 📚
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router/index";
localStorage.clear();
export default {
  data() {
    return {
      username: "",
      password: "",
      errors: [],
    };
  },
  methods: {
    async handleSubmit() {
      this.errors = [];
      try {
        const response = await axios.post(
          "https://192.168.1.11:5000/loginuser",
          {
            username: this.username,
            password: this.password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        const auth_token = await response.data["token"];
        const role = await response.data["role"];
        if (auth_token != "Failed") {
          localStorage.setItem("auth_token", auth_token);
          localStorage.setItem("role", role);
          if (role === "users") {
            router.push("/dashboard");
          } else if (role === "admin") {
            router.push("/dashboard/admin");
          }
        } else {
          throw new Error("Wrong Username or Password!! Try Again!!");
        }
      } catch (error) {
        console.error(error);
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "3000");
      }
    },
  },
};
</script>

<style>
.homepage {
  background-color: #212529;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.hero {
  flex: 1;
  color: #fff;
  background-color: black;
  background-size: cover;
  background-repeat: no-repeat;
}
</style>
