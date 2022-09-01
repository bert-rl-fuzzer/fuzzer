CREATE DATABASE fuzzycrawler_test;
USE fuzzycrawler_test;
CREATE TABLE `user`
(
  `id` bigint NOT NULL,
  `fname` varchar
(255) NOT NULL,
  `lname` varchar
(255) NOT NULL,
  `email` varchar
(400) NOT NULL,
  `pass` varchar
(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `user`
ADD PRIMARY KEY
(`id`),
ADD UNIQUE KEY `email`
(`email`);
ALTER TABLE `user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;
COMMIT;

INSERT INTO `user`
  (`fname`,`lname`
  ,`email`,`pass`) VALUES
('John','Doe','john.doe@example.com','Doe@123');

CREATE TABLE `faq` (
  `id` bigint NOT NULL,
  `question` varchar(500) NOT NULL,
  `answer` text NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `faq`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `faq` ADD FULLTEXT KEY `question` (`question`);

INSERT INTO `faq` (`id`, `question`, `answer`, `date`) VALUES
(1, 'Is FuzzyCrawler Free to Use', 'Yes, FuzzyCrawler is an open-source tool that is licenced under the standard MIT licence. ', '2021-07-03 00:33:34'),
(2, 'Can I Use FuzzyCrawler For Commercial Purposes', 'Yes, the FuzzyCrawler tool was designed to offer modern fuzzing methods for various applications and therefore is very easy to integrate through modern testing workflows such as those implemented through CI/CD Pipelines. It can also be used with existing projects to detect vulnerabilities in existing software.', '2021-07-03 00:33:34'),
(3, 'Which is the best Fuzzing method', 'Every Application has different needs and use-case scenarios which means that no one technique can be considered better than others in general. Thus since each software needs is different, FuzzyCrawler offers multiple techniques to support a wider spectrum for testing.', '2021-07-03 00:43:46'),
(4, 'I need multiple types of fuzzers for my project, do I need to download from multiple GitHub repo', 'No, FuzzyCrawler offers a single Github repo that can easily integrate with your project and offer the various types of fuzzers supported by FuzzyCrawler in a single package. ', '2021-07-03 00:43:46');

ALTER TABLE `faq`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;