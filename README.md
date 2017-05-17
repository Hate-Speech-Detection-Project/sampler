# Comments Sampler
Python scripts that can be used to sample the comments into arbitrary sets. For example, an input
of ```[0.2, 0.2, 0.6]``` leads to the creation of three partitions which contain 20%, 20% and 60% 
of the total comments, respectively. The optimization goal is to approach those distributions as
well as possible. However, as this is an NP-complete problem, this is not guaranteed.

## PostgreSQL
Currently, the scripts need a local PostgreSQL running with the following config:

```
dbname='hatespeech' user='postgres' host='localhost' password='admin'
```

It should contain a table called comments with the following schema:

```sql
CREATE TABLE comments(cid INTEGER, pid INTEGER, uid INTEGER, moderated INTEGER,
                      subject VARCHAR, comment VARCHAR, created INTEGER, url VARCHAR);
```

or for the merged dataset:
```sql
CREATE TABLE comments(cid INTEGER, pid INTEGER, uid INTEGER, comment VARCHAR, created INTEGER, url VARCHAR, fid REAL, timestamp REAL, hate BOOLEAN);
```

Comments can be imported from a cleansed CSV file:

```sql
COPY comments FROM '<file name>' DELIMITER ',' CSV ENCODING 'UTF8' HEADER;
```
