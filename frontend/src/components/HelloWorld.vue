<template>
  <div class="homepage">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img
            src="@/assets/logo_livbrary.png"
            alt="Logo"
            width="100"
            class="d-inline-block align-top"
          />
        </a>
        <ul class="nav justify-content-end">
          <li class="nav-item">
            <a class="nav-link text-opacity-50" href="/login">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-opacity-50" href="/signup">Signup</a>
          </li>
        </ul>
      </div>
    </nav>
    <div
      class="hero d-flex align-items-center justify-content-center text-center"
    >
      <pre class="ascii-art text-white">


    _____  ______          _____     __          _______ _______ _    _      _______          __     _____ 
  |  __ \|  ____|   /\   |  __ \    \ \        / /_   _|__   __| |  | |    / ____\ \        / /\   / ____|
  | |__) | |__     /  \  | |  | |    \ \  /\  / /  | |    | |  | |__| |   | (___  \ \  /\  / /  \ | |  __ 
  |  _  /|  __|   / /\ \ | |  | |     \ \/  \/ /   | |    | |  |  __  |    \___ \  \ \/  \/ / /\ \| | |_ |
  | | \ \| |____ / ____ \| |__| |      \  /\  /   _| |_   | |  | |  | |    ____) |  \  /\  / ____ \ |__| |
  |_|  \_\______/_/    \_\_____/        \/  \/   |_____|  |_|  |_|  |_|   |_____/    \/  \/_/    \_\_____|
    
  

    _________________________________________________________
    ||-------------------------------------------------------||
    ||.--.    .-._                        .----.             ||
    |||==|____| |H|___            .---.___|""""|_____.--.___ ||
    |||  |====| | |xxx|_          |+++|=-=|_  _|-=+=-|==|---|||
    |||==|    | | |   | \         |   |   |_\/_|📙 📙|  | ^ |||
    |||  |    | | |   |\ \   .--. |   |=-=|_/\_|📕 📕|  | ^ |||
    |||  |    | | |   |_\ \_( ** )|   |   |    |📗 📗|  | ^ |||
    |||==|====| |H|xxx|  \ \ |''| |+++|=-=|""""|-=+=-|==|---|||
    ||`--^----'-^-^---'   `-' ""  '---^---^----^-----^--^---^||
    ||-------------------------------------------------------||
    ||-------------------------------------------------------||
  

      </pre>
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
  name: "HelloWorld",
  data() {
    return {
      isNavOpen: false,
    };
  },
};
</script>

<style scoped>
.homepage {
  background-color: #212529;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer {
  font-family: "Roboto", sans-serif;
}

.hero {
  flex: 1;
  color: #fff;
  background-color: black;
  background-size: cover;
  background-repeat: no-repeat;
  font-family: "Source Serif Pro", serif;
}

.ascii-art {
  margin: 0 auto;
}

.footer {
  font-family: "Roboto", sans-serif;
}
</style>
