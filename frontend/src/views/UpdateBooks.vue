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
          <router-link class="nav-link active" to="/dashboard/admin"
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
      class="text-white bg-black container-fluid d-flex flex-column align-items-center"
    >
      <br />
      <br />
      <br />
      <div class="row w-100">
        <div class="col-md-6 d-flex justify-content-center image">
          <img
            :src="book.cover_photo"
            class="img-fluid book-cover"
            alt="Book Cover"
          />
        </div>
        <div class="col-md-6 mt-4">
          <h2>{{ book.name }}</h2>
          <p class="card-text">By {{ book.author }}</p>
          <div>
            <router-link
              :to="{ path: '/genres' }"
              class="text-info"
              style="text-decoration: none"
            >
              Genre : {{ book.genre_name }}
            </router-link>
          </div>
          <br />
          <form
            @submit.prevent="updateBook"
            class="d-flex flex-column col-md-6"
          >
            <div class="form-outline mb-4">
              <label class="form-label" for="name">Full Name</label>
              <br />
              <input
                v-model="name"
                type="text"
                class="form-control"
                id="name"
                placeholder="Enter Book Name"
              />
            </div>
            <div class="form-outline mb-4">
              <label class="form-label" for="author">Author</label>
              <br />
              <input
                v-model="author"
                type="text"
                class="form-control"
                id="author"
                placeholder="Enter Author's Name"
              />
            </div>
            <div class="form-outline mb-4">
              <label class="form-label" for="genre">Genre</label>
              <br />
              <input
                v-model="genre"
                type="text"
                class="form-control"
                id="genre"
                placeholder="Enter Genre Name"
              />
            </div>
            <button type="submit" class="btn btn-primary d-block mt-4 col-md-6">
              Update Book
            </button>
          </form>
          <button @click="deleteBook" class="btn btn-danger d-block mt-4 col-3">
            Delete Book
          </button>
          <div v-if="msg.length > 0" class="alert mt-4">
            <ul class="list-unstyled">
              <li v-for="msg in msg" :key="msg">
                <pre class="text-center">
              #######################################
              {{ msg }}
              #######################################
                </pre>
              </li>
            </ul>
          </div>
        </div>
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
      msg: [],
    };
  },
  created() {
    const authToken = localStorage.getItem("auth_token");
    this.fetchBookDetails(authToken);
  },
  methods: {
    async fetchBookDetails(authToken) {
      try {
        const response = await axios.get(
          "https://192.168.1.11:5000/books/" + this.bookId,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        this.book = response.data;
      } catch (error) {
        console.error("Error fetching user books:", error);
      }
    },
    async updateBook() {
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
        };
        const response = await axios.patch(
          "https://192.168.1.11:5000/books/" + this.bookId,
          data,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        console.log(response.data);
        this.msg.push("Update Successfull!!");
        window.location.reload();
        setTimeout(() => (this.msg = []), "5000");
      } catch (error) {
        this.msg.push(error);
        setTimeout(() => (this.msg = []), "5000");
        window.location.reload();
      }
    },
    async deleteBook() {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }
      try {
        const response = await axios.delete(
          "https://192.168.1.11:5000/books/" + this.bookId,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        console.log(response.data);
        this.msg.push(response.data);
        setTimeout(() => {
          this.msg = [];
          router.push("/dashboard/admin");
        }, 5000);
      } catch (error) {
        this.msg.push(error);
        setTimeout(() => (this.msg = []), "5000");
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
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
