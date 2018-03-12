     $(document).ready(function () {
         console.log("slider init");
         // Plugin initialization
         $('.slider').slider({
            indicators: false
         });

         console.log("carousel init")
         $('.carousel').carousel();

         console.log('matchheight');
         $('.item').matchHeight();
     })
