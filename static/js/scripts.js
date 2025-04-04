document.addEventListener("DOMContentLoaded", function () {
  // Variables para paginación
  let allGames = [];
  let filteredGames = []; // Nueva variable para los juegos filtrados
  let currentPage = 1;
  let gamesPerPage = 10;
  let totalPages = 0;
  let searchActive = false; // Para controlar si hay búsqueda activa

  // Inicialización y carga de datos
  fetchGames();

  // Función para obtener los juegos desde el JSON
  function fetchGames() {
    fetch("/resultados_acumulados.json")
      .then((response) => response.json())
      .then((data) => {
        allGames = data;
        filteredGames = data; // Inicialmente, filteredGames es igual a allGames
        totalPages = Math.ceil(allGames.length / gamesPerPage);
        
        // Configurar eventos primero
        setupPaginationEvents();
        
        // Luego renderizar
        renderPagination();
        renderGames(filteredGames, currentPage);
      })
      .catch((error) => {
        console.error("Error cargando los datos:", error);
        const gameLoading = document.getElementById("game-loading");
        if (gameLoading) {
          gameLoading.innerHTML =
            '<p class="error">Error al cargar los datos. Por favor, intenta de nuevo más tarde.</p>';
        }
      });
  }

  // Función para configurar eventos de paginación
  function setupPaginationEvents() {
    const gamesPerPageSelect = document.getElementById('games-per-page');
    const gameSearchInput = document.getElementById('game-search');
    
    // Verificar si los elementos existen antes de asignar eventos
    if (gamesPerPageSelect) {
      gamesPerPageSelect.addEventListener('change', function() {
        gamesPerPage = parseInt(this.value);
        currentPage = 1; // Volver a la primera página
        
        // Actualizar según si hay búsqueda activa o no
        if (searchActive) {
          totalPages = Math.ceil(filteredGames.length / gamesPerPage);
          renderGames(filteredGames, currentPage);
        } else {
          totalPages = Math.ceil(allGames.length / gamesPerPage);
          renderGames(allGames, currentPage);
        }
        
        renderPagination();
      });
    } else {
      console.error("Elemento 'games-per-page' no encontrado");
    }

    if (gameSearchInput) {
      gameSearchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm === '') {
          // Si el término de búsqueda está vacío, mostrar todos los juegos
          searchActive = false;
          filteredGames = allGames;
          totalPages = Math.ceil(allGames.length / gamesPerPage);
          currentPage = 1;
          renderGames(allGames, currentPage);
        } else {
          // Filtrar juegos por el término de búsqueda
          searchActive = true;
          filteredGames = allGames.filter(game => 
            (game.numero_juego && game.numero_juego.toString().includes(searchTerm)) ||
            (game.equipo_1 && game.equipo_1.nombre && game.equipo_1.nombre.toLowerCase().includes(searchTerm)) ||
            (game.equipo_2 && game.equipo_2.nombre && game.equipo_2.nombre.toLowerCase().includes(searchTerm))
          );
          
          totalPages = Math.ceil(filteredGames.length / gamesPerPage);
          currentPage = 1; // Volver a la primera página al buscar
          renderGames(filteredGames, currentPage);
        }
        
        renderPagination();
      });
    } else {
      console.error("Elemento 'game-search' no encontrado");
    }
  }

  // Función para renderizar los controles de paginación
  function renderPagination() {
    const paginationContainer = document.getElementById('pagination-controls');
    
    if (!paginationContainer) {
      console.error("Contenedor de paginación no encontrado");
      return;
    }
    
    // Si no hay páginas, mostrar mensaje y salir
    if (totalPages === 0) {
      paginationContainer.innerHTML = '';
      return;
    }
    
    let paginationHTML = '';
    
    // Botón anterior
    paginationHTML += `<button class="page-btn prev-btn" ${currentPage === 1 ? 'disabled' : ''}>Anterior</button>`;
    
    // Páginas numeradas
    paginationHTML += '<div class="page-numbers">';
    
    // Primera página
    if (currentPage > 2) {
      paginationHTML += `<button class="page-btn" data-page="1">1</button>`;
      if (currentPage > 3) {
        paginationHTML += `<span class="page-ellipsis">...</span>`;
      }
    }
    
    // Página anterior
    if (currentPage > 1) {
      paginationHTML += `<button class="page-btn" data-page="${currentPage - 1}">${currentPage - 1}</button>`;
    }
    
    // Página actual
    paginationHTML += `<button class="page-btn active" data-page="${currentPage}">${currentPage}</button>`;
    
    // Página siguiente
    if (currentPage < totalPages) {
      paginationHTML += `<button class="page-btn" data-page="${currentPage + 1}">${currentPage + 1}</button>`;
    }
    
    // Última página
    if (currentPage < totalPages - 1) {
      if (currentPage < totalPages - 2) {
        paginationHTML += `<span class="page-ellipsis">...</span>`;
      }
      paginationHTML += `<button class="page-btn" data-page="${totalPages}">${totalPages}</button>`;
    }
    
    paginationHTML += '</div>';
    
    // Botón siguiente
    paginationHTML += `<button class="page-btn next-btn" ${currentPage === totalPages ? 'disabled' : ''}>Siguiente</button>`;
    
    paginationContainer.innerHTML = paginationHTML;
    
    // Agregar eventos a los botones de paginación
    document.querySelectorAll('.page-btn[data-page]').forEach(button => {
      button.addEventListener('click', function() {
        currentPage = parseInt(this.dataset.page);
        renderPagination();
        
        // Renderizar juegos filtrados o todos según estado de búsqueda
        if (searchActive) {
          renderGames(filteredGames, currentPage);
        } else {
          renderGames(allGames, currentPage);
        }
      });
    });
    
    // Eventos para botones anterior y siguiente
    const prevBtn = document.querySelector('.prev-btn');
    if (prevBtn) {
      prevBtn.addEventListener('click', function() {
        if (currentPage > 1) {
          currentPage--;
          renderPagination();
          
          // Renderizar juegos filtrados o todos según estado de búsqueda
          if (searchActive) {
            renderGames(filteredGames, currentPage);
          } else {
            renderGames(allGames, currentPage);
          }
        }
      });
    }
    
    const nextBtn = document.querySelector('.next-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', function() {
        if (currentPage < totalPages) {
          currentPage++;
          renderPagination();
          
          // Renderizar juegos filtrados o todos según estado de búsqueda
          if (searchActive) {
            renderGames(filteredGames, currentPage);
          } else {
            renderGames(allGames, currentPage);
          }
        }
      });
    }
  }

  // Función para renderizar los juegos (modificada para paginación)
  function renderGames(games, page) {
    const gameList = document.getElementById("game-list");
    const gameLoading = document.getElementById("game-loading");
    const infoText = document.getElementById("pagination-info");

    // Ocultar mensaje de carga
    if (gameLoading) {
      gameLoading.style.display = "none";
    }

    // Limpiar la lista actual
    if (gameList) {
      gameList.innerHTML = "";
    } else {
      console.error("Elemento 'game-list' no encontrado");
      return;
    }

    // Si no hay juegos, mostrar mensaje
    if (!games || games.length === 0) {
      gameList.innerHTML = "<p>No hay juegos disponibles con los criterios de búsqueda actuales.</p>";
      if (infoText) infoText.textContent = "No hay juegos";
      return;
    }

    // Calcular índices para paginación
    const startIndex = (page - 1) * gamesPerPage;
    const endIndex = Math.min(startIndex + gamesPerPage, games.length);
    const gamesOnPage = games.slice(startIndex, endIndex);

    // Actualizar texto informativo
    if (infoText) {
      infoText.textContent = `Mostrando ${startIndex + 1}-${endIndex} de ${games.length} juegos`;
    }

    // Resto del código para renderizar los juegos (sin cambios)
    gamesOnPage.forEach((game) => {
      // Solo procesar si tiene información de identificación
      if (!game.id_juego || !game.equipo_1 || !game.equipo_2) return;

      // [El resto del código para crear gameDetails permanece igual]
      
      // Creación de gameDetails, gameHeader, gameBody, etc.
      const gameDetails = document.createElement("div");
      gameDetails.className = "game-details";
      gameDetails.id = `game-${game.id_juego}`;

      // Crear cabecera del juego
      const gameHeader = document.createElement("div");
      gameHeader.className = "game-header";
      gameHeader.innerHTML = `
      <span class="game-number">Juego #${game.numero_juego}</span>
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
    </p>

    <!-- Estadísticas de género -->
    <h4>Estadísticas de Género</h4>
    <table>
        <tr>
            <th>Categoría</th>
            <th>Valor</th>
        </tr>
        <tr>
            <td>Género con más victorias</td>
            <td>${game.genero_con_mas_victorias}</td>
        </tr>
        <tr>
            <td colspan="2"><strong>Victorias por género (este juego)</strong></td>
        </tr>
        <tr>
            <td>Masculino (M)</td>
            <td>${game.generos_victorias_totales.M}</td>
        </tr>
        <tr>
            <td>Femenino (F)</td>
            <td>${game.generos_victorias_totales.F}</td>
        </tr>
        <tr>
            <td colspan="2"><strong>Victorias por género (global)</strong></td>
        </tr>
        <tr>
            <td>Masculino (M)</td>
            <td>${game.generos_victorias_globales.M}</td>
        </tr>
        <tr>
            <td>Femenino (F)</td>
            <td>${game.generos_victorias_globales.F}</td>
        </tr>
    </table>`;

      gameBody.innerHTML = bodyHTML;
      gameBody.style.display = "none"; // Inicialmente oculto

      // Añadir elementos al contenedor de detalles
      gameDetails.appendChild(gameHeader);
      gameDetails.appendChild(gameBody);
      gameList.appendChild(gameDetails);
    });
  }
});