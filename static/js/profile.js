$('.follow-btn').on('click', function(event){
    event.preventDefault()
    let profile = $(this)
    let profile_user_id = profile.attr('value')
    $.ajax({
        url: profile.attr('data-href'),
        type: 'POST',
        data: {
            'user_id': profile_user_id
        },
        dataType: 'json',
        timeout: 10000
    })
    .done(function(resp){
        $('#following-id').toggleClass('following-hide');
        $('#follow-id').toggleClass('follow-hide');
        $('#follower-count').text(resp.follower_count);
        if (resp.follower_count === 1) {
            $('#follower').text('Follower');
        } else {
            $('#follower').text('Followers');
        }
    })
    .fail(function(resp, e){
        location.href = resp.responseText;
    })
});
