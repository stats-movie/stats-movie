const sliders3 = document.querySelector(".carrosselBox3");
let scrollAmount3 = 0;
let scrollPerClick3 = 170;
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
  const apiKey3 = "7f14aef7a818f9ca8d8fb0597e94b962";

  try {
    const response3 = await axios.get(
      `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey3}&sort_by=vote_average.desc`
    );

    const movies3 = response3.data.results;

    movies3.forEach((movie, index) => {
      sliders3.insertAdjacentHTML(
        "beforeend",
        `<img class="img-${index} slider-img" src="https://image.tmdb.org/t/p/w300/${movie.poster_path}"/>`
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