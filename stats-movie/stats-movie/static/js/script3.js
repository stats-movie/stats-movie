const sliders3 = document.querySelector(".carrosselBox3");
let scrollAmount3 = 0;
let scrollPerClick3 = 167;
const imagePadding3 = 20;

function sliderScrollLeft3() {
  scrollAmount3 = Math.max(0, scrollAmount3 - scrollPerClick3);
  sliders3.scrollTo({
    top: 0,
    left: scrollAmount3,
    behavior: "smooth",
  });
}

function sliderScrollRight3() {
  const maxScrollLeft3 = sliders3.scrollWidth - sliders3.clientWidth;
  if (scrollAmount3 < maxScrollLeft3) {
    scrollAmount3 = Math.min(maxScrollLeft3, scrollAmount3 + scrollPerClick3);
    sliders3.scrollTo({
      top: 0,
      left: scrollAmount3,
      behavior: "smooth",
    });
  }
}

async function showMovieData3() {
  const apiKey3 = "e67016b01ef609b82437fde192dabd82";

  try {
    const response3 = await axios.get(
      `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey3}&include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_count.desc&with_genres=16`
    );

    const movies3 = response3.data.results;

    movies3.forEach((movie, index) => {
      sliders3.insertAdjacentHTML(
        "beforeend",
        `<a href="https://www.themoviedb.org/movie/${movie.id}?language=pt-BR"><img class="img-${index} slider-img" src="https://image.tmdb.org/t/p/w300/${movie.poster_path}"/></a>`
      );
    });

    const firstImage3 = document.querySelector("img-0");
    if (firstImage3) {
      scrollPerClick3 = firstImage3 + imagePadding3;
    }
  } catch (error) {
    console.error("erro ao buscar filme", error);
  }
}

showMovieData3();