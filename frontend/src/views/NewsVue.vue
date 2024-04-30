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
          <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/user/books">My Books</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/genres">Genres</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link active" to="/news">News</router-link>
        </li>
      </ul>
    </nav>
    <div class="container-fluid">
      <iframe
        src="https://192.168.1.11:5000/news"
        alt=""
        srcset=""
        class="w-100 border-0"
        style="height: 90vh"
      />
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
export default {
  name: "NewsVuw",
  beforeRouteLeave(to, from, next) {
    next();
  },
};
</script>

<style scoped>
.container-fluid {
  background-color: rgb(0, 0, 0);
  display: flex;
  flex: 1;
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
