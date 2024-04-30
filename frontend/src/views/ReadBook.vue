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
          <router-link class="nav-link active" to="/user/books"
            >My Books</router-link
          >
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Genres</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/news">News</router-link>
        </li>
      </ul>
    </nav>

    <div class="bg-black text-white container-fluid">
      <div class="row mt-4">
        <div class="col-md-6">
          <iframe
            type="application/pdf"
            style="width: 120%; height: 150%"
            :src="book.location"
            class="img-fluid book-cover"
            alt="Book Cover"
          />
        </div>
        <div class="col-md-6 mt-4">
          <h2>{{ book.name }}</h2>
          <p class="card-text">by {{ book.author }}</p>
          <p class="card-text">{{ book.genre_name }}</p>
          <div v-if="notes.length > 0">
            <h4>Notes:</h4>
            <table class="table table-striped table-dark">
              <thead>
                <tr>
                  <th scope="col">Page Number</th>
                  <th scope="col">Content</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="note in notes" :key="note.id">
                  <td>{{ note.page_number }}</td>
                  <td>{{ note.content }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="form-group">
            <label for="pg_number">Page Number:</label>
            <input
              v-model="newNote.pg_number"
              type="number"
              class="form-control bg-dark text-white"
              id="pg_number"
              :placeholder="43"
            />
          </div>
          <div class="form-group">
            <label for="content">Note:</label>
            <textarea
              v-model="newNote.content"
              class="form-control text-white bg-dark"
              id="content"
              rows="3"
            ></textarea>
          </div>
          <button @click="addNote" class="btn btn-primary col-3 d-block mt-5">
            Add Notes
          </button>
          <button @click="returnBook" class="btn btn-danger col-3 d-block mt-5">
            Return Book
          </button>
          <div v-if="msg.length > 0" class="alert">
            <ul class="list-unstyled">
              <li v-for="msg in msg" :key="msg">
                <pre>
                ##################################
                    {{ msg }}
                ##################################
              </pre
                >
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
import router from "@/router/index";
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
      notes: [],
      newNote: {
        pg_number: 0,
        content: "",
      },
    };
  },
  created() {
    const authToken = localStorage.getItem("auth_token");
    this.fetchBookDetails(authToken);
    this.fetchNotes(authToken);
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
        if (response.status != 200) {
          router.push("/dashboard");
        } else {
          this.book = response.data;
        }
      } catch (error) {
        console.error("Error fetching user books:", error);
      }
    },
    async fetchNotes(authToken) {
      try {
        const response = await axios.get(
          "https://192.168.1.11:5000/user/notes/" + this.bookId,
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
          }
        );
        this.notes = response.data;
        console.log(this.notes);
      } catch (error) {
        console.error("Error fetching notes:", error);
      }
    },
    async addNote() {
      const authToken = localStorage.getItem("auth_token");

      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }

      const url = "https://192.168.1.11:5000/user/notes";
      const data = {
        book_id: this.bookId,
        pg_number: this.newNote.pg_number,
        content: this.newNote.content,
      };

      const headers = {
        Authorization: `Bearer ` + authToken,
        "Content-Type": "application/json",
      };

      try {
        const response = await axios.post(url, data, { headers });

        const responseData = await response.data;
        console.log("Response:", responseData);
        if (responseData == "Empty Note") {
          this.msg.push("Add Page Number and Content");
          setTimeout(() => (this.msg = []), "3000");
        } else {
          this.msg.push(responseData);
          this.notes.push(responseData.note);
          this.newNote.pg_number = 0;
          this.newNote.content = "";
          window.location.reload();
        }
      } catch (error) {
        console.error("Error requesting book addition:", error);
        alert("Error: " + error.message);
      }
    },
    returnBook() {
      if (confirm("Are you sure you want to return this book?")) {
        this.confirmReturn();
      }
    },
    async confirmReturn() {
      const authToken = localStorage.getItem("auth_token");

      if (!authToken) {
        console.error("Missing authToken in localStorage");
        return;
      }

      const data = {
        bookId: this.bookId,
      };
      console.log(data);
      console.log(authToken);
      console.log(this.authToken);
      try {
        const response = await axios.delete(
          "https://192.168.1.11:5000/duebooks",
          {
            headers: {
              Authorization: "Bearer " + authToken,
            },
            data: data,
          }
        );
        const responseData = await response.data;
        console.log("Response:", responseData);
        router.push("/user/books");
      } catch (error) {
        console.error("Error Returning Book! Contact Admin:", error);
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
  flex-direction: column;
  min-height: 100vh;
  flex: 1;
}

.footer {
  position: relative;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
