$('.like-btn').on('click',　function(event){
    event.preventDefault();
    let like = $(this);
    let comment_id = like.attr('value');
    $.ajax({
        url: like.attr('data-href'),
        type: 'POST',
        data:{
          'comment_id': comment_id
        },
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(resp){
        // toggleでhide-heartクラスの挿入・削除
        $('#comment-like-' + comment_id).toggleClass('hide-heart');
        $('#comment-not-like-' + comment_id).toggleClass('hide-heart_blank');
        // resp.like_countでいいねの数を更新
        $('#comment-like-count-' + comment_id).text(resp.comment_like_count)
    })
    .fail(function(resp, e){
        location.href = resp.responseText;
    })
});

$('.detail-like-btn').on('click',　function(event){
    event.preventDefault();
    let like = $(this);
    let tweet_id = like.attr('value');
    $.ajax({
        url: like.attr('data-href'),
        type: 'POST',
        data:{
          'tweet_id': tweet_id
        },
        dataType: 'json',
        timeout: 10000,
    })
    .done(function(resp){
        // toggleでhide-heartクラスの挿入・削除
        $('#detail-like').toggleClass('hide-heart');
        $('#detail-not-like').toggleClass('hide-heart_blank');
        // resp.like_countでいいねの数を更新
        $('#tweet-detail-like').text(resp.detail_like_count + '件のいいね！')
    })
    .fail(function(resp, e){
        location.href = resp.responseText;
    })
});
