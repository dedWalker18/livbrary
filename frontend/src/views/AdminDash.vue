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
      <form class="d-flex m-lg-4" role="search">
        <div class="input-group">
          <input
            class="form-control me-2"
            type="text"
            placeholder="Search..."
            aria-label="Search"
            v-model="searchQuery"
          />
        </div>
      </form>
      <div class="d-flex flex-wrap">
        <img
          src="/admin-profile.png"
          alt="Avatar"
          class="img-thumbnail rounded-circle border-4 border-info"
          style="width: 100px; height: 100px"
        />
      </div>
    </nav>
    <div class="container-fluid">
      <br />
      <br />
      <br />
      <div class="flex row h-100 justify-content-center">
        <div class="col-md-8" v-if="filteredList.length > 0">
          <div class="card-deck">
            <div v-for="book in filteredList" :key="book.id">
              <div class="card bg-dark mb-3">
                <router-link
                  :to="{ path: '/dashboard/admin/update/' + book.id }"
                  class="card-link stretched-link"
                  style="text-decoration: none"
                >
                  <img
                    :src="book.cover_photo"
                    class="card-img-top"
                    alt="Book Cover"
                  />
                  <div class="card-body">
                    <h5 class="card-title text-white">{{ book.name }}</h5>
                    <p class="card-text text-white">
                      By {{ book.author }} <br />
                      Genre: {{ book.genre_name }}
                    </p>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-white">No books found.</p>
      </div>
      <br />
      <h4
        class="text-white"
        style="
          text-align: center;
          font-family: 'Courier New', Courier, monospace;
        "
      >
        ###User Analytics###
      </h4>
      <div>
        <div class="card-deck">
          <div v-for="graph in graphs" :key="graph.id">
            <div class="card bg-dark mb-3">
              <img
                :src="graph.src"
                alt="Image"
                style="
                  display: flex;
                  margin: auto;
                  cursor: zoom-in;
                  background-color: rgb(230, 230, 230);
                  transition: background-color 300ms ease 0s;
                  --darkreader-inline-bgcolor: #26292b;
                  width: 400px;
                "
              />
            </div>
          </div>
        </div>
        <br />
        <br />
        <br />
        <br />
        <br />
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
      auth_token: "",
      allBooks: [],
      msg: [],
      userBooks: [],
      searchQuery: "",
      avatar: "",
      name: "",
      username: "",
      notes: [],
      streak: "",
      graphs: [
        {
          id: 1,
          src: "https://192.168.1.11:5000/analytics/0",
        },
        {
          id: 1,
          src: "https://192.168.1.11:5000/analytics/1",
        },
        {
          id: 1,
          src: "https://192.168.1.11:5000/analytics/2",
        },
      ],
      email: "",
      password: "",
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
    };
  },
  mounted() {
    const authToken = localStorage.getItem("auth_token");
    if (!authToken || authToken === "Failed") {
      this.msg.push("Not Logged In!!!");
      setTimeout(() => (this.$router.push("/login"), "5000"));
    } else {
      if (!this.allBooks.length) {
        this.fetchAllBooks();
      }
    }
    this.fetchDashboard(authToken);
  },
  methods: {
    async fetchAllBooks() {
      try {
        const response = await axios.get("https://192.168.1.11:5000/books/all");
        this.allBooks = await response.data;
      } catch (error) {
        console.error("Error fetching all books:", error);
      }
    },
    async fetchDashboard(authToken) {
      try {
        const response = await axios.get(
          "https://192.168.1.11:5000/dashboard",
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        this.userBooks = response.data["books"];
        this.avatar = response.data["avatar"];
        localStorage.setItem("avatar", response.data["avatar"]);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
  },
  computed: {
    filteredList() {
      return this.allBooks.filter((book) => {
        const searchTerm = this.searchQuery.toLowerCase();
        return (
          book.name.toLowerCase().includes(searchTerm) ||
          book.author.toLowerCase().includes(searchTerm) ||
          book.genre_name.toLowerCase().includes(searchTerm)
        );
      });
    },
  },
};
</script>

<style scoped>
.container-fluid {
  background-color: rgb(0, 0, 0);
  display: flex;
  flex-direction: column;
  min-height: 120vh;
}

.card-deck {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

.card {
  min-width: 250px;
  max-width: 250px;
  min-height: 350px;
  max-height: 350px;
  color: white;
  margin: 10px;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.footer {
  position: relative;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
