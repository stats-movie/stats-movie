const sliders = document.querySelector(".carrosselBox");
let scrollAmount = 0;
let scrollPerClick = 177;
const imagePadding = 20;

function sliderScrollLeft() {
  scrollAmount = Math.max(0, scrollAmount - scrollPerClick);
  sliders.scrollTo({
    top: 0,
    left: scrollAmount,
    behavior: "smooth",
  });
}

function sliderScrollRight() {
  const maxScrollLeft = sliders.scrollWidth - sliders.clientWidth;
  if (scrollAmount < maxScrollLeft) {
    scrollAmount = Math.min(maxScrollLeft, scrollAmount + scrollPerClick);
    sliders.scrollTo({
      top: 0,
      left: scrollAmount,
      behavior: "smooth",
    });
  }
}

async function showMovieData() {
  const apiKey = "e67016b01ef609b82437fde192dabd82";

  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&include_video=false&sort_by=popularity.desc`
    );  

    const movies = response.data.results;

    movies.forEach((movie, index) => {
      sliders.insertAdjacentHTML(
        "beforeend",
        `<a href="https://www.themoviedb.org/movie/${movie.id}?language=pt-BR"><img class="img-${index} slider-img" src="https://image.tmdb.org/t/p/w300/${movie.poster_path}"/></a>`
      );
    });

    const firstImage = document.querySelector("img-0")
    if (firstImage) {
      scrollPerClick = firstImage + imagePadding;
    }
  } catch (error) {
    console.error("erro ao buscar filme", error);
  }
}

showMovieData();