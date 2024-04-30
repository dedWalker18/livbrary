import router from '@/router';
<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <router-link class="navbar-brand" to="/">
        <img
          class="logo"
          alt="Vue logo"
          src="@/assets/logo_livbrary.png"
          style="width: 100px"
        />
      </router-link>

      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link" to="/dashboard/admin"
            >Dashboard</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dashboard/admin/requests"
            >Requests</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dashboard/admin/duebooks"
            >Due Books</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link active" to="/dashboard/admin/add/book"
            >Add Book</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dashboard/admin/add/genre"
            >Add Genre</router-link
          >
        </li>
      </ul>
      <div class="d-flex flex-wrap">
        <img
          src="/admin-profile.png"
          alt="Avatar"
          class="img-thumbnail rounded-circle border-4 border-info"
          style="width: 100px; height: 100px"
        />
      </div>
    </nav>

    <div
      class="text-white bg-black container-fluid d-flex flex-column text-center align-items-center"
    >
      <br />
      <br />
      <br />
      <form
        @submit.prevent="addBook"
        class="d-flex flex-column justify-content-center align-items-center"
      >
        <div class="form-outline mb-4">
          <label class="form-label" for="name">Book Name</label>
          <br />
          <input
            v-model="name"
            type="text"
            class="form-control mt-2"
            id="name"
            placeholder="Enter Name"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="author">Author</label>
          <br />
          <input
            v-model="author"
            type="text"
            class="form-control mt-2"
            id="author"
            placeholder="Enter Author's Name"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="genre">Genre</label>
          <br />
          <input
            v-model="genre"
            type="genre"
            class="form-control mt-2"
            id="genre"
            placeholder="Enter Genre"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="location">Location</label>
          <br />
          <input
            v-model="location"
            type="location"
            class="form-control mt-2"
            id="location"
            placeholder="Ex. - /pdfs/<FileName.pdf>"
            required
          />
        </div>
        <div class="form-outline mb-4">
          <label class="form-label" for="cover_photo">Cover Photo Path</label>
          <br />
          <input
            v-model="cover_photo"
            type="cover_photo"
            class="form-control mt-2"
            id="cover_photo"
            placeholder="Ex. - /cover/<FileName.png>"
            required
          />
        </div>
        <button type="submit" class="btn btn-success mt-4">Add Book</button>
      </form>

      <div v-if="errors.length > 0" class="alert">
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

export default {
  props: {
    bookId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      book: [],
      name: "",
      author: "",
      genre: "",
      location: "",
      cover_photo: "",
      errors: [],
      msg: [],
    };
  },
  methods: {
    async addBook() {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }
      try {
        const data = {
          name: this.name,
          author: this.author,
          genre: this.genre,
          location: this.location,
          cover: this.cover_photo,
        };
        const response = await axios.post(
          "https://192.168.1.11:5000/books",
          data,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        console.log(response.data);
        this.msg.push("Added Successfull!!");
        setTimeout(() => (this.msg = []), "5000");
      } catch (error) {
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "5000");
      }
    },
  },
};
</script>

<style scoped>
.container-fluid {
  background-color: rgb(0, 0, 0);
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 85vh;
}

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
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
