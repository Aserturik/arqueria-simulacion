// static/js/scripts.js
document.addEventListener("DOMContentLoaded", function () {
  // Inicialización y carga de datos
  fetchGames();

  // Función para obtener los juegos desde el JSON
  function fetchGames() {
    fetch("/resultados_acumulados.json")
      .then((response) => response.json())
      .then((data) => {
        renderGames(data);
        createSummaryStatistics(data);
      })
      .catch((error) => {
        console.error("Error cargando los datos:", error);
        document.getElementById("game-loading").innerHTML =
          '<p class="error">Error al cargar los datos. Por favor, intenta de nuevo más tarde.</p>';
      });
  }

  // Función para renderizar los juegos
  function renderGames(games) {
    const gameList = document.getElementById("game-list");
    const gameLoading = document.getElementById("game-loading");

    // Ocultar mensaje de carga
    if (gameLoading) {
      gameLoading.style.display = "none";
    }

    // Si no hay juegos, mostrar mensaje
    if (!games || games.length === 0) {
      gameList.innerHTML = "<p>No hay juegos disponibles.</p>";
      return;
    }

    // Crear lista de juegos
    games.forEach((game, index) => {
      // Solo procesar si tiene información de identificación
      if (!game.id_juego || !game.equipo_1 || !game.equipo_2) return;

      const gameDetails = document.createElement("div");
      gameDetails.className = "game-details";
      gameDetails.id = `game-${game.id_juego}`;

      // Crear cabecera del juego
      const gameHeader = document.createElement("div");
      gameHeader.className = "game-header";
      gameHeader.innerHTML = `
        <span class="game-number">Juego #${
          game.numero_juego || index + 1
        }</span>
        <span class="game-result">${game.equipo_ganador.nombre} vs ${
        game.equipo_ganador.nombre === game.equipo_1.nombre
          ? game.equipo_2.nombre
          : game.equipo_1.nombre
      }</span>
        <span class="toggle-icon">▼</span>
      `;

      // Manejar clic para expandir/contraer detalles
      gameHeader.addEventListener("click", function () {
        const body = this.nextElementSibling;
        const isActive = gameDetails.classList.contains("active");

        // Alternar estado activo
        if (isActive) {
          gameDetails.classList.remove("active");
          body.style.display = "none";
          this.querySelector(".toggle-icon").textContent = "▼";
        } else {
          gameDetails.classList.add("active");
          body.style.display = "block";
          this.querySelector(".toggle-icon").textContent = "▲";
        }
      });

      // Crear cuerpo del juego con jugadores destacados
      const gameBody = document.createElement("div");
      gameBody.className = "game-body";

      // Verificamos si el juego tiene información de jugadores destacados
      const hasLuckyPlayer =
        game.jugador_con_mas_suerte &&
        game.jugador_con_mas_suerte !== "No determinado";
      const hasExpPlayer =
        game.jugador_con_mas_experiencia &&
        game.jugador_con_mas_experiencia !== "No determinado";

      // Contenido HTML para el cuerpo
      let bodyHTML = `
        <p><strong>ID del Juego:</strong> ${game.id_juego}</p>
        
        <!-- Tabla de Jugadores Destacados -->
        <h4>Jugadores Destacados</h4>
        <table>
            <thead>
                <tr>
                    <th>Categoría</th>
                    <th>Nombre</th>
                    <th>Valor</th>
                </tr>
            </thead>
            <tbody>`;

      // Añadir jugador con más suerte si existe
      if (hasLuckyPlayer) {
        bodyHTML += `
              <tr>
                  <td>Jugador con más suerte</td>
                  <td>${game.jugador_con_mas_suerte.nombre}</td>
                  <td>${game.jugador_con_mas_suerte.suerte}</td>
              </tr>`;
      }

      // Añadir jugador con más experiencia si existe
      if (hasExpPlayer) {
        bodyHTML += `
              <tr>
                  <td>Jugador con más experiencia</td>
                  <td>${game.jugador_con_mas_experiencia.nombre}</td>
                  <td>${game.jugador_con_mas_experiencia.experiencia}</td>
              </tr>`;
      }

      // Si no hay ningún jugador destacado, mostrar mensaje
      if (!hasLuckyPlayer && !hasExpPlayer) {
        bodyHTML += `
              <tr>
                  <td colspan="3">No hay información de jugadores destacados</td>
              </tr>`;
      }

      bodyHTML += `
          </tbody>
      </table>
      
      <!-- Tabla de Resultados de Equipos -->
      <h4>Resultados del Juego</h4>
      <table>
          <tr>
              <th>Equipo</th>
              <th>Rondas Ganadas</th>
              <th>Puntaje Total</th>
          </tr>
          <tr>
              <td>${game.equipo_1.nombre}</td>
              <td>${game.equipo_1.rondas_ganadas}</td>
              <td>${game.equipo_1.puntaje_total}</td>
          </tr>
          <tr>
              <td>${game.equipo_2.nombre}</td>
              <td>${game.equipo_2.rondas_ganadas}</td>
              <td>${game.equipo_2.puntaje_total}</td>
          </tr>
      </table>
      
      <!-- Ganador del juego -->
      <p>
          <strong>Ganador: </strong>
          ${
            game.equipo_ganador.nombre === "Empate"
              ? "Empate"
              : `${game.equipo_ganador.nombre} con ${game.equipo_ganador.puntaje} puntos`
          }
      </p>`;

      gameBody.innerHTML = bodyHTML;
      gameBody.style.display = "none"; // Inicialmente oculto

      // Añadir elementos al contenedor de detalles
      gameDetails.appendChild(gameHeader);
      gameDetails.appendChild(gameBody);
      gameList.appendChild(gameDetails);
    });
  }

  // Función para crear estadísticas de resumen
  function createSummaryStatistics(games) {
    if (!games || games.length === 0) return;

    // Contadores para estadísticas
    const equiposVictorias = {};
    const jugadoresSuerte = {};
    const jugadoresExperiencia = {};

    // Procesar cada juego
    games.forEach((game) => {
      // Contar victorias por equipo
      if (game.equipo_ganador && game.equipo_ganador.nombre !== "Empate") {
        const equipoNombre = game.equipo_ganador.nombre;
        equiposVictorias[equipoNombre] =
          (equiposVictorias[equipoNombre] || 0) + 1;
      }

      // Registrar jugadores con más suerte
      if (
        game.jugador_con_mas_suerte &&
        typeof game.jugador_con_mas_suerte !== "string"
      ) {
        const jugadorSuerte = game.jugador_con_mas_suerte.nombre;
        jugadoresSuerte[jugadorSuerte] =
          (jugadoresSuerte[jugadorSuerte] || 0) + 1;
      }

      // Registrar jugadores con más experiencia
      if (
        game.jugador_con_mas_experiencia &&
        typeof game.jugador_con_mas_experiencia !== "string"
      ) {
        const jugadorExp = game.jugador_con_mas_experiencia.nombre;
        jugadoresExperiencia[jugadorExp] =
          (jugadoresExperiencia[jugadorExp] || 0) + 1;
      }
    });

    // Actualizar la sección de estadísticas
    updateStatisticsSection(
      "equipos-stats",
      equiposVictorias,
      "Victorias por Equipo"
    );
    updateStatisticsSection(
      "jugadores-suerte-stats",
      jugadoresSuerte,
      "Jugadores con Más Suerte"
    );
    updateStatisticsSection(
      "jugadores-exp-stats",
      jugadoresExperiencia,
      "Jugadores con Más Experiencia"
    );
  }

  // Función para actualizar una sección de estadísticas
  function updateStatisticsSection(elementId, data, title) {
    const container = document.getElementById(elementId);
    if (!container) return;

    // Ordenar los datos por valor (descendente)
    const sortedData = Object.entries(data)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5); // Top 5

    // Crear la tabla HTML
    let html = `
      <h3>${title}</h3>
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Cantidad</th>
          </tr>
        </thead>
        <tbody>
    `;

    // Añadir filas
    sortedData.forEach(([nombre, cantidad]) => {
      html += `
        <tr>
          <td>${nombre}</td>
          <td>${cantidad}</td>
        </tr>
      `;
    });

    html += `
        </tbody>
      </table>
    `;

    container.innerHTML = html;
  }
});
