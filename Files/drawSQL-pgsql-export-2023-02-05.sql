CREATE TABLE "user"(
    "id" BIGINT NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "national_id" BIGINT NOT NULL
);
ALTER TABLE
    "user" ADD PRIMARY KEY("id");
ALTER TABLE
    "user" ADD CONSTRAINT "user_national_id_unique" UNIQUE("national_id");
CREATE TABLE "bank_account"(
    "bank_id" BIGINT NOT NULL,
    "account_type_id" BIGINT NOT NULL,
    "bank_account_number" BIGINT NOT NULL,
    "bank_password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "phone_number" BIGINT NOT NULL,
    "balance" BIGINT NOT NULL,
    "id" BIGINT NOT NULL
);
ALTER TABLE
    "bank_account" ADD CONSTRAINT "bank_account_bank_account_number_unique" UNIQUE("bank_account_number");
ALTER TABLE
    "bank_account" ADD PRIMARY KEY("id");
CREATE TABLE "bank"(
    "central_bank_id" BIGINT NOT NULL,
    "bank_name" BIGINT NOT NULL,
    "id" BIGINT NOT NULL
);
ALTER TABLE
    "bank" ADD PRIMARY KEY("id");
CREATE TABLE "central_bank"(
    "id" BIGINT NOT NULL,
    "country" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "central_bank" ADD PRIMARY KEY("id");
CREATE TABLE "account_type"(
    "central_bank_id" BIGINT NOT NULL,
    "account_type" VARCHAR(255) NOT NULL,
    "minimum_balance" BIGINT NOT NULL,
    "number_of_users" BIGINT NOT NULL,
    "id" BIGINT NOT NULL
);
ALTER TABLE
    "account_type" ADD PRIMARY KEY("id");
CREATE TABLE "user_account"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "bank_account_id" BIGINT NOT NULL
);
ALTER TABLE
    "user_account" ADD PRIMARY KEY("id");
CREATE TABLE "card"(
    "id" BIGINT NOT NULL,
    "metro_account_id" BIGINT NOT NULL,
    "one_trip" BOOLEAN NULL,
    "credit_card" BOOLEAN NULL,
    "expirable" BOOLEAN NULL,
    "expire_date" DATE NULL,
    "balance" BIGINT NULL
);
ALTER TABLE
    "card" ADD PRIMARY KEY("id");
CREATE TABLE "trip"(
    "id" BIGINT NOT NULL,
    "metro_account_id" BIGINT NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "origin" VARCHAR(255) NOT NULL,
    "destination" VARCHAR(255) NOT NULL,
    "price" BIGINT NOT NULL,
    "status" BOOLEAN NOT NULL
);
ALTER TABLE
    "trip" ADD PRIMARY KEY("id");
CREATE TABLE "metro_account"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "metro_username" VARCHAR(255) NOT NULL,
    "metro_password" VARCHAR(255) NOT NULL,
    "super_user" BOOLEAN NOT NULL,
    "banned" BOOLEAN NOT NULL,
    "email" BIGINT NOT NULL,
    "phone_number" BIGINT NOT NULL
);
ALTER TABLE
    "metro_account" ADD PRIMARY KEY("id");
ALTER TABLE
    "metro_account" ADD CONSTRAINT "metro_account_metro_username_unique" UNIQUE("metro_username");
CREATE TABLE "phone_number"(
    "id" BIGINT NOT NULL,
    "phone_number" BIGINT NOT NULL,
    "company" VARCHAR(255) NOT NULL,
    "user_id" BIGINT NOT NULL
);
ALTER TABLE
    "phone_number" ADD PRIMARY KEY("id");
ALTER TABLE
    "phone_number" ADD CONSTRAINT "phone_number_phone_number_unique" UNIQUE("phone_number");
CREATE TABLE "Email"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "email_address" BIGINT NOT NULL
);
ALTER TABLE
    "Email" ADD PRIMARY KEY("id");
ALTER TABLE
    "Email" ADD CONSTRAINT "email_email_address_unique" UNIQUE("email_address");
ALTER TABLE
    "user_account" ADD CONSTRAINT "user_account_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "trip" ADD CONSTRAINT "trip_metro_account_id_foreign" FOREIGN KEY("metro_account_id") REFERENCES "metro_account"("id");
ALTER TABLE
    "bank" ADD CONSTRAINT "bank_central_bank_id_foreign" FOREIGN KEY("central_bank_id") REFERENCES "central_bank"("id");
ALTER TABLE
    "card" ADD CONSTRAINT "card_metro_account_id_foreign" FOREIGN KEY("metro_account_id") REFERENCES "metro_account"("id");
ALTER TABLE
    "bank_account" ADD CONSTRAINT "bank_account_bank_id_foreign" FOREIGN KEY("bank_id") REFERENCES "bank"("id");
ALTER TABLE
    "bank_account" ADD CONSTRAINT "bank_account_account_type_id_foreign" FOREIGN KEY("account_type_id") REFERENCES "account_type"("id");
ALTER TABLE
    "user_account" ADD CONSTRAINT "user_account_bank_account_id_foreign" FOREIGN KEY("bank_account_id") REFERENCES "bank_account"("id");
ALTER TABLE
    "account_type" ADD CONSTRAINT "account_type_central_bank_id_foreign" FOREIGN KEY("central_bank_id") REFERENCES "central_bank"("id");
ALTER TABLE
    "metro_account" ADD CONSTRAINT "metro_account_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "phone_number" ADD CONSTRAINT "phone_number_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "Email" ADD CONSTRAINT "email_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");