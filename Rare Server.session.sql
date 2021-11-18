DELETE from auth_user
WHERE id > 1;

Delete from rareapi_rareuser
WHERE id > 1;

DELETE from rareapi_posttag
Where id = 1;

DELETE FROM authtoken_token
WHERE user_id = 11;

UPDATE  auth_user
SET
    is_active = 1
WHERE id = 1;

DELETE FROM rareapi_post
WHERE user_id > 1;