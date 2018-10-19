--User Table
insert into user(user_id,username,email,pw_hash)
  values('6d213a68-5814-11e8-9c2d-fa7ae01bbebc','userseven','seven@gmail.com','pbkdf2:sha256:50000$mlet8TOQ$d309fd45cf88ee0a8ef86520fde2de32e21852349d899ea5ff28c55ddd450a56');

insert into user(user_id,username,email,pw_hash)
  values('6d213e5a-5814-11e8-9c2d-fa7ae01bbebc','usereight','eight@gmail.com','pbkdf2:sha256:50000$VCAgFUqy$451917d12a7b1abee75554fc47f1ddff2e07e547aa8b1d342b77f0255787bbaf');

insert into user(user_id,username,email,pw_hash)
  values('6d214116-5814-11e8-9c2d-fa7ae01bbebc','usernine','nine@gmail.com','pbkdf2:sha256:50000$FrfIxP6e$f19d499d7b083180b51f9d4a57072e966f3a0aa8e597a12daca640a04632b94b');

insert into user(user_id,username,email,pw_hash)
  values('6d21426a-5814-11e8-9c2d-fa7ae01bbebc','userten','ten@gmail.com','pbkdf2:sha256:50000$Ehc1G3jc$91e61825974afbf57cd5414c82bce9d340ae59ff212d2bd4d0bf163c093eea8a');

insert into user(user_id,username,email,pw_hash)
  values('6d21445e-5814-11e8-9c2d-fa7ae01bbebc','usereleven','eleven@gmail.com','pbkdf2:sha256:50000$5KzViQgM$d9f71048d53c7c2b829c6fb24dfd770d8bff4ac14b97afae371fc52b61c8d2d1');

insert into user(user_id,username,email,pw_hash)
  values('6d2145da-5814-11e8-9c2d-fa7ae01bbebc','usertwelve','twelve@gmail.com','pbkdf2:sha256:50000$U7oU7xmm$4eed7cd4a85479802ad3459248ed4b17402413be0933f201cccd27faae3f484e');



  insert into follower
    values('6d213a68-5814-11e8-9c2d-fa7ae01bbebc','6d213e5a-5814-11e8-9c2d-fa7ae01bbebc');

  insert into follower
    values('6d214116-5814-11e8-9c2d-fa7ae01bbebc','6d21426a-5814-11e8-9c2d-fa7ae01bbebc');

  insert into follower
    values('6d21426a-5814-11e8-9c2d-fa7ae01bbebc','6d213e5a-5814-11e8-9c2d-fa7ae01bbebc');


    insert into message(author_id,text,pub_date)
      values('6d21426a-5814-11e8-9c2d-fa7ae01bbebc','This is the fifth post',1519063781);
