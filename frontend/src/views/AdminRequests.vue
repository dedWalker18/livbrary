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
          <router-link class="nav-link active" to="/dashboard/admin/requests"
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
    <div>
      <div class="container-fluid">
        <div class="container text-center text-white mt-5">
          <h1>Book Issue Requests</h1>
          <table
            class="table table-striped table-dark table-bordered text-center text-white"
          >
            <thead>
              <tr>
                <th>ID</th>
                <th>Book ID</th>
                <th>User ID</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.id">
                <td>{{ request.id }}</td>
                <td>{{ request.book_id }}</td>
                <td>{{ request.user_id }}</td>
                <td>
                  <button
                    @click="issueBook(request.user_id, request.book_id)"
                    class="btn btn-outline-primary"
                  >
                    Issue Book
                  </button>
                  <button
                    @click="deleteRequest(request.id)"
                    class="btn btn-outline-danger"
                  >
                    Delete Request
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
import router from "@/router/index";
export default {
  data() {
    return {
      requests: [],
    };
  },
  created() {
    this.fetchRequests();
  },
  methods: {
    async fetchRequests() {
      const authToken = localStorage.getItem("auth_token");

      if (!authToken) {
        console.error("Missing authToken in localStorage");
        router.push("/login");
      }

      const url = "https://192.168.1.11:5000/requests";
      const headers = new Headers({
        Authorization: `Bearer ` + authToken,
        "Content-Type": "application/json",
      });
      try {
        const response = await fetch(url, {
          headers,
        });

        if (!response.ok) {
          throw new Error(`Some Issue Occured. Try Again!!}`);
        }
        const responseData = await response.json();
        this.requests = responseData;
        return responseData;
      } catch (error) {
        console.error("Error requesting book addition:", error);
        alert("Error: " + error.message);
      }
    },
    async issueBook(userId, bookId) {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        router.push("/login");
      }
      const url = "https://192.168.1.11:5000/user/books";
      const data = {
        user_id: userId,
        book_id: bookId,
      };

      const headers = {
        Authorization: `Bearer ` + authToken,
        "Content-Type": "application/json",
      };
      const response = await axios.post(url, data, { headers });
      console.log(response);
      window.location.reload();
    },
    async deleteRequest(request) {
      const authToken = localStorage.getItem("auth_token");
      if (!authToken) {
        console.error("Missing authToken in localStorage");
        router.push("/login");
      }
      const response = await axios.delete(
        "https://192.168.1.11:5000/requests/" + request,
        {
          headers: {
            Authorization: "Bearer " + authToken,
          },
        }
      );
      window.location.reload();
      console.log(response);
    },
  },
};
</script>

<style scoped>
.container-fluid {
  background-color: rgb(0, 0, 0);
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 100vh;
}

.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
}
</style>
