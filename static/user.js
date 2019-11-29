$(document).ready(function(){
    $('form').on('submit', function(event){

        $.ajax({
            data : {
                collage_type: $('#collage_type').val(),
                time_frame: $('#time_frame').val(),
                size: $('#size').val()
            },
            type: 'POST',
            url: '/collage'
        })

        .done(function(data) {
        if (!data.hasOwnProperty('error')){
          artwork = JSON.parse(data);
          var item;
          for (item=0; item < artwork.items.length; item++){
             console.log(artwork.items[item]);
           }
        }
        else{
          alert(data.error)
        }

        })

        event.preventDefault();

    });
});
