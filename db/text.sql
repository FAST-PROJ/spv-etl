-- Database text reference to delta tables from delta.io
CREATE DATABASE text;
USE text;

-- Files list
CREATE TABLE `files` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `created_at` timestamp
);

-- Raw text, this is a bronze quality table
CREATE TABLE `ingestion_files` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `fileId` int,
  `rawText` longtext,
  `created_at` timestamp
);

ALTER TABLE `ingestion_files` ADD FOREIGN KEY (`fileId`) REFERENCES `files` (`id`);

-- Refined text, this is a silver quality table
CREATE TABLE `refined_files` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `fileId` int,
  `refinedText` longtext,
  `created_at` timestamp
);

ALTER TABLE `refined_files` ADD FOREIGN KEY (`fileId`) REFERENCES `files` (`id`);

-- Feature text, this is a gold quality table for data analytics
CREATE TABLE `feature_files` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `fileId` int,
  `word` longtext,
  `sentence` longtext,
  `created_at` timestamp
);

ALTER TABLE `feature_files` ADD FOREIGN KEY (`fileId`) REFERENCES `files` (`id`);

-- some samples for test
INSERT INTO text.files (full_name) VALUES ('manual_ps5');
INSERT INTO text.files (full_name) VALUES ('artigo');
