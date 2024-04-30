<template>
  <div class="homepage">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <router-link class="navbar-brand" to="/">
        <img
          class="logo"
          alt="Vue logo"
          src="../assets/logo_livbrary.png"
          style="width: 100px"
        />
      </router-link>

      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/user/books">My Books</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Genres</router-link>
        </li>
      </ul>
      <div class="d-flex flex-wrap">
        <router-link class="navbar-brand" to="/dashboard/user/settings/">
          <img
            :src="avatars[this.avatar - 1].src"
            alt="Avatar"
            class="img-thumbnail rounded-circle border-4 border-danger"
            style="width: 100px; height: 100px"
          />
        </router-link>
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
          <label class="form-label" for="username">Full Name</label>
          <br />
          <input
            v-model="name"
            type="text"
            class="form-control"
            id="name"
            placeholder="Enter Name"
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="username">Email</label>
          <br />
          <input
            v-model="email"
            type="email"
            class="form-control"
            id="email"
            placeholder="Enter Email"
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
        <button type="submit" class="btn btn-info">Update</button>
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
      <div v-if="msg.length > 0" class="alert">
        <ul class="list-unstyled">
          <li v-for="msg in msg" :key="msg">
            <pre>
              #######################################
                {{ msg }}
              #######################################
              </pre
            >
          </li>
        </ul>
      </div>
      <br />
      <br />
      <div>
        <button type="button" class="btn btn-warning" @click="logoutUser">
          Logout
        </button>
        <br />
        <br />
        <br />
        <button type="button" class="btn btn-danger" @click="confirmDelete">
          Delete Account
        </button>
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
import router from "@/router";

export default {
  data() {
    return {
      name: "",
      email: "",
      errors: [],
      avatar: "",
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
  mounted() {
    this.avatar = localStorage.getItem("avatar");
    this.authToken = localStorage.getItem("auth_token");
  },
  methods: {
    async handleSubmit() {
      this.errors = [];
      this.msg = [];
      try {
        const data = {
          name: this.name,
          email: this.email,
          avatarid: this.selectedAvatarId,
        };
        console.log(data);
        const response = await axios.patch(
          "https://192.168.1.11:5000/users",
          data,
          {
            headers: {
              Authorization: "Bearer " + this.authToken,
            },
          }
        );
        if (response.data) {
          this.msg.push(response.data);
          setTimeout(() => (this.msg = []), "3000");
          router.push("/dashboard");
        }
      } catch (error) {
        console.error(error);
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "3000");
      }
    },
    selectAvatar(id) {
      this.selectedAvatarId = id;
    },
    confirmDelete() {
      if (confirm("Are you sure you want to delete your account?")) {
        this.deleteUser();
      }
    },
    async logoutUser() {
      try {
        const response = await axios.get("https://192.168.1.11:5000/logout", {
          headers: {
            Authorization: "Bearer " + this.authToken,
          },
        });
        console.log(response.data);
        this.msg.push("Logging You Out in 3...2..1.");
        setTimeout(() => this.$router.push("/"), "3000");
      } catch (error) {
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "3000");
      }
    },
    async deleteUser() {
      try {
        const response = await axios.delete("https://192.168.1.11:5000/users", {
          headers: {
            Authorization: "Bearer " + this.authToken,
          },
        });
        console.log(response.data);
        this.$router.push("/");
        setTimeout(() => (this.msg = []), "3000");
      } catch (error) {
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
.user-avatar {
  cursor: pointer;
}
</style>
