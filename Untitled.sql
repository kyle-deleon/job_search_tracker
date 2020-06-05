-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema job_search_tracker
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `job_search_tracker` ;

-- -----------------------------------------------------
-- Schema job_search_tracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `job_search_tracker` DEFAULT CHARACTER SET utf8 ;
USE `job_search_tracker` ;

-- -----------------------------------------------------
-- Table `job_search_tracker`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `job_search_tracker`.`users` ;

CREATE TABLE IF NOT EXISTS `job_search_tracker`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `job_search_tracker`.`jobs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `job_search_tracker`.`jobs` ;

CREATE TABLE IF NOT EXISTS `job_search_tracker`.`jobs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `company_name` VARCHAR(255) NULL,
  `position` VARCHAR(255) NULL,
  `platform` VARCHAR(255) NULL,
  `company_link` VARCHAR(255) NULL,
  `has_notes` TINYINT(1) NULL,
  `notes` VARCHAR(255) NULL,
  `status` VARCHAR(255) NULL,
  `follow_up` VARCHAR(255) NULL,
  `next_step` VARCHAR(255) NULL,
  `has_interview` TINYINT(1) NULL,
  `interview_date` DATETIME NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_jobs_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_jobs_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `job_search_tracker`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
