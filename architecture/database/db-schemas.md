# BigQuery Schemas

## Users

```bash
bq mk \
--table \
--description "Users Database" \
--label organization:development \
cadeira-nuvem-2122:bq_cloud_2122.db_users \
db_user_schema.json
```

Populate with example data for development

```sql
INSERT INTO `cadeira-nuvem-2122.bq_cloud_2122.db_users` (userId, usercreatedts, username, acctdesc, n_following, n_followers, n_totaltweets) 
            VALUES(111,CURRENT_DATETIME(), 'Obama','Thank you for your service', 3, 3, 999)
```