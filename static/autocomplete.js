MOVIE_URL = "https://api.themoviedb.org/3/search/movie?api_key=1ed4e17d7cb07549e8a7884c5dde6577&&query=";


var options = {
        url: function(name){
            console.log(MOVIE_URL + name);
            return MOVIE_URL + name;
        },

        listLocation: "results",
        getValue: "title"
    };


console.log(options.getValue)

$("#title").easyAutocomplete(options);
