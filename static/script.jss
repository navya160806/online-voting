const carousel = document.querySelector('.leader-carousel');
let index = 0;

function slideCards() {
  index++;
  if (index > 1) index = 0; // 2 sets: first 3, then next 3
  carousel.style.transform = `translateX(-${index * 100}%)`;
}

setInterval(slideCards, 3000);
