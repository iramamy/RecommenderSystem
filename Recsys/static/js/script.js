function userScroll() {
    const navbar = document.querySelector('.navbar');
  
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.classList.add('bg-black');
      } else {
        navbar.classList.remove('bg-black');
      }
    });
  }
  
  document.addEventListener('DOMContentLoaded', userScroll);