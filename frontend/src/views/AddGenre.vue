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
          <router-link class="nav-link" to="/dashboard/admin/add/book"
            >Add Book</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link active" to="/dashboard/admin/add/genre"
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
      <h1>Add Genre</h1>
      <br />
      <form
        @submit.prevent="addGenre"
        class="d-flex flex-column justify-content-center align-items-center"
      >
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

        <button type="submit" class="btn btn-success mt-4">Add Genre</button>
      </form>
      <br />
      <br />
      <br />
      <h1>Delete Genre</h1>
      <br />
      <div>
        <select
          v-model="selectedGenre"
          class="bg-black text-white form-select form-select-lg mb-3"
        >
          <option disabled value="">None</option>
          <option v-for="genre in genres" :key="genre.name">
            {{ genre.name }}
          </option>
        </select>
        <button @click="deleteGenre" class="btn btn-danger mt-4">
          Delete Genre
        </button>
      </div>

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
  data() {
    return {
      genre: "",
      genres: [],
      errors: [],
      msg: [],
      selectedGenre: "",
    };
  },
  mounted() {
    this.fetchGenres();
  },
  methods: {
    async fetchGenres() {
      const response = await axios.get("https://192.168.1.11:5000/genre");
      this.genres = response.data;
    },
    async addGenre() {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }
      try {
        const data = {
          genre_name: this.genre,
        };
        const response = await axios.post(
          "https://192.168.1.11:5000/genre",
          data,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        if (response.data == "Genre Exists") {
          this.errors.push("Genre Already Exists !!!");
          setTimeout(() => (this.errors = []), "5000");
        } else {
          this.msg.push("Added Successfull!!");
          window.location.reload();
          setTimeout(() => (this.msg = []), "5000");
        }
      } catch (error) {
        this.errors.push(error);
        setTimeout(() => (this.errors = []), "5000");
      }
    },
    async deleteGenre() {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }
      if (this.selectedGenre == "") {
        this.msg.push("Please Select a Genre First");
        setTimeout(() => (this.msg = []), "3000");
      } else {
        try {
          const response = await axios.delete(
            "https://192.168.1.11:5000/genre",
            {
              headers: {
                Authorization: "Bearer " + authToken,
              },
              data: {
                genre_name: this.selectedGenre,
              },
            }
          );
          if (response.data == "Remove Books") {
            this.errors.push("Remove all books from this Genre First");
            setTimeout(() => (this.errors = []), "3000");
          } else {
            this.msg.push("Deleted Successfull!!");
            window.location.reload();
            setTimeout(() => (this.msg = []), "5000");
          }
        } catch (error) {
          this.errors.push(error);
          setTimeout(() => (this.errors = []), "5000");
        }
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
  position: relative;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
