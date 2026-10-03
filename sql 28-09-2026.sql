CREATE TABLE Departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL
);


CREATE TABLE Employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    dept_id INT,
    salary DECIMAL(10,2),
    manager_id INT,
    join_date DATE,

    FOREIGN KEY (dept_id)
        REFERENCES Departments(dept_id),

    FOREIGN KEY (manager_id)
        REFERENCES Employees(emp_id)
);


CREATE TABLE Projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    dept_id INT,
    budget DECIMAL(12,2),

    FOREIGN KEY (dept_id)
        REFERENCES Departments(dept_id)
);


CREATE TABLE EmployeeProjects (
    emp_id INT,
    project_id INT,
    hours_worked INT,

    PRIMARY KEY (emp_id, project_id),

    FOREIGN KEY (emp_id)
        REFERENCES Employees(emp_id),

    FOREIGN KEY (project_id)
        REFERENCES Projects(project_id)
);



CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR(50)
);

INSERT INTO Departments
(dept_id, dept_name)
VALUES
(1, 'IT'),
(2, 'HR'),
(3, 'Finance'),
(4, 'Marketing'),
(5, 'Sales');


INSERT INTO Employees(emp_id, emp_name, dept_id, salary, manager_id, join_date)
VALUES
(101, 'Rahul', 1, 90000, NULL, '2020-01-15'),
(102, 'Priya', 2, 85000, NULL, '2019-06-10'),
(103, 'Arjun', 3, 95000, NULL, '2021-03-20'),
(104, 'Sneha', 4, 80000, NULL, '2020-08-12'),
(105, 'Kiran', 5, 88000, NULL, '2019-11-05');


INSERT INTO Employees
(emp_id, emp_name, dept_id, salary, manager_id, join_date)
VALUES
(106, 'Vamshi', 1, 60000, 101, '2023-07-01'),
(107, 'Anil', 1, 55000, 101, '2024-01-10'),
(108, 'Meena', 2, 58000, 102, '2022-09-15'),
(109, 'Ravi', 3, 62000, 103, '2023-02-18'),
(110, 'Divya', 4, 57000, 104, '2022-05-25'),
(111, 'Suresh', 5, 59000, 105, '2024-03-11');



INSERT INTO Projects
(project_id, project_name, dept_id, budget)
VALUES
(201, 'AI Platform', 1, 500000),
(202, 'Employee Portal', 2, 200000),
(203, 'Financial Analytics', 3, 350000),
(204, 'Marketing Campaign', 4, 150000),
(205, 'Sales Dashboard', 5, 250000),
(206, 'Cloud Migration', 1, 450000);


INSERT INTO EmployeeProjects
(emp_id, project_id, hours_worked)
VALUES
(101, 201, 120),
(106, 201, 180),
(107, 201, 150),

(101, 206, 100),
(107, 206, 200),

(102, 202, 160),
(108, 202, 190),

(103, 203, 140),
(109, 203, 210),

(104, 204, 130),
(110, 204, 170),

(105, 205, 150),
(111, 205, 190);



INSERT INTO Orders
(order_id, customer_id, order_date, amount, status)
VALUES
(1001, 501, '2025-01-05', 2500.00, 'Completed'),
(1002, 502, '2025-01-10', 4500.00, 'Completed'),
(1003, 503, '2025-01-15', 1200.00, 'Pending'),
(1004, 501, '2025-02-02', 3200.00, 'Completed'),
(1005, 504, '2025-02-10', 5600.00, 'Cancelled'),
(1006, 505, '2025-02-18', 1800.00, 'Pending'),
(1007, 502, '2025-03-01', 7200.00, 'Completed'),
(1008, 506, '2025-03-05', 2100.00, 'Completed'),
(1009, 503, '2025-03-12', 3900.00, 'Pending'),
(1010, 507, '2025-03-20', 6500.00, 'Completed');



SELECT * FROM Departments;
SELECT * FROM Employees;
SELECT * FROM Projects;
SELECT * FROM EmployeeProjects;
SELECT * FROM Orders;


select d.dept_name, count(*) as n_emp, avg(salary) as avg_sal, max(salary) as max_sal, min(salary) as min_sal from Departments d left join Employees e on  d.dept_id=e.emp_id group by dept_name;
select dept_id,emp_id, emp_name, salary from (select dept_id,emp_id,emp_name,salary, dense_rank() over(partition by dept_id order by salary desc) as rnk from Employees) e where rnk=2 
select emp_id, emp_name, salary, dept_id from (select dept_id, emp_id,emp_name, salary, avg(salary) over(partition by dept_id) as dept_avg from Employees) e where salary>dept_avg; 
select m.emp_id AS manager_id, m.emp_name AS manager_name, m.salary AS manager_salary,COUNT(e.emp_id) AS report_count,SUM(e.salary) AS total_team_salary FROM Employees m JOIN Employees e ON m.emp_id = e.manager_id GROUP BY m.emp_id,m.emp_name,m.salary HAVING COUNT(e.emp_id) >= 2;
select distinct d.dept_id,d.dept_name from Departments d join Employees e on d.dept_id=e.emp_id left join Projects p on d.dept_id=p.dept_id where p.project_id is NUll; 
