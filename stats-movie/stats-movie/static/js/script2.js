const sliders2 = document.querySelector(".carrosselBox2");
let scrollAmount2 = 0;
let scrollPerClick2 = 167;
const imagePadding2 = 20;

function sliderScrollLeft2() {
  scrollAmount2 = Math.max(0, scrollAmount2 - scrollPerClick2);
  sliders2.scrollTo({
    top: 0,
    left: scrollAmount2,
    behavior: "smooth",
  });
}

function sliderScrollRight2() {
  const maxScrollLeft2 = sliders2.scrollWidth - sliders2.clientWidth;
  if (scrollAmount2 < maxScrollLeft2) {
    scrollAmount2 = Math.min(maxScrollLeft2, scrollAmount2 + scrollPerClick2);
    sliders2.scrollTo({
      top: 0,
      left: scrollAmount2,
      behavior: "smooth",
    });
  }
}

async function showMovieData2() {
  const apiKey2 = "e67016b01ef609b82437fde192dabd82";

  try {
    const response2 = await axios.get(
      `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey2}&include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_average.desc&vote_count.gte=10000'`
    );

    const movies2 = response2.data.results;

    movies2.forEach((movie, index) => {
      sliders2.insertAdjacentHTML(
        "beforeend",
        `<img class="img-${index} slider-img" src="https://image.tmdb.org/t/p/w300/${movie.poster_path}"/>`
      );
    });

    const firstImage2 = document.querySelector("img-0");
    if (firstImage2) {
      scrollPerClick2 = firstImage2 + imagePadding2;
    }
  } catch (error) {
    console.error("erro ao buscar filme", error);
  }
}

showMovieData2();