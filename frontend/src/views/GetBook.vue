import router from '@/router';
<template>
  <div>
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
        <li class="nav-item">
          <router-link class="nav-link" to="/news">News</router-link>
        </li>
      </ul>
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
          <button @click="requestBook()" class="btn btn-primary d-block mt-4">
            Request to Add to Bookshelf
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
    async requestBook() {
      const authToken = localStorage.getItem("auth_token");

      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }

      const url = "https://192.168.1.11:5000/requests";
      const body = JSON.stringify({ book_id: this.bookId });

      const headers = new Headers({
        Authorization: "Bearer " + authToken,
        "Content-Type": "application/json",
      });

      try {
        const response = await fetch(url, {
          method: "POST",
          headers,
          body,
        });

        if (!response.ok) {
          throw new Error(`Some Issue Occured. Try Again!!}`);
        }

        const responseData = await response.json();
        console.log("Response:", responseData);
        this.msg.push(responseData);
        setTimeout(() => (this.msg = []), "5000");
      } catch (error) {
        console.error("Error requesting book addition:", error);
        alert("Error: " + error.message);
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
