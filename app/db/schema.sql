
DROP TABLE IF EXISTS active_med;
DROP TABLE IF EXISTS allergy;
DROP TABLE IF EXISTS hist_med;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS patient_allergy;
DROP TABLE IF EXISTS user;


CREATE TABLE "active_med" (
	"active_med_id"	INTEGER NOT NULL,
	"patient_id"	INTEGER NOT NULL,
	"med_name"	TEXT NOT NULL,
	"med_dose"	TEXT NOT NULL,
	"med_directions"	TEXT NOT NULL,
	"med_start_date"	TEXT NOT NULL,
	"comment"	TEXT,
	PRIMARY KEY("active_med_id" AUTOINCREMENT)
);

CREATE TABLE "allergy" (
	"allergy_id"	INTEGER NOT NULL,
	"allergy_name"	TEXT NOT NULL,
	PRIMARY KEY("allergy_id" AUTOINCREMENT)
);

CREATE TABLE "hist_med" (
	"hist_med_id"	INTEGER NOT NULL,
	"patient_id"	INTEGER NOT NULL,
	"med_name"	TEXT NOT NULL,
	"med_dose"	TEXT NOT NULL,
	"med_directions"	TEXT NOT NULL,
	"med_end_date"	TEXT NOT NULL,
	"comment"	TEXT,
	PRIMARY KEY("hist_med_id" AUTOINCREMENT)
);

CREATE TABLE "patient" (
	"patient_id"	INTEGER NOT NULL,
	"fname"	TEXT NOT NULL,
	"lname"	TEXT NOT NULL,
	"mname"	TEXT,
	"dob"	TEXT NOT NULL,
	"weight"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("patient_id" AUTOINCREMENT)
);

CREATE TABLE "patient_allergy" (
	"patient_id"	INTEGER NOT NULL,
	"allergy_id"	INTEGER NOT NULL
);

CREATE TABLE "user" (
	"user_id"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);