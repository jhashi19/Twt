$('.like-btn').on('click',　function(event){
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
      // ブラウザバックでいいねの挙動がおかしくなる。
      // toggleでhide-heartクラスの挿入・削除
      $('#tweet-like-' + tweet_id).toggleClass('hide-heart');
      $('#tweet-not-like-' + tweet_id).toggleClass('hide-heart_blank');
      // resp.like_countでいいねの数を更新
      $('#tweet-like-count-' + tweet_id).text(resp.like_count);
  })
  .fail(function(resp, e){
    location.href = resp.responseText;
  })
});
