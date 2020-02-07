$(document).ready(function() {
    // CSRF code
    function getCookie(name) {
        let cookieValue = null;
        let i = 0;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // LIKE COMMENT
    $('.like_comment').on('click', function(e) {
        e.preventDefault();
        const $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_comment/",
            method: 'POST',
            data: data,
            success: function(data) {
                    $(".counter_like_" + data['id']).text(data['comment'])
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    // LIKE DEAL
    $('.like').on('click', function() {
        const $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_dislike/like/",
            method: 'POST',
            data: data,
            success: function(data) {
                const deal_counter = data['deal_counter'];
                const counter_multiple = deal_counter * 10;
                const session_id = data['session_data'];
                const id_deal = data['id'];
                $(".counter_like_deal_" + data['id']).text(deal_counter);
                    $("#progress-bar-" + data['id']).attr('aria-valuenow', deal_counter);
                    $("#progress-bar-" + data['id']).css('width', counter_multiple + '%');
                    if (session_id[id_deal] === 'like') {
                        $(".btn-like-" + id_deal ).attr('disabled', true);
                    }

                    console.log(session_id[id_deal])
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    // DISLIKE DEAL
    $('.dislike').on('click', function() {
        const $this = $(this),
            data = $this.data();

        $.ajax({
            url: "/like_dislike/dislike/",
            method: 'POST',
            data: data,
            success: function(data) {
                const deal_counter = data['deal_counter'];
                const counter_multiple = deal_counter * 10;
                const session_id = data['session_data'];
                const id_deal = data['id'].toString();
                $(".counter_like_deal_" + data['id']).text(deal_counter);
                $("#progress-bar-" + data['id']).attr('aria-valuenow', deal_counter);
                $("#progress-bar-" + data['id']).css('width', counter_multiple + '%');
                if (session_id[id_deal] === 'like') {
                        $(".btn-like-" + id_deal ).attr('disabled', true);
                }
            },
            error: function(d) {
                console.log(d);
            }
        });
    });

    // SLIDER SIDEBAR FOR DEALS
    $('.sidebar-slider').slick({
        vertical: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 3,
        verticalSwiping: true,
        prevArrow: $('.prev_arrow'),
        nextArrow: $('.next_arrow')
  }).on('wheel', (function(e) {
      e.preventDefault();

      if (e.originalEvent.deltaY < 0) {
        $(this).slick('slickNext');
      } else {
        $(this).slick('slickPrev');
      }
    }));

    // SLIDER SIDEBAR FOR DEALS
    $('.sidebar-slider_shops').slick({
        vertical: true,
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        verticalSwiping: true,
        prevArrow: $('.prev_arrow_shops'),
        nextArrow: $('.next_arrow_shops')
  });

    $('.sidebar-slider_home').slick({
        vertical: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        verticalSwiping: true,
        prevArrow: $('.prev_arrow_home'),
        nextArrow: $('.next_arrow_home')
  });
    $('.sidebar-slider_cat').slick({
        vertical: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        verticalSwiping: true,
        prevArrow: $('.prev_arrow_cat'),
        nextArrow: $('.next_arrow_cat')
  });

    $('#comment_message').val('')

});
