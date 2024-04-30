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
          <router-link class="nav-link active" to="#">My Books</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Genres</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/news">News</router-link>
        </li>
      </ul>
      <div class="d-flex flex-wrap">
        <router-link class="navbar-brand" to="/dashboard/user/settings/">
          <img
            :src="avatars[this.avatar - 1].src"
            alt="Avatar"
            class="img-thumbnail rounded-circle border-4 border-info"
            style="width: 100px; height: 100px"
          />
        </router-link>
      </div>
    </nav>
    <div class="container-fluid">
      <br />
      <br />
      <br />
      <div class="flex row h-100 justify-content-center text-white">
        <div
          v-if="msgs.length > 0"
          class="alert d-flex flex-column justify-content-center align-items-center"
        >
          <ul class="list-unstyled text-white">
            <li v-for="msg in msgs" :key="msg">
              <pre class="justify-content-center align-items-center">
      ####################################################
          {{ msg }}
      ####################################################
            </pre
              >
            </li>
          </ul>
        </div>
        <div class="col-md-8" v-if="userBooks.length > 0">
          <div class="card-deck">
            <div v-for="book in userBooks" :key="book.id">
              <div class="card bg-dark mb-3">
                <router-link
                  :to="{ path: '/user/read/' + book.id }"
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
          <h4
            style="font-family: 'Courier New', Courier, monospace"
            class="mt-5 mb-4"
          >
            Your Notes
          </h4>
        </div>
        <p v-else class="text-center text-white">No books found.</p>
        <div class="justify-content-center col-8">
          <table
            class="table table-dark"
            style="font-family: 'Courier New', Courier, monospace"
          >
            <thead>
              <tr>
                <th scope="col">Book ID</th>
                <th scope="col">Content</th>
                <th scope="col">Page Number</th>
                <th scope="col">Options</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="note in this.notes" :key="note.id">
                <td>{{ note.book_id }}</td>
                <td>{{ note.content }}</td>
                <td>{{ note.page_number }}</td>
                <td>
                  <button @click="deleteNote(note.id)" class="btn btn-danger">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
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
  data() {
    return {
      auth_token: "",
      msgs: [],
      userBooks: [],
      searchQuery: "",
      avatar: 3,
      name: "",
      username: "",
      notes: [],
      streak: "",
      graph_path: [],
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
      this.msgs.push("Not Logged In!!!");
      setTimeout(() => (this.$router.push("/login"), "5000"));
    } else this.fetchDashboard(authToken);
  },
  methods: {
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
        this.userBooks = await response.data["books"];
        this.avatar = response.data["avatar"];
        this.graph_path = response.data["graph_path"];
        this.notes = response.data["notes"];
        this.streak = response.data["streak"];
        console.log(this.streak);
        if (this.streak >= 1) {
          this.msgs.push(
            `Congartualations!! Current Login Streak ${this.streak} 🔥`
          );
          setTimeout(() => (this.msgs = []), "1500");
        } else {
          this.msgs.push(`Pro Tip - Login Daily to become a Pro Reader!!`);
          setTimeout(() => (this.msgs = []), "3000");
        }
      } catch (error) {
        console.error("Error fetching user books:", error);
      }
    },
    async deleteNote(note_id) {
      try {
        const authToken = localStorage.getItem("auth_token");
        const response = await axios.delete(
          "https://192.168.1.11:5000/user/notes/" + note_id,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        const result = response.data;
        this.msgs.push(result);
        window.location.reload();
      } catch (error) {
        this.msgs.push(error);
        setTimeout(() => (this.msgs = []), "3000");
      }
    },
  },
};
</script>

<style scoped>
.container-fluid {
  background-color: rgb(0, 0, 0);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
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
