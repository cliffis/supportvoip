CREATE TABLE IF NOT EXISTS log_yealink (
id integer PRIMARY KEY AUTOINCREMENT,
model text NOT NULL,
mac text NOT NULL,
number text NOT NULL,
tabnumber text NOT NULL,
adminowner text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
nikname text NOT NULL,
firstname text NOT NULL,
lastname text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS dssphone_hab (
key_number text NOT NULL,
label_number text,
value_number text,
module_number text NOT NULL,
time text NOT NULL
);

CREATE TABLE IF NOT EXISTS ad_users (
sAMAccountName text NOT NULL,
eng_name text NOT NULL,
rus_name text NOT NULL,
telephoneNumber text,
mobile text,
title text,
department text,
mail text,
time text NOT NULL
);



CREATE TABLE IF NOT EXISTS conf_36861 (
CallerIDNum text NOT NULL,
CallerIDName text,
ConfbridgeTalking text,
TimeStart text,
TimeEnd text
);