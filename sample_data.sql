-- Sample data for University Planner
-- Run this after database_setup.sql

USE university_planner;

-- Sample Students
INSERT INTO students (username, password, email, phone) VALUES
('john_doe', 'pass123', 'john@student.com', '9876543210'),
('jane_smith', 'pass123', 'jane@student.com', '9876543211'),
('bob_wilson', 'pass123', 'bob@student.com', '9876543212');

-- Sample Subjects for john_doe (student_id = 2)
INSERT INTO subjects (name, code, professor, student_id) VALUES
('Data Structures', 'CS201', 'Dr. Smith', 2),
('Database Management', 'CS301', 'Dr. Johnson', 2),
('Web Development', 'CS302', 'Prof. Williams', 2),
('Operating Systems', 'CS401', 'Dr. Brown', 2);

-- Sample Subjects for jane_smith (student_id = 3)
INSERT INTO subjects (name, code, professor, student_id) VALUES
('Computer Networks', 'CS402', 'Prof. Davis', 3),
('Software Engineering', 'CS403', 'Dr. Miller', 3),
('Machine Learning', 'CS501', 'Dr. Anderson', 3);

-- Sample Attendance for john_doe's subjects
-- Data Structures (subject_id = 1) - Good attendance 85%
INSERT INTO attendance (subject_id, date, status, notes) VALUES
(1, '2024-12-01', 'present', 'Learned about arrays'),
(1, '2024-12-02', 'present', 'Stack implementation'),
(1, '2024-12-03', 'present', 'Queue basics'),
(1, '2024-12-04', 'absent', 'Was sick'),
(1, '2024-12-05', 'present', 'Linked lists'),
(1, '2024-12-06', 'present', 'Trees introduction'),
(1, '2024-12-09', 'present', 'Binary trees'),
(1, '2024-12-10', 'present', 'BST operations'),
(1, '2024-12-11', 'present', 'Graph basics'),
(1, '2024-12-12', 'absent', 'Family emergency'),
(1, '2024-12-13', 'present', 'Graph traversal'),
(1, '2024-12-14', 'present', 'DFS and BFS');

-- Database Management (subject_id = 2) - Low attendance 65%
INSERT INTO attendance (subject_id, date, status, notes) VALUES
(2, '2024-12-01', 'absent', 'Overslept'),
(2, '2024-12-02', 'present', 'SQL basics'),
(2, '2024-12-03', 'absent', 'Had another class'),
(2, '2024-12-04', 'present', 'Joins'),
(2, '2024-12-05', 'present', 'Normalization'),
(2, '2024-12-06', 'absent', 'Not feeling well'),
(2, '2024-12-09', 'present', 'Transactions'),
(2, '2024-12-10', 'absent', 'Missed bus'),
(2, '2024-12-11', 'present', 'Indexing'),
(2, '2024-12-12', 'absent', 'Weather'),
(2, '2024-12-13', 'present', 'Stored procedures'),
(2, '2024-12-14', 'absent', 'Had to work');

-- Web Development (subject_id = 3) - Perfect attendance 100%
INSERT INTO attendance (subject_id, date, status, notes) VALUES
(3, '2024-12-01', 'present', 'HTML basics'),
(3, '2024-12-03', 'present', 'CSS styling'),
(3, '2024-12-05', 'present', 'JavaScript intro'),
(3, '2024-12-08', 'present', 'DOM manipulation'),
(3, '2024-12-10', 'present', 'React basics'),
(3, '2024-12-12', 'present', 'React hooks'),
(3, '2024-12-14', 'present', 'State management');

-- Sample Assignments
INSERT INTO assignments (subject_id, title, description, deadline, status) VALUES
-- Completed
(1, 'Array Implementation', 'Implement dynamic array in Python', '2024-12-10', 'completed'),
(3, 'HTML Portfolio', 'Create personal portfolio website', '2024-12-08', 'completed'),

-- Due Today
(2, 'Database Design Project', 'Design database for library system', '2024-12-14', 'pending'),

-- Due Soon
(1, 'Tree Traversal Assignment', 'Implement inorder, preorder, postorder', '2024-12-16', 'pending'),
(4, 'Process Scheduling Simulator', 'Simulate FCFS and Round Robin', '2024-12-17', 'pending'),

-- Due This Week
(3, 'React Todo App', 'Build todo app with React and local storage', '2024-12-18', 'pending'),

-- Due Later
(2, 'SQL Query Optimization', 'Optimize given slow queries', '2024-12-25', 'pending'),
(1, 'Graph Algorithms Project', 'Implement Dijkstra and Bellman-Ford', '2024-12-28', 'pending');

-- Sample assignments for jane_smith
INSERT INTO assignments (subject_id, title, description, deadline, status) VALUES
(5, 'Network Protocol Analysis', 'Analyze TCP/IP protocol', '2024-12-20', 'pending'),
(6, 'UML Diagrams', 'Create class and sequence diagrams', '2024-12-22', 'pending'),
(7, 'Linear Regression Model', 'Build and train linear regression', '2024-12-30', 'pending');

-- Sample Timetable for john_doe
INSERT INTO timetable (subject_id, day_of_week, start_time, end_time, room) VALUES
-- Monday
(1, 'Monday', '09:00:00', '10:30:00', 'Room 101'),
(2, 'Monday', '11:00:00', '12:30:00', 'Lab 201'),
(3, 'Monday', '14:00:00', '15:30:00', 'Lab 301'),

-- Tuesday
(4, 'Tuesday', '09:00:00', '10:30:00', 'Room 102'),
(1, 'Tuesday', '14:00:00', '15:30:00', 'Room 101'),

-- Wednesday
(2, 'Wednesday', '09:00:00', '10:30:00', 'Lab 201'),
(3, 'Wednesday', '11:00:00', '12:30:00', 'Lab 301'),

-- Thursday
(1, 'Thursday', '09:00:00', '10:30:00', 'Room 101'),
(4, 'Thursday', '11:00:00', '12:30:00', 'Room 102'),

-- Friday
(2, 'Friday', '09:00:00', '10:30:00', 'Lab 201'),
(3, 'Friday', '11:00:00', '12:30:00', 'Lab 301'),
(1, 'Friday', '14:00:00', '15:30:00', 'Room 101');

-- Sample Timetable for jane_smith
INSERT INTO timetable (subject_id, day_of_week, start_time, end_time, room) VALUES
-- Monday
(5, 'Monday', '10:00:00', '11:30:00', 'Room 201'),
(6, 'Monday', '13:00:00', '14:30:00', 'Room 202'),

-- Wednesday
(7, 'Wednesday', '10:00:00', '11:30:00', 'Lab 401'),
(5, 'Wednesday', '14:00:00', '15:30:00', 'Room 201'),

-- Friday
(6, 'Friday', '09:00:00', '10:30:00', 'Room 202'),
(7, 'Friday', '11:00:00', '12:30:00', 'Lab 401');

-- Show summary
SELECT 'Sample data inserted successfully!' as Status;
SELECT COUNT(*) as 'Total Students' FROM students;
SELECT COUNT(*) as 'Total Subjects' FROM subjects;
SELECT COUNT(*) as 'Total Attendance Records' FROM attendance;
SELECT COUNT(*) as 'Total Assignments' FROM assignments;
SELECT COUNT(*) as 'Total Timetable Entries' FROM timetable;
