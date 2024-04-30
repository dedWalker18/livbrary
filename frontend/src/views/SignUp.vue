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
          <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link text-white" href="/signup">Signup</a>
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
          <label class="form-label" for="name">Full Name</label>
          <br />
          <input
            v-model="name"
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter Name"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Username</label>
          <br />
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
            placeholder="This Cannot be changed Later!!"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="email">Email</label>
          <br />
          <input
            v-model="email"
            type="email"
            class="form-control"
            id="email"
            placeholder="Enter Email"
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
        <div class="form-outline mb-4">
          <label for="avatar">Avatar</label>
          <div class="d-flex flex-wrap">
            <img
              v-for="avatar in avatars"
              :key="avatar.id"
              :src="avatar.src"
              @click="selectAvatar(avatar.id)"
              :class="{
                'border-4 border-info': selectedAvatarId === avatar.id,
              }"
              alt="Avatar"
              class="img-thumbnail rounded-circle mr-2"
              style="width: 100px; height: 100px"
            />
          </div>
        </div>
        <button type="submit" class="btn btn-dark">Register</button>
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
              </pre
            >
          </li>
        </ul>
      </div>
      <div v-if="msg.length > 0" class="alert alert-success">
        <ul>
          <li v-for="msg in msg" :key="msg">
            <pre>
            #######################################
                    {{ msg }}
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
import router from "@/router";
import axios from "axios";
export default {
  data() {
    return {
      name: "",
      username: "",
      email: "",
      password: "",
      errors: [],
      msg: [],
      avatars: [
        {
          id: 1,
          src: "https://img.freepik.com/free-vector/user-circles-set_78370-4704.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 2,
          src: "https://img.freepik.com/free-photo/androgynous-avatar-non-binary-queer-person_23-2151100226.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 3,
          src: "https://img.freepik.com/premium-photo/memoji-happy-man-white-background-emoji_826801-6839.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 4,
          src: "https://img.freepik.com/free-psd/3d-illustration-person-with-long-hair_23-2149436197.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
        {
          id: 5,
          src: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?size=626&ext=jpg&ga=GA1.1.972355406.1713266629&semt=sph",
        },
      ],
      selectedAvatarId: null,
    };
  },
  methods: {
    async handleSubmit() {
      this.errors = [];
      this.msg = [];
      try {
        const data = {
          name: this.name,
          username: this.username,
          email: this.email,
          password: this.password,
          roles: "users",
          avatarid: this.selectedAvatarId,
        };
        const response = await axios.post(
          "https://192.168.1.11:5000/signup",
          data
        );
        if (response.data["message"] === "Usernname already taken") {
          throw new Error("Usernname already taken");
        } else if (data.message == "Admin Already Exists") {
          throw new Error("Admin Already Exists!!");
        } else {
          setTimeout(() => router.push("/login"), "5000");
          this.msg.push(
            "Signup Successfull!! You will be automatically Redirected..."
          );
        }
      } catch (error) {
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "3000");
      }
    },
    selectAvatar(id) {
      this.selectedAvatarId = id;
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
.user-avatar {
  cursor: pointer;
}
</style>
