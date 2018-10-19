--User Table
insert into user(user_id,username,email,pw_hash)
  values('cee4fd76-5813-11e8-9c2d-fa7ae01bbebc','userone','one@gmail.com','pbkdf2:sha256:50000$gqWzYorx$ac40267bd4b4daea5e61fb85d08b20a5e7d20b91078af30772674617b73666bb');

insert into user(user_id,username,email,pw_hash)
  values('cee50316-5813-11e8-9c2d-fa7ae01bbebc','usertwo','two@gmail.com','pbkdf2:sha256:50000$srlmGRs9$d9e48c0d802cc1f0feee3e1393ca4a890857ef8bd2eb46e7b363681d094b1703');

insert into user(user_id,username,email,pw_hash)
  values('cee5046a-5813-11e8-9c2d-fa7ae01bbebc','userthree','three@gmail.com','pbkdf2:sha256:50000$7YNohO2v$d2a1f2e500df35695158695dfab13ba94761edb15cc57e04174d386ec9148962');

insert into user(user_id,username,email,pw_hash)
  values('25153094-5814-11e8-9c2d-fa7ae01bbebc','userfour','four@gmail.com','pbkdf2:sha256:50000$opuKB3uu$0d8de3fa0495c6d35acd843e0b07aeadea2ff5bacd76beb158121ff4236af437');

insert into user(user_id,username,email,pw_hash)
  values('2515374c-5814-11e8-9c2d-fa7ae01bbebc','userfive','five@gmail.com','pbkdf2:sha256:50000$cMdN5Ozr$2b179314af488334fbba8b2a760ecdd52416e02f31c49ad761371f2c604e68a2');

insert into user(user_id,username,email,pw_hash)
  values('251535ee-5814-11e8-9c2d-fa7ae01bbebc','usersix','six@gmail.com','pbkdf2:sha256:50000$09bjHWxB$35330d1e06c93b4e878a6de3fa4e12baaee147d0532df490e047e8ef17c29f24');



--Follower table
insert into follower
  values('cee50316-5813-11e8-9c2d-fa7ae01bbebc','cee5046a-5813-11e8-9c2d-fa7ae01bbebc');

insert into follower
  values('cee5046a-5813-11e8-9c2d-fa7ae01bbebc','cee50316-5813-11e8-9c2d-fa7ae01bbebc');

insert into follower
  values('cee50316-5813-11e8-9c2d-fa7ae01bbebc','2515374c-5814-11e8-9c2d-fa7ae01bbebc');





--Message table
insert into message(author_id,text,pub_date)
  values('2515374c-5814-11e8-9c2d-fa7ae01bbebc','This is the first post',1519063659);

insert into message(author_id,text,pub_date)
  values('cee50316-5813-11e8-9c2d-fa7ae01bbebc','This is the second post',1519063659);

insert into message(author_id,text,pub_date)
  values('cee5046a-5813-11e8-9c2d-fa7ae01bbebc','This is the third post',1519063781);

insert into message(author_id,text,pub_date)
  values('2515374c-5814-11e8-9c2d-fa7ae01bbebc','This is the fourth post',1519063659);
