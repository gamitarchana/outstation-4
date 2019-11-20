(
  function () {
    $(".carousel-next").on('click', function(e){
      e.stopImmediatePropagation();

      let carouselDiv = this.attributes['href'].value;
      let activeSlide = $('#'+carouselDiv).children('div.carousel-slide-active');
      let nextSlide = $(activeSlide).next('.hide');

      if(nextSlide.length != 0){
        $(nextSlide).removeClass("hide");
        $(nextSlide).addClass("carousel-slide-active");
        $(activeSlide).addClass("hide");
        $(activeSlide).removeClass("carousel-slide-active");
      }
    });

    $(".carousel-prev").on('click', function(e){
        e.stopImmediatePropagation();

        let carouselDiv = this.attributes['href'].value;
        let activeSlide = $('#'+carouselDiv).children('div.carousel-slide-active');
        let prevSlide = $(activeSlide).prev('.hide');

        if(prevSlide.length != 0){
          $(prevSlide).removeClass("hide");
          $(prevSlide).addClass("carousel-slide-active");
          $(activeSlide).addClass("hide");
          $(activeSlide).removeClass("carousel-slide-active");
        }
    });
})();
