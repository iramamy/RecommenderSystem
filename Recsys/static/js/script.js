function userScroll() {
    const navbar = document.querySelector('.navbar');
  
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.classList.add('bg-background');
      } else {
        navbar.classList.remove('bg-background');
      }
    });
  }
  
  document.addEventListener('DOMContentLoaded', userScroll);


// Message
setTimeout(function(){
  $("#message").fadeOut('slow')
}, 10000);


// Filtering
$(document).ready(function(){
  $(".filter-checkbox").on('click', function(){
    console.log('Clicked');

    let filter_object = {};

    $(".filter-checkbox").each(function(){
      let filter_value = $(this).val();
      let filter_key = $(this).data('filter');

      filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+filter_key +']:checked')).map(function(element){
        return element.value
      });
    })

    let visible = 12;

    const HandleGetData = () => {
      $.ajax({
        url: `/filter/${visible}`,
        data: filter_object,
        dataType: 'json',
        success: function(response){
  
          $('#filtered-genre').html(response.data);
          $('#pagination-container').html(response.pagination);
          
          is_all = response.max;
          console.log('is_all', is_all);

          if (is_all) {
            $('#maxsize-text').show(); 
            $('#load-btn').hide(); 
          } else {
            $('#maxsize-text').hide();
            $('#load-btn').show();
          }
        }
      })
    }

    HandleGetData()

    $(document).on('click', '#load-btn', function() {
      console.log('Load button clicked');
      visible += 12;
      HandleGetData();
    });
  })
})
